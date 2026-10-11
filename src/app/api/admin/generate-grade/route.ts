import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifyGenSecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { isAiQuestionsEnabled, isAiQuestionsSanityEnabled } from '@/lib/llm/featureFlags';
import { authorQuestion, sanityCheck } from '@/lib/llm/author';
import { persistAuthoredQuestion } from '@/lib/llm/persistAuthored';
import { getTopicsForGrade } from '@/data/topicTree';
import { validateBody, ValidationError } from '@/lib/validateBody';

export const dynamic = 'force-dynamic';
export const maxDuration = 300;

type Difficulty = 'Easy' | 'Medium' | 'Hard';
const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

// Opus authoring (+ sanity check) is slow, so stay well under maxDuration and
// let the caller re-invoke to resume — each run only tops up the shortfall.
const DEFAULT_PER_SUBTOPIC = 50;
const MAX_PER_SUBTOPIC = 150;
const DEFAULT_BUDGET_MS = 250_000;

/** Split a per-sub-topic total evenly across the three difficulties. */
function splitTargets(total: number): Record<Difficulty, number> {
  const base = Math.floor(total / 3);
  const rem = total % 3;
  return { Easy: base + (rem > 0 ? 1 : 0), Medium: base + (rem > 1 ? 1 : 0), Hard: base };
}

interface SlotResult {
  topicId: string;
  topicName: string;
  subTopicKey: string;
  difficulty: Difficulty;
  target: number;
  existing: number;
  created: number;
  rejected: number;
  failed: number;
}

/**
 * POST /api/admin/generate-grade?secret=AI_GEN_SECRET
 * Body: { grade: number, perSubtopic?: number, subTopicKeys?: string[], budgetMs?: number }
 *
 * Feature 5b batch driver. For each keyed sub-topic of the grade (from the topic
 * tree) × each difficulty, authors deep Opus questions until the sub-topic reaches
 * `perSubtopic` (split evenly across difficulties). Each question is tagged with a
 * subTopic that CONTAINS the sub-topic key so it routes into the right lesson.
 *
 * Resumable + time-boxed: only the shortfall is generated, so re-invoke until
 * `done: true`. Gated by AI_QUESTIONS_ENABLED + AI_GEN_SECRET.
 */
export async function POST(req: Request) {
  const { searchParams } = new URL(req.url);
  if (!verifyGenSecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!isAiQuestionsEnabled()) {
    return NextResponse.json({ error: 'Question generation is disabled.' }, { status: 403 });
  }
  if (!isLlmConfigured()) {
    return NextResponse.json({ error: 'LLM is not configured.' }, { status: 503 });
  }

  let grade: number;
  let perSubtopic: number;
  let subTopicKeys: string[] | undefined;
  let budgetMs: number;
  try {
    const parsed = validateBody<{
      grade: number;
      perSubtopic?: number;
      subTopicKeys?: string[];
      budgetMs?: number;
    }>(await req.json(), {
      grade: 'number',
      perSubtopic: 'number?',
      subTopicKeys: 'array?',
      budgetMs: 'number?',
    });
    grade = parsed.grade;
    perSubtopic = Math.max(1, Math.min(MAX_PER_SUBTOPIC, parsed.perSubtopic ?? DEFAULT_PER_SUBTOPIC));
    subTopicKeys = Array.isArray(parsed.subTopicKeys)
      ? parsed.subTopicKeys.filter((k): k is string => typeof k === 'string')
      : undefined;
    budgetMs = Math.max(30_000, Math.min(DEFAULT_BUDGET_MS, parsed.budgetMs ?? DEFAULT_BUDGET_MS));
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  // Only sub-topic-keyed nodes can be routed by the subTopic ILIKE filter.
  let nodes = getTopicsForGrade(grade).filter((n) => !!n.subTopicKey);
  if (subTopicKeys && subTopicKeys.length) {
    const wanted = new Set(subTopicKeys.map((k) => k.toLowerCase()));
    nodes = nodes.filter((n) => wanted.has((n.subTopicKey as string).toLowerCase()));
  }
  if (nodes.length === 0) {
    return NextResponse.json(
      { error: `No keyed sub-topics found for grade ${grade}.` },
      { status: 404 },
    );
  }

  const targets = splitTargets(perSubtopic);
  const sanityOn = isAiQuestionsSanityEnabled();
  const start = Date.now();
  const overBudget = () => Date.now() - start > budgetMs;

  const results: SlotResult[] = [];
  let totalCreated = 0;
  let remaining = 0;
  let stoppedForTime = false;

  for (const node of nodes) {
    const key = node.subTopicKey as string;
    const storedSubTopic = `Grade ${grade} — ${node.name} (${key})`;

    for (const difficulty of DIFFICULTIES) {
      const target = targets[difficulty];

      const existing = await prisma.question.count({
        where: {
          topicId: node.dbTopicId,
          difficulty,
          source: 'ai_generated',
          subTopic: { contains: key, mode: 'insensitive' },
        },
      });

      const slot: SlotResult = {
        topicId: node.dbTopicId,
        topicName: node.name,
        subTopicKey: key,
        difficulty,
        target,
        existing,
        created: 0,
        rejected: 0,
        failed: 0,
      };

      const needed = target - existing;
      if (needed <= 0) {
        results.push(slot);
        continue;
      }

      // Existing stems (any source) to steer the model away from duplicates.
      const avoidStems = (
        await prisma.question.findMany({
          where: {
            topicId: node.dbTopicId,
            subTopic: { contains: key, mode: 'insensitive' },
          },
          select: { questionText: true },
          orderBy: { id: 'desc' },
          take: 12,
        })
      ).map((q) => q.questionText);

      for (let i = 0; i < needed; i++) {
        if (overBudget()) {
          stoppedForTime = true;
          break;
        }
        try {
          const q = await authorQuestion({
            topicId: node.dbTopicId,
            topicName: node.name,
            subTopic: storedSubTopic,
            difficulty,
            grade,
            avoidStems,
          });

          if (sanityOn && !(await sanityCheck(q, grade))) {
            slot.rejected += 1;
            continue;
          }

          const id = await persistAuthoredQuestion(node.dbTopicId, storedSubTopic, difficulty, q);
          slot.created += 1;
          totalCreated += 1;
          avoidStems.push(q.questionText);
        } catch (err) {
          logError('[admin/generate-grade] author failed', err);
          slot.failed += 1;
        }
      }

      remaining += Math.max(0, target - (existing + slot.created));
      results.push(slot);
      if (stoppedForTime) break;
    }
    if (stoppedForTime) break;
  }

  // Count shortfall for slots we never reached (when we broke out early).
  if (stoppedForTime) {
    const touched = new Set(results.map((r) => `${r.topicId}__${r.subTopicKey}__${r.difficulty}`));
    for (const node of nodes) {
      const key = node.subTopicKey as string;
      for (const difficulty of DIFFICULTIES) {
        if (!touched.has(`${node.dbTopicId}__${key}__${difficulty}`)) {
          remaining += targets[difficulty];
        }
      }
    }
  }

  return NextResponse.json({
    grade,
    perSubtopic,
    targetsPerDifficulty: targets,
    sanityCheck: sanityOn,
    totalCreated,
    remaining,
    done: remaining === 0,
    stoppedForTime,
    elapsedMs: Date.now() - start,
    results,
  });
}

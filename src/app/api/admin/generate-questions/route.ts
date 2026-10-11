import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifyGenSecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { isAiQuestionsEnabled, isAiQuestionsSanityEnabled } from '@/lib/llm/featureFlags';
import { authorQuestion, sanityCheck } from '@/lib/llm/author';
import { persistAuthoredQuestion } from '@/lib/llm/persistAuthored';
import { validateBody, ValidationError } from '@/lib/validateBody';

export const dynamic = 'force-dynamic';
export const maxDuration = 300;

type Difficulty = 'Easy' | 'Medium' | 'Hard';
const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];
const MAX_COUNT = 20;

/**
 * POST /api/admin/generate-questions?secret=AI_GEN_SECRET
 * Body: { topicId, subTopic?, difficulty?, count? }
 *
 * Feature 5b. Generates AI-authored questions, runs an optional sanity
 * self-check (AI_QUESTIONS_SANITY, default-on), and persists survivors tagged
 * `source='ai_generated'`. Gated by AI_QUESTIONS_ENABLED + AI_GEN_SECRET.
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

  let topicId: string;
  let subTopic: string;
  let difficulty: Difficulty | undefined;
  let count: number;
  try {
    const parsed = validateBody<{
      topicId: string;
      subTopic?: string;
      difficulty?: string;
      count?: number;
    }>(await req.json(), {
      topicId: 'string',
      subTopic: 'string?',
      difficulty: 'string?',
      count: 'number?',
    });
    topicId = parsed.topicId;
    subTopic = parsed.subTopic?.trim() ?? '';
    difficulty =
      parsed.difficulty && DIFFICULTIES.includes(parsed.difficulty as Difficulty)
        ? (parsed.difficulty as Difficulty)
        : undefined;
    count = Math.max(1, Math.min(MAX_COUNT, parsed.count ?? 1));
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  const topic = await prisma.topic.findUnique({
    where: { id: topicId },
    select: { name: true, grade: true },
  });
  if (!topic) {
    return NextResponse.json({ error: 'Topic not found' }, { status: 404 });
  }

  const grade = topic.grade;
  const sanityOn = isAiQuestionsSanityEnabled();

  const created: string[] = [];
  let rejected = 0;
  let failed = 0;

  for (let i = 0; i < count; i++) {
    const diff = difficulty ?? DIFFICULTIES[i % DIFFICULTIES.length];
    try {
      const q = await authorQuestion({
        topicId,
        topicName: topic.name,
        subTopic,
        difficulty: diff,
        grade,
      });

      if (sanityOn) {
        const ok = await sanityCheck(q, grade);
        if (!ok) {
          rejected += 1;
          continue;
        }
      }

      const id = await persistAuthoredQuestion(topicId, subTopic, diff, q);
      created.push(id);
    } catch (err) {
      logError('[admin/generate-questions] author failed', err);
      failed += 1;
    }
  }

  return NextResponse.json({
    topicId,
    requested: count,
    created: created.length,
    rejected,
    failed,
    sanityCheck: sanityOn,
    ids: created,
  });
}

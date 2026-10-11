import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';
import { prisma } from '@/lib/db';
import { verifyGenSecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { isAiQuestionsEnabled } from '@/lib/llm/featureFlags';
import { sanityCheck, type AuthoredQuestion } from '@/lib/llm/author';
import { enrichTextbookQuestion, solveTextbookFresh } from '@/lib/llm/enrich';
import { persistAuthoredQuestion } from '@/lib/llm/persistAuthored';
import { getTopicsForGrade } from '@/data/topicTree';
import { validateBody, ValidationError } from '@/lib/validateBody';

export const dynamic = 'force-dynamic';
export const maxDuration = 300;

// Opus enrich + Sonnet verify are slow (~2–4 LLM calls/question), so stay well
// under maxDuration and let the caller re-invoke to resume — each run only
// attempts records that don't yet have a DB row.
const DEFAULT_BUDGET_MS = 250_000;

interface TextbookRecord {
  ref: string;
  id: string;
  chapter: number;
  chapterTitle: string;
  subTopicKey: string;
  storedSubTopic: string;
  questionText: string;
  option1: string;
  option2: string;
  option3: string;
  option4: string;
  printedAnswer: 'A' | 'B' | 'C' | 'D' | null;
}

const ANSWER_KEYS = ['A', 'B', 'C', 'D'] as const;

// Module-cached data file (bundled on Vercel via outputFileTracingIncludes).
let cachedRecords: TextbookRecord[] | null = null;
function loadRecords(): TextbookRecord[] | null {
  if (cachedRecords) return cachedRecords;
  const p = path.join(process.cwd(), 'data', 'ipm-textbook-grade5.json');
  if (!fs.existsSync(p)) return null;
  cachedRecords = JSON.parse(fs.readFileSync(p, 'utf-8')) as TextbookRecord[];
  return cachedRecords;
}

interface ChapterCounts {
  created: number;
  skippedExisting: number;
  verifiedPrinted: number;
  freshSolved: number;
  rejected: number;
  failed: number;
}

function emptyCounts(): ChapterCounts {
  return { created: 0, skippedExisting: 0, verifiedPrinted: 0, freshSolved: 0, rejected: 0, failed: 0 };
}

/**
 * POST /api/admin/import-textbook?secret=AI_GEN_SECRET
 * Body: { grade?: number, chapters?: number[], limit?: number, budgetMs?: number }
 *
 * Imports the digitized IPM "Mathematics Scholarship Std. V" MCQs into Grade 5.
 * Every answer is LLM-VERIFIED before persist (printed → sanityCheck; answerless
 * or sanity-failing → N=3 self-consistency), and the teaching layer is generated
 * grounded on the verified answer. Rows are tagged `source='ipm_textbook'` and
 * stay invisible until `AI_TEXTBOOK_SERVE` is on.
 *
 * Resumable + time-boxed: records already present (by deterministic id) are
 * skipped, so re-invoke until `done: true`. Gated by AI_QUESTIONS_ENABLED +
 * AI_GEN_SECRET (serving is a separate flag).
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
  let chapters: number[] | undefined;
  let limit: number | undefined;
  let budgetMs: number;
  try {
    const parsed = validateBody<{
      grade?: number;
      chapters?: number[];
      limit?: number;
      budgetMs?: number;
    }>(await req.json(), {
      grade: 'number?',
      chapters: 'array?',
      limit: 'number?',
      budgetMs: 'number?',
    });
    grade = parsed.grade ?? 5;
    chapters = Array.isArray(parsed.chapters)
      ? parsed.chapters.filter((c): c is number => typeof c === 'number')
      : undefined;
    limit = typeof parsed.limit === 'number' && parsed.limit > 0 ? Math.floor(parsed.limit) : undefined;
    budgetMs = Math.max(30_000, Math.min(DEFAULT_BUDGET_MS, parsed.budgetMs ?? DEFAULT_BUDGET_MS));
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  const allRecords = loadRecords();
  if (!allRecords) {
    return NextResponse.json({ error: 'Textbook data file not found.' }, { status: 404 });
  }

  const topicId = `grade${grade}`;
  const topicNameByKey = new Map(
    getTopicsForGrade(grade)
      .filter((n) => !!n.subTopicKey)
      .map((n) => [n.subTopicKey as string, n.name]),
  );

  // Eligible records for this grade's data file, optionally filtered by chapter.
  const chapterSet = chapters && chapters.length ? new Set(chapters) : null;
  const eligible = allRecords.filter((r) => !chapterSet || chapterSet.has(r.chapter));

  // Resumability: skip records whose deterministic id already has a DB row.
  const existingRows = await prisma.question.findMany({
    where: { id: { in: eligible.map((r) => r.id) } },
    select: { id: true },
  });
  const existingIds = new Set(existingRows.map((r) => r.id));

  const start = Date.now();
  const overBudget = () => Date.now() - start > budgetMs;

  const perChapter = new Map<number, ChapterCounts>();
  const bump = (chapter: number, field: keyof ChapterCounts) => {
    let c = perChapter.get(chapter);
    if (!c) {
      c = emptyCounts();
      perChapter.set(chapter, c);
    }
    c[field] += 1;
  };

  let created = 0;
  let skippedExisting = 0;
  let verifiedPrinted = 0;
  let freshSolved = 0;
  let rejected = 0;
  let failed = 0;
  let attempted = 0;
  let remaining = 0;
  let stoppedForTime = false;

  for (const rec of eligible) {
    if (existingIds.has(rec.id)) {
      skippedExisting += 1;
      bump(rec.chapter, 'skippedExisting');
      continue;
    }

    if (stoppedForTime || overBudget() || (limit !== undefined && attempted >= limit)) {
      if (overBudget()) stoppedForTime = true;
      remaining += 1;
      continue;
    }

    attempted += 1;

    const options = {
      option1: rec.option1,
      option2: rec.option2,
      option3: rec.option3,
      option4: rec.option4,
    };

    try {
      // ── 1. Verify the answer ────────────────────────────────────────────────
      let verifiedKey: 'A' | 'B' | 'C' | 'D' | null = null;
      let viaFresh = false;

      if (rec.printedAnswer && (ANSWER_KEYS as readonly string[]).includes(rec.printedAnswer)) {
        const probe: AuthoredQuestion = {
          questionText: rec.questionText,
          ...options,
          correctAnswer: rec.printedAnswer,
          hint1: '', hint2: '', hint3: '',
          stepByStep: [],
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
        };
        if (await sanityCheck(probe, grade)) {
          verifiedKey = rec.printedAnswer;
        }
      }

      if (!verifiedKey) {
        // Printed answer absent or failed sanity → decide by self-consistency.
        const fresh = await solveTextbookFresh(rec.questionText, options, grade);
        if (fresh.correctKey) {
          verifiedKey = fresh.correctKey;
          viaFresh = true;
        } else {
          rejected += 1;
          bump(rec.chapter, 'rejected');
          continue;
        }
      }

      // ── 2. Enrich (grounded on the verified answer) ─────────────────────────
      const topicName = topicNameByKey.get(rec.subTopicKey) ?? rec.chapterTitle;
      const enrichment = await enrichTextbookQuestion({
        questionText: rec.questionText,
        options,
        correctAnswer: verifiedKey,
        grade,
        topicName,
        subTopic: rec.storedSubTopic,
      });

      // ── 3. Persist ──────────────────────────────────────────────────────────
      const q: AuthoredQuestion = {
        questionText: rec.questionText,
        ...options,
        correctAnswer: verifiedKey,
        hint1: enrichment.hint1,
        hint2: enrichment.hint2,
        hint3: enrichment.hint3,
        stepByStep: enrichment.stepByStep,
        misconceptionA: enrichment.misconceptionA,
        misconceptionB: enrichment.misconceptionB,
        misconceptionC: enrichment.misconceptionC,
        misconceptionD: enrichment.misconceptionD,
      };

      await persistAuthoredQuestion(topicId, rec.storedSubTopic, enrichment.difficulty, q, {
        source: 'ipm_textbook',
        id: rec.id,
      });

      created += 1;
      bump(rec.chapter, 'created');
      if (viaFresh) {
        freshSolved += 1;
        bump(rec.chapter, 'freshSolved');
      } else {
        verifiedPrinted += 1;
        bump(rec.chapter, 'verifiedPrinted');
      }
    } catch (err) {
      logError('[admin/import-textbook] import failed', err);
      failed += 1;
      bump(rec.chapter, 'failed');
    }
  }

  const perChapterObj: Record<string, ChapterCounts> = {};
  for (const [chapter, counts] of Array.from(perChapter.entries())) {
    perChapterObj[chapter] = counts;
  }

  return NextResponse.json({
    grade,
    totalEligible: eligible.length,
    created,
    skippedExisting,
    verifiedPrinted,
    freshSolved,
    rejected,
    failed,
    remaining,
    done: remaining === 0,
    stoppedForTime,
    elapsedMs: Date.now() - start,
    perChapter: perChapterObj,
  });
}

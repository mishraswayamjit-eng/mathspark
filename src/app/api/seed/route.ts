import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import * as fs from 'fs';
import * as path from 'path';
// The bank reader and the one mapping from a bank question to a database row.
// Shared with the build-time sync (scripts/bank/sync.mjs), which is plain Node
// and cannot import TypeScript, so the shared module is plain JavaScript.
import { BANK_TOPICS, bankQuestionToRow, loadBank } from '../../../../scripts/bank/bankRows.mjs';
import type { BankQuestion } from '../../../../scripts/bank/bankRows.mjs';

export const dynamic = 'force-dynamic';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Derive grade from topicId: gradeN → N; ch-series / dh → 4 */
function getTopicGrade(topicId: string): number {
  const m = topicId.match(/^grade(\d)$/);
  return m ? parseInt(m[1], 10) : 4;
}

// ---------------------------------------------------------------------------
// The questions to seed
// ---------------------------------------------------------------------------

interface SeedQuestions {
  /** 'bank' = data/bank (carries topic nodes); 'file' = the old single file. */
  from: 'bank' | 'file';
  questions: BankQuestion[];
}

// Read once per warm instance: the files do not change within a deployment.
let cachedSeedQuestions: SeedQuestions | null = null;

/** The questions, in a fixed order so that paging is stable. Null when there is nothing to read. */
function loadSeedQuestions(): SeedQuestions | null {
  if (cachedSeedQuestions) return cachedSeedQuestions;

  const bank = loadBank(process.cwd());
  if (bank.exists && bank.questions.length > 0) {
    cachedSeedQuestions = { from: 'bank', questions: bank.questions };
    return cachedSeedQuestions;
  }

  // Fallback for the time before data/bank exists: the old single seed file.
  // This branch (and the `from` flag) can go once data/mathspark_complete_seed.json is deleted.
  const dataPath = path.join(process.cwd(), 'data', 'mathspark_complete_seed.json');
  if (!fs.existsSync(dataPath)) return null;
  const { questions } = JSON.parse(fs.readFileSync(dataPath, 'utf-8')) as { questions: BankQuestion[] };
  cachedSeedQuestions = { from: 'file', questions };
  return cachedSeedQuestions;
}

// ---------------------------------------------------------------------------
// Topic + Subscription definitions
// ---------------------------------------------------------------------------

// The pools live beside the mapping (scripts/bank/bankRows.mjs) so the seed
// route and the build-time sync agree on which pool ids are valid.
const TOPICS = BANK_TOPICS;

const PLANS = [
  { id: 'plan_starter_monthly',   name: 'Starter',          tier: 1, priceINR: 50000,   durationDays: 30,  dailyLimitMinutes: 60,   aiChatDailyLimit: 5,   features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":false,"adaptiveEngine":false,"dashboard":false,"misconceptionFeedback":false,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
  { id: 'plan_advanced_monthly',  name: 'Advanced',         tier: 2, priceINR: 150000,  durationDays: 30,  dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
  { id: 'plan_unlimited_monthly', name: 'Unlimited',        tier: 3, priceINR: 500000,  durationDays: 30,  dailyLimitMinutes: 1440, aiChatDailyLimit: 100, features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":true,"misconceptionFeedback":true,"badges":true,"streaks":true,"aiTutor":true,"mockTest":true,"parentDashboard":true}' },
  { id: 'plan_starter_annual',    name: 'Starter Annual',   tier: 1, priceINR: 480000,  durationDays: 365, dailyLimitMinutes: 60,   aiChatDailyLimit: 5,   features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":false,"adaptiveEngine":false,"dashboard":false,"misconceptionFeedback":false,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
  { id: 'plan_advanced_annual',   name: 'Advanced Annual',  tier: 2, priceINR: 1440000, durationDays: 365, dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
  { id: 'plan_unlimited_annual',  name: 'Unlimited Annual', tier: 3, priceINR: 4800000, durationDays: 365, dailyLimitMinutes: 1440, aiChatDailyLimit: 100, features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":true,"misconceptionFeedback":true,"badges":true,"streaks":true,"aiTutor":true,"mockTest":true,"parentDashboard":true}' },
  { id: 'plan_advanced_weekly',   name: 'Advanced Weekly',  tier: 2, priceINR: 49900,   durationDays: 7,   dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
];

const PAGE_SIZE = 200; // questions per API call

// ---------------------------------------------------------------------------
// GET /api/seed?secret=xxx&page=0
// Every page: ensures topics + plans exist, then seeds the next batch.
// Safe to retry — all writes are upserts.
// ---------------------------------------------------------------------------
export async function GET(req: Request) {
  // ── Auth (timing-safe) ───────────────────────────────────────────────────
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // ── Interactive question seeding ──────────────────────────────────────────
  if (searchParams.get('page') === 'interactive') {
    try {
      const INTERACTIVE_QUESTIONS = [
        // 2× tapToColor — fraction shading
        {
          id: 'INTERACTIVE_TAP_RECT_01',
          topicId: 'ch07-08',
          subTopic: 'Fraction representation',
          difficulty: 'Easy',
          questionText: 'Shade 3/8 of the rectangle. Tap the parts you want to shade.',
          questionLatex: '',
          option1: '3 parts', option2: '4 parts', option3: '5 parts', option4: '6 parts',
          correctAnswer: 'A',
          hint1: 'Count carefully — you need exactly 3 out of 8 parts.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'tapToColor',
          interactionData: { shape: 'rectangle', totalParts: 8, correctCount: 3, columns: 4, label: 'Shade 3/8 of this shape' },
        },
        {
          id: 'INTERACTIVE_TAP_CIRCLE_01',
          topicId: 'ch07-08',
          subTopic: 'Fraction representation',
          difficulty: 'Easy',
          questionText: 'Shade 2/6 of the circle. Tap the slices you want to shade.',
          questionLatex: '',
          option1: '2 slices', option2: '3 slices', option3: '4 slices', option4: '1 slice',
          correctAnswer: 'A',
          hint1: 'You need to shade exactly 2 out of 6 equal slices.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'tapToColor',
          interactionData: { shape: 'circle', totalParts: 6, correctCount: 2, label: 'Shade 2/6 of this circle' },
        },
        // 2× dragToSort — number ordering
        {
          id: 'INTERACTIVE_DRAG_FRAC_01',
          topicId: 'ch07-08',
          subTopic: 'Comparing fractions',
          difficulty: 'Medium',
          questionText: 'Arrange these fractions from smallest to largest.',
          questionLatex: '',
          option1: '3/4, 1/2, 1/4, 1/8', option2: '1/8, 1/4, 1/2, 3/4', option3: '1/4, 1/8, 1/2, 3/4', option4: '1/2, 1/4, 3/4, 1/8',
          correctAnswer: 'B',
          hint1: 'Compare the fractions by finding a common denominator or thinking about what portion of a whole each represents.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'dragToSort',
          interactionData: { items: ['3/4', '1/2', '1/4', '1/8'], correctOrder: [3, 2, 1, 0], instruction: 'Drag to arrange from smallest to largest' },
        },
        {
          id: 'INTERACTIVE_DRAG_DEC_01',
          topicId: 'ch11',
          subTopic: 'Comparing decimals',
          difficulty: 'Medium',
          questionText: 'Arrange these decimals from smallest to largest.',
          questionLatex: '',
          option1: '0.75, 0.3, 0.5, 0.08', option2: '0.08, 0.3, 0.5, 0.75', option3: '0.3, 0.08, 0.5, 0.75', option4: '0.5, 0.3, 0.75, 0.08',
          correctAnswer: 'B',
          hint1: 'Compare digit by digit: look at tenths place first, then hundredths.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'dragToSort',
          interactionData: { items: ['0.75', '0.3', '0.5', '0.08'], correctOrder: [3, 1, 2, 0], instruction: 'Drag to arrange from smallest to largest' },
        },
        // 2× chartTap — pictograph reading
        {
          id: 'INTERACTIVE_CHART_PICTO_01',
          topicId: 'dh',
          subTopic: 'Data Handling',
          difficulty: 'Easy',
          questionText: 'In the pictograph below, which fruit is the most popular? Tap on it.',
          questionLatex: '',
          option1: 'Apple', option2: 'Banana', option3: 'Mango', option4: 'Orange',
          correctAnswer: 'C',
          hint1: 'Count the pictures for each fruit and find the one with the most.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'chartTap',
          interactionData: {
            diagramType: 'pictograph',
            correctRegion: 'mango',
            regions: [
              { id: 'apple',  label: 'Apple',  x: 10, y: 10, width: 80, height: 20 },
              { id: 'banana', label: 'Banana', x: 10, y: 30, width: 80, height: 20 },
              { id: 'mango',  label: 'Mango',  x: 10, y: 50, width: 80, height: 20 },
              { id: 'orange', label: 'Orange', x: 10, y: 70, width: 80, height: 20 },
            ],
          },
        },
        {
          id: 'INTERACTIVE_CHART_PICTO_02',
          topicId: 'dh',
          subTopic: 'Data Handling',
          difficulty: 'Easy',
          questionText: 'In the pictograph below, which sport has the fewest students? Tap on it.',
          questionLatex: '',
          option1: 'Cricket', option2: 'Football', option3: 'Tennis', option4: 'Basketball',
          correctAnswer: 'C',
          hint1: 'Count the pictures for each sport and find the one with the fewest.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'chartTap',
          interactionData: {
            diagramType: 'pictograph',
            correctRegion: 'tennis',
            regions: [
              { id: 'cricket',    label: 'Cricket',    x: 10, y: 10, width: 80, height: 20 },
              { id: 'football',   label: 'Football',   x: 10, y: 30, width: 80, height: 20 },
              { id: 'tennis',     label: 'Tennis',      x: 10, y: 50, width: 80, height: 20 },
              { id: 'basketball', label: 'Basketball', x: 10, y: 70, width: 80, height: 20 },
            ],
          },
        },
        // 2× tileBuild — fill the blanks of a worked line (answers hand-checked)
        {
          id: 'INTERACTIVE_TILE_EQN_01',
          topicId: 'ch14',
          subTopic: 'Solving equations',
          difficulty: 'Medium',
          // 2n + 3 = 11  →  2n = 11 − 3 = 8  →  n = 8 ÷ 2 = 4
          questionText: 'Solve 2n + 3 = 11. Tap the tiles to fill the blanks.',
          questionLatex: '',
          option1: 'n = 4', option2: 'n = 7', option3: 'n = 8', option4: 'n = 14',
          correctAnswer: 'A',
          hint1: 'Undo the + 3 first, then undo the × 2.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'tileBuild',
          interactionData: {
            parts: ['2n = 11 −', null, '=', null, ', so n =', null],
            tiles: ['8', '3', '14', '4', '7'],
            solution: ['3', '8', '4'],
            instruction: 'Tap a tile to drop it into the next blank',
          },
        },
        {
          id: 'INTERACTIVE_TILE_FRAC_01',
          topicId: 'ch07-08',
          subTopic: 'Adding fractions',
          difficulty: 'Medium',
          // 1/2 = 2/4, so 1/4 + 1/2 = 1/4 + 2/4 = 3/4
          questionText: 'Add 1/4 + 1/2. Tap the tiles to fill the blanks.',
          questionLatex: '',
          option1: '3/4', option2: '2/6', option3: '2/4', option4: '1/6',
          correctAnswer: 'A',
          hint1: 'Change 1/2 into quarters first, so both fractions have the same bottom number.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'tileBuild',
          interactionData: {
            parts: ['1/2 =', null, '/ 4,', 'so 1/4 + 1/2 =', null, '/ 4'],
            tiles: ['1', '2', '3', '4', '6'],
            solution: ['2', '3'],
            instruction: 'Tap a tile to drop it into the next blank',
          },
        },
        // 2× numberLine — drag the point to a value (answers hand-checked)
        {
          id: 'INTERACTIVE_NLINE_DEC_01',
          topicId: 'ch11',
          subTopic: 'Decimals on a number line',
          difficulty: 'Easy',
          // seven tenths = 0.7
          questionText: 'Where is seven tenths on the number line? Drag the point to it.',
          questionLatex: '',
          option1: '0.7', option2: '0.07', option3: '7.0', option4: '0.17',
          correctAnswer: 'A',
          hint1: 'Work out what each small step on this line is worth.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'numberLine',
          interactionData: {
            min: 0, max: 1, step: 0.1, labelEvery: 5, correctValue: 0.7, hideValue: true,
            instruction: 'Drag the point, or tap the line',
          },
        },
        {
          id: 'INTERACTIVE_NLINE_FRAC_01',
          topicId: 'ch07-08',
          subTopic: 'Fractions on a number line',
          difficulty: 'Medium',
          // each step is 1/4; 3/4 is three steps from 0 (= 0.75)
          questionText: 'Where is 3/4 on a number line from 0 to 2? Drag the point to it.',
          questionLatex: '',
          option1: 'Between 0 and 1, closer to 1', option2: 'Exactly halfway between 0 and 1',
          option3: 'Between 1 and 2', option4: 'Exactly at 1',
          correctAnswer: 'A',
          hint1: 'Work out what each small step on this line is worth, then think about quarters.',
          hint2: '', hint3: '',
          stepByStep: '[]',
          misconceptionA: '', misconceptionB: '', misconceptionC: '', misconceptionD: '',
          source: 'interactive_seed',
          interactionType: 'numberLine',
          interactionData: {
            min: 0, max: 2, step: 0.25, labelEvery: 4, correctValue: 0.75, hideValue: true,
            instruction: 'Drag the point, or tap the line',
          },
        },
      ];

      // Parallelize upserts — the interactive set is tiny (<10 rows) so a
      // single Promise.all stays comfortably under the Neon free-tier
      // connection cap. The chunked larger seed below uses the same pattern.
      const results = await Promise.all(
        INTERACTIVE_QUESTIONS.map((q) => {
          const { interactionType, interactionData, ...rest } = q;
          return prisma.question.upsert({
            where: { id: q.id },
            update: { ...rest, interactionType, interactionData: interactionData as object },
            create: { ...rest, interactionType, interactionData: interactionData as object },
          });
        }),
      );
      const seeded = results.length;

      return NextResponse.json({
        done: true,
        seeded,
        message: `Seeded ${seeded} interactive questions (tapToColor, dragToSort, chartTap)`,
      });
    } catch (err) {
      logError('[seed] Interactive seed error:', err);
      return NextResponse.json(
        { error: `Interactive seed failed: ${err instanceof Error ? err.message : String(err)}` },
        { status: 500 },
      );
    }
  }

  try {
    const page = parseInt(searchParams.get('page') ?? '0', 10);

    // ── Load the questions: the bank (data/bank), or the old file before it exists ──
    const loaded = loadSeedQuestions();
    if (!loaded) {
      return NextResponse.json(
        { error: 'No questions found. Expected the question bank (data/bank/gradeN/*.json) or data/mathspark_complete_seed.json.' },
        { status: 500 },
      );
    }
    const questions = loaded.questions;
    const fromBank = loaded.from === 'bank';

    // ── ALWAYS ensure topics + plans exist (idempotent, fast) ──────────────
    // This runs on every page so a retry after failure never hits a missing-topic FK error.
    await Promise.all([
      ...TOPICS.map((t) => {
        const grade = getTopicGrade(t.id);
        return prisma.topic.upsert({
          where:  { id: t.id },
          update: { ...t, grade },
          create: { ...t, grade },
        });
      }),
      ...PLANS.map(({ id, ...data }) =>
        prisma.subscription.upsert({ where: { id }, update: data, create: { id, ...data } }),
      ),
    ]);

    // ── Seed this page of questions ─────────────────────────────────────────
    const start = page * PAGE_SIZE;
    const batch = questions.slice(start, start + PAGE_SIZE);

    let seededCount = 0;
    const skipped: string[] = [];

    // Chunked parallel upserts — Vercel Hobby has a 10s hard timeout and
    // Neon's free tier caps at ~5 pooled connections. CHUNK_SIZE=20 gives
    // a ~10x speedup over serial upserts while staying within the pool.
    const CHUNK_SIZE = 20;
    for (let i = 0; i < batch.length; i += CHUNK_SIZE) {
      const chunk = batch.slice(i, i + CHUNK_SIZE);
      const results = await Promise.all(chunk.map(async (q) => {
        try {
          // The one mapping, shared with the build-time sync. `retired` is never written here.
          const { id, nodeId, ...content } = bankQuestionToRow(q);
          // The old file carries no topic nodes: leave `nodeId` alone rather than clearing it.
          const f = fromBank ? { ...content, nodeId } : content;
          await prisma.question.upsert({ where: { id }, update: f, create: { id, ...f } });
          return { ok: true as const, id };
        } catch (err) {
          const msg = err instanceof Error ? err.message : String(err);
          const badId = q && typeof q.id === 'string' ? q.id : '(no id)';
          logError(`[seed] Skipping question ${badId}:`, msg);
          return { ok: false as const, id: badId };
        }
      }));
      for (const r of results) {
        if (r.ok) seededCount++;
        else skipped.push(r.id);
      }
    }

    const totalSeeded = start + seededCount;
    const done = start + batch.length >= questions.length;

    return NextResponse.json({
      done,
      seeded:   totalSeeded,
      total:    questions.length,
      nextPage: done ? null : page + 1,
      skipped:  skipped.length,
      message:  done
        ? `All ${questions.length} questions seeded!${skipped.length ? ` (${skipped.length} skipped)` : ''}`
        : `Seeded ${totalSeeded}/${questions.length}${skipped.length ? ` · ${skipped.length} skipped this page` : ''}`,
    });

  } catch (err) {
    logError(`[seed] Fatal error on page ${new URL(req.url).searchParams.get('page')}`, err);
    return NextResponse.json(
      { error: `Seed failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

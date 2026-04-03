import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Strip null bytes — PostgreSQL rejects \x00 in text columns (error 22021) */
function s(str: string | undefined | null): string {
  return (str ?? '').replace(/\x00/g, '');
}

/** Derive grade from topicId: gradeN → N; ch-series / dh → 4 */
function getTopicGrade(topicId: string): number {
  const m = topicId.match(/^grade(\d)$/);
  return m ? parseInt(m[1], 10) : 4;
}

/**
 * Remap topicIds that appear in the seed JSON but are not valid FK targets.
 * The seed JSON uses bare chapter numbers (ch01, ch07, ch09) where the DB
 * uses merged-range IDs (ch01-05, ch07-08, ch09-10).
 */
const TOPIC_ID_REMAP: Record<string, string> = {
  'ch01': 'ch01-05', 'ch02': 'ch01-05', 'ch03': 'ch01-05',
  'ch04': 'ch01-05', 'ch05': 'ch01-05',
  'ch07': 'ch07-08', 'ch08': 'ch07-08',
  'ch09': 'ch09-10', 'ch10': 'ch09-10',
};

/**
 * Derive topicId from question ID when no explicit topicId is in the JSON.
 */
function getTopicId(questionId: string): string {
  const upper = questionId.toUpperCase();
  if (upper.startsWith('Q_DH_'))  return 'dh';
  if (upper.startsWith('PYQ_'))   return 'grade4'; // real IPM Std.4 past papers
  // EXT_G*, VAR_EXT_G*, VAR_G* patterns → grade pool
  const gradeMatch = upper.match(/(?:EXT|VAR_EXT|VAR)_G(\d)/);
  if (gradeMatch) {
    const g = parseInt(gradeMatch[1], 10);
    if (g >= 2 && g <= 9) return `grade${g}`;
  }
  const match = upper.match(/^Q_CH(\d+)_/);
  if (!match) return 'ch11';
  const n = parseInt(match[1], 10);
  if (n <= 5)              return 'ch01-05';
  if (n === 6)             return 'ch06';
  if (n === 7 || n === 8)  return 'ch07-08';
  if (n === 9 || n === 10) return 'ch09-10';
  return `ch${String(n).padStart(2, '0')}`;
}

/** Resolve a question's topicId with remapping + fallback chain */
function resolveTopicId(questionId: string, rawTopicId: string | undefined, validIds: Set<string>): string {
  // 1. Start with explicit JSON value (or derive from ID)
  let tid = rawTopicId ?? getTopicId(questionId);
  // 2. Remap known bad values (ch01→ch01-05, ch07→ch07-08, ch09→ch09-10, etc.)
  tid = TOPIC_ID_REMAP[tid] ?? tid;
  // 3. If still invalid, derive from ID
  if (!validIds.has(tid)) tid = getTopicId(questionId);
  // 4. If still invalid (unexpected ID format), default to ch11
  if (!validIds.has(tid)) tid = 'ch11';
  return tid;
}

// ---------------------------------------------------------------------------
// Topic + Subscription definitions
// ---------------------------------------------------------------------------

const TOPICS = [
  // Grade 4 curriculum chapters
  { id: 'ch01-05', name: 'Number System & Place Value',    chapterNumber: '1-5'  },
  { id: 'ch06',    name: 'Factors & Multiples',             chapterNumber: '6'    },
  { id: 'ch07-08', name: 'Fractions',                       chapterNumber: '7-8'  },
  { id: 'ch09-10', name: 'Operations & BODMAS',             chapterNumber: '9-10' },
  { id: 'ch11',    name: 'Decimal Fractions',               chapterNumber: '11'   },
  { id: 'ch12',    name: 'Decimal Units of Measurement',    chapterNumber: '12'   },
  { id: 'ch13',    name: 'Algebraic Expressions',           chapterNumber: '13'   },
  { id: 'ch14',    name: 'Equations',                       chapterNumber: '14'   },
  { id: 'ch15',    name: 'Puzzles & Magic Squares',         chapterNumber: '15'   },
  { id: 'ch16',    name: 'Sequence & Series',               chapterNumber: '16'   },
  { id: 'ch17',    name: 'Measurement of Time & Calendar',  chapterNumber: '17'   },
  { id: 'ch18',    name: 'Angles',                          chapterNumber: '18'   },
  { id: 'ch19',    name: 'Triangles',                       chapterNumber: '19'   },
  { id: 'ch20',    name: 'Quadrilaterals',                  chapterNumber: '20'   },
  { id: 'ch21',    name: 'Circle',                          chapterNumber: '21'   },
  { id: 'dh',      name: 'Data Handling & Graphs',          chapterNumber: 'DH'   },
  // IPM past-paper / practice pools (Grades 2–9)
  { id: 'grade2',  name: 'Grade 2 — IPM Practice',         chapterNumber: 'G2'   },
  { id: 'grade3',  name: 'Grade 3 — IPM Practice',         chapterNumber: 'G3'   },
  { id: 'grade4',  name: 'Grade 4 — IPM Past Papers',      chapterNumber: 'G4'   },
  { id: 'grade5',  name: 'Grade 5 — IPM Practice',         chapterNumber: 'G5'   },
  { id: 'grade6',  name: 'Grade 6 — IPM Practice',         chapterNumber: 'G6'   },
  { id: 'grade7',  name: 'Grade 7 — IPM Practice',         chapterNumber: 'G7'   },
  { id: 'grade8',  name: 'Grade 8 — IPM Practice',         chapterNumber: 'G8'   },
  { id: 'grade9',  name: 'Grade 9 — IPM Practice',         chapterNumber: 'G9'   },
];

const VALID_TOPIC_IDS = new Set(TOPICS.map((t) => t.id));

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
  // ── Auth ──────────────────────────────────────────────────────────────────
  const secret = process.env.SEED_SECRET;
  const { searchParams } = new URL(req.url);
  if (!secret || searchParams.get('secret') !== secret) {
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
      ];

      let seeded = 0;
      for (const q of INTERACTIVE_QUESTIONS) {
        const { interactionType, interactionData, ...rest } = q;
        await prisma.question.upsert({
          where: { id: q.id },
          update: { ...rest, interactionType, interactionData: interactionData as object },
          create: { ...rest, interactionType, interactionData: interactionData as object },
        });
        seeded++;
      }

      return NextResponse.json({
        done: true,
        seeded,
        message: `Seeded ${seeded} interactive questions (tapToColor, dragToSort, chartTap)`,
      });
    } catch (err) {
      console.error('[seed] Interactive seed error:', err);
      return NextResponse.json(
        { error: `Interactive seed failed: ${err instanceof Error ? err.message : String(err)}` },
        { status: 500 },
      );
    }
  }

  try {
    const page = parseInt(searchParams.get('page') ?? '0', 10);

    // ── Load seed JSON ──────────────────────────────────────────────────────
    const dataPath = path.join(process.cwd(), 'data', 'mathspark_complete_seed.json');
    if (!fs.existsSync(dataPath)) {
      return NextResponse.json(
        { error: 'Seed file not found. Make sure data/mathspark_complete_seed.json is committed.' },
        { status: 500 },
      );
    }
    const { questions } = JSON.parse(fs.readFileSync(dataPath, 'utf-8')) as {
      questions: Array<{
        id: string; topicId?: string; year?: number; questionNumber?: number;
        subTopic?: string; difficulty?: string; questionText?: string;
        questionLatex?: string; options?: Array<{ id: string; text: string }>;
        correctAnswer?: string; hints?: string[]; stepByStep?: unknown[];
        misconceptions?: Record<string, string>; source?: string;
      }>;
    };

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

    for (const q of batch) {
      try {
        const topicId = resolveTopicId(q.id, q.topicId, VALID_TOPIC_IDS);
        const f = {
          topicId,
          subTopic:       s(q.subTopic),
          difficulty:     s(q.difficulty)    || 'Medium',
          questionText:   s(q.questionText),
          questionLatex:  s(q.questionLatex),
          option1:        s(q.options?.[0]?.text),
          option2:        s(q.options?.[1]?.text),
          option3:        s(q.options?.[2]?.text),
          option4:        s(q.options?.[3]?.text),
          correctAnswer:  s(q.correctAnswer)  || 'A',
          hint1:          s(q.hints?.[0]),
          hint2:          s(q.hints?.[1]),
          hint3:          s(q.hints?.[2]),
          stepByStep:     s(JSON.stringify(q.stepByStep ?? [])),
          misconceptionA: s(q.misconceptions?.['A']),
          misconceptionB: s(q.misconceptions?.['B']),
          misconceptionC: s(q.misconceptions?.['C']),
          misconceptionD: s(q.misconceptions?.['D']),
          source:         s(q.source)         || 'auto_generated',
          year:           q.year              ?? null,
          questionNumber: q.questionNumber    ?? null,
        };
        await prisma.question.upsert({ where: { id: q.id }, update: f, create: { id: q.id, ...f } });
        seededCount++;
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        console.error(`[seed] Skipping question ${q.id}:`, msg);
        skipped.push(q.id);
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
    console.error('[seed] Fatal error on page', new URL(req.url).searchParams.get('page'), err);
    return NextResponse.json(
      { error: `Seed failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

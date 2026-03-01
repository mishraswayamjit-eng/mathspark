import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

// ---------------------------------------------------------------------------
// Topic definitions (mirrors prisma/seed.ts)
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
 * Derive topicId from question ID when no explicit topicId is in the JSON.
 * PYQ questions (PYQ_YYYY_QNN) → 'grade4' (Grade 4 IPM past papers pool).
 * ch-series questions → mapped by chapter number.
 * Everything else → 'ch11' fallback.
 */

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
  // IPM past-paper pools (Grades 2–9)
  { id: 'grade2',  name: 'Grade 2 — IPM Practice',         chapterNumber: 'G2'   },
  { id: 'grade3',  name: 'Grade 3 — IPM Practice',         chapterNumber: 'G3'   },
  { id: 'grade4',  name: 'Grade 4 — IPM Past Papers',      chapterNumber: 'G4'   },
  { id: 'grade5',  name: 'Grade 5 — IPM Practice',         chapterNumber: 'G5'   },
  { id: 'grade6',  name: 'Grade 6 — IPM Practice',         chapterNumber: 'G6'   },
  { id: 'grade7',  name: 'Grade 7 — IPM Practice',         chapterNumber: 'G7'   },
  { id: 'grade8',  name: 'Grade 8 — IPM Practice',         chapterNumber: 'G8'   },
  { id: 'grade9',  name: 'Grade 9 — IPM Practice',         chapterNumber: 'G9'   },
];

function getTopicId(questionId: string): string {
  const upper = questionId.toUpperCase();
  if (upper.startsWith('Q_DH_'))  return 'dh';
  if (upper.startsWith('PYQ_'))   return 'grade4'; // real IPM Std.4 past papers
  const match = upper.match(/^Q_CH(\d+)_/);
  if (!match) return 'ch11';
  const n = parseInt(match[1], 10);
  if (n <= 5)              return 'ch01-05';
  if (n === 6)             return 'ch06';
  if (n === 7 || n === 8)  return 'ch07-08';
  if (n === 9 || n === 10) return 'ch09-10';
  return `ch${String(n).padStart(2, '0')}`;
}

const PAGE_SIZE = 75; // questions per API call — safe for Vercel's 300s limit

// ---------------------------------------------------------------------------
// GET /api/seed?secret=xxx&page=0
// page=0 → seeds topics + first batch of questions
// page=N → seeds next batch
// ---------------------------------------------------------------------------
export async function GET(req: Request) {
  // ── Auth ─────────────────────────────────────────────────────────────────
  const secret = process.env.SEED_SECRET;
  if (!secret) {
    return NextResponse.json(
      { error: 'SEED_SECRET env var not set. Add it in Vercel → Settings → Environment Variables.' },
      { status: 500 },
    );
  }
  const { searchParams } = new URL(req.url);
  if (searchParams.get('secret') !== secret) {
    return NextResponse.json({ error: 'Wrong secret.' }, { status: 401 });
  }

  try {
  const page = parseInt(searchParams.get('page') ?? '0', 10);

  // ── Load seed JSON ────────────────────────────────────────────────────────
  const dataPath = path.join(process.cwd(), 'data', 'mathspark_complete_seed.json');
  if (!fs.existsSync(dataPath)) {
    return NextResponse.json({ error: 'Seed file not found. Make sure data/mathspark_complete_seed.json is committed.' }, { status: 500 });
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

  // ── Page 0: upsert all 24 topics + 7 subscription plans ─────────────────
  if (page === 0) {
    await Promise.all(
      TOPICS.map((t) => {
        const grade = getTopicGrade(t.id);
        return prisma.topic.upsert({
          where:  { id: t.id },
          update: { ...t, grade },
          create: { ...t, grade },
        });
      }),
    );

    const PLANS = [
      { id: 'plan_starter_monthly',  name: 'Starter',          tier: 1, priceINR: 50000,   durationDays: 30,  dailyLimitMinutes: 60,   aiChatDailyLimit: 5,   features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":false,"adaptiveEngine":false,"dashboard":false,"misconceptionFeedback":false,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
      { id: 'plan_advanced_monthly', name: 'Advanced',         tier: 2, priceINR: 150000,  durationDays: 30,  dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
      { id: 'plan_unlimited_monthly',name: 'Unlimited',        tier: 3, priceINR: 500000,  durationDays: 30,  dailyLimitMinutes: 1440, aiChatDailyLimit: 100, features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":true,"misconceptionFeedback":true,"badges":true,"streaks":true,"aiTutor":true,"mockTest":true,"parentDashboard":true}' },
      { id: 'plan_starter_annual',   name: 'Starter Annual',   tier: 1, priceINR: 480000,  durationDays: 365, dailyLimitMinutes: 60,   aiChatDailyLimit: 5,   features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":false,"adaptiveEngine":false,"dashboard":false,"misconceptionFeedback":false,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
      { id: 'plan_advanced_annual',  name: 'Advanced Annual',  tier: 2, priceINR: 1440000, durationDays: 365, dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
      { id: 'plan_unlimited_annual', name: 'Unlimited Annual', tier: 3, priceINR: 4800000, durationDays: 365, dailyLimitMinutes: 1440, aiChatDailyLimit: 100, features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":true,"misconceptionFeedback":true,"badges":true,"streaks":true,"aiTutor":true,"mockTest":true,"parentDashboard":true}' },
      { id: 'plan_advanced_weekly',  name: 'Advanced Weekly',  tier: 2, priceINR: 49900,   durationDays: 7,   dailyLimitMinutes: 300,  aiChatDailyLimit: 25,  features: '{"practice":true,"chapters":true,"hints":true,"stepByStep":true,"progressTracking":true,"diagnosticQuiz":true,"adaptiveEngine":true,"dashboard":false,"misconceptionFeedback":true,"badges":false,"streaks":false,"aiTutor":true,"mockTest":false,"parentDashboard":false}' },
    ];
    await Promise.all(
      PLANS.map(({ id, ...data }) =>
        prisma.subscription.upsert({ where: { id }, update: data, create: { id, ...data } }),
      ),
    );
  }

  // ── Seed this page of questions ───────────────────────────────────────────
  const start = page * PAGE_SIZE;
  const batch = questions.slice(start, start + PAGE_SIZE);

  if (batch.length > 0) {
    await prisma.$transaction(
      batch.map((q) => {
        const f = {
          topicId:        q.topicId ?? getTopicId(q.id), // prefer explicit topicId from JSON
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
        return prisma.question.upsert({ where: { id: q.id }, update: f, create: { id: q.id, ...f } });
      }),
    );
  }

  const seeded = Math.min(start + PAGE_SIZE, questions.length);
  const done   = seeded >= questions.length;

  return NextResponse.json({
    done,
    seeded,
    total:    questions.length,
    nextPage: done ? null : page + 1,
    message:  done
      ? `All ${questions.length} questions seeded!`
      : `Seeded ${seeded}/${questions.length}`,
  });
  } catch (err) {
    console.error('[seed] Error on page', new URL(req.url).searchParams.get('page'), err);
    return NextResponse.json(
      { error: `Seed failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

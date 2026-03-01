import { PrismaClient } from '@prisma/client';
import * as fs from 'fs';
import * as path from 'path';

const prisma = new PrismaClient();

// ---------------------------------------------------------------------------
// Topic definitions — matches CLAUDE.md exactly
// ---------------------------------------------------------------------------

/** Derive grade from topicId: gradeN → N; ch-series / dh → 4 */
function getTopicGrade(topicId: string): number {
  const m = topicId.match(/^grade(\d)$/);
  return m ? parseInt(m[1], 10) : 4;
}

const TOPIC_MAP: Record<string, { id: string; name: string; chapterNumber: string }> = {
  // Grade 4 curriculum chapters
  'ch01-05': { id: 'ch01-05', name: 'Number System & Place Value',    chapterNumber: '1-5'  },
  'ch06':    { id: 'ch06',    name: 'Factors & Multiples',             chapterNumber: '6'    },
  'ch07-08': { id: 'ch07-08', name: 'Fractions',                       chapterNumber: '7-8'  },
  'ch09-10': { id: 'ch09-10', name: 'Operations & BODMAS',             chapterNumber: '9-10' },
  'ch11':    { id: 'ch11',    name: 'Decimal Fractions',               chapterNumber: '11'   },
  'ch12':    { id: 'ch12',    name: 'Decimal Units of Measurement',    chapterNumber: '12'   },
  'ch13':    { id: 'ch13',    name: 'Algebraic Expressions',           chapterNumber: '13'   },
  'ch14':    { id: 'ch14',    name: 'Equations',                       chapterNumber: '14'   },
  'ch15':    { id: 'ch15',    name: 'Puzzles & Magic Squares',         chapterNumber: '15'   },
  'ch16':    { id: 'ch16',    name: 'Sequence & Series',               chapterNumber: '16'   },
  'ch17':    { id: 'ch17',    name: 'Measurement of Time & Calendar',  chapterNumber: '17'   },
  'ch18':    { id: 'ch18',    name: 'Angles',                          chapterNumber: '18'   },
  'ch19':    { id: 'ch19',    name: 'Triangles',                       chapterNumber: '19'   },
  'ch20':    { id: 'ch20',    name: 'Quadrilaterals',                  chapterNumber: '20'   },
  'ch21':    { id: 'ch21',    name: 'Circle',                          chapterNumber: '21'   },
  'dh':      { id: 'dh',      name: 'Data Handling & Graphs',          chapterNumber: 'DH'   },
  // IPM past-paper pools (Grades 2–9)
  'grade2':  { id: 'grade2',  name: 'Grade 2 — IPM Practice',         chapterNumber: 'G2'   },
  'grade3':  { id: 'grade3',  name: 'Grade 3 — IPM Practice',         chapterNumber: 'G3'   },
  'grade4':  { id: 'grade4',  name: 'Grade 4 — IPM Past Papers',      chapterNumber: 'G4'   },
  'grade5':  { id: 'grade5',  name: 'Grade 5 — IPM Practice',         chapterNumber: 'G5'   },
  'grade6':  { id: 'grade6',  name: 'Grade 6 — IPM Practice',         chapterNumber: 'G6'   },
  'grade7':  { id: 'grade7',  name: 'Grade 7 — IPM Practice',         chapterNumber: 'G7'   },
  'grade8':  { id: 'grade8',  name: 'Grade 8 — IPM Practice',         chapterNumber: 'G8'   },
  'grade9':  { id: 'grade9',  name: 'Grade 9 — IPM Practice',         chapterNumber: 'G9'   },
};

// ---------------------------------------------------------------------------
// Map a question ID like "Q_CH11_042" or "Q_DH_003" → topic ID
// ---------------------------------------------------------------------------
function getTopicId(questionId: string): string {
  const upper = questionId.toUpperCase();

  if (upper.startsWith('Q_DH_')) return 'dh';

  const match = upper.match(/^Q_CH(\d+)_/);
  if (!match) {
    console.warn(`  ⚠ Cannot parse topic from: ${questionId} — defaulting to ch11`);
    return 'ch11';
  }

  const n = parseInt(match[1], 10);
  if (n >= 1 && n <= 5)  return 'ch01-05';
  if (n === 6)           return 'ch06';
  if (n === 7 || n === 8)  return 'ch07-08';
  if (n === 9 || n === 10) return 'ch09-10';
  // ch11-ch21 → 'ch11', 'ch12', …, 'ch21'
  return `ch${String(n).padStart(2, '0')}`;
}

// ---------------------------------------------------------------------------
// Main seed function
// ---------------------------------------------------------------------------
async function main() {
  const dataPath = path.join(process.cwd(), 'data', 'mathspark_complete_seed.json');

  if (!fs.existsSync(dataPath)) {
    throw new Error(`Seed file not found at: ${dataPath}\nPlace mathspark_complete_seed.json in the data/ folder.`);
  }

  const raw  = fs.readFileSync(dataPath, 'utf-8');
  const data = JSON.parse(raw) as {
    metadata: { totalQuestions: number };
    questions: Array<{
      id: string;
      topicId?: string;          // explicit for PYQ questions
      year?: number;             // PYQ: 2016-2019
      questionNumber?: number;   // PYQ: original exam order
      subTopic?: string;
      difficulty?: string;
      questionText?: string;
      questionLatex?: string;
      options?: Array<{ id: string; text: string }>;
      correctAnswer?: string;
      hints?: string[];
      stepByStep?: unknown[];
      misconceptions?: Record<string, string>;
      source?: string;
    }>;
  };

  const questions = data.questions;
  console.log(`\n🌱 Starting MathSpark seed — ${questions.length} questions\n`);

  // ── 1. Upsert topics (16 ch-series + 8 grade-pool = 24 total) ─────────────
  for (const topic of Object.values(TOPIC_MAP)) {
    const grade = getTopicGrade(topic.id);
    await prisma.topic.upsert({
      where:  { id: topic.id },
      update: { name: topic.name, chapterNumber: topic.chapterNumber, grade },
      create: { ...topic, grade },
    });
  }
  console.log(`✓ ${Object.keys(TOPIC_MAP).length} topics seeded`);

  // ── 2. Upsert questions in batches of 50 (SQLite-safe) ───────────────────
  const BATCH = 50;
  let done = 0;
  let skipped = 0;

  for (let i = 0; i < questions.length; i += BATCH) {
    const batch = questions.slice(i, i + BATCH);

    await prisma.$transaction(
      batch.map((q) => {
        // PYQ questions carry an explicit topicId in the JSON
        const topicId        = q.topicId ?? getTopicId(q.id);
        const options        = q.options        ?? [];
        const hints          = q.hints          ?? [];
        const misconceptions = q.misconceptions ?? {};

        const fields = {
          topicId,
          subTopic:      q.subTopic      ?? '',
          difficulty:    q.difficulty    ?? 'Medium',
          questionText:  q.questionText  ?? '',
          questionLatex: q.questionLatex ?? '',
          option1:       options[0]?.text ?? '',
          option2:       options[1]?.text ?? '',
          option3:       options[2]?.text ?? '',
          option4:       options[3]?.text ?? '',
          correctAnswer: q.correctAnswer  ?? 'A',
          hint1:         hints[0]         ?? '',
          hint2:         hints[1]         ?? '',
          hint3:         hints[2]         ?? '',
          stepByStep:    JSON.stringify(q.stepByStep ?? []),
          misconceptionA: misconceptions['A'] ?? '',
          misconceptionB: misconceptions['B'] ?? '',
          misconceptionC: misconceptions['C'] ?? '',
          misconceptionD: misconceptions['D'] ?? '',
          source:         q.source        ?? 'auto_generated',
          year:           q.year          ?? null,
          questionNumber: q.questionNumber ?? null,
        };

        return prisma.question.upsert({
          where:  { id: q.id },
          update: fields,
          create: { id: q.id, ...fields },
        });
      })
    );

    done += batch.length;
    process.stdout.write(`\r  Questions: ${done}/${questions.length}`);
  }

  console.log(`\n✓ ${done} questions seeded (${skipped} skipped)\n`);

  // ── 3. Upsert subscription plans ──────────────────────────────────────────
  const SUBSCRIPTION_PLANS = [
    {
      id: 'plan_starter_monthly', name: 'Starter', tier: 1,
      priceINR: 50000, durationDays: 30, dailyLimitMinutes: 60, aiChatDailyLimit: 5,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:false,adaptiveEngine:false,dashboard:false,misconceptionFeedback:false,badges:false,streaks:false,aiTutor:true,mockTest:false,parentDashboard:false }),
    },
    {
      id: 'plan_advanced_monthly', name: 'Advanced', tier: 2,
      priceINR: 150000, durationDays: 30, dailyLimitMinutes: 300, aiChatDailyLimit: 25,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:true,adaptiveEngine:true,dashboard:false,misconceptionFeedback:true,badges:false,streaks:false,aiTutor:true,mockTest:false,parentDashboard:false }),
    },
    {
      id: 'plan_unlimited_monthly', name: 'Unlimited', tier: 3,
      priceINR: 500000, durationDays: 30, dailyLimitMinutes: 1440, aiChatDailyLimit: 100,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:true,adaptiveEngine:true,dashboard:true,misconceptionFeedback:true,badges:true,streaks:true,aiTutor:true,mockTest:true,parentDashboard:true }),
    },
    {
      id: 'plan_starter_annual', name: 'Starter Annual', tier: 1,
      priceINR: 480000, durationDays: 365, dailyLimitMinutes: 60, aiChatDailyLimit: 5,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:false,adaptiveEngine:false,dashboard:false,misconceptionFeedback:false,badges:false,streaks:false,aiTutor:true,mockTest:false,parentDashboard:false }),
    },
    {
      id: 'plan_advanced_annual', name: 'Advanced Annual', tier: 2,
      priceINR: 1440000, durationDays: 365, dailyLimitMinutes: 300, aiChatDailyLimit: 25,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:true,adaptiveEngine:true,dashboard:false,misconceptionFeedback:true,badges:false,streaks:false,aiTutor:true,mockTest:false,parentDashboard:false }),
    },
    {
      id: 'plan_unlimited_annual', name: 'Unlimited Annual', tier: 3,
      priceINR: 4800000, durationDays: 365, dailyLimitMinutes: 1440, aiChatDailyLimit: 100,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:true,adaptiveEngine:true,dashboard:true,misconceptionFeedback:true,badges:true,streaks:true,aiTutor:true,mockTest:true,parentDashboard:true }),
    },
    {
      id: 'plan_advanced_weekly', name: 'Advanced Weekly', tier: 2,
      priceINR: 49900, durationDays: 7, dailyLimitMinutes: 300, aiChatDailyLimit: 25,
      features: JSON.stringify({ practice:true,chapters:true,hints:true,stepByStep:true,progressTracking:true,diagnosticQuiz:true,adaptiveEngine:true,dashboard:false,misconceptionFeedback:true,badges:false,streaks:false,aiTutor:true,mockTest:false,parentDashboard:false }),
    },
  ];
  for (const plan of SUBSCRIPTION_PLANS) {
    const { id, ...data } = plan;
    await prisma.subscription.upsert({ where: { id }, update: data, create: { id, ...data } });
  }
  console.log(`✓ ${SUBSCRIPTION_PLANS.length} subscription plans seeded`);

  // ── 4. Quick sanity check ─────────────────────────────────────────────────
  const counts = await prisma.$queryRaw<Array<{ topicId: string; cnt: bigint }>>`
    SELECT topicId, COUNT(*) as cnt FROM Question GROUP BY topicId ORDER BY topicId
  `;

  console.log('📊 Questions per topic:');
  for (const row of counts) {
    const name = TOPIC_MAP[row.topicId]?.name ?? row.topicId;
    console.log(`   ${row.topicId.padEnd(10)} ${String(row.cnt).padStart(4)}  ${name}`);
  }

  const total = await prisma.question.count();
  console.log(`\n🎉 Done! ${total} questions in database.\n`);
}

main()
  .catch((e) => {
    console.error('\n❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());

import { MS_PER_DAY } from '@/lib/timeConstants';
import { prisma, USABLE_QUESTION_FILTER } from '@/lib/db';
import { getTopicsForGrade } from '@/data/topicTree';
import type { TestType, PYQYear } from '@/types';

// ── Config ────────────────────────────────────────────────────────────────────

export const TEST_CONFIG = {
  quick: { totalQuestions: 15, timeLimitMs: 20 * 60 * 1000, easy: 4, medium: 6,  hard: 5  },
  half:  { totalQuestions: 30, timeLimitMs: 40 * 60 * 1000, easy: 8, medium: 12, hard: 10 },
  full:  { totalQuestions: 50, timeLimitMs: 60 * 60 * 1000, easy: 15, medium: 20, hard: 15 },
  ipm:   { totalQuestions: 40, timeLimitMs: 60 * 60 * 1000, easy: 9, medium: 19, hard: 12 },
  pyq:   { totalQuestions: 40, timeLimitMs: 60 * 60 * 1000, easy: 0, medium: 0,  hard: 0  },
} as const;

// ── IPM Blueprint (from metadata.mockTestBlueprint) ───────────────────────────
// Each entry: topicId (DB), count, difficulty breakdown (E/M/H)
// Source: ch01→ch01-05, ch07→ch07-08, ch09→ch09-10, roman→ch01-05 (merged)

interface BlueprintSlot {
  topicId: string;
  subTopicKey?: string;
  count: number;
  easy: number;
  medium: number;
  hard: number;
}

// Grade 4: hand-tuned to match real IPM paper distribution (2016-2025 analysis)
// dh removed (Data Handling not tested in real IPM), ch09-10 bumped from 2→3
const MOCK_BLUEPRINT: BlueprintSlot[] = [
  { topicId: 'ch01-05', count: 5, easy: 1, medium: 3, hard: 1 }, // Numbers, Place Value, Roman, Squares
  { topicId: 'ch06',    count: 4, easy: 1, medium: 2, hard: 1 }, // Factors, Divisibility, LCM/HCF
  { topicId: 'ch07-08', count: 3, easy: 1, medium: 1, hard: 1 }, // Fractions
  { topicId: 'ch09-10', count: 3, easy: 1, medium: 1, hard: 1 }, // Operations & BODMAS
  { topicId: 'ch11',    count: 3, easy: 1, medium: 1, hard: 1 }, // Decimal Fractions
  { topicId: 'ch12',    count: 2, easy: 1, medium: 1, hard: 0 }, // Units of Measurement
  { topicId: 'ch13',    count: 2, easy: 0, medium: 1, hard: 1 }, // Algebraic Expressions
  { topicId: 'ch14',    count: 3, easy: 1, medium: 1, hard: 1 }, // Equations
  { topicId: 'ch15',    count: 3, easy: 0, medium: 1, hard: 2 }, // Puzzles & Magic Squares
  { topicId: 'ch16',    count: 2, easy: 0, medium: 1, hard: 1 }, // Sequences
  { topicId: 'ch17',    count: 2, easy: 0, medium: 1, hard: 1 }, // Time & Calendar
  { topicId: 'ch18',    count: 2, easy: 1, medium: 1, hard: 0 }, // Angles
  { topicId: 'ch19',    count: 2, easy: 0, medium: 1, hard: 1 }, // Triangles
  { topicId: 'ch20',    count: 3, easy: 1, medium: 1, hard: 1 }, // Quadrilaterals
  { topicId: 'ch21',    count: 1, easy: 0, medium: 1, hard: 0 }, // Circle
]; // Total: 40

const ALL_TOPIC_IDS = [
  'ch01-05', 'ch06', 'ch07-08', 'ch09-10', 'ch11', 'ch12',
  'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'dh',
];

export const TOPIC_NAMES: Record<string, string> = {
  'ch01-05': 'Number System & Place Value',
  'ch06':    'Factors & Multiples',
  'ch07-08': 'Fractions',
  'ch09-10': 'Operations & BODMAS',
  'ch11':    'Decimal Fractions',
  'ch12':    'Decimal Units of Measurement',
  'ch13':    'Algebraic Expressions',
  'ch14':    'Equations',
  'ch15':    'Puzzles & Magic Squares',
  'ch16':    'Sequence & Series',
  'ch17':    'Measurement of Time & Calendar',
  'ch18':    'Angles',
  'ch19':    'Triangles',
  'ch20':    'Quadrilaterals',
  'ch21':    'Circle',
  'dh':      'Data Handling & Graphs',
  // IPM past-paper pools (Grades 2–9)
  'grade2':  'Grade 2 — IPM Practice',
  'grade3':  'Grade 3 — IPM Practice',
  'grade4':  'Grade 4 — IPM Practice',
  'grade5':  'Grade 5 — IPM Practice',
  'grade6':  'Grade 6 — IPM Practice',
  'grade7':  'Grade 7 — IPM Practice',
  'grade8':  'Grade 8 — IPM Practice',
  'grade9':  'Grade 9 — IPM Practice',
};

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Safe JSON parse for stepByStep — never crash on bad data */
function safeParseSteps(json: string | null): unknown[] {
  try { return JSON.parse(json ?? '[]'); } catch { return []; }
}

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── Dynamic Blueprint for Grades 2-3, 5-9 ────────────────────────────────────
// Builds a blueprint from topicTree examWeight values.
// Uses subTopicKey for filtering within the gradeN pool.

function buildGradeBlueprint(grade: number): BlueprintSlot[] {
  const topics = getTopicsForGrade(grade).filter(t => !t.id.endsWith('_ipm'));
  const totalQuestions = TEST_CONFIG.ipm.totalQuestions; // 40

  // Calculate raw counts from examWeight, then adjust to hit totalQuestions
  const raw = topics.map(t => ({
    topicId: t.dbTopicId,
    subTopicKey: t.subTopicKey,
    rawCount: Math.max(2, Math.round(t.examWeight * totalQuestions)),
    examWeight: t.examWeight,
  }));

  // Adjust to hit exact total
  let sum = raw.reduce((s, r) => s + r.rawCount, 0);
  while (sum > totalQuestions) {
    // Shrink the largest slot (that's > 2)
    const largest = raw.filter(r => r.rawCount > 2).sort((a, b) => b.rawCount - a.rawCount)[0];
    if (!largest) break;
    largest.rawCount--;
    sum--;
  }
  while (sum < totalQuestions) {
    // Grow the slot with highest weight
    const best = raw.sort((a, b) => b.examWeight - a.examWeight)[0];
    best.rawCount++;
    sum++;
  }

  return raw.map(r => {
    const easy = Math.round(r.rawCount * 0.23);
    const hard = Math.round(r.rawCount * 0.30);
    const medium = r.rawCount - easy - hard;
    return {
      topicId: r.topicId,
      subTopicKey: r.subTopicKey,
      count: r.rawCount,
      easy,
      medium,
      hard,
    };
  });
}

// ── PYQ Paper Generator ───────────────────────────────────────────────────────

export async function generatePYQPaper(year: PYQYear) {
  const source = `previous_year_${year}`;
  const cfg = TEST_CONFIG.pyq;

  const questions = await prisma.question.findMany({
    where: { source, ...USABLE_QUESTION_FILTER },
    orderBy: { questionNumber: 'asc' },
    select: {
      id: true, topicId: true, difficulty: true, source: true,
      questionText: true, questionLatex: true,
      option1: true, option2: true, option3: true, option4: true,
      correctAnswer: true, hint1: true, hint2: true, hint3: true,
      stepByStep: true,
      misconceptionA: true, misconceptionB: true, misconceptionC: true, misconceptionD: true,
      subTopic: true, year: true, questionNumber: true,
    },
  });

  if (questions.length === 0) {
    throw new Error(`No PYQ questions found for year ${year}`);
  }

  // Shuffle so students don't memorize question order across attempts
  const shuffled = shuffle(questions);

  return {
    questions: shuffled.map((q) => ({
      ...q,
      stepByStep: safeParseSteps(q.stepByStep),
    })),
    timeLimitMs:    cfg.timeLimitMs,
    totalQuestions: shuffled.length,
  };
}

// ── IPM Blueprint Paper Generator ─────────────────────────────────────────────

const PYQ_SOURCES = ['previous_year_2016', 'previous_year_2017', 'previous_year_2018', 'previous_year_2019'];

const QUESTION_SELECT = {
  id: true, topicId: true, difficulty: true, source: true,
  questionText: true, questionLatex: true,
  option1: true, option2: true, option3: true, option4: true,
  correctAnswer: true, hint1: true, hint2: true, hint3: true,
  stepByStep: true,
  misconceptionA: true, misconceptionB: true, misconceptionC: true, misconceptionD: true,
  subTopic: true,
} as const;

async function generateIPMPaper(studentId: string, grade: number) {
  const cfg = TEST_CONFIG.ipm;

  // Avoid questions used in last 3 tests
  const recentTests = await prisma.mockTest.findMany({
    where: { studentId, status: 'completed' },
    orderBy: { completedAt: 'desc' },
    take: 3,
    select: { responses: { select: { questionId: true } } },
  });
  const recentIds = new Set(
    recentTests.flatMap((t) => t.responses.map((r) => r.questionId)),
  );

  // All grades now use blueprint-based topic distribution
  const blueprint = grade === 4 ? MOCK_BLUEPRINT : buildGradeBlueprint(grade);

  // Collect all DB topic IDs needed
  const topicIds = [...new Set(blueprint.map(b => b.topicId))];

  const allQuestions = await prisma.question.findMany({
    where: {
      topicId: { in: topicIds },
      source: { notIn: PYQ_SOURCES },
      ...USABLE_QUESTION_FILTER,
    },
    select: QUESTION_SELECT,
  });

  type QRow = typeof allQuestions[number];

  // Pool by topicId (or subTopicKey) + difficulty
  // For grades 2-3,5-9: further filter by subTopic ILIKE within the gradeN pool
  function buildPoolKey(slot: BlueprintSlot, difficulty: string): string {
    return slot.subTopicKey
      ? `${slot.topicId}__${slot.subTopicKey}__${difficulty}`
      : `${slot.topicId}__${difficulty}`;
  }

  const poolMap = new Map<string, QRow[]>();
  for (const slot of blueprint) {
    for (const diff of ['Easy', 'Medium', 'Hard']) {
      const key = buildPoolKey(slot, diff);
      const filtered = allQuestions.filter(q => {
        if (q.topicId !== slot.topicId) return false;
        if (q.difficulty !== diff) return false;
        if (slot.subTopicKey) {
          return (q.subTopic ?? '').toLowerCase().includes(slot.subTopicKey.toLowerCase());
        }
        return true;
      });
      poolMap.set(key, filtered);
    }
  }

  // Also build fallback pools per topicId+difficulty (ignoring subTopicKey)
  // Used when a subTopicKey-filtered pool runs dry
  const fallbackPool = new Map<string, QRow[]>();
  for (const q of allQuestions) {
    const key = `${q.topicId}__${q.difficulty}`;
    if (!fallbackPool.has(key)) fallbackPool.set(key, []);
    fallbackPool.get(key)!.push(q);
  }

  function pickOne(slot: BlueprintSlot, difficulty: string, used: Set<string>): QRow | null {
    const key = buildPoolKey(slot, difficulty);
    let pool = poolMap.get(key) ?? [];
    let candidates = pool.filter(q => !used.has(q.id) && !recentIds.has(q.id) && q.source === 'hand_crafted');
    if (!candidates.length) candidates = pool.filter(q => !used.has(q.id) && !recentIds.has(q.id));
    if (!candidates.length) candidates = pool.filter(q => !used.has(q.id));
    // Fallback: try the broader pool (ignoring subTopicKey)
    if (!candidates.length && slot.subTopicKey) {
      const fbKey = `${slot.topicId}__${difficulty}`;
      pool = fallbackPool.get(fbKey) ?? [];
      candidates = pool.filter(q => !used.has(q.id) && !recentIds.has(q.id));
      if (!candidates.length) candidates = pool.filter(q => !used.has(q.id));
    }
    if (!candidates.length) candidates = pool;
    if (!candidates.length) return null;
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  const easy:   QRow[] = [];
  const medium: QRow[] = [];
  const hard:   QRow[] = [];
  const used = new Set<string>();

  // Fill from blueprint slots
  for (const slot of blueprint) {
    const diffs: Array<[string, number]> = [
      ['Easy', slot.easy], ['Medium', slot.medium], ['Hard', slot.hard],
    ];
    for (const [diff, count] of diffs) {
      for (let i = 0; i < count; i++) {
        const q = pickOne(slot, diff, used);
        if (!q) continue;
        used.add(q.id);
        if (diff === 'Easy')   easy.push(q);
        else if (diff === 'Medium') medium.push(q);
        else hard.push(q);
      }
    }
  }

  const ordered = [...shuffle(easy), ...shuffle(medium), ...shuffle(hard)].slice(0, cfg.totalQuestions);

  if (ordered.length < cfg.totalQuestions) {
    console.warn(`[mockTest] IPM paper generated ${ordered.length}/${cfg.totalQuestions} questions — insufficient pool for grade ${grade}`);
  }

  return {
    questions: ordered.map((q) => ({
      ...q,
      stepByStep: safeParseSteps(q.stepByStep),
    })),
    timeLimitMs:    cfg.timeLimitMs,
    totalQuestions: ordered.length,
  };
}

// ── Topic distribution for quick/half/full ────────────────────────────────────

function buildTopicDistribution(
  type: 'quick' | 'half' | 'full',
  topicIds: string[],
  weakestIds: string[],
): Map<string, number> {
  const dist = new Map<string, number>();
  const n = topicIds.length;

  if (type === 'full') {
    topicIds.forEach((id) => dist.set(id, 3));
    const extras = weakestIds.filter((id) => topicIds.includes(id)).slice(0, 2);
    const toBoost = extras.length >= 2 ? extras : [...extras, ...topicIds.slice(0, 2 - extras.length)];
    toBoost.slice(0, 2).forEach((id) => dist.set(id, 4));
  } else if (type === 'half') {
    const base = Math.floor(30 / n);
    const remainder = 30 - base * n;
    topicIds.forEach((id) => dist.set(id, base));
    const boostIds = [...weakestIds.filter((id) => topicIds.includes(id)), ...topicIds]
      .filter((id, idx, arr) => arr.indexOf(id) === idx)
      .slice(0, remainder);
    boostIds.forEach((id) => dist.set(id, (dist.get(id) ?? 0) + 1));
  } else {
    // quick: 15 topics get 1 Q, drop strongest
    topicIds.forEach((id) => dist.set(id, 1));
  }

  return dist;
}

// ── Main Generator ────────────────────────────────────────────────────────────

export async function generateMockPaper(
  studentId: string,
  type: TestType,
  requestedTopicIds?: string[],
  year?: PYQYear,
  grade: number = 4,
) {
  // Delegate to specialised generators
  if (type === 'pyq' && year) return generatePYQPaper(year);
  if (type === 'ipm')        return generateIPMPaper(studentId, grade);

  const cfg = TEST_CONFIG[type as 'quick' | 'half' | 'full'];
  const topicIds = requestedTopicIds?.length ? requestedTopicIds : ALL_TOPIC_IDS;

  // Student progress for weak/strong ordering
  const progress = await prisma.progress.findMany({ where: { studentId } });
  const accuracyMap = new Map<string, number>();
  progress.forEach((p) => {
    accuracyMap.set(p.topicId, p.attempted > 0 ? p.correct / p.attempted : 0);
  });

  const weakestIds  = [...topicIds].sort((a, b) => (accuracyMap.get(a) ?? 0) - (accuracyMap.get(b) ?? 0));
  const strongestIds = [...topicIds].sort((a, b) => (accuracyMap.get(b) ?? 0) - (accuracyMap.get(a) ?? 0));

  let activeTopicIds = topicIds;
  if (type === 'quick' && topicIds.length > 15) {
    activeTopicIds = topicIds.filter((id) => id !== strongestIds[0]);
  }

  // Avoid recent test questions
  const recentTests = await prisma.mockTest.findMany({
    where: { studentId, status: 'completed' },
    orderBy: { completedAt: 'desc' },
    take: 3,
    select: { responses: { select: { questionId: true } } },
  });
  const recentIds = new Set(recentTests.flatMap((t) => t.responses.map((r) => r.questionId)));

  const allQuestions = await prisma.question.findMany({
    where: {
      topicId: { in: activeTopicIds },
      source: { notIn: PYQ_SOURCES },
      ...USABLE_QUESTION_FILTER,
    },
    select: QUESTION_SELECT,
  });

  type QRow = typeof allQuestions[number];

  const poolMap = new Map<string, QRow[]>();
  for (const q of allQuestions) {
    const key = `${q.topicId}__${q.difficulty}`;
    if (!poolMap.has(key)) poolMap.set(key, []);
    poolMap.get(key)!.push(q);
  }

  function pickQuestion(topicId: string, difficulty: string, used: Set<string>): QRow | null {
    const key  = `${topicId}__${difficulty}`;
    const pool = poolMap.get(key) ?? [];
    let candidates = pool.filter((q) => !used.has(q.id) && !recentIds.has(q.id) && q.source === 'hand_crafted');
    if (!candidates.length) candidates = pool.filter((q) => !used.has(q.id) && !recentIds.has(q.id));
    if (!candidates.length) candidates = pool.filter((q) => !used.has(q.id));
    if (!candidates.length) candidates = pool;
    if (!candidates.length) return null;
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  const topicDist = buildTopicDistribution(type as 'quick' | 'half' | 'full', activeTopicIds, weakestIds);
  const diffOrder = ['Easy', 'Medium', 'Hard'] as const;
  const diffTargets = { Easy: cfg.easy, Medium: cfg.medium, Hard: cfg.hard };
  const diffCounts  = { Easy: 0, Medium: 0, Hard: 0 };

  const easy:   QRow[] = [];
  const medium: QRow[] = [];
  const hard:   QRow[] = [];
  const usedIds = new Set<string>();

  for (const [topicId, qCount] of Array.from(topicDist.entries())) {
    for (let i = 0; i < qCount; i++) {
      let picked: QRow | null = null;
      for (const diff of diffOrder) {
        if (diffCounts[diff] < diffTargets[diff]) {
          picked = pickQuestion(topicId, diff, usedIds);
          if (picked) { diffCounts[diff]++; break; }
        }
      }
      if (!picked) {
        for (const diff of diffOrder) {
          picked = pickQuestion(topicId, diff, usedIds);
          if (picked) { diffCounts[diff]++; break; }
        }
      }
      if (picked) {
        usedIds.add(picked.id);
        if (picked.difficulty === 'Easy')   easy.push(picked);
        else if (picked.difficulty === 'Medium') medium.push(picked);
        else hard.push(picked);
      }
    }
  }

  const ordered = [...shuffle(easy), ...shuffle(medium), ...shuffle(hard)].slice(0, cfg.totalQuestions);

  if (ordered.length < cfg.totalQuestions) {
    console.warn(`[mockTest] ${type} paper generated ${ordered.length}/${cfg.totalQuestions} questions — insufficient pool`);
  }

  return {
    questions: ordered.map((q) => ({ ...q, stepByStep: safeParseSteps(q.stepByStep) })),
    timeLimitMs:    cfg.timeLimitMs,
    totalQuestions: ordered.length,
  };
}

// ── Helpers for Mega test ─────────────────────────────────────────────────────

async function getRecentlySeenIds(studentId: string, days: number): Promise<string[]> {
  const since = new Date(Date.now() - days * MS_PER_DAY);
  const attempts = await prisma.attempt.findMany({
    where: { studentId, createdAt: { gte: since } },
    select: { questionId: true },
  });
  return Array.from(new Set(attempts.map((a) => a.questionId)));
}

// ── Mega Test Generator ───────────────────────────────────────────────────────

export async function generateMegaTest(studentId: string, grade: number) {
  const topics = getTopicsForGrade(grade).map((t) => t.dbTopicId);
  const uniqueTopics = Array.from(new Set(topics));

  const recentIds = await getRecentlySeenIds(studentId, 30);

  const questions = await prisma.question.findMany({
    where: {
      topicId: { in: uniqueTopics },
      difficulty: 'Hard',
      id: { notIn: recentIds.length > 0 ? recentIds : ['__none__'] },
      ...USABLE_QUESTION_FILTER,
    },
    select: {
      id: true, topicId: true, difficulty: true, source: true,
      questionText: true, questionLatex: true,
      option1: true, option2: true, option3: true, option4: true,
      correctAnswer: true, hint1: true, hint2: true, hint3: true,
      stepByStep: true,
      misconceptionA: true, misconceptionB: true, misconceptionC: true, misconceptionD: true,
      subTopic: true,
    },
    take: 50,
    orderBy: { id: 'asc' },
  });

  const shuffled = shuffle(questions).slice(0, 15);

  return {
    questions: shuffled.map((q) => ({ ...q, stepByStep: safeParseSteps(q.stepByStep) })),
    timeLimitMs:    45 * 60 * 1000,
    totalQuestions: shuffled.length,
  };
}

export { ALL_TOPIC_IDS };

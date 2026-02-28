import { prisma } from '@/lib/db';
import type { TestType } from '@/types';

// ── Config ────────────────────────────────────────────────────────────────────

export const TEST_CONFIG = {
  quick: { totalQuestions: 15, timeLimitMs: 20 * 60 * 1000, easy: 4, medium: 6, hard: 5 },
  half:  { totalQuestions: 30, timeLimitMs: 40 * 60 * 1000, easy: 8, medium: 12, hard: 10 },
  full:  { totalQuestions: 50, timeLimitMs: 60 * 60 * 1000, easy: 15, medium: 20, hard: 15 },
} as const;

const ALL_TOPIC_IDS = [
  'ch01-05', 'ch06', 'ch07-08', 'ch09-10', 'ch11', 'ch12',
  'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'dh',
];

const TOPIC_NAMES: Record<string, string> = {
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
};

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── Topic distribution per test type ─────────────────────────────────────────

function buildTopicDistribution(
  type: TestType,
  topicIds: string[],
  weakestIds: string[],
): Map<string, number> {
  const dist = new Map<string, number>();
  const n = topicIds.length;

  if (type === 'full') {
    // 16 topics: 14 get 3 Qs, 2 get 4 Qs — weakest get the extra
    topicIds.forEach((id) => dist.set(id, 3));
    const extras = weakestIds.filter((id) => topicIds.includes(id)).slice(0, 2);
    // If not enough weak topics, just pick first 2
    const toBoost = extras.length >= 2 ? extras : topicIds.slice(0, 2 - extras.length);
    [...extras, ...toBoost].slice(0, 2).forEach((id) => dist.set(id, 4));
  } else if (type === 'half') {
    // 30 Qs across n topics: most get 2, some get 1
    const base = Math.floor(30 / n);
    const remainder = 30 - base * n;
    topicIds.forEach((id) => dist.set(id, base));
    // Give remainder to weakest topics first
    const boostIds = [...weakestIds.filter((id) => topicIds.includes(id)), ...topicIds]
      .filter((id, idx, arr) => arr.indexOf(id) === idx)
      .slice(0, remainder);
    boostIds.forEach((id) => dist.set(id, (dist.get(id) ?? 0) + 1));
  } else {
    // quick: 15 questions, 15 of 16 topics get 1 Q — drop student's strongest
    topicIds.forEach((id) => dist.set(id, 1));
  }

  return dist;
}

// ── Main generator ────────────────────────────────────────────────────────────

export async function generateMockPaper(
  studentId: string,
  type: TestType,
  requestedTopicIds?: string[],
) {
  const cfg = TEST_CONFIG[type];

  // Determine which topics to use
  const topicIds = requestedTopicIds?.length ? requestedTopicIds : ALL_TOPIC_IDS;

  // Get student progress to find weakest/strongest topics
  const progress = await prisma.progress.findMany({ where: { studentId } });
  const accuracyMap = new Map<string, number>();
  progress.forEach((p) => {
    accuracyMap.set(p.topicId, p.attempted > 0 ? p.correct / p.attempted : 0);
  });

  // Sort topics by accuracy asc (weakest first)
  const weakestIds = [...topicIds].sort(
    (a, b) => (accuracyMap.get(a) ?? 0) - (accuracyMap.get(b) ?? 0),
  );
  // Sort topics by accuracy desc (strongest first)
  const strongestIds = [...topicIds].sort(
    (a, b) => (accuracyMap.get(b) ?? 0) - (accuracyMap.get(a) ?? 0),
  );

  // For quick test: drop the strongest topic
  let activeTopicIds = topicIds;
  if (type === 'quick' && topicIds.length > 15) {
    const dropId = strongestIds[0];
    activeTopicIds = topicIds.filter((id) => id !== dropId);
  }

  // Get question IDs used in last 3 completed tests (avoid repeats)
  const recentTests = await prisma.mockTest.findMany({
    where: { studentId, status: 'completed' },
    orderBy: { completedAt: 'desc' },
    take: 3,
    select: { responses: { select: { questionId: true } } },
  });
  const recentIds = new Set(
    recentTests.flatMap((t) => t.responses.map((r) => r.questionId)),
  );

  // Fetch all questions for relevant topics
  const allQuestions = await prisma.question.findMany({
    where: { topicId: { in: activeTopicIds } },
    select: {
      id: true, topicId: true, difficulty: true, source: true,
      questionText: true, questionLatex: true,
      option1: true, option2: true, option3: true, option4: true,
      correctAnswer: true, hint1: true, hint2: true, hint3: true,
      stepByStep: true,
      misconceptionA: true, misconceptionB: true, misconceptionC: true, misconceptionD: true,
      subTopic: true,
    },
  });

  // Build pools per topic+difficulty
  type QRow = typeof allQuestions[number];
  const poolMap = new Map<string, QRow[]>(); // key: `${topicId}__${difficulty}`

  for (const q of allQuestions) {
    const key = `${q.topicId}__${q.difficulty}`;
    if (!poolMap.has(key)) poolMap.set(key, []);
    poolMap.get(key)!.push(q);
  }

  // Prefer hand_crafted, then avoid recently seen
  function pickQuestion(topicId: string, difficulty: string, used: Set<string>): QRow | null {
    const key = `${topicId}__${difficulty}`;
    const pool = poolMap.get(key) ?? [];
    // Prefer hand_crafted + not recently seen
    let candidates = pool.filter((q) => !used.has(q.id) && !recentIds.has(q.id) && q.source === 'hand_crafted');
    if (!candidates.length) candidates = pool.filter((q) => !used.has(q.id) && !recentIds.has(q.id));
    if (!candidates.length) candidates = pool.filter((q) => !used.has(q.id));
    if (!candidates.length) candidates = pool;
    if (!candidates.length) return null;
    const idx = Math.floor(Math.random() * candidates.length);
    return candidates[idx];
  }

  const topicDist = buildTopicDistribution(type, activeTopicIds, weakestIds);

  // Difficulty distribution helpers
  const diffOrder = ['Easy', 'Medium', 'Hard'] as const;
  const diffTargets = { Easy: cfg.easy, Medium: cfg.medium, Hard: cfg.hard };
  const diffCounts = { Easy: 0, Medium: 0, Hard: 0 };

  const easy:   QRow[] = [];
  const medium: QRow[] = [];
  const hard:   QRow[] = [];
  const usedIds = new Set<string>();

  // First pass: try to get exact difficulty distribution per topic
  for (const [topicId, qCount] of Array.from(topicDist.entries())) {
    const topicQuestions: QRow[] = [];

    // Calculate how many of each difficulty to pick for this topic
    // proportional to difficulty targets
    const topicDiffs: Array<[string, number]> = [];
    for (const diff of diffOrder) {
      const remaining = diffTargets[diff] - diffCounts[diff];
      if (remaining > 0) topicDiffs.push([diff, remaining]);
    }

    for (let i = 0; i < qCount; i++) {
      // Pick difficulty that still has capacity, cycling through
      let picked: QRow | null = null;
      for (const diff of diffOrder) {
        if (diffCounts[diff] < diffTargets[diff]) {
          picked = pickQuestion(topicId, diff, usedIds);
          if (picked) {
            diffCounts[diff]++;
            break;
          }
        }
      }
      // Fallback: any difficulty
      if (!picked) {
        for (const diff of diffOrder) {
          picked = pickQuestion(topicId, diff, usedIds);
          if (picked) { diffCounts[diff]++; break; }
        }
      }
      if (picked) {
        usedIds.add(picked.id);
        topicQuestions.push(picked);
      }
    }

    for (const q of topicQuestions) {
      if (q.difficulty === 'Easy')   easy.push(q);
      else if (q.difficulty === 'Medium') medium.push(q);
      else hard.push(q);
    }
  }

  // Final ordering: Easy → Medium → Hard, shuffle within each band
  const ordered = [...shuffle(easy), ...shuffle(medium), ...shuffle(hard)].slice(0, cfg.totalQuestions);

  return {
    questions: ordered.map((q) => ({
      ...q,
      stepByStep: JSON.parse(q.stepByStep ?? '[]'),
    })),
    timeLimitMs: cfg.timeLimitMs,
    totalQuestions: cfg.totalQuestions,
  };
}

export { TOPIC_NAMES, ALL_TOPIC_IDS };

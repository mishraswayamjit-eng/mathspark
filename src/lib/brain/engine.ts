import { MS_PER_DAY } from '@/lib/timeConstants';
import { prisma } from '@/lib/db';
import { TOPIC_TREE, getTopicsForGrade, isExtraTopicId } from '@/data/topicTree';
import { parseStringArray } from '@/lib/jsonFields';
import { computeStreak, matchesSubTopicKey } from '@/lib/sharedUtils';
import { practiceUrlForNode, practiceUrlForNodeId } from './practiceUrl';
import {
  buildNudges,
  findAccuracyDropNodeIds,
  speedScore,
  streakBeforeToday,
} from './rules';

// ── Shared Types ──────────────────────────────────────────────────────────────

export type TopicStatus = 'mastered' | 'strong' | 'developing' | 'weak' | 'not_started';

export interface TopicMasteryEntry {
  topicId: string;
  topicName: string;
  emoji: string;
  mastery: number;       // 0–1 composite
  accuracy: number;      // correct / attempted
  speed: number;         // 1 - (avgMs / 90000), clamped 0–1
  coverage: number;      // uniqueQsSeen / min(totalQs, 10), clamped 0–1
  recency: number;       // 1 = practiced today; decays to 0 at 30 days
  attemptsCount: number;
  status: TopicStatus;
}

export interface ExamReadinessResult {
  score: number;
  predictedMin: number;
  predictedMax: number;
  daysUntilExam: number | null;
  trend: 'improving' | 'stable' | 'declining';
  components: {
    avgMastery: number;
    syllabusCoverage: number;
    mockPerformance: number;
    consistency: number;
  };
}

export interface TopicPriority {
  topicId: string;
  topicName: string;
  emoji: string;
  priority: number;
  reason: string;
  dbTopicId: string;
  /**
   * The link that practises exactly this node (with `?subTopic=` for keyed
   * grades). Absent on rows stored before it was added: fall back to
   * `practiceUrlForNodeId(topicId)`.
   */
  practiceUrl?: string;
}

export interface DailyPlanItem {
  id: string;
  action: string;
  type: 'practice' | 'flashcards' | 'mock' | 'explore';
  targetUrl: string;
  reason: string;
  estimatedMins: number;
  done: boolean;
  /** The topic-tree node this item is about, when it is about one. Absent on older stored rows. */
  topicId?: string;
}

/** What a nudge is about. The order they win in is `NUDGE_PRIORITY` in `./rules`. */
export type NudgeKind =
  | 'streak_milestone'
  | 'streak_keep'
  | 'accuracy_drop'
  | 'exam_mock'
  | 'idle_topic'
  | 'explore_topic'
  | 'weekend_mock';

export interface Nudge {
  id: string;
  message: string;
  sparkyEmotion: 'happy' | 'thinking' | 'encouraging' | 'celebrating';
  actionUrl: string;
  actionLabel: string;
  priority: number;
  /** Absent on rows stored before kinds existed; those are never shown. */
  kind?: NudgeKind;
  /** ISO time after which the nudge is out of date and is not shown. */
  expiresAt?: string;
}

// ── StudentRecord: passed from recompute to avoid redundant DB fetches ────────

interface StudentRecord {
  grade: number;
  examDate: Date | null;
  focusTopics: string;
  /** Not read: this column is never updated. The streak comes from `computeStreak`. */
  currentStreak?: number;
}

/**
 * How many of the child's latest answers the engine reads. 200 was too few
 * for a keyed grade: Grade 5 has 21 sub-topics, so about ten answers each
 * filled the window and a topic practised a fortnight ago fell out of it and
 * showed as "not started" again. Recency already fades to 0 over 30 days, so
 * 1,000 slim rows comfortably cover a busy month.
 */
const MASTERY_ATTEMPT_WINDOW = 1000;

// ── Helpers ───────────────────────────────────────────────────────────────────

function clamp(v: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, v));
}

function mean(arr: number[]): number {
  if (!arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

// ── a) computeTopicMastery ────────────────────────────────────────────────────

export async function computeTopicMastery(
  studentId: string,
  student?: StudentRecord,
): Promise<TopicMasteryEntry[]> {
  // If student record not provided, fetch it (for standalone calls)
  const resolvedStudent = student ?? await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, focusTopics: true },
  });
  if (!resolvedStudent) return [];

  const grade = resolvedStudent.grade ?? 4;
  const topics = getTopicsForGrade(grade);

  // Only this grade's questions count towards its nodes, so only those are read.
  const gradeDbTopicIds: string[] = [];
  for (const node of topics) {
    if (gradeDbTopicIds.indexOf(node.dbTopicId) === -1) gradeDbTopicIds.push(node.dbTopicId);
  }

  const allAttempts = await prisma.attempt.findMany({
    where: { studentId, question: { topicId: { in: gradeDbTopicIds } } },
    select: {
      questionId: true,
      isCorrect: true,
      timeTakenMs: true,
      createdAt: true,
      question: { select: { topicId: true, subTopic: true } },
    },
    orderBy: { createdAt: 'desc' },
    take: MASTERY_ATTEMPT_WINDOW,
  });

  const entries: TopicMasteryEntry[] = [];

  for (const node of topics) {
    // Filter attempts for this topic node
    const topicAttempts = allAttempts.filter((a) => {
      if (a.question.topicId !== node.dbTopicId) return false;
      if (node.subTopicKey) {
        return matchesSubTopicKey(a.question.subTopic, node.subTopicKey);
      }
      return true;
    });

    const count = topicAttempts.length;
    const correctCount = topicAttempts.filter((a) => a.isCorrect).length;
    const accuracy = count > 0 ? correctCount / count : 0;

    const uniqueQs = new Set(topicAttempts.map((a) => a.questionId)).size;
    const coverage = clamp(uniqueQs / 10, 0, 1);

    // Real time per question once the practice page sends it. Old rows hold 0,
    // which means "not recorded": they are left out, never read as "instant".
    const speed = speedScore(topicAttempts.map((a) => a.timeTakenMs));

    let recency = 0;
    if (count > 0 && topicAttempts[0]) {
      const daysSinceLast = (Date.now() - new Date(topicAttempts[0].createdAt).getTime()) / MS_PER_DAY;
      recency = Math.max(0, 1 - daysSinceLast / 30);
    }

    const mastery = accuracy * 0.4 + coverage * 0.3 + speed * 0.2 + recency * 0.1;

    let status: TopicStatus;
    if (mastery >= 0.8) status = 'mastered';
    else if (mastery >= 0.6) status = 'strong';
    else if (mastery >= 0.35) status = 'developing';
    else if (count > 0) status = 'weak';
    else status = 'not_started';

    entries.push({
      topicId:      node.id,
      topicName:    node.name,
      emoji:        node.emoji,
      mastery,
      accuracy,
      speed,
      coverage,
      recency,
      attemptsCount: count,
      status,
    });
  }

  return entries.sort((a, b) => a.mastery - b.mastery);
}

// ── b) computeExamReadiness ───────────────────────────────────────────────────

export async function computeExamReadiness(
  studentId: string,
  student?: StudentRecord,
  masteries?: TopicMasteryEntry[],
): Promise<ExamReadinessResult> {
  // If student record not provided, fetch it (for standalone calls)
  const resolvedStudent = student ?? await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, examDate: true },
  });

  // Extra-practice topics are not on the real paper: they neither raise nor
  // lower exam readiness (average mastery, share of the syllabus covered).
  const m = examTopicEntries(masteries ?? (await computeTopicMastery(studentId)));
  if (!m.length) {
    return {
      score: 0, predictedMin: 0, predictedMax: 4, daysUntilExam: null,
      trend: 'stable',
      components: { avgMastery: 0, syllabusCoverage: 0, mockPerformance: 0, consistency: 0 },
    };
  }

  const avgMastery = mean(m.map((t) => t.mastery));
  const syllabusCoverage = m.filter((t) => t.attemptsCount >= 5).length / m.length;

  // Collapse 3 separate attempt queries into one parallel pair
  const twoWeeksAgo = new Date(Date.now() - 14 * MS_PER_DAY);
  const oneWeekAgo  = new Date(Date.now() - 7  * MS_PER_DAY);

  const [recentMocks, twoWeekAttempts] = await Promise.all([
    prisma.mockTest.findMany({
      where: { studentId, status: 'completed' },
      orderBy: { completedAt: 'desc' },
      take: 5,
      select: { score: true, totalQuestions: true },
    }),
    prisma.attempt.findMany({
      where: { studentId, createdAt: { gte: twoWeeksAgo } },
      select: { isCorrect: true, createdAt: true },
    }),
  ]);

  // Partition in JS: avoids two extra round-trips
  const recentWeekAttempts = twoWeekAttempts.filter(
    (a) => new Date(a.createdAt) >= oneWeekAgo,
  );
  const priorWeekAttempts = twoWeekAttempts.filter(
    (a) => new Date(a.createdAt) < oneWeekAgo,
  );
  const activeDays = new Set(
    twoWeekAttempts.map((a) => new Date(a.createdAt).toDateString()),
  ).size;

  const mockPerformance = recentMocks.length > 0
    ? mean(recentMocks.map((t) => (t.score ?? 0) / Math.max(t.totalQuestions, 1)))
    : 0;

  const consistency = clamp(activeDays / 14, 0, 1);

  const rawScore = avgMastery * 0.35 + syllabusCoverage * 0.25 + mockPerformance * 0.25 + consistency * 0.15;
  const score = Math.round(rawScore * 100);

  const predicted = rawScore * 40;
  const predictedMin = Math.max(0, Math.round(predicted - 4));
  const predictedMax = Math.min(40, Math.round(predicted + 4));

  // Trend: compare recent week vs prior week accuracy (partitioned from the single query above)
  const recentAcc = recentWeekAttempts.length > 0
    ? recentWeekAttempts.filter((a) => a.isCorrect).length / recentWeekAttempts.length
    : null;
  const priorAcc = priorWeekAttempts.length > 0
    ? priorWeekAttempts.filter((a) => a.isCorrect).length / priorWeekAttempts.length
    : null;

  let trend: 'improving' | 'stable' | 'declining' = 'stable';
  if (recentAcc !== null && priorAcc !== null) {
    const diff = recentAcc - priorAcc;
    if (diff > 0.05) trend = 'improving';
    else if (diff < -0.05) trend = 'declining';
  }

  const examDate = resolvedStudent?.examDate;
  const daysUntilExam = examDate
    ? Math.ceil((new Date(examDate).getTime() - Date.now()) / MS_PER_DAY)
    : null;

  return {
    score, predictedMin, predictedMax, daysUntilExam, trend,
    components: { avgMastery, syllabusCoverage, mockPerformance, consistency },
  };
}

// ── c) computeTopicPriorities ─────────────────────────────────────────────────

export async function computeTopicPriorities(
  studentId: string,
  student?: StudentRecord,
  masteries?: TopicMasteryEntry[],
): Promise<TopicPriority[]> {
  // If student record not provided, fetch it (for standalone calls)
  const resolvedStudent = student ?? await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, focusTopics: true },
  });

  const m = masteries ?? (await computeTopicMastery(studentId));
  const focusTopics = parseStringArray(resolvedStudent?.focusTopics);

  const gradeTopics = getTopicsForGrade(resolvedStudent?.grade ?? 4);
  const maxExamWeight = Math.max(...gradeTopics.map((t) => t.examWeight), 1);

  const priorities: TopicPriority[] = m.map((entry) => {
    const node = TOPIC_TREE.find((t) => t.id === entry.topicId);
    const examWeightScore = node ? node.examWeight / maxExamWeight : 0;
    const gapScore        = 1 - entry.mastery;
    const recencyDecay    = 1 - entry.recency;
    const isFocus         = focusTopics.includes(entry.topicId) ? 0.2 : 0;

    const priority =
      examWeightScore * 0.30 +
      gapScore        * 0.35 +
      recencyDecay    * 0.15 +
      isFocus         * 0.20;

    // Pick the most relevant reason
    let reason = 'Great topic to practice';
    if (entry.attemptsCount === 0) {
      // Nothing answered yet, so nothing is known about accuracy.
      reason = 'New for you — a good one to start';
    } else if (entry.mastery < 0.2) {
      reason = 'A little practice will help here';
    } else if (entry.recency < 0.3) {
      const days = Math.round((1 - entry.recency) * 30);
      reason = `Last practised ${days} days ago`;
    } else if (entry.coverage < 0.3) {
      const pct = Math.round(entry.coverage * 100);
      reason = `Only ${pct}% of question types explored`;
    } else if (node && node.examWeight > 0.12) {
      reason = 'High exam frequency';
    } else if (isFocus > 0) {
      reason = 'You marked this as a focus area';
    }

    return {
      topicId:   entry.topicId,
      topicName: entry.topicName,
      emoji:     entry.emoji,
      priority,
      reason,
      dbTopicId: node?.dbTopicId ?? entry.topicId,
      practiceUrl: node ? practiceUrlForNode(node) : '/chapters',
    };
  });

  return orderPriorities(priorities);
}

/** The entries of exam topics only: extra-practice topics (topicTree `extra`) are left out. */
export function examTopicEntries<T extends { topicId: string }>(entries: T[]): T[] {
  return entries.filter((e) => !isExtraTopicId(e.topicId));
}

/**
 * Highest priority first, with every exam topic ahead of every extra-practice
 * topic: an extra topic is offered only once no exam topic is left to offer.
 * (With examWeight 0 alone, an untouched extra topic would still outrank an
 * exam topic the child has started, because the gap counts for more.)
 */
export function orderPriorities<T extends { topicId: string; priority: number }>(priorities: T[]): T[] {
  return priorities.slice().sort((a, b) => {
    const aExtra = isExtraTopicId(a.topicId);
    const bExtra = isExtraTopicId(b.topicId);
    if (aExtra !== bExtra) return aExtra ? 1 : -1;
    return b.priority - a.priority;
  });
}

// ── d) generateDailyPlan ──────────────────────────────────────────────────────

export async function generateDailyPlan(
  studentId: string,
  student?: StudentRecord,
  masteries?: TopicMasteryEntry[],
): Promise<DailyPlanItem[]> {
  // Pass student through to computeTopicPriorities to avoid a redundant fetch
  const priorities = await computeTopicPriorities(studentId, student, masteries);
  const items: DailyPlanItem[] = [];
  // Topic-tree nodes already in the plan, so "Explore" never repeats one.
  const plannedNodeIds: string[] = [];

  if (priorities[0]) {
    items.push({
      id: 'plan_0',
      action: `Practice ${priorities[0].topicName}`,
      type: 'practice',
      targetUrl: practiceUrlForNodeId(priorities[0].topicId) ?? '/chapters',
      reason: priorities[0].reason,
      estimatedMins: 12,
      done: false,
      topicId: priorities[0].topicId,
    });
    plannedNodeIds.push(priorities[0].topicId);
  }

  if (priorities[1]) {
    items.push({
      id: 'plan_1',
      action: `Practice ${priorities[1].topicName}`,
      type: 'practice',
      targetUrl: practiceUrlForNodeId(priorities[1].topicId) ?? '/chapters',
      reason: priorities[1].reason,
      estimatedMins: 8,
      done: false,
      topicId: priorities[1].topicId,
    });
    plannedNodeIds.push(priorities[1].topicId);
  }

  // Mock test check
  const latestMock = await prisma.mockTest.findFirst({
    where: { studentId },
    orderBy: { startedAt: 'desc' },
    select: { startedAt: true },
  });
  const daysSinceMock = latestMock
    ? (Date.now() - new Date(latestMock.startedAt).getTime()) / MS_PER_DAY
    : Infinity;

  if (daysSinceMock > 7) {
    items.push({
      id: 'plan_mock',
      action: 'Quick Mock Test',
      type: 'mock',
      targetUrl: '/test',
      reason: daysSinceMock === Infinity ? 'Never taken a mock test' : 'No mock test in 7+ days',
      estimatedMins: 20,
      done: false,
    });
  }

  // Coverage gap
  const m = masteries ?? await computeTopicMastery(studentId);
  // Deduped on the node id. (It used to test whether a plan link contained the
  // database topic id, which is the same "grade5" for every Grade 5 node, so
  // this item could never appear for a keyed grade.)
  // An exam topic if one has a gap; an extra-practice topic only when none does.
  const gaps = m.filter((t) => t.coverage < 0.2 && plannedNodeIds.indexOf(t.topicId) === -1);
  const examGaps = examTopicEntries(gaps);
  const coverageGap = examGaps.length > 0 ? examGaps[0] : gaps[0];
  if (coverageGap) {
    const exploreUrl = practiceUrlForNodeId(coverageGap.topicId);
    if (exploreUrl) {
      items.push({
        id: 'plan_explore',
        action: `Explore ${coverageGap.topicName}`,
        type: 'explore',
        targetUrl: exploreUrl,
        reason: 'Lots of new questions to try here',
        estimatedMins: 8,
        done: false,
        topicId: coverageGap.topicId,
      });
    }
  }

  return items.slice(0, 5);
}

// ── e) generateNudges ─────────────────────────────────────────────────────────

export async function generateNudges(
  studentId: string,
  student?: StudentRecord,
  masteries?: TopicMasteryEntry[],
): Promise<Nudge[]> {
  // If student record not provided, fetch it (for standalone calls)
  const resolvedStudent = student ?? await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, examDate: true, focusTopics: true },
  });

  const m = masteries ?? (await computeTopicMastery(studentId));
  const priorities = await computeTopicPriorities(studentId, resolvedStudent ?? undefined, m);
  const now = new Date();

  const nodes = getTopicsForGrade(resolvedStudent?.grade ?? 4);
  const dbTopicIds: string[] = [];
  for (const node of nodes) {
    if (dbTopicIds.indexOf(node.dbTopicId) === -1) dbTopicIds.push(node.dbTopicId);
  }

  const [streakAttempts, twoWeekAttempts, latestMock] = await Promise.all([
    // Days practised, for the streak. `Student.currentStreak` is never
    // updated, so the streak is worked out from the attempts themselves, the
    // way the rest of the app does it (`computeStreak`).
    prisma.attempt.findMany({
      where: {
        studentId,
        createdAt: { gte: new Date(now.getTime() - STREAK_LOOKBACK_DAYS * MS_PER_DAY) },
      },
      select: { createdAt: true },
      orderBy: { createdAt: 'desc' },
      take: STREAK_ATTEMPT_WINDOW,
    }),
    // The last fortnight in this grade's topics, WITH the sub-topic, so a
    // drop in accuracy is found per node and not for the whole grade.
    prisma.attempt.findMany({
      where: {
        studentId,
        createdAt: { gte: new Date(now.getTime() - 14 * MS_PER_DAY) },
        question: { topicId: { in: dbTopicIds } },
      },
      select: {
        isCorrect: true,
        createdAt: true,
        question: { select: { topicId: true, subTopic: true } },
      },
    }),
    prisma.mockTest.findFirst({
      where: { studentId },
      orderBy: { startedAt: 'desc' },
      select: { startedAt: true },
    }),
  ]);

  const examDate = resolvedStudent?.examDate;
  const daysUntilExam = examDate
    ? Math.ceil((new Date(examDate).getTime() - now.getTime()) / MS_PER_DAY)
    : null;
  const daysSinceMock = latestMock
    ? (now.getTime() - new Date(latestMock.startedAt).getTime()) / MS_PER_DAY
    : null;

  // All wording, conditions and the order nudges win in live in ./rules (pure, unit-tested).
  return buildNudges({
    now,
    masteries: m,
    topPriorityNodeId: priorities[0]?.topicId ?? null,
    streakToday: computeStreak(streakAttempts),
    streakBeforeToday: streakBeforeToday(streakAttempts, now),
    accuracyDropNodeIds: findAccuracyDropNodeIds(nodes, twoWeekAttempts, now),
    daysUntilExam,
    daysSinceMock,
  });
}

/** How far back, and how many answers, the streak looks. */
const STREAK_LOOKBACK_DAYS = 120;
const STREAK_ATTEMPT_WINDOW = 3000;

import { prisma } from '@/lib/db';
import { TOPIC_TREE, getTopicsForGrade } from '@/data/topicTree';

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
}

export interface DailyPlanItem {
  id: string;
  action: string;
  type: 'practice' | 'flashcards' | 'mock' | 'explore';
  targetUrl: string;
  reason: string;
  estimatedMins: number;
  done: boolean;
}

export interface Nudge {
  id: string;
  message: string;
  sparkyEmotion: 'happy' | 'thinking' | 'encouraging' | 'celebrating';
  actionUrl: string;
  actionLabel: string;
  priority: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function clamp(v: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, v));
}

function mean(arr: number[]): number {
  if (!arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

// ── a) computeTopicMastery ────────────────────────────────────────────────────

export async function computeTopicMastery(studentId: string): Promise<TopicMasteryEntry[]> {
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, focusTopics: true },
  });
  if (!student) return [];

  const grade = student.grade ?? 4;
  const topics = getTopicsForGrade(grade);

  const allAttempts = await prisma.attempt.findMany({
    where: { studentId },
    select: {
      id: true,
      questionId: true,
      isCorrect: true,
      timeTakenMs: true,
      createdAt: true,
      question: { select: { topicId: true, subTopic: true } },
    },
    orderBy: { createdAt: 'desc' },
    take: 200,
  });

  const entries: TopicMasteryEntry[] = [];

  for (const node of topics) {
    // Filter attempts for this topic node
    const topicAttempts = allAttempts.filter((a) => {
      if (a.question.topicId !== node.dbTopicId) return false;
      if (node.subTopicKey) {
        return a.question.subTopic.toLowerCase().includes(node.subTopicKey.toLowerCase());
      }
      return true;
    });

    const count = topicAttempts.length;
    const correctCount = topicAttempts.filter((a) => a.isCorrect).length;
    const accuracy = count > 0 ? correctCount / count : 0;

    const uniqueQs = new Set(topicAttempts.map((a) => a.questionId)).size;
    const coverage = clamp(uniqueQs / 10, 0, 1);

    const avgMs = mean(topicAttempts.map((a) => a.timeTakenMs).filter((ms) => ms > 0));
    const speed = avgMs > 0 ? clamp(1 - avgMs / 90000, 0, 1) : 0.5;

    let recency = 0;
    if (count > 0 && topicAttempts[0]) {
      const daysSinceLast = (Date.now() - new Date(topicAttempts[0].createdAt).getTime()) / 86400000;
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
  masteries?: TopicMasteryEntry[],
): Promise<ExamReadinessResult> {
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, examDate: true },
  });

  const m = masteries ?? (await computeTopicMastery(studentId));
  if (!m.length) {
    return {
      score: 0, predictedMin: 0, predictedMax: 4, daysUntilExam: null,
      trend: 'stable',
      components: { avgMastery: 0, syllabusCoverage: 0, mockPerformance: 0, consistency: 0 },
    };
  }

  const avgMastery = mean(m.map((t) => t.mastery));
  const syllabusCoverage = m.filter((t) => t.attemptsCount >= 5).length / m.length;

  const recentMocks = await prisma.mockTest.findMany({
    where: { studentId, status: 'completed' },
    orderBy: { completedAt: 'desc' },
    take: 5,
    select: { score: true, totalQuestions: true },
  });
  const mockPerformance = recentMocks.length > 0
    ? mean(recentMocks.map((t) => (t.score ?? 0) / Math.max(t.totalQuestions, 1)))
    : 0;

  const twoWeeksAgo = new Date(Date.now() - 14 * 86400000);
  const recentAttempts = await prisma.attempt.findMany({
    where: { studentId, createdAt: { gte: twoWeeksAgo } },
    select: { createdAt: true },
  });
  const activeDays = new Set(recentAttempts.map((a) => new Date(a.createdAt).toDateString())).size;
  const consistency = clamp(activeDays / 14, 0, 1);

  const rawScore = avgMastery * 0.35 + syllabusCoverage * 0.25 + mockPerformance * 0.25 + consistency * 0.15;
  const score = Math.round(rawScore * 100);

  const predicted = rawScore * 40;
  const predictedMin = Math.max(0, Math.round(predicted - 4));
  const predictedMax = Math.min(40, Math.round(predicted + 4));

  // Trend: compare recent week vs prior week mastery
  const oneWeekAgo  = new Date(Date.now() - 7  * 86400000);
  const twoWeeksAgoDate = new Date(Date.now() - 14 * 86400000);

  const recentWeekAttempts = await prisma.attempt.findMany({
    where: { studentId, createdAt: { gte: oneWeekAgo } },
    select: { isCorrect: true },
  });
  const priorWeekAttempts = await prisma.attempt.findMany({
    where: { studentId, createdAt: { gte: twoWeeksAgoDate, lt: oneWeekAgo } },
    select: { isCorrect: true },
  });

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

  const examDate = student?.examDate;
  const daysUntilExam = examDate
    ? Math.ceil((new Date(examDate).getTime() - Date.now()) / 86400000)
    : null;

  return {
    score, predictedMin, predictedMax, daysUntilExam, trend,
    components: { avgMastery, syllabusCoverage, mockPerformance, consistency },
  };
}

// ── c) computeTopicPriorities ─────────────────────────────────────────────────

export async function computeTopicPriorities(
  studentId: string,
  masteries?: TopicMasteryEntry[],
): Promise<TopicPriority[]> {
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, focusTopics: true },
  });

  const m = masteries ?? (await computeTopicMastery(studentId));
  const focusTopics: string[] = JSON.parse(student?.focusTopics ?? '[]');

  const gradeTopics = getTopicsForGrade(student?.grade ?? 4);
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
    if (entry.mastery < 0.2) {
      reason = 'Very low accuracy — needs attention';
    } else if (entry.recency < 0.3 && entry.attemptsCount > 0) {
      const days = Math.round((1 - entry.recency) * 30);
      reason = `Not practiced in ${days} days`;
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
    };
  });

  return priorities.sort((a, b) => b.priority - a.priority);
}

// ── d) generateDailyPlan ──────────────────────────────────────────────────────

export async function generateDailyPlan(
  studentId: string,
  masteries?: TopicMasteryEntry[],
): Promise<DailyPlanItem[]> {
  const priorities = await computeTopicPriorities(studentId, masteries);
  const items: DailyPlanItem[] = [];

  if (priorities[0]) {
    items.push({
      id: 'plan_0',
      action: `Practice ${priorities[0].topicName}`,
      type: 'practice',
      targetUrl: `/practice/${priorities[0].dbTopicId}`,
      reason: priorities[0].reason,
      estimatedMins: 12,
      done: false,
    });
  }

  if (priorities[1]) {
    items.push({
      id: 'plan_1',
      action: `Practice ${priorities[1].topicName}`,
      type: 'practice',
      targetUrl: `/practice/${priorities[1].dbTopicId}`,
      reason: priorities[1].reason,
      estimatedMins: 8,
      done: false,
    });
  }

  // Mock test check
  const latestMock = await prisma.mockTest.findFirst({
    where: { studentId },
    orderBy: { startedAt: 'desc' },
    select: { startedAt: true },
  });
  const daysSinceMock = latestMock
    ? (Date.now() - new Date(latestMock.startedAt).getTime()) / 86400000
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
  const coverageGap = m.find((t) =>
    t.coverage < 0.2 && !items.some((i) => i.targetUrl.includes(
      TOPIC_TREE.find((n) => n.id === t.topicId)?.dbTopicId ?? '',
    )),
  );
  if (coverageGap) {
    const node = TOPIC_TREE.find((n) => n.id === coverageGap.topicId);
    if (node) {
      items.push({
        id: 'plan_explore',
        action: `Explore ${coverageGap.topicName}`,
        type: 'explore',
        targetUrl: `/practice/${node.dbTopicId}`,
        reason: 'Very few question types tried',
        estimatedMins: 8,
        done: false,
      });
    }
  }

  return items.slice(0, 5);
}

// ── e) generateNudges ─────────────────────────────────────────────────────────

export async function generateNudges(
  studentId: string,
  masteries?: TopicMasteryEntry[],
): Promise<Nudge[]> {
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true, examDate: true, currentStreak: true },
  });

  const m = masteries ?? (await computeTopicMastery(studentId));
  const priorities = await computeTopicPriorities(studentId, m);
  const topPriorityDbTopicId = priorities[0]?.dbTopicId ?? 'ch11';
  const streak = student?.currentStreak ?? 0;

  const nudges: Nudge[] = [];

  // Rule 1: Evening + streak at risk
  const nowIST = new Date(Date.now() + 5.5 * 3600000);
  const hourIST = nowIST.getUTCHours();
  const todayStart = new Date(); todayStart.setHours(0, 0, 0, 0);
  const todayAttempts = await prisma.attempt.count({
    where: { studentId, createdAt: { gte: todayStart } },
  });
  if (hourIST >= 18 && todayAttempts === 0 && streak > 0) {
    nudges.push({
      id: 'nudge_streak',
      message: `Don't break your 🔥${streak}-day streak! Practice now`,
      sparkyEmotion: 'encouraging',
      actionUrl: `/practice/${topPriorityDbTopicId}`,
      actionLabel: 'Practice now',
      priority: 10,
    });
  }

  // Rule 2: Topic with accuracy drop
  if (m.length > 0) {
    const recentWeekAgo = new Date(Date.now() - 7 * 86400000);
    const priorWeekAgo  = new Date(Date.now() - 14 * 86400000);
    for (const entry of m) {
      if (nudges.length >= 3) break;
      const node = TOPIC_TREE.find((t) => t.id === entry.topicId);
      if (!node) continue;

      const recentAttempts = await prisma.attempt.findMany({
        where: {
          studentId,
          createdAt: { gte: recentWeekAgo },
          question: { topicId: node.dbTopicId },
        },
        select: { isCorrect: true },
      });
      const priorAttempts = await prisma.attempt.findMany({
        where: {
          studentId,
          createdAt: { gte: priorWeekAgo, lt: recentWeekAgo },
          question: { topicId: node.dbTopicId },
        },
        select: { isCorrect: true },
      });

      if (recentAttempts.length >= 5 && priorAttempts.length >= 5) {
        const recentAcc = recentAttempts.filter((a) => a.isCorrect).length / recentAttempts.length;
        const priorAcc  = priorAttempts.filter((a) => a.isCorrect).length / priorAttempts.length;
        if (priorAcc - recentAcc > 0.15) {
          nudges.push({
            id: `nudge_drop_${entry.topicId}`,
            message: `${entry.topicName} needs love — accuracy dropped this week`,
            sparkyEmotion: 'thinking',
            actionUrl: `/practice/${node.dbTopicId}`,
            actionLabel: 'Practice now',
            priority: 8,
          });
          break;
        }
      }
    }
  }

  // Rule 3: Long-idle topic
  if (nudges.length < 3) {
    const idleTopic = m.find((t) => {
      const days = Math.round((1 - t.recency) * 30);
      return t.attemptsCount > 0 && days > 14;
    });
    if (idleTopic) {
      const days = Math.round((1 - idleTopic.recency) * 30);
      const node = TOPIC_TREE.find((t) => t.id === idleTopic.topicId);
      nudges.push({
        id: `nudge_idle_${idleTopic.topicId}`,
        message: `You haven't practiced ${idleTopic.topicName} in ${days} days`,
        sparkyEmotion: 'thinking',
        actionUrl: node ? `/practice/${node.dbTopicId}` : '/chapters',
        actionLabel: 'Practice now',
        priority: 6,
      });
    }
  }

  // Rule 4: Exam countdown
  if (nudges.length < 3 && student?.examDate) {
    const readiness = await computeExamReadiness(studentId, m);
    if (readiness.daysUntilExam !== null && readiness.daysUntilExam < 30 && readiness.score < 60) {
      nudges.push({
        id: 'nudge_exam',
        message: `Exam in ${readiness.daysUntilExam} days — readiness ${readiness.score}% — let's focus!`,
        sparkyEmotion: 'encouraging',
        actionUrl: '/home',
        actionLabel: 'View plan',
        priority: 9,
      });
    }
  }

  // Rule 5: Unexplored topic
  if (nudges.length < 3) {
    const unexplored = m.find((t) => t.coverage < 0.3 && t.attemptsCount > 0);
    if (unexplored) {
      const node = TOPIC_TREE.find((t) => t.id === unexplored.topicId);
      nudges.push({
        id: `nudge_explore_${unexplored.topicId}`,
        message: `You've barely scratched ${unexplored.topicName} — let's explore!`,
        sparkyEmotion: 'happy',
        actionUrl: node ? `/practice/${node.dbTopicId}` : '/chapters',
        actionLabel: 'Explore',
        priority: 4,
      });
    }
  }

  // Rule 6: Weekend
  if (nudges.length < 3 && [0, 6].includes(nowIST.getUTCDay())) {
    nudges.push({
      id: 'nudge_weekend',
      message: 'Weekend is perfect for a full mock test! 🏆',
      sparkyEmotion: 'celebrating',
      actionUrl: '/test',
      actionLabel: 'Take test',
      priority: 3,
    });
  }

  // Rule 7: Streak milestone
  if (nudges.length < 3 && [7, 14, 21, 30, 50, 100].includes(streak)) {
    nudges.push({
      id: `nudge_streak_${streak}`,
      message: `🔥 ${streak}-day streak! You're unstoppable!`,
      sparkyEmotion: 'celebrating',
      actionUrl: '/leaderboard',
      actionLabel: 'View leaderboard',
      priority: 5,
    });
  }

  return nudges.sort((a, b) => b.priority - a.priority).slice(0, 3);
}

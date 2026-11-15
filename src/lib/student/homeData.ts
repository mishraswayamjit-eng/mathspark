// SERVER ONLY: talks to the database. Never import this from a client component
// (type-only imports are fine).
//
// One place that assembles everything the Home ("Today") screen shows. Both the
// server-rendered page (src/app/(app)/home/page.tsx) and GET /api/home call it,
// so the JSON the route returns and the page the child sees can never drift.

import { MS_PER_DAY, MS_PER_HOUR } from '@/lib/timeConstants';
import { prisma } from '@/lib/db';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';
import type { ComputedAnalytics } from '@/lib/brain/recompute';
import { endOfIstDay } from '@/lib/brain/rules';
import { getTopicsCached } from '@/lib/topicCache';
import { computeStreak, buildTopicNameMap, matchesSubTopicKey } from '@/lib/sharedUtils';
import { MONETIZATION_ENABLED, UNLIMITED_TIER } from '@/lib/monetization';
import { logError } from '@/lib/logger';
import { getWeekBounds, TIER_NAMES } from '@/lib/leaderboard';
import { TOPIC_TREE, getTopicsForGrade } from '@/data/topicTree';
import type { TopicNode } from '@/data/topicTree';
import type {
  TopicMasteryEntry,
  ExamReadinessResult,
  TopicPriority,
  DailyPlanItem,
  Nudge,
} from '@/lib/brain/engine';

// ── Types ─────────────────────────────────────────────────────────────────────

// Feature 5c: LLM surfacing/narration over the verified Brain Engine signals.
// Numbers come from the engine; this only reorders + narrates.
export interface HomeSurfacePlan {
  headline: string;
  narration: string;
  orderedTopicIds: string[];
  focusTopicId: string | null;
}

export interface HomeStudent {
  id: string;
  name: string;
  grade: number;
  avatarColor: string;
  trialExpiresAt: string | null;
  trialDaysLeft: number | null;
  trialActive: boolean;
  subscriptionTier: number;
  subscriptionName: string | null;
  examDate: string | null;
  examName: string | null;
  dailyGoalMins: number;
}

export interface HomeRecentActivity {
  /** DB topic id (Question.topicId), e.g. "ch11" or "grade5". */
  topicId: string;
  topicName: string;
  correct: number;
  attempted: number;
  pct: number;
  timeAgo: string;
}

export interface HomeData {
  student: HomeStudent;
  streak: number;
  todayCorrect: number;
  topicMastery: TopicMasteryEntry[];
  examReadiness: ExamReadinessResult;
  topicPriorities: TopicPriority[];
  dailyPlan: DailyPlanItem[];
  /** Brain Engine nudges (already computed and stored with the analytics). */
  nudges: Nudge[];
  surfacePlan: HomeSurfacePlan | null;
  recentActivity: HomeRecentActivity[];
  /**
   * Topic-tree ids (the ids used by `topicMastery`), most recently practised
   * first. `recentActivity[].topicId` is a DB topic id and cannot be looked up
   * in `topicMastery`; this can.
   */
  recentTopicIds: string[];
  leagueTier: number;
  leagueName: string;
  leagueRank: number | null;
  weeklyXP: number;
  todayXP: number;
  topicsMasteredCount: number;
  topicsExploredCount: number;
  totalTopics: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

// Analytics fields: Prisma Json? returns objects directly; handle legacy string values too.
function safeJson<T>(val: unknown, fallback: T): T {
  if (!val) return fallback;
  if (typeof val === 'string') {
    try { return JSON.parse(val) as T; } catch { return fallback; }
  }
  return val as T;
}

// DB topic id → the topic-tree nodes that draw their questions from it.
// Grade 4 chapters map one-to-one; keyed grades (e.g. Grade 5) share one DB
// topic across many nodes, told apart by `subTopicKey`.
const NODES_BY_DB_TOPIC: Record<string, TopicNode[]> = {};
TOPIC_TREE.forEach((node) => {
  const list = NODES_BY_DB_TOPIC[node.dbTopicId] || [];
  list.push(node);
  NODES_BY_DB_TOPIC[node.dbTopicId] = list;
});

/** Which topic-tree node an attempted question belongs to (null if none). */
function resolveTreeTopicId(dbTopicId: string, subTopic: string | null | undefined): string | null {
  const nodes = NODES_BY_DB_TOPIC[dbTopicId];
  if (!nodes) return null;
  let keylessId: string | null = null;
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i];
    if (node.subTopicKey) {
      if (matchesSubTopicKey(subTopic, node.subTopicKey)) return node.id;
    } else if (keylessId === null) {
      keylessId = node.id;
    }
  }
  return keylessId;
}

// ── Fresh analytics, within a time budget ─────────────────────────────────────

/**
 * The longest Home waits for a recompute. After this it shows the stored
 * analytics instead; the recompute carries on and is there for the next visit.
 */
const RECOMPUTE_BUDGET_MS = 2000;

// Recomputes running in this server instance, by student. The Home page and
// GET /api/home can ask at the same moment; they share one run.
const recomputesInFlight: Record<string, Promise<ComputedAnalytics | null> | undefined> = {};

function recomputeOnce(
  studentId: string,
  surface: 'background' | 'skip',
): Promise<ComputedAnalytics | null> {
  const running = recomputesInFlight[studentId];
  if (running) return running;
  const started = recomputeStudentAnalytics(studentId, { surface }).then(
    (result) => {
      delete recomputesInFlight[studentId];
      return result;
    },
    (err: unknown) => {
      delete recomputesInFlight[studentId];
      throw err;
    },
  );
  recomputesInFlight[studentId] = started;
  return started;
}

function startTimer(ms: number): { done: Promise<'timeout'>; cancel: () => void } {
  let id: ReturnType<typeof setTimeout> | undefined;
  const done = new Promise<'timeout'>((resolve) => {
    id = setTimeout(() => resolve('timeout'), ms);
  });
  return {
    done,
    cancel: () => {
      if (id !== undefined) clearTimeout(id);
    },
  };
}

/**
 * Recompute the analytics and hand back the result for THIS response.
 * Never throws and never takes longer than the budget: on a failure or a
 * time-out it returns null and the caller shows the stored row.
 */
async function freshAnalytics(
  studentId: string,
  surface: 'background' | 'skip',
): Promise<ComputedAnalytics | null> {
  // A failure becomes null here, so one that happens after the time-out is
  // still logged and is never an unhandled rejection.
  const work = recomputeOnce(studentId, surface).catch((err: unknown) => {
    logError('[homeData] recompute failed; showing stored analytics', err);
    return null;
  });
  const timer = startTimer(RECOMPUTE_BUDGET_MS);
  const winner = await Promise.race([work, timer.done]);
  timer.cancel();
  if (winner === 'timeout') {
    logError(`[homeData] recompute took over ${RECOMPUTE_BUDGET_MS}ms; showing stored analytics`);
    return null;
  }
  return winner;
}

// ── Loader ────────────────────────────────────────────────────────────────────

/**
 * Everything the Home screen needs for one student.
 * Returns null when the student does not exist. Throws on database failure.
 */
export async function loadHomeData(studentId: string): Promise<HomeData | null> {
  // All queries run at the same time.
  const [student, attempts, allTopics, currentMembership, todayUsage] = await Promise.all([
    prisma.student.findUnique({
      where: { id: studentId },
      select: {
        id: true,
        name: true,
        grade: true,
        avatarColor: true,
        examDate: true,
        examName: true,
        dailyGoalMins: true,
        trialExpiresAt: true,
        createdAt: true,
        currentLeagueTier: true,
        totalLifetimeXP: true,
        subscription: { select: { tier: true, name: true } },
        analytics: true,
      },
    }),
    prisma.attempt.findMany({
      where: { studentId },
      select: {
        isCorrect: true,
        createdAt: true,
        question: { select: { topicId: true, subTopic: true } },
      },
      orderBy: { createdAt: 'desc' },
      take: 100,
    }),
    getTopicsCached(),
    // Current week's league membership (for weeklyXP + rank)
    (async () => {
      const { weekStart } = getWeekBounds();
      return prisma.leagueMembership.findFirst({
        where: { studentId, league: { weekStart } },
        select: {
          weeklyXP: true,
          league: {
            select: {
              members: {
                select: { studentId: true, weeklyXP: true },
                orderBy: { weeklyXP: 'desc' as const },
              },
            },
          },
        },
      });
    })(),
    // Today's XP (from UsageLog)
    (async () => {
      const today = new Date();
      today.setUTCHours(0, 0, 0, 0);
      return prisma.usageLog.findUnique({
        where: { studentId_date: { studentId, date: today } },
        select: { xpEarned: true },
      });
    })(),
    // SLOT: NextActionCard — load its data here (add to this Promise.all and to HomeData).
    // SLOT: NudgeStrip — the engine's nudges are already returned below as `nudges`;
    //       load anything extra the strip needs here.
  ]);

  if (!student) return null;

  // The stored analytics (plan, priorities, nudges) are out of date when:
  //   - there are none, or they are over an hour old;
  //   - the child has answered a question since they were worked out
  //     (`attempts` is newest first, and `lastComputedAt` is the moment the
  //     recompute started reading, so nothing answered since is in the row);
  //   - the India-time day has changed (the plan and the day's nudges are per day).
  // Then they are recomputed NOW and this response uses the result, so the plan
  // and nudges never lag a visit behind. The wait is bounded (`freshAnalytics`):
  // on a time-out or failure the stored row is shown, as before.
  const stored = student.analytics;
  const nowMs = Date.now();
  const computedAtMs = stored ? new Date(stored.lastComputedAt).getTime() : 0;
  const newestAttemptMs = attempts.length > 0 ? new Date(attempts[0].createdAt).getTime() : 0;
  const isOld = !stored || nowMs - computedAtMs > MS_PER_HOUR;
  const hasNewAnswers = !!stored && newestAttemptMs > computedAtMs;
  const dayChanged = !!stored && endOfIstDay(new Date(computedAtMs)).getTime() <= nowMs;

  // The Feature 5c narration is an LLM call and is never waited for here. It is
  // refreshed in the background, and only when the row is missing or over an
  // hour old (as often as before), not after every practice session.
  const fresh = isOld || hasNewAnswers || dayChanged
    ? await freshAnalytics(studentId, isOld ? 'background' : 'skip')
    : null;

  const streak = computeStreak(attempts);

  const todayStr = new Date().toDateString();
  const todayCorrect = attempts.filter(
    (a) => a.isCorrect && new Date(a.createdAt).toDateString() === todayStr,
  ).length;

  // Recent activity, grouped by DB topic and day
  const recentAttempts = attempts.slice(0, 50);
  const topicMap = buildTopicNameMap(allTopics);

  const groups = new Map<string, {
    topicId: string; attempted: number; correct: number; latest: Date;
  }>();
  for (const a of recentAttempts) {
    const key = `${a.question.topicId}__${new Date(a.createdAt).toDateString()}`;
    if (!groups.has(key)) {
      groups.set(key, { topicId: a.question.topicId, attempted: 0, correct: 0, latest: new Date(a.createdAt) });
    }
    const g = groups.get(key)!;
    g.attempted++;
    if (a.isCorrect) g.correct++;
  }
  const recentActivity: HomeRecentActivity[] = Array.from(groups.values())
    .sort((a, b) => b.latest.getTime() - a.latest.getTime())
    .slice(0, 4)
    .map((g) => {
      const diffMs = Date.now() - g.latest.getTime();
      const diffH  = Math.floor(diffMs / MS_PER_HOUR);
      const diffD  = Math.floor(diffH / 24);
      const timeAgo = diffD > 0 ? `${diffD}d ago` : diffH > 0 ? `${diffH}h ago` : 'just now';
      return {
        topicId:   g.topicId,
        topicName: topicMap.get(g.topicId) ?? g.topicId,
        correct:   g.correct,
        attempted: g.attempted,
        pct:       g.attempted > 0 ? Math.round(g.correct / g.attempted * 100) : 0,
        timeAgo,
      };
    });

  // Topic-tree ids of what was practised most recently (attempts are newest first).
  const recentTopicIds: string[] = [];
  for (let i = 0; i < recentAttempts.length && recentTopicIds.length < 6; i++) {
    const q = recentAttempts[i].question;
    const treeId = resolveTreeTopicId(q.topicId, q.subTopic);
    if (treeId && recentTopicIds.indexOf(treeId) === -1) recentTopicIds.push(treeId);
  }

  // League + XP derived fields
  const leagueTier = student.currentLeagueTier ?? 1;
  const leagueName: string = TIER_NAMES[leagueTier] ?? 'Bronze';
  const weeklyXP = currentMembership?.weeklyXP ?? 0;
  const todayXP = todayUsage?.xpEarned ?? 0;

  let leagueRank: number | null = null;
  if (currentMembership?.league?.members) {
    const idx = currentMembership.league.members.findIndex((m) => m.studentId === studentId);
    leagueRank = idx >= 0 ? idx + 1 : null;
  }

  const analytics = student.analytics;
  const subscriptionTier = MONETIZATION_ENABLED ? (student.subscription?.tier ?? 0) : UNLIMITED_TIER;
  const subscriptionName = student.subscription?.name ?? null;

  const trialExpiresAt = student.trialExpiresAt;
  const trialDaysLeft  = trialExpiresAt
    ? Math.max(0, Math.ceil((new Date(trialExpiresAt).getTime() - Date.now()) / MS_PER_DAY))
    : null;
  const trialActive = trialDaysLeft !== null && trialDaysLeft > 0;

  // Just recomputed when there is a fresh result; otherwise the stored row.
  const parsedMastery    = fresh ? fresh.topicMastery
    : safeJson<TopicMasteryEntry[]>(analytics?.topicMastery, []);
  const parsedReadiness  = fresh ? fresh.examReadiness
    : safeJson<ExamReadinessResult>(analytics?.examReadiness, {} as ExamReadinessResult);
  const parsedPriorities = fresh ? fresh.topicPriorities
    : safeJson<TopicPriority[]>(analytics?.topicPriorities, []);
  const parsedPlan       = fresh ? fresh.dailyPlan
    : safeJson<DailyPlanItem[]>(analytics?.dailyPlan, []);
  const parsedNudges     = fresh ? fresh.nudges
    : safeJson<Nudge[]>(analytics?.nudges, []);
  // The narration is never recomputed on this path: always the stored one.
  const parsedSurface   = safeJson<HomeSurfacePlan | null>(analytics?.surfacePlan, null);

  // Topic summary counts (from already-parsed analytics, no extra DB query)
  const masteryArray = Array.isArray(parsedMastery) ? parsedMastery : [];
  const topicsMasteredCount = masteryArray.filter((t) => t.status === 'mastered').length;
  const topicsExploredCount = masteryArray.filter((t) => (t.attemptsCount ?? 0) > 0).length;
  const totalTopics = getTopicsForGrade(student.grade).length;

  return {
    student: {
      id:            student.id,
      name:          student.name,
      grade:         student.grade,
      avatarColor:   student.avatarColor,
      trialExpiresAt: trialExpiresAt ? trialExpiresAt.toISOString() : null,
      trialDaysLeft,
      trialActive,
      subscriptionTier,
      subscriptionName,
      examDate:      student.examDate ? student.examDate.toISOString() : null,
      examName:      student.examName ?? null,
      dailyGoalMins: student.dailyGoalMins,
    },
    streak,
    todayCorrect,
    topicMastery:    parsedMastery,
    examReadiness:   parsedReadiness,
    topicPriorities: parsedPriorities,
    dailyPlan:       parsedPlan,
    nudges:          parsedNudges,
    surfacePlan:     parsedSurface,
    recentActivity,
    recentTopicIds,
    leagueTier,
    leagueName,
    leagueRank,
    weeklyXP,
    todayXP,
    topicsMasteredCount,
    topicsExploredCount,
    totalTopics,
  };
}

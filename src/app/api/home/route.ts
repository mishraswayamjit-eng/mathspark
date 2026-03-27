import { MS_PER_DAY, MS_PER_HOUR } from '@/lib/timeConstants';
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';
import { getTopicsCached } from '@/lib/topicCache';
import { computeStreak } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { getWeekBounds, TIER_NAMES } from '@/lib/leaderboard';
import { getTopicsForGrade } from '@/data/topicTree';

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

// GET /api/home
export async function GET() {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Parallelize all 5 DB queries simultaneously
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
      select: { isCorrect: true, createdAt: true, question: { select: { topicId: true } } },
      orderBy: { createdAt: 'desc' },
      take: 100,
    }),
    getTopicsCached(),
    // Query 4 — Current week's league membership (for weeklyXP + rank)
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
    // Query 5 — Today's XP (from UsageLog)
    (async () => {
      const today = new Date();
      today.setUTCHours(0, 0, 0, 0);
      return prisma.usageLog.findUnique({
        where: { studentId_date: { studentId, date: today } },
        select: { xpEarned: true },
      });
    })(),
  ]);

  if (!student) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  // Recompute analytics if missing or stale (> 1 hour)
  // Always fire-and-forget — return immediately with whatever we have (or empty defaults).
  // The next page load will pick up the freshly computed analytics.
  const isStale = !student.analytics ||
    Date.now() - new Date(student.analytics!.lastComputedAt).getTime() > MS_PER_HOUR;

  if (isStale) {
    recomputeStudentAnalytics(studentId).catch((err) =>
      console.error('[api/home] background recompute failed:', err),
    );
  }

  const streak = computeStreak(attempts);

  const todayStr = new Date().toDateString();
  const todayCorrect = attempts.filter(
    (a) => a.isCorrect && new Date(a.createdAt).toDateString() === todayStr,
  ).length;

  // Recent activity
  const recentAttempts = attempts.slice(0, 50);
  const topicMap = new Map(allTopics.map((t) => [t.id, t.name]));

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
  const recentActivity = Array.from(groups.values())
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

  // League + XP derived fields
  const leagueTier = student.currentLeagueTier ?? 1;
  const leagueName = TIER_NAMES[leagueTier] ?? 'Bronze';
  const weeklyXP = currentMembership?.weeklyXP ?? 0;
  const todayXP = todayUsage?.xpEarned ?? 0;

  let leagueRank: number | null = null;
  if (currentMembership?.league?.members) {
    const idx = currentMembership.league.members.findIndex(m => m.studentId === studentId);
    leagueRank = idx >= 0 ? idx + 1 : null;
  }

  const analytics = student.analytics;
  const subscriptionTier = student.subscription?.tier ?? 0;
  const subscriptionName = student.subscription?.name ?? null;

  const trialExpiresAt = student.trialExpiresAt;
  const trialDaysLeft  = trialExpiresAt
    ? Math.max(0, Math.ceil((new Date(trialExpiresAt).getTime() - Date.now()) / MS_PER_DAY))
    : null;
  const trialActive = trialDaysLeft !== null && trialDaysLeft > 0;

  // Analytics fields: Prisma Json? returns objects directly; handle legacy string values too
  function safeJson<T>(val: unknown, fallback: T): T {
    if (!val) return fallback;
    if (typeof val === 'string') { try { return JSON.parse(val) as T; } catch { return fallback; } }
    return val as T;
  }
  const parsedMastery    = safeJson(analytics?.topicMastery,    [] as unknown[]);
  const parsedReadiness  = safeJson(analytics?.examReadiness,   {} as Record<string, unknown>);
  const parsedPriorities = safeJson(analytics?.topicPriorities, [] as unknown[]);
  const parsedPlan       = safeJson(analytics?.dailyPlan,       [] as unknown[]);
  const parsedNudges     = safeJson(analytics?.nudges,          [] as unknown[]);

  // Topic summary counts (from already-parsed analytics, no extra DB query)
  const masteryArray = parsedMastery as Array<{ status?: string; attemptsCount?: number }>;
  const topicsMasteredCount = masteryArray.filter(t => t.status === 'mastered').length;
  const topicsExploredCount = masteryArray.filter(t => (t.attemptsCount ?? 0) > 0).length;
  const totalTopics = getTopicsForGrade(student.grade).length;

  return NextResponse.json(
    {
      student: {
        id:            student.id,
        name:          student.name,
        grade:         student.grade,
        avatarColor:   student.avatarColor,
        trialExpiresAt: trialExpiresAt?.toISOString() ?? null,
        trialDaysLeft,
        trialActive,
        subscriptionTier,
        subscriptionName,
        examDate:     student.examDate?.toISOString() ?? null,
        examName:     student.examName ?? null,
        dailyGoalMins: student.dailyGoalMins,
      },
      streak,
      todayCorrect,
      topicMastery:    parsedMastery,
      examReadiness:   parsedReadiness,
      topicPriorities: parsedPriorities,
      dailyPlan:       parsedPlan,
      nudges:          parsedNudges,
      recentActivity,
      leagueTier,
      leagueName,
      leagueRank,
      weeklyXP,
      todayXP,
      topicsMasteredCount,
      topicsExploredCount,
      totalTopics,
    },
    {
      headers: {
        'Cache-Control': 's-maxage=30, stale-while-revalidate=120',
      },
    },
  );
}

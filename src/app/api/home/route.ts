import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

function computeStreak(attempts: Array<{ createdAt: Date }>): number {
  if (!attempts.length) return 0;
  const days = new Set(attempts.map((a) => new Date(a.createdAt).toDateString()));
  const today = new Date();
  let streak = 0;
  for (let i = 0; i < 365; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    if (days.has(d.toDateString())) streak++;
    else break;
  }
  return streak;
}

// GET /api/home?studentId=xxx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const student = await prisma.student.findUnique({
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
      subscription: { select: { tier: true, name: true } },
      analytics: true,
    },
  });

  if (!student) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  // Recompute analytics if missing or stale (> 1 hour) — fire-and-forget, never block response
  const ONE_HOUR = 60 * 60 * 1000;
  const isStale = !student.analytics ||
    Date.now() - new Date(student.analytics.lastComputedAt).getTime() > ONE_HOUR;

  if (isStale) {
    recomputeStudentAnalytics(studentId).catch((err) =>
      console.error('[api/home] background recompute failed:', err),
    );
  }

  // Streak + today's correct
  const attempts = await prisma.attempt.findMany({
    where: { studentId },
    select: { isCorrect: true, createdAt: true, question: { select: { topicId: true } } },
    orderBy: { createdAt: 'desc' },
  });

  const streak = computeStreak(attempts);

  const todayStr = new Date().toDateString();
  const todayCorrect = attempts.filter(
    (a) => a.isCorrect && new Date(a.createdAt).toDateString() === todayStr,
  ).length;

  // Recent activity
  const recentAttempts = attempts.slice(0, 50);
  const allTopics = await prisma.topic.findMany({ select: { id: true, name: true } });
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
      const diffH  = Math.floor(diffMs / 3600000);
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

  const analytics = student.analytics;
  const subscriptionTier = student.subscription?.tier ?? 0;
  const subscriptionName = student.subscription?.name ?? null;

  const trialExpiresAt = student.trialExpiresAt;
  const trialDaysLeft  = trialExpiresAt
    ? Math.max(0, Math.ceil((new Date(trialExpiresAt).getTime() - Date.now()) / 86400000))
    : null;
  const trialActive = trialDaysLeft !== null && trialDaysLeft > 0;

  return NextResponse.json({
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
    topicMastery:    (analytics?.topicMastery    ?? []),
    examReadiness:   (analytics?.examReadiness   ?? {}),
    topicPriorities: (analytics?.topicPriorities ?? []),
    dailyPlan:       (analytics?.dailyPlan       ?? []),
    nudges:          (analytics?.nudges          ?? []),
    recentActivity,
  });
}

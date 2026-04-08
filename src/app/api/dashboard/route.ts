import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { computeWeeklyData, computeRecentActivity } from '@/lib/studentDashboard';

// ── Route ─────────────────────────────────────────────────────────────────────

export const dynamic = 'force-dynamic';

// GET /api/dashboard
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const [student, progress, attempts, allTopics] = await Promise.all([
      prisma.student.findUnique({
        where: { id: studentId },
        select: {
          id: true, name: true, displayName: true, grade: true,
          avatarColor: true, createdAt: true, currentLeagueTier: true,
          totalLifetimeXP: true, currentStreak: true, longestStreak: true,
          totalDaysPracticed: true, examName: true, examDate: true,
          dailyGoalMins: true, trialExpiresAt: true,
          subscription: { select: { tier: true } },
        },
      }),
      prisma.progress.findMany({ where: { studentId }, include: { topic: true } }),
      prisma.attempt.findMany({
        where: { studentId },
        select: {
          isCorrect: true,
          createdAt: true,
          question: { select: { topicId: true } },
        },
        orderBy: { createdAt: 'desc' },
        take: 100,
      }),
      getTopicsCached(),
    ]);

    if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

    const topicMap = new Map(allTopics.map((t) => [t.id, t.name]));

    const progressMap = new Map(progress.map((p) => [p.topicId, p]));
    const gradeTopics = allTopics.filter((t) => t.grade === student.grade);
    const topics = gradeTopics
      .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
      .map((t) => {
        const p = progressMap.get(t.id);
        return {
          ...t,
          mastery:   p?.mastery   ?? 'NotStarted',
          attempted: p?.attempted ?? 0,
          correct:   p?.correct   ?? 0,
        };
      });

    // Prefer Practicing topics with lowest accuracy; fall back to any non-mastered
    const practicing = topics.filter((t) => t.mastery === 'Practicing');
    const fallback   = topics.filter((t) => t.attempted > 0 && t.mastery !== 'Mastered');
    const pool       = practicing.length > 0 ? practicing : fallback;
    const weakest    = pool.sort(
      (a, b) => (a.correct / Math.max(a.attempted, 1)) - (b.correct / Math.max(b.attempted, 1)),
    )[0];

    return NextResponse.json(
      {
        student,
        stats: {
          totalSolved:      attempts.filter((a) => a.isCorrect).length,
          topicsMastered:   progress.filter((p) => p.mastery === 'Mastered').length,
          streakDays:       computeStreak(attempts),
          totalLifetimeXP:  (student as unknown as { totalLifetimeXP?: number }).totalLifetimeXP ?? 0,
        },
        topics,
        weeklyData:       computeWeeklyData(attempts),
        weakestTopicId:   weakest?.id ?? topics[0]?.id ?? null,
        weakestTopicName: weakest?.name ?? null,
        recentActivity:   computeRecentActivity(attempts, topicMap),
        subscriptionTier: (student as { subscription?: { tier: number } | null }).subscription?.tier ?? 0,
      },
      {
        headers: {
          'Cache-Control': 's-maxage=30, stale-while-revalidate=120',
        },
      },
    );
  } catch (err) {
    console.error('[dashboard]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

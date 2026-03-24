import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

function computeWeeklyData(attempts: Array<{ createdAt: Date; isCorrect: boolean }>) {
  const today = new Date();
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(d.getDate() - (6 - i));
    const dateStr = d.toDateString();
    return {
      date: d.toLocaleDateString('en-IN', { weekday: 'short' }),
      count: attempts.filter(
        (a) => a.isCorrect && new Date(a.createdAt).toDateString() === dateStr,
      ).length,
    };
  });
}

// GET /api/profile
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
          dailyGoalMins: true, trialExpiresAt: true, badges: true,
          subscription: { select: { tier: true, name: true } },
        },
      }),
      prisma.progress.findMany({ where: { studentId }, include: { topic: true } }),
      prisma.attempt.findMany({
        where: { studentId },
        select: { isCorrect: true, createdAt: true, timeTakenMs: true },
        orderBy: { createdAt: 'asc' }, // asc for consecutive-streak computation
        take: 300,
      }),
      getTopicsCached(),
    ]);

    if (!student) {
      return NextResponse.json({ error: 'Student not found' }, { status: 404 });
    }

    // Max consecutive correct answers
    let maxConsecutive = 0;
    let current = 0;
    for (const a of attempts) {
      if (a.isCorrect) { current++; maxConsecutive = Math.max(maxConsecutive, current); }
      else current = 0;
    }

    // Correct answers completed under 10 seconds (timeTakenMs must be recorded > 0)
    const fastCorrects = attempts.filter(
      (a) => a.isCorrect && a.timeTakenMs > 0 && a.timeTakenMs < 10_000,
    ).length;

    const correctAttempts = attempts.filter((a) => a.isCorrect);

    const topics = allTopics
      .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
      .map((t) => {
        const p = progress.find((x) => x.topicId === t.id);
        return {
          ...t,
          mastery:   p?.mastery   ?? 'NotStarted',
          attempted: p?.attempted ?? 0,
          correct:   p?.correct   ?? 0,
        };
      });

    const weakest = topics
      .filter((t) => t.attempted > 0 && t.mastery !== 'Mastered')
      .sort((a, b) => (a.correct / a.attempted) - (b.correct / b.attempted))[0];

    return NextResponse.json(
      {
        student,
        stats: {
          totalSolved:            correctAttempts.length,
          totalAttempted:         attempts.length,
          topicsMastered:         progress.filter((p) => p.mastery === 'Mastered').length,
          streakDays:             computeStreak(correctAttempts),
          maxConsecutiveCorrect:  maxConsecutive,
          fastCorrects,
        },
        topics,
        weeklyData:     computeWeeklyData(attempts),
        weakestTopicId: weakest?.id ?? topics[0]?.id ?? null,
      },
      {
        headers: {
          'Cache-Control': 's-maxage=60, stale-while-revalidate=300',
        },
      },
    );
  } catch (err) {
    console.error('[profile] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

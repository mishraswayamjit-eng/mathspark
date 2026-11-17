import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak, buildLookupMap } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { computeWeeklyData, weeklyWindowStart } from '@/lib/studentDashboard';
import { loadStreakAttempts } from '@/lib/student/streakData';
import { logError } from '@/lib/logger';

// Per-child data: never stored by the browser or any shared cache.
const NO_STORE = { 'Cache-Control': 'private, no-store' };

/** How many of the latest answers the longest run of right answers is looked for in. */
const RUN_ATTEMPT_WINDOW = 1000;

// GET /api/profile
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
    }

    const now = new Date();
    const [
      student, progress, attempts, allTopics,
      streakAttempts, weekAttempts, totalSolved, totalAttempted, fastCorrects,
    ] = await Promise.all([
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
      // The child's latest answers, newest first, for the longest run of right
      // answers. (This used to be the OLDEST 300 answers ever, so nothing a
      // child did after their first 300 questions showed on the profile.)
      prisma.attempt.findMany({
        where: { studentId },
        select: { isCorrect: true },
        orderBy: { createdAt: 'desc' },
        take: RUN_ATTEMPT_WINDOW,
      }),
      getTopicsCached(),
      // When the child answered (times only): the day streak, counted the same
      // way as on Home and Progress.
      loadStreakAttempts(studentId, now),
      // Every answer in the weekly chart's seven India-time days.
      prisma.attempt.findMany({
        where: { studentId, createdAt: { gte: weeklyWindowStart(now) } },
        select: { isCorrect: true, createdAt: true },
      }),
      // Totals are counted in the database, not from a slice of rows.
      prisma.attempt.count({ where: { studentId, isCorrect: true } }),
      prisma.attempt.count({ where: { studentId } }),
      // Correct answers completed under 10 seconds (timeTakenMs must be recorded > 0)
      prisma.attempt.count({
        where: { studentId, isCorrect: true, timeTakenMs: { gt: 0, lt: 10_000 } },
      }),
    ]);

    if (!student) {
      return NextResponse.json({ error: 'Student not found' }, { status: 404, headers: NO_STORE });
    }

    // Max consecutive correct answers (within the latest RUN_ATTEMPT_WINDOW answers).
    // The rows are newest first; a run is the same length read in either direction.
    let maxConsecutive = 0;
    let current = 0;
    for (let i = 0; i < attempts.length; i++) {
      if (attempts[i].isCorrect) { current++; maxConsecutive = Math.max(maxConsecutive, current); }
      else current = 0;
    }

    const progressMap = buildLookupMap(progress, 'topicId');
    const topics = allTopics
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

    const weakest = topics
      .filter((t) => t.attempted > 0 && t.mastery !== 'Mastered')
      .sort((a, b) => (a.correct / a.attempted) - (b.correct / b.attempted))[0];

    return NextResponse.json(
      {
        student,
        stats: {
          totalSolved,
          totalAttempted,
          topicsMastered:         progress.filter((p) => p.mastery === 'Mastered').length,
          streakDays:             computeStreak(streakAttempts, false, now),
          maxConsecutiveCorrect:  maxConsecutive,
          fastCorrects,
        },
        topics,
        weeklyData:     computeWeeklyData(weekAttempts, true, now),
        weakestTopicId: weakest?.id ?? topics[0]?.id ?? null,
      },
      { headers: NO_STORE },
    );
  } catch (err) {
    logError('[profile] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}

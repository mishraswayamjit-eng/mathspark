import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import type { PublicProfile, WeeklyAwardData } from '@/types';

// GET /api/profile/[studentId] — public profile (no PII)
export async function GET(
  _req: Request,
  { params }: { params: { studentId: string } },
) {
  try {
    const { studentId } = params;

    const student = await prisma.student.findUnique({
      where:  { id: studentId },
      select: {
        id:                    true,
        name:                  true,
        displayName:           true,
        avatarColor:           true,
        currentLeagueTier:     true,
        totalLifetimeXP:       true,
        hiddenFromLeaderboard: true,
        createdAt:             true,
        currentStreak:         true,
      },
    });

    if (!student || student.hiddenFromLeaderboard) {
      return NextResponse.json({ error: 'Profile not found' }, { status: 404 });
    }

    // Stats from attempts
    const [totalAttempts, totalCorrect, masteredCount, awards] = await Promise.all([
      prisma.attempt.count({ where: { studentId } }),
      prisma.attempt.count({ where: { studentId, isCorrect: true } }),
      prisma.progress.count({ where: { studentId, mastery: 'Mastered' } }),
      prisma.weeklyAward.findMany({
        where:   { studentId },
        orderBy: { weekStart: 'desc' },
        take:    10,
        select:  { awardType: true, value: true, studentId: true },
      }),
    ]);

    const profile: PublicProfile = {
      studentId:        student.id,
      displayName:      student.displayName ?? student.name.split(' ')[0],
      avatarColor:       student.avatarColor,
      currentLeagueTier: student.currentLeagueTier,
      totalLifetimeXP:  student.totalLifetimeXP,
      totalSolved:      totalCorrect,
      topicsMastered:   masteredCount,
      currentStreak:    student.currentStreak,
      joinedAt:         student.createdAt.toISOString(),
      awards:           awards.map((a) => ({
        awardType:   a.awardType as WeeklyAwardData['awardType'],
        value:       a.value,
        studentId:   a.studentId,
        displayName: student.displayName ?? student.name.split(' ')[0],
      })),
    };

    return NextResponse.json(profile);
  } catch (err) {
    console.error('[profile GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

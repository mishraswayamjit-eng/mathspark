import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak, getDisplayName, buildLookupMap } from '@/lib/sharedUtils';
import { computeWeeklyData } from '@/lib/studentDashboard';

export const dynamic = 'force-dynamic';

// GET /api/parent/report/[studentId]
// Returns limited dashboard data — requires an authenticated parent
// who owns this student (prevents IDOR via guessed studentIds).
export async function GET(
  _req: Request,
  { params }: { params: { studentId: string } },
) {
  const { studentId } = params;

  if (!studentId || typeof studentId !== 'string' || studentId.length > 30) {
    return NextResponse.json({ error: 'Invalid studentId' }, { status: 400 });
  }

  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Ownership check: only the student's parent may view this report.
  const owned = await prisma.student.findFirst({
    where: { id: studentId, parentId: session.user.id, deletedAt: null },
    select: { id: true },
  });
  if (!owned) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  // Streak and the weekly chart only need recent days; the lifetime total is
  // counted in the database, so it is not capped by how many rows are read.
  const recentSince = new Date(Date.now() - 60 * 24 * 60 * 60 * 1000);

  const [student, progress, attempts, allTopics, totalSolved] = await Promise.all([
    prisma.student.findUnique({
      where: { id: studentId },
      select: {
        name: true,
        displayName: true,
        grade: true,
      },
    }),
    prisma.progress.findMany({ where: { studentId }, include: { topic: true } }),
    prisma.attempt.findMany({
      where: { studentId, createdAt: { gte: recentSince } },
      select: { isCorrect: true, createdAt: true },
      orderBy: { createdAt: 'desc' },
      take: 5000,
    }),
    getTopicsCached(),
    prisma.attempt.count({ where: { studentId, isCorrect: true } }),
  ]);

  if (!student) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  const progressMap = buildLookupMap(progress, 'topicId');
  // Only the child's own grade: a Grade 5 report must not list the Grade 4
  // chapters. (filter() also copies, so the shared topic cache is not re-sorted.)
  const topics = allTopics
    .filter((t) => t.grade === student.grade)
    .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
    .map((t) => {
      const p = progressMap.get(t.id);
      return {
        id:        t.id,
        name:      t.name,
        mastery:   p?.mastery   ?? 'NotStarted',
        attempted: p?.attempted ?? 0,
        correct:   p?.correct   ?? 0,
      };
    });

  return NextResponse.json(
    {
      student: { name: getDisplayName(student.name, student.displayName), grade: student.grade },
      stats: {
        totalSolved,
        topicsMastered: topics.filter((t) => t.mastery === 'Mastered').length,
        streakDays:     computeStreak(attempts),
      },
      topics,
      weeklyData: computeWeeklyData(attempts),
    },
    {
      headers: { 'Cache-Control': 'private, no-store' },
    },
  );
}

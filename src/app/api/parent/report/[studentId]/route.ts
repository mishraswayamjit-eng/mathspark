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

  const [student, progress, attempts, allTopics] = await Promise.all([
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
      where: { studentId },
      select: { isCorrect: true, createdAt: true },
      orderBy: { createdAt: 'desc' },
      take: 100,
    }),
    getTopicsCached(),
  ]);

  if (!student) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  const progressMap = buildLookupMap(progress, 'topicId');
  const topics = allTopics
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
        totalSolved:    attempts.filter((a) => a.isCorrect).length,
        topicsMastered: progress.filter((p) => p.mastery === 'Mastered').length,
        streakDays:     computeStreak(attempts),
      },
      topics,
      weeklyData: computeWeeklyData(attempts),
    },
    {
      headers: { 'Cache-Control': 's-maxage=60, stale-while-revalidate=300' },
    },
  );
}

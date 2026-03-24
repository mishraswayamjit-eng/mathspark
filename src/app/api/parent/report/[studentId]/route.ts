import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak } from '@/lib/sharedUtils';

export const dynamic = 'force-dynamic';

function computeWeeklyData(attempts: Array<{ createdAt: Date }>) {
  const today = new Date();
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(d.getDate() - (6 - i));
    const dateStr = d.toDateString();
    return {
      date:  d.toLocaleDateString('en-IN', { weekday: 'short' }),
      count: attempts.filter((a) => new Date(a.createdAt).toDateString() === dateStr).length,
    };
  });
}

// GET /api/parent/report/[studentId]
// Public endpoint for share links — returns limited dashboard data (no PII).
export async function GET(
  _req: Request,
  { params }: { params: { studentId: string } },
) {
  const { studentId } = params;

  if (!studentId || typeof studentId !== 'string' || studentId.length > 30) {
    return NextResponse.json({ error: 'Invalid studentId' }, { status: 400 });
  }

  const [student, progress, attempts, allTopics] = await Promise.all([
    prisma.student.findUnique({
      where: { id: studentId },
      select: {
        name: true,
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

  const topics = allTopics
    .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
    .map((t) => {
      const p = progress.find((x) => x.topicId === t.id);
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
      student: { name: student.name, grade: student.grade },
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

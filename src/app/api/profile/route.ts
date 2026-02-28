import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

function computeStreakDays(attempts: Array<{ createdAt: Date }>): number {
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

// GET /api/profile?studentId=xxx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const [student, progress, attempts, allTopics] = await Promise.all([
    prisma.student.findUnique({ where: { id: studentId } }),
    prisma.progress.findMany({ where: { studentId }, include: { topic: true } }),
    prisma.attempt.findMany({
      where: { studentId },
      select: { isCorrect: true, createdAt: true, timeTakenMs: true },
      orderBy: { createdAt: 'asc' }, // asc for consecutive-streak computation
    }),
    prisma.topic.findMany(),
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

  return NextResponse.json({
    student,
    stats: {
      totalSolved:            correctAttempts.length,
      totalAttempted:         attempts.length,
      topicsMastered:         progress.filter((p) => p.mastery === 'Mastered').length,
      streakDays:             computeStreakDays(correctAttempts),
      maxConsecutiveCorrect:  maxConsecutive,
      fastCorrects,
    },
    topics,
    weeklyData:     computeWeeklyData(attempts),
    weakestTopicId: weakest?.id ?? topics[0]?.id ?? null,
  });
}

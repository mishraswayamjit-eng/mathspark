import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import type { RecentSession } from '@/types';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

// ── Streak: consecutive days with at least 1 attempt backwards from today ─────
function computeStreak(attempts: Array<{ createdAt: Date }>): number {
  if (attempts.length === 0) return 0;
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

// ── Weekly chart: attempts per day for last 7 days ────────────────────────────
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

// ── Recent activity: last 5 (topicId × calendar-day) sessions ─────────────────
function computeRecentActivity(
  attempts: Array<{ isCorrect: boolean; createdAt: Date; question: { topicId: string } }>,
  topicMap: Map<string, string>,
): RecentSession[] {
  const groups = new Map<string, { topicId: string; attempted: number; correct: number; latest: Date }>();

  for (const a of attempts) {
    const topicId = a.question.topicId;
    const dayKey  = new Date(a.createdAt).toDateString();
    const key     = `${topicId}__${dayKey}`;

    if (!groups.has(key)) {
      groups.set(key, { topicId, attempted: 0, correct: 0, latest: new Date(a.createdAt) });
    }
    const g = groups.get(key)!;
    g.attempted++;
    if (a.isCorrect) g.correct++;
    const at = new Date(a.createdAt);
    if (at > g.latest) g.latest = at;
  }

  return Array.from(groups.values())
    .sort((a, b) => b.latest.getTime() - a.latest.getTime())
    .slice(0, 5)
    .map((g) => ({
      topicId:   g.topicId,
      topicName: topicMap.get(g.topicId) ?? g.topicId,
      attempted: g.attempted,
      correct:   g.correct,
      createdAt: g.latest.toISOString(),
    }));
}

// ── Route ─────────────────────────────────────────────────────────────────────

export const dynamic = 'force-dynamic';

// GET /api/dashboard?studentId=xxx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const [student, progress, attempts, allTopics] = await Promise.all([
    prisma.student.findUnique({
      where:   { id: studentId },
      include: { subscription: { select: { tier: true } } },
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
    }),
    prisma.topic.findMany(),
  ]);

  if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

  const topicMap = new Map(allTopics.map((t) => [t.id, t.name]));

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

  // Prefer Practicing topics with lowest accuracy; fall back to any non-mastered
  const practicing = topics.filter((t) => t.mastery === 'Practicing');
  const fallback   = topics.filter((t) => t.attempted > 0 && t.mastery !== 'Mastered');
  const pool       = practicing.length > 0 ? practicing : fallback;
  const weakest    = pool.sort(
    (a, b) => (a.correct / Math.max(a.attempted, 1)) - (b.correct / Math.max(b.attempted, 1)),
  )[0];

  return NextResponse.json({
    student,
    stats: {
      totalSolved:    attempts.filter((a) => a.isCorrect).length,
      topicsMastered: progress.filter((p) => p.mastery === 'Mastered').length,
      streakDays:     computeStreak(attempts),
    },
    topics,
    weeklyData:       computeWeeklyData(attempts),
    weakestTopicId:   weakest?.id ?? topics[0]?.id ?? null,
    weakestTopicName: weakest?.name ?? null,
    recentActivity:   computeRecentActivity(attempts, topicMap),
    subscriptionTier: (student as { subscription?: { tier: number } | null }).subscription?.tier ?? 0,
  });
}

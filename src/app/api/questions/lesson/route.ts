import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// GET /api/questions/lesson?topicId=xxx&studentId=xxx&count=10
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId   = searchParams.get('topicId');
  const studentId = searchParams.get('studentId');
  const count     = Math.min(parseInt(searchParams.get('count') ?? '10', 10), 20);

  if (!topicId || !studentId) {
    return NextResponse.json({ error: 'topicId and studentId required' }, { status: 400 });
  }

  // Get student mastery for this topic
  const progress = await prisma.progress.findUnique({
    where: { studentId_topicId: { studentId, topicId } },
  });
  const mastery = progress?.mastery ?? 'NotStarted';

  // Exclude recently-seen questions (last 30 attempts for this topic)
  const recent = await prisma.attempt.findMany({
    where: { studentId, question: { topicId } },
    orderBy: { createdAt: 'desc' },
    take: 30,
    select: { questionId: true },
  });
  const seenIds = recent.map((a) => a.questionId);

  // Fetch unseen questions first; fallback to all if not enough
  let pool = await prisma.question.findMany({
    where: { topicId, id: { notIn: seenIds } },
  });
  if (pool.length < count) {
    pool = await prisma.question.findMany({ where: { topicId } });
  }

  // Group by difficulty and shuffle each group
  const byDiff: Record<string, typeof pool> = { Easy: [], Medium: [], Hard: [] };
  pool.forEach((q) => byDiff[q.difficulty]?.push(q));
  Object.keys(byDiff).forEach((d) => { byDiff[d] = shuffle(byDiff[d]); });

  // Difficulty distribution per mastery
  const dist: Record<string, number> =
    mastery === 'NotStarted' ? { Easy: 4, Medium: 4, Hard: 2 } :
    mastery === 'Mastered'   ? { Easy: 1, Medium: 4, Hard: 5 } :
                               { Easy: 2, Medium: 5, Hard: 3 };

  // Pick by difficulty, then shuffle and trim to count
  const selected: typeof pool = [];
  for (const [diff, n] of Object.entries(dist)) {
    selected.push(...byDiff[diff].slice(0, n));
  }

  let final = shuffle(selected).slice(0, count);

  // Fill any shortfall from remaining pool
  if (final.length < count) {
    const used  = new Set(final.map((q) => q.id));
    const extra = shuffle(pool.filter((q) => !used.has(q.id)));
    final = [...final, ...extra].slice(0, count);
  }

  return NextResponse.json(
    final.map((q) => ({ ...q, stepByStep: JSON.parse(q.stepByStep ?? '[]') })),
  );
}

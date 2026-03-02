import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/diagnostic?topicId=&difficulty=Medium&exclude=id1,id2
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId   = searchParams.get('topicId');
  const difficulty = searchParams.get('difficulty') ?? 'Medium';
  const excludeRaw = searchParams.get('exclude') ?? '';
  const excludeIds = excludeRaw ? excludeRaw.split(',').filter(Boolean) : [];

  if (!topicId) {
    return NextResponse.json({ error: 'topicId required' }, { status: 400 });
  }

  // Fetch a pool of candidates, then randomly select one so each session gets different questions
  let pool = await prisma.question.findMany({
    where: {
      topicId,
      difficulty: difficulty as 'Easy' | 'Medium' | 'Hard',
      id: { notIn: excludeIds },
    },
    take: 80,
  });

  // Fallback to any difficulty in this topic
  if (!pool.length) {
    pool = await prisma.question.findMany({
      where: { topicId, id: { notIn: excludeIds } },
      take: 80,
    });
  }

  if (!pool.length) {
    return NextResponse.json({ error: 'No question found' }, { status: 404 });
  }

  const q = pool[Math.floor(Math.random() * pool.length)];
  return NextResponse.json({ ...q, stepByStep: JSON.parse(q.stepByStep ?? '[]') });
}

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

  // Try requested difficulty first
  let q = await prisma.question.findFirst({
    where: {
      topicId,
      difficulty: difficulty as 'Easy' | 'Medium' | 'Hard',
      id: { notIn: excludeIds },
    },
    orderBy: { id: 'asc' },
  });

  // Fallback to any difficulty in this topic
  if (!q) {
    q = await prisma.question.findFirst({
      where: { topicId, id: { notIn: excludeIds } },
      orderBy: { id: 'asc' },
    });
  }

  if (!q) {
    return NextResponse.json({ error: 'No question found' }, { status: 404 });
  }

  return NextResponse.json({ ...q, stepByStep: JSON.parse(q.stepByStep ?? '[]') });
}

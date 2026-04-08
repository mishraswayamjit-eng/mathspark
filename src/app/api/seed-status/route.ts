import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// GET /api/seed-status?secret=xxx
// Returns question counts per topic so you can verify the seed is complete.
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const [topicCounts, total] = await Promise.all([
    prisma.topic.findMany({
      select: {
        id: true,
        name: true,
        grade: true,
        _count: { select: { questions: true } },
      },
      orderBy: { grade: 'asc' },
    }),
    prisma.question.count(),
  ]);

  const topics = topicCounts.map((t) => ({
    id:    t.id,
    name:  t.name,
    grade: t.grade,
    count: t._count.questions,
  }));

  const empty = topics.filter((t) => t.count === 0);

  return NextResponse.json({
    total,
    topicCount: topics.length,
    topics,
    emptyTopics: empty,
    healthy: empty.length === 0 && total > 10000,
  });
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/mock-tests/history?studentId=&limit=&offset=
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const limit  = Math.min(Math.max(parseInt(searchParams.get('limit') ?? '50', 10) || 50, 1), 100);
  const offset = Math.max(parseInt(searchParams.get('offset') ?? '0', 10) || 0, 0);

  const tests = await prisma.mockTest.findMany({
    where: { studentId },
    orderBy: { startedAt: 'desc' },
    take: limit,
    skip: offset,
    select: {
      id: true, type: true, totalQuestions: true, timeLimitMs: true,
      startedAt: true, completedAt: true, score: true, accuracy: true, status: true,
    },
  });

  return NextResponse.json(tests);
}

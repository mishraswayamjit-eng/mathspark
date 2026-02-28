import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/mock-tests/history?studentId=
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const tests = await prisma.mockTest.findMany({
    where: { studentId },
    orderBy: { startedAt: 'desc' },
    select: {
      id: true, type: true, totalQuestions: true, timeLimitMs: true,
      startedAt: true, completedAt: true, score: true, accuracy: true, status: true,
      _count: { select: { responses: true } },
    },
  });

  return NextResponse.json(tests);
}

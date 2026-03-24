import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

// GET /api/mock-tests/history?limit=&offset=
export async function GET(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
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
  } catch (err) {
    console.error('[mock-tests/history]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

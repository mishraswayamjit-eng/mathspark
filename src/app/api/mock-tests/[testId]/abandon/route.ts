import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';

// POST /api/mock-tests/[testId]/abandon
// Ends an open test without a score, so the child can start a different one.
// Idempotent: a test that is already over is left exactly as it is.
export async function POST(
  _req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    if (!checkRateLimit(`mock-tests-abandon:${studentId}`, 20, 600_000)) {
      return NextResponse.json({ error: 'Too many requests. Try again in a moment.' }, { status: 429 });
    }

    const { testId } = params;
    const mockTest = await prisma.mockTest.findUnique({
      where: { id: testId },
      select: { studentId: true, status: true },
    });
    if (!mockTest) {
      return NextResponse.json({ error: 'Test not found' }, { status: 404 });
    }
    if (mockTest.studentId !== studentId) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    if (mockTest.status === 'in_progress') {
      // The status is in the filter too, so a test submitted at the same moment keeps its score.
      await prisma.mockTest.updateMany({
        where: { id: testId, studentId, status: 'in_progress' },
        data: { status: 'abandoned', completedAt: new Date() },
      });
    }
    return NextResponse.json({ ok: true });
  } catch (err) {
    logError('[mock-tests abandon]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { validateBody, ValidationError } from '@/lib/validateBody';

// PATCH /api/mock-tests/[testId]/response
// Body: { questionNumber, selectedAnswer?, flagged?, additionalTimeMs? }
export async function PATCH(
  req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { testId } = params;
    const { questionNumber, selectedAnswer, flagged, additionalTimeMs } = validateBody<{
      questionNumber: number;
      selectedAnswer?: string;
      flagged?: boolean;
      additionalTimeMs?: number;
    }>(
      await req.json(),
      { questionNumber: 'number', selectedAnswer: 'string?', flagged: 'boolean?', additionalTimeMs: 'number?' },
    );

    if (!questionNumber) {
      return NextResponse.json({ error: 'questionNumber required' }, { status: 400 });
    }

    // Verify test exists, is in progress, and belongs to student
    const mockTest = await prisma.mockTest.findUnique({
      where: { id: testId },
      select: { status: true, studentId: true },
    });
    if (!mockTest) {
      return NextResponse.json({ error: 'Test not found' }, { status: 404 });
    }
    if (mockTest.studentId !== studentId) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }
    if (mockTest.status !== 'in_progress') {
      return NextResponse.json({ error: 'Test already completed' }, { status: 409 });
    }

    // Build update data
    const updateData: Record<string, unknown> = {};
    if (selectedAnswer !== undefined) {
      updateData.selectedAnswer = selectedAnswer;
      updateData.answeredAt = new Date();
    }
    if (flagged !== undefined) {
      updateData.flagged = flagged;
    }
    // Validate questionNumber is a positive integer
    if (typeof questionNumber !== 'number' || questionNumber < 1) {
      return NextResponse.json({ error: 'Invalid questionNumber' }, { status: 400 });
    }

    // Split into two operations: regular fields + atomic time increment
    if (Object.keys(updateData).length > 0) {
      await prisma.mockTestResponse.updateMany({
        where: { mockTestId: testId, questionNumber },
        data: updateData,
      });
    }

    // Atomic time increment — avoids race condition with concurrent PATCHes
    if (additionalTimeMs !== undefined && additionalTimeMs > 0) {
      await prisma.mockTestResponse.updateMany({
        where: { mockTestId: testId, questionNumber },
        data: { timeTakenMs: { increment: additionalTimeMs } },
      });
    }

    return new Response(null, { status: 204 });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    console.error('[mock-tests PATCH response]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// PATCH /api/mock-tests/[testId]/response
// Body: { questionNumber, selectedAnswer?, flagged?, additionalTimeMs? }
export async function PATCH(
  req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const { testId } = params;
    const body = await req.json();
    const { questionNumber, selectedAnswer, flagged, additionalTimeMs } = body as {
      questionNumber: number;
      selectedAnswer?: string;
      flagged?: boolean;
      additionalTimeMs?: number;
    };

    if (!questionNumber) {
      return NextResponse.json({ error: 'questionNumber required' }, { status: 400 });
    }

    // Verify test exists and is in progress
    const mockTest = await prisma.mockTest.findUnique({
      where: { id: testId },
      select: { status: true },
    });
    if (!mockTest) {
      return NextResponse.json({ error: 'Test not found' }, { status: 404 });
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
    console.error('[mock-tests PATCH response]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

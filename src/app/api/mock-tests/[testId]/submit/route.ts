import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// POST /api/mock-tests/[testId]/submit
// Idempotent — re-submitting returns existing results
export async function POST(
  _req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const { testId } = params;

    const mockTest = await prisma.mockTest.findUnique({
      where: { id: testId },
      include: {
        responses: {
          include: {
            question: { select: { correctAnswer: true } },
          },
        },
        student: { select: { parentEmail: true, name: true } },
      },
    });

    if (!mockTest) {
      return NextResponse.json({ error: 'Test not found' }, { status: 404 });
    }

    // Idempotent: already completed
    if (mockTest.status === 'completed') {
      return NextResponse.json({ testId });
    }

    // Grade each response
    const graded = mockTest.responses.map((r) => ({
      id: r.id,
      isCorrect: r.selectedAnswer != null
        ? r.selectedAnswer === r.question.correctAnswer
        : false,
    }));

    // Compute score + accuracy
    const answered = graded.filter((r) => {
      const resp = mockTest.responses.find((x) => x.id === r.id);
      return resp?.selectedAnswer != null;
    });
    const correct  = graded.filter((r) => r.isCorrect).length;
    const accuracy = answered.length > 0 ? correct / answered.length : 0;

    // Update each response isCorrect in a transaction
    await prisma.$transaction([
      ...graded.map((r) =>
        prisma.mockTestResponse.update({
          where: { id: r.id },
          data:  { isCorrect: r.isCorrect },
        }),
      ),
      prisma.mockTest.update({
        where: { id: testId },
        data: {
          status:      'completed',
          score:       correct,
          accuracy,
          completedAt: new Date(),
        },
      }),
    ]);

    return NextResponse.json({ testId });
  } catch (err) {
    console.error('[mock-tests submit POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

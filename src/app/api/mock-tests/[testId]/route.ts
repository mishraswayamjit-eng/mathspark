import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/mock-tests/[testId]
export async function GET(
  _req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const { testId } = params;

    const mockTest = await prisma.mockTest.findUnique({
      where: { id: testId },
      include: {
        responses: {
          orderBy: { questionNumber: 'asc' },
          include: {
            question: {
              select: {
                id: true, topicId: true, subTopic: true, difficulty: true,
                questionText: true, questionLatex: true,
                option1: true, option2: true, option3: true, option4: true,
                correctAnswer: true,
                hint1: true, hint2: true, hint3: true,
                stepByStep: true,
                misconceptionA: true, misconceptionB: true,
                misconceptionC: true, misconceptionD: true,
                source: true,
              },
            },
          },
        },
      },
    });

    if (!mockTest) {
      return NextResponse.json({ error: 'Test not found' }, { status: 404 });
    }

    // Parse stepByStep JSON for each question
    const result = {
      ...mockTest,
      responses: mockTest.responses.map((r) => ({
        ...r,
        question: r.question
          ? { ...r.question, stepByStep: JSON.parse(r.question.stepByStep ?? '[]') }
          : undefined,
      })),
    };

    return NextResponse.json(result);
  } catch (err) {
    console.error('[mock-tests GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

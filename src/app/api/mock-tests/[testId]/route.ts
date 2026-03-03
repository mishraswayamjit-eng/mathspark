import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

function safeParseSteps(json: string | null): unknown[] {
  try { return JSON.parse(json ?? '[]'); } catch { return []; }
}

// GET /api/mock-tests/[testId]?studentId=xxx
export async function GET(
  req: Request,
  { params }: { params: { testId: string } },
) {
  try {
    const { testId } = params;
    const { searchParams } = new URL(req.url);
    const requestingStudentId = searchParams.get('studentId');

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

    // Auth: verify requesting student owns this test
    if (requestingStudentId && mockTest.studentId !== requestingStudentId) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const result = {
      ...mockTest,
      responses: mockTest.responses.map((r) => ({
        ...r,
        question: r.question
          ? { ...r.question, stepByStep: safeParseSteps(r.question.stepByStep) }
          : undefined,
      })),
    };

    return NextResponse.json(result);
  } catch (err) {
    console.error('[mock-tests GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

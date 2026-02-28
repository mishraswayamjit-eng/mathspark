import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { generateMockPaper } from '@/lib/mockTest';
import type { TestType, PYQYear } from '@/types';

// POST /api/mock-tests
// Body: { studentId, type, topicIds?, year? }
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { studentId, type, topicIds, year } = body as {
      studentId: string;
      type: TestType;
      topicIds?: string[];
      year?: PYQYear;
    };

    if (!studentId || !type) {
      return NextResponse.json({ error: 'studentId and type required' }, { status: 400 });
    }

    if (!['quick', 'half', 'full', 'ipm', 'pyq'].includes(type)) {
      return NextResponse.json({ error: 'Invalid test type' }, { status: 400 });
    }

    if (type === 'pyq' && !year) {
      return NextResponse.json({ error: 'year required for pyq type' }, { status: 400 });
    }

    // Check for existing in-progress test
    const existing = await prisma.mockTest.findFirst({
      where: { studentId, status: 'in_progress' },
      orderBy: { startedAt: 'desc' },
    });
    if (existing) {
      return NextResponse.json({ testId: existing.id, resumed: true });
    }

    // Generate paper
    const paper = await generateMockPaper(studentId, type, topicIds, year);

    // Create MockTest + all responses
    const mockTest = await prisma.mockTest.create({
      data: {
        studentId,
        type,
        totalQuestions: paper.questions.length,
        timeLimitMs: paper.timeLimitMs,
        status: 'in_progress',
        responses: {
          createMany: {
            data: paper.questions.map((q, idx) => ({
              questionId: q.id,
              questionNumber: idx + 1,
            })),
          },
        },
      },
    });

    return NextResponse.json({ testId: mockTest.id, resumed: false });
  } catch (err) {
    console.error('[mock-tests POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { generateMockPaper, generateMegaTest } from '@/lib/mockTest';
import type { TestType, PYQYear } from '@/types';

// POST /api/mock-tests
// Body: { studentId, type, topicIds?, year? }
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { studentId, type, topicIds, year, grade } = body as {
      studentId: string;
      type: TestType;
      topicIds?: string[];
      year?: PYQYear;
      grade?: number;
    };

    if (!studentId || !type) {
      return NextResponse.json({ error: 'studentId and type required' }, { status: 400 });
    }
    if (typeof studentId !== 'string' || studentId.length > 30) {
      return NextResponse.json({ error: 'Invalid studentId' }, { status: 400 });
    }
    if (typeof type !== 'string' || !['quick', 'half', 'full', 'ipm', 'pyq', 'mega'].includes(type)) {
      return NextResponse.json({ error: 'Invalid test type' }, { status: 400 });
    }
    if (topicIds && (!Array.isArray(topicIds) || topicIds.some((t: unknown) => typeof t !== 'string' || (t as string).length > 30))) {
      return NextResponse.json({ error: 'Invalid topicIds' }, { status: 400 });
    }
    if (grade !== undefined && (typeof grade !== 'number' || grade < 2 || grade > 9)) {
      return NextResponse.json({ error: 'Invalid grade' }, { status: 400 });
    }

    if (type === 'pyq' && !year) {
      return NextResponse.json({ error: 'year required for pyq type' }, { status: 400 });
    }

    // Validate studentId exists
    const student = await prisma.student.findUnique({
      where: { id: studentId },
      select: { id: true, grade: true },
    });
    if (!student) {
      return NextResponse.json({ error: 'Student not found' }, { status: 404 });
    }

    // Validate mega grade range
    const effectiveGrade = grade ?? (topicIds?.[0]?.startsWith('grade') ? parseInt(topicIds[0].replace('grade', ''), 10) : student.grade) ?? 4;
    if (type === 'mega' && (effectiveGrade < 2 || effectiveGrade > 9)) {
      return NextResponse.json({ error: 'Invalid grade for mega test (must be 2-9)' }, { status: 400 });
    }

    // Check for existing in-progress test (inside serializable transaction to prevent race)
    const result = await prisma.$transaction(async (tx) => {
      const existing = await tx.mockTest.findFirst({
        where: { studentId, status: 'in_progress' },
        orderBy: { startedAt: 'desc' },
      });
      if (existing) {
        return { testId: existing.id, resumed: true };
      }

      // Generate paper — mega uses its own generator
      const paper = type === 'mega'
        ? await generateMegaTest(studentId, effectiveGrade)
        : await generateMockPaper(studentId, type, topicIds, year, student.grade);

      if (paper.questions.length === 0) {
        throw new Error('Insufficient questions to generate test');
      }

      // Create MockTest + all responses atomically
      const mockTest = await tx.mockTest.create({
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

      return { testId: mockTest.id, resumed: false };
    });

    return NextResponse.json(result);
  } catch (err) {
    console.error('[mock-tests POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

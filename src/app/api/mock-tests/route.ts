import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { generateMockPaper, generateMegaTest } from '@/lib/mockTest';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import type { TestType, PYQYear } from '@/types';

// POST /api/mock-tests
// Body: { type, topicIds?, year?, grade? }
export async function POST(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Rate limit: 5 test creations per 10 minutes per student
    if (!checkRateLimit(`mock-tests:${studentId}`, 5, 600_000)) {
      return NextResponse.json({ error: 'Too many tests created. Try again later.' }, { status: 429 });
    }

    const { type, topicIds, year, grade } = validateBody<{
      type: TestType;
      topicIds?: string[];
      year?: PYQYear;
      grade?: number;
    }>(
      await req.json(),
      { type: 'string', topicIds: 'array?', year: 'number?', grade: 'number?' },
    );

    if (!type) {
      return NextResponse.json({ error: 'type required' }, { status: 400 });
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

    // Check for existing in-progress test first (fast, no heavy lock)
    const existing = await prisma.mockTest.findFirst({
      where: { studentId, status: 'in_progress' },
      orderBy: { startedAt: 'desc' },
      select: { id: true },
    });
    if (existing) {
      return NextResponse.json({ testId: existing.id, resumed: true });
    }

    // Generate paper OUTSIDE the transaction — these run multiple DB queries
    // and would cause lock contention / timeouts inside a transaction
    const paper = type === 'mega'
      ? await generateMegaTest(studentId, effectiveGrade)
      : await generateMockPaper(studentId, type, topicIds, year, student.grade);

    if (paper.questions.length === 0) {
      console.error(`[mock-tests POST] 0 questions for type=${type} grade=${effectiveGrade} student=${studentId}`);
      return NextResponse.json({ error: 'Not enough questions available for this test type. Please try a different test.' }, { status: 500 });
    }

    // Create MockTest + responses atomically (lightweight — just inserts)
    const result = await prisma.$transaction(async (tx) => {
      // Re-check inside transaction to prevent race between concurrent requests
      const existingInTx = await tx.mockTest.findFirst({
        where: { studentId, status: 'in_progress' },
        select: { id: true },
      });
      if (existingInTx) {
        return { testId: existingInTx.id, resumed: true };
      }

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
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    console.error('[mock-tests POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';

const AttemptsSchema = z.object({
  studentId:   z.string().min(1),
  questionId:  z.string().min(1),
  topicId:     z.string().min(1),
  selected:    z.enum(['A', 'B', 'C', 'D']),
  hintUsed:    z.number().int().min(0).max(3).default(0),
  timeTakenMs: z.number().int().min(0).default(0),
});

// POST /api/attempts
// body: { studentId, questionId, topicId, selected, hintUsed?, timeTakenMs? }
// isCorrect is computed server-side — NOT accepted from the client
export async function POST(req: Request) {
  try {
    const parsed = AttemptsSchema.safeParse(await req.json());
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }
    const { studentId, questionId, topicId, selected, hintUsed, timeTakenMs } = parsed.data;

    const question = await prisma.question.findUnique({
      where: { id: questionId },
      select: { correctAnswer: true },
    });
    if (!question) {
      return NextResponse.json({ error: 'Question not found' }, { status: 404 });
    }

    const isCorrect = selected === question.correctAnswer;

    const attempt = await prisma.attempt.create({
      data: { studentId, questionId, selected, isCorrect, hintUsed, timeTakenMs },
    });

    // Recalculate + persist mastery
    await updateProgress(studentId, topicId);

    return NextResponse.json(attempt, { status: 201 });
  } catch (err) {
    console.error('[POST /api/attempts]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

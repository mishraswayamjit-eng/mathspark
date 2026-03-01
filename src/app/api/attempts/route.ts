import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';

// POST /api/attempts
// body: { studentId, questionId, topicId, selected, isCorrect, hintUsed?, timeTakenMs? }
export async function POST(req: Request) {
  const body = await req.json();
  const {
    studentId, questionId, topicId, selected, isCorrect,
    hintUsed = 0, timeTakenMs = 0, misconceptionType = null,
    isBonusQuestion = false, parentQuestionId = null,
  } = body;

  if (!studentId || !questionId || !topicId || !selected) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  const attempt = await prisma.attempt.create({
    data: {
      studentId, questionId, selected, isCorrect,
      hintUsed, timeTakenMs, misconceptionType,
      isBonusQuestion, parentQuestionId,
    },
  });

  // Recalculate + persist mastery
  await updateProgress(studentId, topicId);

  return NextResponse.json(attempt, { status: 201 });
}

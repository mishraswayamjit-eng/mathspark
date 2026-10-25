import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';

// POST /api/questions/preview/check
// Server-side grading for preview questions (landing page HeroDemo).
// Body: { questionId: string, selected: string }
export async function POST(req: Request) {
  try {
    const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
    if (!checkRateLimit(`preview-check:${ip}`, 20, 60_000)) {
      return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }

    const { questionId, selected } = await req.json();

    if (!questionId || typeof questionId !== 'string') {
      return NextResponse.json({ error: 'questionId required' }, { status: 400 });
    }
    if (!selected || !['A', 'B', 'C', 'D'].includes(selected)) {
      return NextResponse.json({ error: 'selected must be A, B, C, or D' }, { status: 400 });
    }

    // Scope to the exact pool the public preview endpoint serves. Using
    // findFirst with the same filter means this unauthenticated grader can only
    // reveal answers for the handful of hand-crafted Medium preview questions,
    // not enumerate the entire 6k-question answer key by guessing ids.
    const question = await prisma.question.findFirst({
      where: { id: questionId, difficulty: 'Medium', source: 'hand_crafted' },
      select: { correctAnswer: true },
    });

    if (!question) {
      return NextResponse.json({ error: 'Question not found' }, { status: 404 });
    }

    const isCorrect = selected === question.correctAnswer;

    return NextResponse.json({
      isCorrect,
      correctAnswer: question.correctAnswer,
    });
  } catch {
    return NextResponse.json({ error: 'Check failed' }, { status: 500 });
  }
}

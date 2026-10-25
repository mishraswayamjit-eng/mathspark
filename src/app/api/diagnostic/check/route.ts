import { NextResponse } from 'next/server';
import { prisma, USABLE_QUESTION_FILTER } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';

// POST /api/diagnostic/check
// Server-side grading for diagnostic questions (onboarding quiz).
// Body: { questionId: string, selected: string }
export async function POST(req: Request) {
  try {
    const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
    if (!checkRateLimit(`diagnostic-check:${ip}`, 20, 60_000)) {
      return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }

    const { questionId, selected } = await req.json();

    if (!questionId || typeof questionId !== 'string') {
      return NextResponse.json({ error: 'questionId required' }, { status: 400 });
    }
    if (!selected || !['A', 'B', 'C', 'D'].includes(selected)) {
      return NextResponse.json({ error: 'selected must be A, B, C, or D' }, { status: 400 });
    }

    // Scope to the usable question pool the diagnostic endpoint actually serves.
    // findFirst with the shared filter means this unauthenticated grader can only
    // reveal answers for real, servable questions keyed by a known id — it can't
    // be used to dump the whole answer key by brute-forcing arbitrary ids.
    const question = await prisma.question.findFirst({
      where: { id: questionId, ...USABLE_QUESTION_FILTER },
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

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
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

    const question = await prisma.question.findUnique({
      where: { id: questionId },
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

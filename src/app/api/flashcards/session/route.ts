import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

/**
 * POST /api/flashcards/session
 * Body: { studentId, mode, cardsReviewed, cardsCorrect, duration }
 *
 * Records a completed flashcard session.
 */
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { studentId, mode, cardsReviewed, cardsCorrect, duration } = body as {
      studentId?: string;
      mode?: string;
      cardsReviewed?: number;
      cardsCorrect?: number;
      duration?: number;
    };

    if (!studentId || !mode || cardsReviewed == null) {
      return NextResponse.json(
        { error: 'studentId, mode, and cardsReviewed required' },
        { status: 400 },
      );
    }

    const session = await prisma.flashcardSession.create({
      data: {
        studentId,
        mode,
        cardsReviewed,
        cardsCorrect: cardsCorrect ?? 0,
        duration: duration ?? 0,
        xpEarned: 0,
      },
    });

    return NextResponse.json({ ok: true, sessionId: session.id });
  } catch (err) {
    console.error('[flashcards/session] Error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

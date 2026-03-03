import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// Leitner box → review interval in days
const BOX_INTERVALS = [0, 1, 2, 5, 14, 30]; // index 0 unused; box 1→1d, box 2→2d, etc.

/**
 * POST /api/flashcards/progress
 * Body: { studentId, cardId, correct: boolean }
 *
 * Updates Leitner box state for one card:
 *   correct → box = min(box + 1, 5), streak++
 *   wrong   → box = 1, streak = 0
 * Sets nextReviewAt = now + BOX_INTERVALS[newBox] days
 */
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { studentId, cardId, correct } = body as {
      studentId?: string;
      cardId?: string;
      correct?: boolean;
    };

    if (!studentId || !cardId || typeof correct !== 'boolean') {
      return NextResponse.json(
        { error: 'studentId, cardId, and correct (boolean) required' },
        { status: 400 },
      );
    }

    const now = new Date();

    // Fetch existing progress (if any)
    const existing = await prisma.flashcardProgress.findUnique({
      where: { studentId_cardId: { studentId, cardId } },
    });

    const oldBox = existing?.leitnerBox ?? 1;
    const newBox = correct ? Math.min(oldBox + 1, 5) : 1;
    const intervalDays = BOX_INTERVALS[newBox] ?? 1;
    const nextReviewAt = new Date(now.getTime() + intervalDays * 86_400_000);

    const streak = correct ? (existing?.streakOnCard ?? 0) + 1 : 0;

    const progress = await prisma.flashcardProgress.upsert({
      where: { studentId_cardId: { studentId, cardId } },
      create: {
        studentId,
        cardId,
        leitnerBox: newBox,
        nextReviewAt,
        timesSeen: 1,
        timesCorrect: correct ? 1 : 0,
        lastSeenAt: now,
        streakOnCard: streak,
      },
      update: {
        leitnerBox: newBox,
        nextReviewAt,
        timesSeen: { increment: 1 },
        timesCorrect: correct ? { increment: 1 } : undefined,
        lastSeenAt: now,
        streakOnCard: streak,
      },
    });

    return NextResponse.json({
      ok: true,
      leitnerBox: progress.leitnerBox,
      nextReviewAt: progress.nextReviewAt,
      streakOnCard: progress.streakOnCard,
    });
  } catch (err) {
    console.error('[flashcards/progress] Error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

/**
 * POST /api/flashcards/progress/session
 * Body: { studentId, mode, cardsReviewed, cardsCorrect, duration }
 *
 * Records a completed flashcard session.
 * (Kept as a separate function but same route file for simplicity.)
 */

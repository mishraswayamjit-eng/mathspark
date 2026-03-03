import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { computeCardXP } from '@/lib/flashcardXP';

export const dynamic = 'force-dynamic';

// Leitner box → review interval in days
const BOX_INTERVALS = [0, 1, 2, 5, 14, 30]; // index 0 unused; box 1→1d, box 2→2d, etc.

const BOX_NAMES = ['', 'Rookie', 'Rising', 'Strong', 'Expert', 'Master'];

/**
 * POST /api/flashcards/progress
 * Body: { studentId, cardId, correct: boolean }
 *
 * Updates Leitner box state for one card:
 *   correct → box = min(box + 1, 5), streak++
 *   wrong   → box = 1, streak = 0
 * Sets nextReviewAt = now + BOX_INTERVALS[newBox] days
 *
 * Returns oldBox, newBox, leveledUp, milestone flags for client celebrations.
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

    const wasNew = !existing;
    const oldBox = existing?.leitnerBox ?? 0; // 0 = never seen
    const newBox = correct ? Math.min(Math.max(oldBox, 1) + 1, 5) : 1;
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

    // Detect level-up and milestones
    const leveledUp = correct && newBox > oldBox && oldBox > 0;
    const reachedMastery = newBox === 5 && oldBox < 5;
    const reachedStrong = newBox >= 3 && oldBox < 3;

    // Compute XP for this card
    const cardXP = computeCardXP(correct, leveledUp, reachedMastery, reachedStrong);

    return NextResponse.json({
      ok: true,
      oldBox,
      newBox: progress.leitnerBox,
      oldBoxName: BOX_NAMES[oldBox] ?? '',
      newBoxName: BOX_NAMES[newBox] ?? '',
      leveledUp,
      reachedMastery,
      reachedStrong,
      wasNew,
      nextReviewAt: progress.nextReviewAt,
      streakOnCard: progress.streakOnCard,
      xpEarned: cardXP.xp,
      xpBreakdown: cardXP.breakdown,
    });
  } catch (err) {
    console.error('[flashcards/progress] Error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

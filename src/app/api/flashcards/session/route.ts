import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { computeSessionXP, getAchievedMilestone, getMilestoneProgress } from '@/lib/flashcardXP';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { validateBody, ValidationError } from '@/lib/validateBody';

export const dynamic = 'force-dynamic';

/**
 * POST /api/flashcards/session
 * Body: { mode, cardsReviewed, cardsCorrect, duration }
 */
export async function POST(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = validateBody<{ mode?: string; cardsReviewed?: number; cardsCorrect?: number; duration?: number; bonusXP?: number }>(
      await req.json(),
      { mode: 'string?', cardsReviewed: 'number?', cardsCorrect: 'number?', duration: 'number?' },
    );
    const { mode, cardsReviewed, cardsCorrect, duration } = body;

    if (!mode || cardsReviewed == null) {
      return NextResponse.json(
        { error: 'mode and cardsReviewed required' },
        { status: 400 },
      );
    }
    if (typeof mode !== 'string' || mode.length > 30) {
      return NextResponse.json({ error: 'Invalid mode' }, { status: 400 });
    }
    if (typeof cardsReviewed !== 'number' || cardsReviewed < 0 || cardsReviewed > 1000) {
      return NextResponse.json({ error: 'Invalid cardsReviewed' }, { status: 400 });
    }

    // ── Compute study streak for XP multiplier ───────────────────────────
    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);

    // Single query: fetch all session dates in last 365 days
    const cutoff = new Date(todayStart);
    cutoff.setDate(cutoff.getDate() - 365);
    const sessions = await prisma.flashcardSession.findMany({
      where: { studentId, createdAt: { gte: cutoff } },
      select: { createdAt: true },
      orderBy: { createdAt: 'desc' },
    });

    // Build set of unique date keys
    const datesWithSessions = new Set(
      sessions.map((s) => {
        const d = new Date(s.createdAt);
        return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
      }),
    );

    // Walk backwards from today counting consecutive days
    let dailyStreak = 0;
    const day = new Date(todayStart);
    for (let i = 0; i < 365; i++) {
      const key = `${day.getFullYear()}-${day.getMonth()}-${day.getDate()}`;
      // For today (i=0), count this session as contributing
      if (datesWithSessions.has(key) || i === 0) {
        dailyStreak++;
        day.setDate(day.getDate() - 1);
      } else {
        break;
      }
    }

    // ── Compute session XP ───────────────────────────────────────────────
    const bonusXP = body.bonusXP ?? 0; // accumulated per-card bonuses from level-ups
    const { totalXP, baseXP, streakMultiplier, streakBonus } = computeSessionXP(
      cardsCorrect ?? 0,
      cardsReviewed,
      dailyStreak,
      bonusXP,
    );

    // Check streak milestone
    const achievedMilestone = getAchievedMilestone(dailyStreak);
    const milestoneXP = achievedMilestone?.xpBonus ?? 0;
    const finalXP = totalXP + milestoneXP;

    const session = await prisma.flashcardSession.create({
      data: {
        studentId,
        mode,
        cardsReviewed,
        cardsCorrect: cardsCorrect ?? 0,
        duration: duration ?? 0,
        xpEarned: finalXP,
      },
    });

    // ── Update student's lifetime XP ─────────────────────────────────────
    try {
      await prisma.student.update({
        where: { id: studentId },
        data: { totalLifetimeXP: { increment: finalXP } },
      });
    } catch (err) {
      console.error('[flashcards/session] XP update failed:', err);
    }

    const milestoneProgress = getMilestoneProgress(dailyStreak);

    return NextResponse.json({
      ok: true,
      sessionId: session.id,
      xp: {
        total: finalXP,
        base: baseXP,
        streakMultiplier,
        streakBonus,
        milestoneBonus: milestoneXP,
      },
      streak: {
        days: dailyStreak,
        achievedMilestone: achievedMilestone ?? null,
        nextMilestone: milestoneProgress.milestone,
        progress: milestoneProgress.progress,
      },
    });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    console.error('[flashcards/session] Error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

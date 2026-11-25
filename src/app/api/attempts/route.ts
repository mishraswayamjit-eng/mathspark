import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';
import { computeXPForAttempt, ensureCurrentWeekLeague } from '@/lib/leaderboard';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateInteractiveAnswer } from '@/lib/interactiveGrading';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { istDayStart, usageDayKey } from '@/lib/sharedUtils';

/** XP for a right answer on a question already tried earlier the same day. */
const REVIEW_XP = 10;

// POST /api/attempts
// body: { questionId, topicId, selected, isCorrect, hintUsed?, timeTakenMs?, isBonusQuestion? }
export async function POST(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Rate limit: 60 attempts per minute per student
    if (!checkRateLimit(`attempts:${studentId}`, 60, 60_000)) {
      return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }

    let rawBody: unknown;
    try {
      rawBody = await req.json();
    } catch {
      return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
    }

    const body = validateBody<{
      questionId: string; topicId: string; selected: string; isCorrect: boolean;
      hintUsed?: number; timeTakenMs?: number; misconceptionType?: string;
      isBonusQuestion?: boolean; parentQuestionId?: string;
      interactiveAnswer?: string;
    }>(rawBody, {
      questionId: 'string', topicId: 'string', selected: 'string', isCorrect: 'boolean',
      hintUsed: 'number?', timeTakenMs: 'number?', misconceptionType: 'string?',
      isBonusQuestion: 'boolean?', parentQuestionId: 'string?',
      interactiveAnswer: 'string?',
    });

    const {
      questionId, topicId, selected,
      hintUsed = 0, misconceptionType = null,
      isBonusQuestion = false, parentQuestionId = null,
      interactiveAnswer,
    } = body;

    // Time on the question as the client measured it. Stored for analytics
    // (the mastery "speed" figure) ONLY: the XP decision below uses the
    // server's own timer. Kept to a whole number of milliseconds between 0 and
    // 10 minutes so an odd value can never fail the insert; 0 means "not known".
    const rawTimeMs = body.timeTakenMs;
    const timeTakenMs =
      typeof rawTimeMs === 'number' && isFinite(rawTimeMs)
        ? Math.min(600_000, Math.max(0, Math.round(rawTimeMs)))
        : 0;

    if (questionId.length > 50) {
      return NextResponse.json({ error: 'Invalid questionId' }, { status: 400 });
    }
    if (topicId.length > 30) {
      return NextResponse.json({ error: 'Invalid topicId' }, { status: 400 });
    }
    if (!['A', 'B', 'C', 'D'].includes(selected)) {
      return NextResponse.json({ error: 'Invalid selected' }, { status: 400 });
    }
    if (interactiveAnswer !== undefined && interactiveAnswer.length > 300) {
      return NextResponse.json({ error: 'Invalid interactiveAnswer' }, { status: 400 });
    }

    // Server-side grading: look up the correct answer and override client's isCorrect
    const question = await prisma.question.findUnique({
      where: { id: questionId },
      select: { correctAnswer: true, interactionType: true, interactionData: true, topicId: true },
    });
    if (!question) {
      return NextResponse.json({ error: 'Question not found' }, { status: 404 });
    }
    // Interactive questions: grade what the child actually built/tapped/dragged
    // (`interactiveAnswer`, a JSON string). `selected` stays an A-D letter for the
    // attempt record. MCQ: compare selected === correctAnswer.
    const serverIsCorrect = question.interactionType
      ? validateInteractiveAnswer(question.interactionType, question.interactionData, interactiveAnswer ?? selected)
      : selected === question.correctAnswer;

    // The daily log (XP cap, question count) is keyed on the India-time day.
    const today = usageDayKey();

    // Resolve the student's current-week league membership BEFORE the main tx.
    // `ensureCurrentWeekLeague` does its own writes (membership row + maybe league
    // row creation), so threading it inside `prisma.$transaction` would risk
    // a long-running transaction holding row locks. Instead, we resolve the
    // membership id up-front, then the main tx atomically writes attempt +
    // usageLog + leagueMembership.weeklyXP + student.totalLifetimeXP together.
    const membership = await ensureCurrentWeekLeague(studentId).catch((err) => {
      // League ensure failures should not block recording the attempt — log and
      // continue without weekly XP. The attempt + usageLog still record cleanly.
      logError('[attempts] ensureCurrentWeekLeague failed:', err);
      return null;
    });

    // The start of today in India, for the "second try today" rule below.
    const indiaDayStart = istDayStart(new Date());

    // ── Atomic core: create attempt + count daily usage + cap XP + league/lifetime XP ─
    const { attempt, xpAwarded } = await prisma.$transaction(async (tx) => {
      // Validate student exists
      const student = await tx.student.findUnique({ where: { id: studentId }, select: { id: true } });
      if (!student) throw new Error('Student not found');

      const created = await tx.attempt.create({
        data: {
          studentId, questionId, selected, isCorrect: serverIsCorrect,
          hintUsed, timeTakenMs, misconceptionType,
          isBonusQuestion, parentQuestionId,
        },
      });

      await tx.usageLog.upsert({
        where:  { studentId_date: { studentId, date: today } },
        update: { questionsAttempted: { increment: 1 } },
        create: { studentId, date: today, questionsAttempted: 1 },
      });

      // The upsert above locks this student's row for today, so from here on
      // the student's attempts are handled one at a time: a second request that
      // arrived together with this one waits there until this one is committed,
      // and then sees this attempt in the two reads below. Read before that
      // point, two simultaneous requests could each miss the other.

      // Server-authoritative anti-tap timer: time since the student's PREVIOUS
      // recorded attempt, not the client-supplied `timeTakenMs` (which a script
      // can forge to dodge the 3s XP gate). First-ever attempt → undefined →
      // full credit. The client value is still stored on the row for analytics.
      const previous = await tx.attempt.findFirst({
        where:   { studentId, id: { not: created.id } },
        orderBy: { createdAt: 'desc' },
        select:  { createdAt: true },
      });
      const serverElapsedMs = previous ? created.createdAt.getTime() - previous.createdAt.getTime() : undefined;

      // A second try at the same question on the same India-time day (the review
      // round, "review mistakes") comes after the correct answer has been shown,
      // so it earns the review amount, not the full amount. Worked out from the
      // recorded attempts: the client is not asked.
      const sameQuestionToday = await tx.attempt.count({
        where: { studentId, questionId, createdAt: { gte: indiaDayStart } },
      });
      const isRepeatToday = sameQuestionToday > 1;

      // Compute and atomically cap daily XP within the same transaction
      const fullXP = computeXPForAttempt(serverIsCorrect, isBonusQuestion, serverElapsedMs);
      const rawXP = isRepeatToday ? Math.min(fullXP, REVIEW_XP) : fullXP;
      let awarded = 0;

      if (rawXP > 0) {
        const todayLog = await tx.usageLog.findUnique({
          where:  { studentId_date: { studentId, date: today } },
          select: { xpEarned: true },
        });
        const xpToday  = todayLog?.xpEarned ?? 0;
        const xpActual = Math.min(rawXP, Math.max(0, 500 - xpToday));

        if (xpActual > 0) {
          await tx.usageLog.update({
            where: { studentId_date: { studentId, date: today } },
            data:  { xpEarned: { increment: xpActual } },
          });
          // League weeklyXP + student totalLifetimeXP increment in the same tx so
          // a partial failure can't leave usageLog incremented but the league
          // standing untouched (or vice versa).
          if (membership) {
            await tx.leagueMembership.update({
              where: { id: membership.id },
              data:  { weeklyXP: { increment: xpActual } },
            });
          }
          await tx.student.update({
            where: { id: studentId },
            data:  { totalLifetimeXP: { increment: xpActual } },
          });
          awarded = xpActual;
        }
      }

      return { attempt: created, xpAwarded: awarded };
    });

    // ── Progress update — fire-and-forget (safe if it lags; idempotent) ────────
    // Use the question's REAL server-side topicId (not the client-supplied
    // `topicId`) so a forged body can never recompute mastery against a topic
    // the question doesn't belong to.
    updateProgress(studentId, question.topicId).catch((err) =>
      logError('[attempts] progress update failed:', err),
    );

    return NextResponse.json({ ...attempt, xpAwarded }, { status: 201 });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    logError('[attempts] POST failed:', err);
    return NextResponse.json({ error: 'Could not record attempt' }, { status: 500 });
  }
}

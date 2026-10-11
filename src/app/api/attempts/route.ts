import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';
import { computeXPForAttempt, ensureCurrentWeekLeague } from '@/lib/leaderboard';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateInteractiveAnswer } from '@/lib/interactiveGrading';
import { logError } from '@/lib/logger';

// POST /api/attempts
// body: { questionId, topicId, selected, isCorrect, hintUsed?, timeTakenMs?, isBonusQuestion? }
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limit: 60 attempts per minute per student
  if (!checkRateLimit(`attempts:${studentId}`, 60, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  const body = await req.json();
  const {
    questionId, topicId, selected, isCorrect,
    hintUsed = 0, timeTakenMs = 0, misconceptionType = null,
    isBonusQuestion = false, parentQuestionId = null,
  } = body;

  if (!questionId || !topicId || !selected) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }
  if (typeof questionId !== 'string' || questionId.length > 50) {
    return NextResponse.json({ error: 'Invalid questionId' }, { status: 400 });
  }
  if (typeof topicId !== 'string' || topicId.length > 30) {
    return NextResponse.json({ error: 'Invalid topicId' }, { status: 400 });
  }
  if (typeof selected !== 'string' || !['A', 'B', 'C', 'D'].includes(selected)) {
    return NextResponse.json({ error: 'Invalid selected' }, { status: 400 });
  }
  if (typeof isCorrect !== 'boolean') {
    return NextResponse.json({ error: 'Invalid isCorrect' }, { status: 400 });
  }

  // Server-side grading: look up the correct answer and override client's isCorrect
  const question = await prisma.question.findUnique({
    where: { id: questionId },
    select: { correctAnswer: true, interactionType: true, interactionData: true },
  });
  if (!question) {
    return NextResponse.json({ error: 'Question not found' }, { status: 404 });
  }
  // Interactive questions: validate via interactiveGrading; MCQ: compare selected === correctAnswer
  const serverIsCorrect = question.interactionType
    ? validateInteractiveAnswer(question.interactionType, question.interactionData, selected)
    : selected === question.correctAnswer;

  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);

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

    // Compute and atomically cap daily XP within the same transaction
    const rawXP = computeXPForAttempt(serverIsCorrect, isBonusQuestion, timeTakenMs);
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
  updateProgress(studentId, topicId).catch((err) =>
    logError('[attempts] progress update failed:', err),
  );

  return NextResponse.json({ ...attempt, xpAwarded }, { status: 201 });
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';
import { computeXPForAttempt, ensureCurrentWeekLeague } from '@/lib/leaderboard';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';

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
    select: { correctAnswer: true },
  });
  if (!question) {
    return NextResponse.json({ error: 'Question not found' }, { status: 404 });
  }
  const serverIsCorrect = selected === question.correctAnswer;

  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);

  // ── Atomic core: create attempt + count daily usage + cap XP ──────────────
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
        awarded = xpActual;
      }
    }

    return { attempt: created, xpAwarded: awarded };
  }).catch((err) => {
    if ((err as Error).message === 'Student not found') throw err;
    throw err;
  });

  // ── Progress update — fire-and-forget (safe if it lags; idempotent) ────────
  updateProgress(studentId, topicId).catch((err) =>
    console.error('[attempts] progress update failed:', err),
  );

  // ── League + lifetime XP — fire-and-forget (usageLog already updated above) ─
  if (xpAwarded > 0) {
    ensureCurrentWeekLeague(studentId)
      .then((membership) =>
        Promise.all([
          prisma.leagueMembership.update({
            where: { id: membership.id },
            data:  { weeklyXP: { increment: xpAwarded } },
          }),
          prisma.student.update({
            where: { id: studentId },
            data:  { totalLifetimeXP: { increment: xpAwarded } },
          }),
        ]),
      )
      .catch((err) => console.error('[attempts] league XP award failed:', err));
  }

  return NextResponse.json({ ...attempt, xpAwarded }, { status: 201 });
}

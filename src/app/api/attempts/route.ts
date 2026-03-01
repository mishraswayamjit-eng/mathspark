import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';
import { computeXPForAttempt, addWeeklyXP } from '@/lib/leaderboard';

// POST /api/attempts
// body: { studentId, questionId, topicId, selected, isCorrect, hintUsed?, timeTakenMs?, isBonusQuestion? }
export async function POST(req: Request) {
  const body = await req.json();
  const {
    studentId, questionId, topicId, selected, isCorrect,
    hintUsed = 0, timeTakenMs = 0, misconceptionType = null,
    isBonusQuestion = false, parentQuestionId = null,
  } = body;

  if (!studentId || !questionId || !topicId || !selected) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);

  const [attempt] = await Promise.all([
    prisma.attempt.create({
      data: {
        studentId, questionId, selected, isCorrect,
        hintUsed, timeTakenMs, misconceptionType,
        isBonusQuestion, parentQuestionId,
      },
    }),
    prisma.usageLog.upsert({
      where:  { studentId_date: { studentId, date: today } },
      update: { questionsAttempted: { increment: 1 } },
      create: { studentId, date: today, questionsAttempted: 1 },
    }),
    updateProgress(studentId, topicId),
  ]);

  // ── XP tracking ───────────────────────────────────────────────────────────
  const rawXP = computeXPForAttempt(isCorrect, isBonusQuestion, timeTakenMs);
  let xpAwarded = 0;

  if (rawXP > 0) {
    // Check daily XP cap (500/day)
    const todayLog = await prisma.usageLog.findUnique({
      where:  { studentId_date: { studentId, date: today } },
      select: { xpEarned: true },
    });
    const xpToday  = todayLog?.xpEarned ?? 0;
    const xpActual = Math.min(rawXP, Math.max(0, 500 - xpToday));
    if (xpActual > 0) {
      await addWeeklyXP(studentId, xpActual);
      xpAwarded = xpActual;
    }
  }

  return NextResponse.json({ ...attempt, xpAwarded }, { status: 201 });
}

export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { addWeeklyXP } from '@/lib/leaderboard';
import { logError } from '@/lib/logger';
import { LESSON_TOPICS } from '@/data/lessonTopics';

// GET — return all lesson progress for the authenticated student
export async function GET() {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const progress = await prisma.lessonProgress.findMany({
    where: { studentId },
    select: {
      topicSlug: true,
      levelId: true,
      quizScore: true,
      durationSec: true,
      completedAt: true,
    },
  });

  return NextResponse.json({ progress });
}

// POST — upsert lesson progress (keeps highest score)
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`lesson-progress:${studentId}`, 10, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  try {
    const body = validateBody<{
      topicSlug: string;
      levelId: number;
      quizScore: number;
      durationSec: number;
    }>(await req.json(), {
      topicSlug: 'string',
      levelId: 'number',
      quizScore: 'number',
      durationSec: 'number',
    });

    const { topicSlug, levelId } = body;

    // The topic must be a real concept lesson. Every lesson has levels 1 to 5
    // (data/lessons/*.json), so a whole number in that range is a real level.
    let knownTopic = false;
    for (let i = 0; i < LESSON_TOPICS.length; i++) {
      if (LESSON_TOPICS[i].id === topicSlug) { knownTopic = true; break; }
    }
    if (!knownTopic) {
      return NextResponse.json({ error: 'Unknown lesson topic' }, { status: 400 });
    }
    if (!Number.isInteger(levelId) || levelId < 1 || levelId > 5) {
      return NextResponse.json({ error: 'levelId must be a whole number from 1 to 5' }, { status: 400 });
    }
    if (!Number.isFinite(body.quizScore) || body.quizScore < 0 || body.quizScore > 100) {
      return NextResponse.json({ error: 'quizScore must be 0-100' }, { status: 400 });
    }
    const quizScore = Math.round(body.quizScore);
    const durationSec = Number.isFinite(body.durationSec)
      ? Math.min(86_400, Math.max(0, Math.round(body.durationSec)))
      : 0;

    // Check if this is a first-time completion
    const existing = await prisma.lessonProgress.findUnique({
      where: {
        studentId_topicSlug_levelId: { studentId, topicSlug, levelId },
      },
      select: { quizScore: true },
    });

    const isFirstTime = !existing;
    const isPerfect = quizScore === 100;

    // Upsert — keep highest score
    const progress = await prisma.lessonProgress.upsert({
      where: {
        studentId_topicSlug_levelId: { studentId, topicSlug, levelId },
      },
      create: {
        studentId,
        topicSlug,
        levelId,
        quizScore,
        durationSec,
      },
      update: {
        quizScore: existing && existing.quizScore > quizScore
          ? existing.quizScore
          : quizScore,
        durationSec,
        completedAt: new Date(),
      },
    });

    // XP calculation. A level pays once: in full the first time it is finished,
    // and after that only for the part of the score that is better than the
    // best so far. Doing the same quiz again for the same (or a lower) score
    // earns nothing, so a level can never pay more than one perfect first go.
    // (The score itself is still the one the quiz screen worked out.)
    const bonusFor = (score: number) => Math.round((score / 100) * 30); // 0-30
    let base = 0;
    let scoreBonus = 0;
    let firstTimeBonus = 0;
    let perfectBonus = 0;
    if (isFirstTime) {
      base = 20;
      scoreBonus = bonusFor(quizScore);
      firstTimeBonus = 20;
      perfectBonus = isPerfect ? 15 : 0;
    } else if (existing && quizScore > existing.quizScore) {
      scoreBonus = Math.max(0, bonusFor(quizScore) - bonusFor(existing.quizScore));
      perfectBonus = isPerfect ? 15 : 0;
    }
    const totalXP = base + scoreBonus + firstTimeBonus + perfectBonus;

    if (totalXP > 0) await addWeeklyXP(studentId, totalXP);

    return NextResponse.json({
      ok: true,
      progress: {
        topicSlug: progress.topicSlug,
        levelId: progress.levelId,
        quizScore: progress.quizScore,
      },
      xp: { total: totalXP, base, scoreBonus, firstTimeBonus, perfectBonus },
    });
  } catch (e) {
    if (e instanceof ValidationError) {
      return NextResponse.json({ error: e.message }, { status: 400 });
    }
    logError('POST /api/lessons/progress error:', e);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { addWeeklyXP } from '@/lib/leaderboard';

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

    const { topicSlug, levelId, quizScore, durationSec } = body;

    // Validate ranges
    if (levelId < 1 || levelId > 5) {
      return NextResponse.json({ error: 'levelId must be 1-5' }, { status: 400 });
    }
    if (quizScore < 0 || quizScore > 100) {
      return NextResponse.json({ error: 'quizScore must be 0-100' }, { status: 400 });
    }

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

    // XP calculation
    const base = 20;
    const scoreBonus = Math.round((quizScore / 100) * 30); // 0-30
    const firstTimeBonus = isFirstTime ? 20 : 0;
    const perfectBonus = isPerfect ? 15 : 0;
    const totalXP = base + scoreBonus + firstTimeBonus + perfectBonus;

    await addWeeklyXP(studentId, totalXP);

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
    console.error('POST /api/lessons/progress error:', e);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';
import { teachFor } from '@/lib/teach/lookup';

/**
 * GET /api/teach/[questionId]
 *
 * The "Explain it to me" lesson for one question: `{ questionId, beats }`.
 * 404 when no lesson has been written for it.
 *
 * A lesson walks through the whole solution, so it is refused (403) while the
 * question is part of a mock test this student still has in progress.
 *
 * GET /api/teach/[questionId]?check=1
 *
 * The light version a screen uses to decide whether to offer the lesson:
 * `{ questionId, available }`, never the lesson itself. `available` is false
 * both when there is no lesson and when a test in progress holds it back.
 *
 * Lessons are written and checked offline. Nothing is generated here, and
 * nothing here touches grading, XP or mastery.
 */
export async function GET(
  req: Request,
  { params }: { params: { questionId: string } },
) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // One check and one lesson per question, so this is generous for real use.
  if (!checkRateLimit(`teach:${studentId}`, 120, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  const questionId = typeof params.questionId === 'string' ? params.questionId : '';
  const checkOnly = new URL(req.url).searchParams.get('check') === '1';

  const lesson = questionId ? teachFor(questionId) : undefined;
  if (!lesson) {
    if (checkOnly) return NextResponse.json({ questionId, available: false });
    return NextResponse.json({ error: 'No lesson for this question' }, { status: 404 });
  }

  try {
    // Is this question sitting in a test the student has not finished?
    const inOpenTest = await prisma.mockTestResponse.findFirst({
      where: {
        questionId,
        mockTest: { studentId, status: 'in_progress' },
      },
      select: { id: true },
    });

    if (inOpenTest) {
      if (checkOnly) return NextResponse.json({ questionId, available: false });
      return NextResponse.json({ error: 'This question is part of a test in progress' }, { status: 403 });
    }

    if (checkOnly) return NextResponse.json({ questionId, available: true });
    return NextResponse.json({ questionId, beats: lesson.beats });
  } catch (err) {
    logError('[teach GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

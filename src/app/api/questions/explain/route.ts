import { NextResponse } from 'next/server';
import { prisma, USABLE_QUESTION_FILTER, aiSourceFilter } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { parseUnknownArray } from '@/lib/jsonFields';
import { matchesSubTopicKey } from '@/lib/sharedUtils';
import { logError } from '@/lib/logger';
import { withVisual } from '@/lib/figures/lookup';
import { hasTeachScript } from '@/lib/teach/lookup';

export const dynamic = 'force-dynamic';

/** A test left open this long after its time ran out no longer counts as in progress. */
const TEST_GRACE_MS = 10 * 60_000;

/**
 * GET /api/questions/explain?questionId=&topicId=&subTopic=
 *
 * One given question, in exactly the shape /api/questions/next sends, so the
 * practice screen can open on it with its "Explain it to me" lesson
 * (the `teach` link from the next-best-action card).
 *
 * It is sent only when ALL of these hold; otherwise the answer is 404 and the
 * screen carries on with ordinary practice:
 *   - a lesson has been written for the question;
 *   - the question is usable, its source is switched on, and it belongs to the
 *     topic (and the sub-topic, when one is given) the screen is practising;
 *   - this student has already attempted it (the link is only ever made for a
 *     question the child missed, so this route cannot be used to look up
 *     questions the child has never been shown);
 *   - the student has no test in progress.
 *
 * Read-only. Nothing here touches grading, XP or mastery, and no model is called.
 */
export async function GET(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    if (!checkRateLimit(`questions-explain:${studentId}`, 30, 60_000)) {
      return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }

    const { searchParams } = new URL(req.url);
    const questionId = searchParams.get('questionId') ?? '';
    const topicId    = searchParams.get('topicId') ?? '';
    const subTopic   = searchParams.get('subTopic') ?? '';

    if (!questionId || !topicId) {
      return NextResponse.json({ error: 'questionId and topicId required' }, { status: 400 });
    }
    if (questionId.length > 50 || topicId.length > 30 || subTopic.length > 100) {
      return NextResponse.json({ error: 'Invalid parameter length' }, { status: 400 });
    }

    const notAvailable = () =>
      NextResponse.json({ error: 'Question not available' }, { status: 404 });

    if (!hasTeachScript(questionId)) return notAvailable();

    const [question, attempted, openTests] = await Promise.all([
      prisma.question.findFirst({
        where: { id: questionId, topicId, ...USABLE_QUESTION_FILTER, ...aiSourceFilter() },
      }),
      prisma.attempt.findFirst({
        where: { studentId, questionId },
        select: { id: true },
      }),
      prisma.mockTest.findMany({
        where: { studentId, status: 'in_progress' },
        select: {
          startedAt: true,
          timeLimitMs: true,
          responses: { where: { questionId }, select: { id: true }, take: 1 },
        },
        orderBy: { startedAt: 'desc' },
        take: 10,
      }),
    ]);

    if (!question || !attempted) return notAvailable();
    if (subTopic && !matchesSubTopicKey(question.subTopic, subTopic)) return notAvailable();

    const nowMs = Date.now();
    for (let i = 0; i < openTests.length; i++) {
      const t = openTests[i];
      // The question sits in an unfinished test (the lesson route would hold it back too).
      if (t.responses.length > 0) return notAvailable();
      // A test is running right now: nothing is explained meanwhile.
      if (nowMs < new Date(t.startedAt).getTime() + t.timeLimitMs + TEST_GRACE_MS) return notAvailable();
    }

    const stepByStep = parseUnknownArray(question.stepByStep);
    // Same payload as /api/questions/next (correctAnswer included for the same
    // reason: practice marks the answer on the spot, and /api/attempts re-grades
    // on the server, so XP, mastery and progress never depend on this value).
    return NextResponse.json(withVisual({ ...question, stepByStep }, { withSolution: true }));
  } catch (err) {
    logError('[questions/explain] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { parseUnknownArray } from '@/lib/jsonFields';
import { withVisual } from '@/lib/figures/lookup';
import { isLlmConfigured } from '@/lib/llm/client';
import { isBoardCoachEnabled } from '@/lib/llm/featureFlags';
import { askBoardCoach, type BoardCoachQuestion } from '@/lib/llm/boardCoach';

export const dynamic = 'force-dynamic';
// NOTE: ignored on Vercel Hobby (10s hard limit); the model call gives up at 9s.
export const maxDuration = 30;

/**
 * POST /api/coach/board: the live board coach.
 *
 * Body: { questionId, image, spoken?, lastSay?, asked? }
 *   image    base64 JPEG of the pencil pad, no data-URL prefix
 *   spoken   how many remarks the coach has made on this question so far
 *   lastSay  its last remark, so it does not repeat itself
 *   asked    true when the child pressed "Check my working"
 * Reply: { status, say, quiet }. When `quiet` is true the client says nothing.
 *
 * Coaching only: nothing here reads or writes XP, mastery or grading, and the
 * picture is neither logged nor stored.
 */

// Looks per student. The client asks at most once every 12 seconds and 6 times
// a question; these are the server's own ceilings.
const PER_MINUTE = 6;
const PER_DAY = 150;
const PER_QUESTION = 10;
const PER_QUESTION_WINDOW_MS = 30 * 60_000;

// The client sends a JPEG about 1000px on its longest side (roughly 50-200 KB).
// Anything much larger is not from the pad.
const MAX_IMAGE_BASE64_CHARS = 1_500_000;
const MIN_IMAGE_BASE64_CHARS = 200;
const MAX_QUESTION_ID_CHARS = 100;
const MAX_LAST_SAY_CHARS = 300;
const MAX_SPOKEN = 50;

function quietJson(status: number, error: string): Response {
  return Response.json({ error }, { status });
}

export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) return quietJson(401, 'Unauthorized');

  // Kill switch, and no key: 503 tells the pad to stop asking for this visit.
  if (!isBoardCoachEnabled() || !isLlmConfigured()) {
    return quietJson(503, 'The board coach is not available.');
  }

  if (!checkRateLimit(`coach-board:${studentId}`, PER_MINUTE, 60_000)
    || !checkRateLimit(`coach-board-day:${studentId}`, PER_DAY, 24 * 60 * 60_000)) {
    return quietJson(429, 'Sparky is resting for a moment.');
  }

  let questionId: string;
  let image: string;
  let spoken = 0;
  let lastSay = '';
  let asked = false;
  try {
    const parsed = validateBody<{
      questionId: string; image: string; spoken?: number; lastSay?: string; asked?: boolean;
    }>(
      await req.json(),
      { questionId: 'string', image: 'string', spoken: 'number?', lastSay: 'string?', asked: 'boolean?' },
    );
    questionId = parsed.questionId.trim();
    image = parsed.image;
    if (typeof parsed.spoken === 'number' && Number.isFinite(parsed.spoken)) {
      spoken = Math.min(MAX_SPOKEN, Math.max(0, Math.floor(parsed.spoken)));
    }
    if (typeof parsed.lastSay === 'string') lastSay = parsed.lastSay.slice(0, MAX_LAST_SAY_CHARS);
    asked = parsed.asked === true;
  } catch (err) {
    if (err instanceof ValidationError) return quietJson(400, err.message);
    return quietJson(400, 'Invalid request body');
  }

  if (!questionId || questionId.length > MAX_QUESTION_ID_CHARS) {
    return quietJson(400, 'questionId required');
  }
  // A JPEG, as plain base64: the right length, the right alphabet, and the JPEG
  // signature (FF D8 FF, which is "/9j/" in base64).
  if (image.length < MIN_IMAGE_BASE64_CHARS || image.length > MAX_IMAGE_BASE64_CHARS
    || image.indexOf('/9j/') !== 0 || !/^[A-Za-z0-9+/]+=*$/.test(image)) {
    return quietJson(400, 'That picture of the pad could not be used.');
  }

  if (!checkRateLimit(`coach-board-q:${studentId}:${questionId}`, PER_QUESTION, PER_QUESTION_WINDOW_MS)) {
    return quietJson(429, 'Sparky has had enough looks at this one.');
  }

  try {
    const [inTest, row, student] = await Promise.all([
      // No coaching on a question that is part of a test this student is sitting.
      prisma.mockTestResponse.findFirst({
        where: { questionId, mockTest: { studentId, status: 'in_progress' } },
        select: { id: true },
      }),
      prisma.question.findUnique({
        where: { id: questionId },
        select: {
          id: true, questionText: true, questionLatex: true,
          option1: true, option2: true, option3: true, option4: true,
          correctAnswer: true, stepByStep: true,
        },
      }),
      prisma.student.findUnique({ where: { id: studentId }, select: { grade: true } }),
    ]);

    if (inTest) return quietJson(403, 'The board coach is not available during a test.');
    if (!row) return quietJson(404, 'Question not found');

    // Parse the steps first, so the corrected ones can replace them.
    const steps: { text: string; latex?: string }[] = [];
    const rawSteps = parseUnknownArray(row.stepByStep);
    for (let i = 0; i < rawSteps.length; i++) {
      const s = rawSteps[i];
      if (!s || typeof s !== 'object') continue;
      const o = s as Record<string, unknown>;
      if (typeof o.text !== 'string') continue;
      steps.push(typeof o.latex === 'string' ? { text: o.text, latex: o.latex } : { text: o.text });
    }
    const fixed = withVisual({ ...row, stepByStep: steps }, { withSolution: true });

    const question: BoardCoachQuestion = {
      questionText: fixed.questionText,
      questionLatex: fixed.questionLatex,
      option1: fixed.option1,
      option2: fixed.option2,
      option3: fixed.option3,
      option4: fixed.option4,
      correctAnswer: fixed.correctAnswer,
      steps: Array.isArray(fixed.stepByStep) ? fixed.stepByStep : steps,
    };

    const reply = await askBoardCoach(question, image, {
      grade: student ? student.grade : 5,
      spoken,
      lastSay,
      asked,
    });
    return Response.json(reply, { headers: { 'Cache-Control': 'no-store' } });
  } catch (err) {
    // Status and name only: never the request, which carries the picture.
    const e = err as { status?: number; name?: string };
    logError(`[coach/board] could not coach: ${e && e.name ? e.name : 'unknown'} ${e && e.status ? e.status : ''}`);
    return quietJson(502, 'Sparky could not have a look just now.');
  }
}

import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { parseUnknownArray } from '@/lib/jsonFields';
import { isLlmConfigured } from '@/lib/llm/client';
import { streamCompletion } from '@/lib/llm/complete';
import { kidSafeRules, gradeDescriptor } from '@/lib/llm/guardrails';
import { buildGroundedUserPrompt } from '@/lib/llm/grounding';

export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/**
 * POST /api/ai/stuck-coach
 * Body: { questionId }
 *
 * Streams Socratic coaching for a student who is stuck (2nd wrong attempt on
 * the same question). Grounded in the verified `stepByStep` — it guides toward
 * the next step WITHOUT ever stating the final answer (withholdFinalAnswer).
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`ai-stuck-coach:${studentId}`, 20, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }

  let questionId: string;
  try {
    const parsed = validateBody<{ questionId: string }>(await req.json(), {
      questionId: 'string',
    });
    questionId = parsed.questionId;
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!isLlmConfigured()) {
    return Response.json({ error: 'AI coach is not configured.' }, { status: 503 });
  }

  const [student, question] = await Promise.all([
    prisma.student.findUnique({ where: { id: studentId }, select: { grade: true } }),
    prisma.question.findUnique({
      where: { id: questionId },
      select: { questionText: true, stepByStep: true },
    }),
  ]);

  if (!question) {
    return Response.json({ error: 'Question not found' }, { status: 404 });
  }

  const grade = student?.grade ?? 4;

  // Extract verified step text (grounding) without leaking the final answer.
  // We drop the last step, which typically states the answer outright.
  const steps = parseUnknownArray(question.stepByStep)
    .map((s) => {
      if (!s || typeof s !== 'object') return '';
      const obj = s as { text?: unknown; latex?: unknown };
      const text = typeof obj.text === 'string' ? obj.text : '';
      const latex = typeof obj.latex === 'string' ? obj.latex : '';
      return latex ? `${text} (${latex})` : text;
    })
    .filter((t) => t.length > 0);

  const groundingSteps = steps.length > 1 ? steps.slice(0, -1) : steps;

  const system = `You are Sparky, a warm, patient math tutor for a ${gradeDescriptor(grade)}. The student has tried this question twice and is stuck. Coach them Socratically: point at ONE small next step or ask ONE guiding question that nudges their thinking forward. Never reveal the final answer — the goal is for them to get there themselves.

${kidSafeRules(grade)}

Keep it to 2-3 short sentences. Warm, encouraging, never discouraging. End with a gentle "you've got this" style line.`;

  const userPrompt = buildGroundedUserPrompt({
    task: 'Give the stuck student ONE small Socratic nudge toward the next step. Do not state the final answer.',
    questionText: question.questionText,
    verifiedSteps: groundingSteps,
    withholdFinalAnswer: true,
  });

  const stream = streamCompletion(
    {
      model: 'sonnet',
      maxTokens: 400,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    },
    {
      onErrorFallback:
        "I'm having a little trouble right now! 🤔 Try the hints below, or look at the first step and take it one piece at a time.",
      onError: (err) => logError('[ai/stuck-coach] stream error', err),
    },
  );

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-cache',
    },
  });
}

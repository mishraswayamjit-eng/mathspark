import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { findLesson } from '@/lib/lessonData';
import { isLlmConfigured } from '@/lib/llm/client';
import { streamCompletion } from '@/lib/llm/complete';
import { kidSafeRules, gradeDescriptor } from '@/lib/llm/guardrails';
import { buildGroundedUserPrompt } from '@/lib/llm/grounding';

export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/**
 * POST /api/ai/lesson-reexplain
 * Body: { topicSlug, levelId, lessonId }
 *
 * Streams a simpler re-explanation of a verified lesson for a confused student.
 * Grounded in the lesson JSON — never invents new math.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`ai-reexplain:${studentId}`, 15, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }

  let topicSlug: string;
  let levelId: number;
  let lessonId: string;
  try {
    const parsed = validateBody<{ topicSlug: string; levelId: number; lessonId: string }>(
      await req.json(),
      { topicSlug: 'string', levelId: 'number', lessonId: 'string' },
    );
    topicSlug = parsed.topicSlug;
    levelId = parsed.levelId;
    lessonId = parsed.lessonId;
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  const found = findLesson(topicSlug, levelId, lessonId);
  if (!found) {
    return Response.json({ error: 'Lesson not found' }, { status: 404 });
  }

  if (!isLlmConfigured()) {
    return Response.json({ error: 'AI explainer is not configured.' }, { status: 503 });
  }

  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true },
  });
  const grade = student?.grade ?? found.topic.gradeRange[0] ?? 4;

  const { topic, lesson } = found;

  // Build the verified lesson content as grounding context.
  const lessonContent = [
    `Lesson title: ${lesson.title}`,
    `Intro: ${lesson.intro}`,
    ...(lesson.explanation?.length ? [`Explanation: ${lesson.explanation.join(' ')}`] : []),
    ...(lesson.steps?.length
      ? [`Steps:\n${lesson.steps.map((s, i) => `${i + 1}. ${s.text}${s.notation ? ` (${s.notation})` : ''}`).join('\n')}`]
      : []),
    ...(lesson.rule ? [`Rule: ${lesson.rule}`] : []),
    ...(lesson.tip ? [`Tip: ${lesson.tip}`] : []),
  ].join('\n');

  const system = `You are Sparky, a warm math tutor for a ${gradeDescriptor(grade)}. The student said they are confused by the "${topic.topic}" lesson below. Re-explain the SAME idea in a simpler, friendlier way, using ONE fresh everyday analogy and very small steps. Do NOT introduce any new math facts beyond what the lesson covers.

${kidSafeRules(grade)}

Keep it short — a few short sentences or a tiny bullet list. End with a gentle encouraging line.`;

  const userPrompt = buildGroundedUserPrompt({
    task: 'Re-explain this lesson simply for a confused student, grounded only in the content below.',
    context: lessonContent,
  });

  const stream = streamCompletion(
    {
      model: 'sonnet',
      maxTokens: 350,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    },
    {
      onErrorFallback: "I'm having a little trouble explaining right now! 🤔 Try reading the steps above once more, or ask Sparky in Chat.",
      onError: (err) => logError('[ai/lesson-reexplain] stream error', err),
    },
  );

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-cache',
    },
  });
}

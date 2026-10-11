import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { complete } from '@/lib/llm/complete';
import { kidSafeRules, gradeDescriptor } from '@/lib/llm/guardrails';
import { buildGroundedUserPrompt } from '@/lib/llm/grounding';
import { getOrCreateExplanation } from '@/lib/llm/cache';
import { MODELS } from '@/lib/llm/models';
import type { AnswerKey } from '@/types';

export const dynamic = 'force-dynamic';

/**
 * POST /api/ai/misconception
 * Body: { questionId, selected }
 *
 * Returns a warm 1–2 line personalized nudge that re-expresses the verified
 * `misconception{X}` text for the option the child chose. Cache-first. Returns
 * `{ nudge: null }` on any failure so the client falls back to the static box.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`ai-misconception:${studentId}`, 20, 60_000)) {
    return NextResponse.json({ nudge: null }, { status: 200 });
  }

  let questionId: string;
  let selected: AnswerKey;
  try {
    const parsed = validateBody<{ questionId: string; selected: string }>(
      await req.json(),
      { questionId: 'string', selected: 'string' },
    );
    questionId = parsed.questionId;
    if (!['A', 'B', 'C', 'D'].includes(parsed.selected)) {
      return NextResponse.json({ error: 'selected must be A|B|C|D' }, { status: 400 });
    }
    selected = parsed.selected as AnswerKey;
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  // If the key is missing, tell the client to use the static floor immediately.
  if (!isLlmConfigured()) {
    return NextResponse.json({ nudge: null });
  }

  const [student, question] = await Promise.all([
    prisma.student.findUnique({ where: { id: studentId }, select: { grade: true } }),
    prisma.question.findUnique({
      where: { id: questionId },
      select: {
        questionText: true,
        misconceptionA: true,
        misconceptionB: true,
        misconceptionC: true,
        misconceptionD: true,
      },
    }),
  ]);

  if (!student || !question) {
    return NextResponse.json({ nudge: null });
  }

  const misconceptionMap: Record<AnswerKey, string> = {
    A: question.misconceptionA,
    B: question.misconceptionB,
    C: question.misconceptionC,
    D: question.misconceptionD,
  };
  const verifiedMisconception = misconceptionMap[selected]?.trim();

  // No verified misconception text → nothing to ground on; use static floor.
  if (!verifiedMisconception) {
    return NextResponse.json({ nudge: null });
  }

  const grade = student.grade;

  const result = await getOrCreateExplanation({
    feature: 'misconception',
    refId: questionId,
    variant: selected,
    grade,
    generate: async () => {
      const system = `You are Sparky, a warm math tutor for a ${gradeDescriptor(grade)}. A student just picked a wrong answer. Turn the "common mistake" note below into ONE or TWO short, warm sentences that gently help them see WHERE their thinking slipped — without ever stating the correct answer.

${kidSafeRules(grade)}

Keep it to 2 sentences max. Do not include the correct answer or a full solution.`;

      const userPrompt = buildGroundedUserPrompt({
        task: 'Rewrite the common-mistake note as a warm 1–2 line nudge for the child.',
        questionText: question.questionText,
        context: `Common mistake for the option they chose: ${verifiedMisconception}`,
        withholdFinalAnswer: true,
      });

      const { text } = await complete({
        model: 'haiku',
        maxTokens: 120,
        system,
        messages: [{ role: 'user', content: userPrompt }],
      });

      return { content: text.trim(), model: MODELS.haiku };
    },
  });

  if (!result) {
    return NextResponse.json({ nudge: null });
  }

  return NextResponse.json({ nudge: result.content, cached: result.cached });
}

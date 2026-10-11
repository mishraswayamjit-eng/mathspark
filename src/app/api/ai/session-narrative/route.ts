import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { isLlmConfigured } from '@/lib/llm/client';
import { complete } from '@/lib/llm/complete';
import { kidSafeRules, gradeDescriptor, sanitizePromptText } from '@/lib/llm/guardrails';
import { buildGroundedUserPrompt } from '@/lib/llm/grounding';
import { MODELS } from '@/lib/llm/models';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

interface ResultItem {
  wasCorrect: boolean;
  questionText?: string;
}

/**
 * POST /api/ai/session-narrative
 * Body: { topicName?, results: QuestionResult[] }
 *
 * Returns a warm 2-sentence summary addressed to the CHILD, grounded in the
 * session's correct/total count. Delivery-only (never grades). Returns
 * `{ narrative: null }` on any failure so the UI simply omits it.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`ai-session:${studentId}`, 10, 60_000)) {
    return NextResponse.json({ narrative: null });
  }

  let topicName: string;
  let rawResults: unknown;
  try {
    const parsed = validateBody<{ topicName?: string; results: unknown[] }>(
      await req.json(),
      { topicName: 'string?', results: 'array' },
    );
    topicName = parsed.topicName ?? '';
    rawResults = parsed.results;
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!isLlmConfigured()) {
    return NextResponse.json({ narrative: null });
  }

  const results = (rawResults as unknown[])
    .filter((r): r is ResultItem => !!r && typeof r === 'object' && typeof (r as ResultItem).wasCorrect === 'boolean')
    .slice(0, 50);

  if (results.length === 0) {
    return NextResponse.json({ narrative: null });
  }

  const total = results.length;
  const correct = results.filter((r) => r.wasCorrect).length;

  try {
    const student = await prisma.student.findUnique({
      where: { id: studentId },
      select: { name: true, grade: true },
    });
    if (!student) return NextResponse.json({ narrative: null });

    const grade = student.grade;
    const safeTopic = sanitizePromptText(topicName, 80);

    const system = `You are Sparky, a warm math tutor for a ${gradeDescriptor(grade)}. The student just finished a short practice session. Celebrate their effort in exactly 2 short, upbeat sentences, then (if they missed some) gently encourage them to keep going. Address the child directly by name. Never scold.

${kidSafeRules(grade)}`;

    const userPrompt = buildGroundedUserPrompt({
      task: 'Write a 2-sentence encouraging session wrap-up for the child.',
      context: [
        `Child's name: ${sanitizePromptText(student.name, 50)}`,
        safeTopic ? `Topic practiced: ${safeTopic}` : '',
        `They got ${correct} out of ${total} correct this session.`,
      ].filter(Boolean).join('\n'),
      withholdFinalAnswer: true,
    });

    const { text } = await complete({
      model: 'haiku',
      maxTokens: 120,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    });

    const narrative = text.trim();
    return NextResponse.json({ narrative: narrative || null });
  } catch (err) {
    logError('[ai/session-narrative] generation failed', err);
    return NextResponse.json({ narrative: null });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { isAiSolveEnabled } from '@/lib/llm/featureFlags';
import { checkAndIncrementUsage } from '@/lib/llm/usage';
import { solveGrounded, solveFresh } from '@/lib/llm/solve';

export const dynamic = 'force-dynamic';
export const maxDuration = 60;

/**
 * POST /api/solve  (Feature 5a — gated by AI_SOLVE_ENABLED)
 * Body: { questionId?, problemText? }
 *
 *  - questionId  → grounded re-expression of the verified DB answer.
 *  - problemText → fresh homework solve via self-consistency + disclaimer.
 *
 * Usage-gated (shared daily AI budget) + rate-limited. Every solve is audited
 * in AiSolveLog. Fresh solves never touch graded practice.
 */
export async function POST(req: Request) {
  if (!isAiSolveEnabled()) {
    return NextResponse.json({ error: 'Solve is not available right now.' }, { status: 403 });
  }

  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`ai-solve:${studentId}`, 10, 60_000)) {
    return NextResponse.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }

  if (!isLlmConfigured()) {
    return NextResponse.json({ error: 'Solve is not configured.' }, { status: 503 });
  }

  let questionId: string | undefined;
  let problemText: string | undefined;
  try {
    const parsed = validateBody<{ questionId?: string; problemText?: string }>(
      await req.json(),
      { questionId: 'string?', problemText: 'string?' },
    );
    questionId = parsed.questionId?.trim() || undefined;
    problemText = parsed.problemText?.trim() || undefined;
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!questionId && !problemText) {
    return NextResponse.json({ error: 'Provide a questionId or problemText.' }, { status: 400 });
  }

  // Count this against the shared daily AI budget.
  const usage = await checkAndIncrementUsage(studentId, 'solve');
  if (!usage.allowed) {
    return NextResponse.json(
      { error: "You've used all your AI help for today — come back tomorrow! 🌙" },
      { status: 429 },
    );
  }

  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { grade: true },
  });
  const grade = student?.grade ?? 4;

  try {
    const result = questionId
      ? await solveGrounded(questionId, grade)
      : await solveFresh(problemText as string, grade);

    if (!result) {
      return NextResponse.json({ error: 'Question not found.' }, { status: 404 });
    }

    // Audit trail (best-effort — never block the response on logging).
    prisma.aiSolveLog
      .create({
        data: {
          studentId,
          path: result.path,
          input: questionId ?? (problemText as string).slice(0, 1000),
          answer: result.answer.slice(0, 500),
          agreement: result.agreement,
          model: result.model,
          flagged: result.flagged,
        },
      })
      .catch((err) => logError('[solve] audit log', err));

    return NextResponse.json({
      explanation: result.explanation,
      path: result.path,
      flagged: result.flagged,
      remaining: Number.isFinite(usage.remaining) ? usage.remaining : undefined,
    });
  } catch (err) {
    logError('[solve] generation failed', err);
    return NextResponse.json(
      { error: "I couldn't work this one out — try asking Sparky in Chat!" },
      { status: 502 },
    );
  }
}

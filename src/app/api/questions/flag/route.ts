import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const FlagSchema = z.object({
  questionId: z.string().min(1),
  studentId:  z.string().min(1),
  reason:     z.enum(['wrong_answer', 'confusing', 'too_hard', 'other']).default('other'),
});

// POST /api/questions/flag
export async function POST(req: Request) {
  try {
    const parsed = FlagSchema.safeParse(await req.json());
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }
    const { questionId, studentId, reason } = parsed.data;

    // Store as a simple Attempt-like record — we don't have a Flag model,
    // so log it to console for now (admin can grep logs).
    // This is intentionally lightweight — no DB schema change needed.
    console.log(JSON.stringify({
      type: 'question_flag',
      questionId,
      studentId,
      reason,
      ts: new Date().toISOString(),
    }));

    // Also verify the question exists
    const question = await prisma.question.findUnique({
      where: { id: questionId },
      select: { id: true },
    });
    if (!question) {
      return NextResponse.json({ error: 'Question not found' }, { status: 404 });
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[POST /api/questions/flag]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

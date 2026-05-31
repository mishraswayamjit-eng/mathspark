import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const ResetBodySchema = z.object({
  studentId: z.string().min(1),
});

// POST /api/progress/reset
// body: { studentId: string }
// Deletes all Progress records and Attempt records for the student
export async function POST(req: Request) {
  try {
    const body = await req.json();

    const parsed = ResetBodySchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { studentId } = parsed.data;

    await prisma.attempt.deleteMany({ where: { studentId } });
    await prisma.progress.deleteMany({ where: { studentId } });

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[POST /api/progress/reset]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

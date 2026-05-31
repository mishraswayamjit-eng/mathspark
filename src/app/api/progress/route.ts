import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const ProgressQuerySchema = z.object({
  studentId: z.string().min(1),
});

// GET /api/progress?studentId=xxx
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);

    const parsed = ProgressQuerySchema.safeParse({
      studentId: searchParams.get('studentId') ?? undefined,
    });

    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { studentId } = parsed.data;

    const progress = await prisma.progress.findMany({
      where: { studentId },
      include: { topic: { select: { name: true } } },
    });

    const progressWithNames = progress.map((p) => ({
      ...p,
      topicName: p.topic?.name ?? p.topicId,
    }));

    return NextResponse.json(progressWithNames);
  } catch (err) {
    console.error('[GET /api/progress]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

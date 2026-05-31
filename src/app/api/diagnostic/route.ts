import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const DiagnosticQuerySchema = z.object({
  topicId:    z.string().min(1),
  difficulty: z.enum(['Easy', 'Medium', 'Hard']).default('Medium'),
  exclude:    z.string().optional(),  // comma-separated IDs, parse after validation
});

// GET /api/diagnostic?topicId=&difficulty=Medium&exclude=id1,id2
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);

    const parsed = DiagnosticQuerySchema.safeParse({
      topicId:    searchParams.get('topicId') ?? undefined,
      difficulty: searchParams.get('difficulty') ?? undefined,
      exclude:    searchParams.get('exclude') ?? undefined,
    });

    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { topicId, difficulty, exclude } = parsed.data;
    const excludeIds = exclude ? exclude.split(',').filter(Boolean) : [];

    // Try requested difficulty first
    let q = await prisma.question.findFirst({
      where: {
        topicId,
        difficulty,
        id: { notIn: excludeIds },
      },
      orderBy: { id: 'asc' },
    });

    // Fallback to any difficulty in this topic
    if (!q) {
      q = await prisma.question.findFirst({
        where: { topicId, id: { notIn: excludeIds } },
        orderBy: { id: 'asc' },
      });
    }

    if (!q) {
      return NextResponse.json({ error: 'No question found' }, { status: 404 });
    }

    return NextResponse.json({ ...q, stepByStep: JSON.parse(q.stepByStep ?? '[]') });
  } catch (err) {
    console.error('[GET /api/diagnostic]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

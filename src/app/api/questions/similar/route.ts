import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// GET /api/questions/similar?subTopic=...&questionId=...
// Returns a random question from the same subTopic (preferring auto_generated).
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const subTopic  = searchParams.get('subTopic');
  const questionId = searchParams.get('questionId');

  if (!subTopic) {
    return NextResponse.json({ error: 'subTopic required' }, { status: 400 });
  }

  const candidates = await prisma.question.findMany({
    where: {
      subTopic,
      ...(questionId ? { id: { not: questionId } } : {}),
    },
  });

  if (candidates.length === 0) {
    return NextResponse.json({ error: 'No similar questions found' }, { status: 404 });
  }

  // Prefer auto_generated so the student sees a fresh example
  const autoGen = candidates.filter((q) => q.source === 'auto_generated');
  const pool    = autoGen.length > 0 ? autoGen : candidates;
  const q       = pool[Math.floor(Math.random() * pool.length)];

  let stepByStep: unknown[] = [];
  try { stepByStep = JSON.parse(q.stepByStep); } catch { stepByStep = []; }

  return NextResponse.json({ ...q, stepByStep });
}

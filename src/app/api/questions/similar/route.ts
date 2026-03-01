import { NextResponse } from 'next/server';
import { findSimilarQuestion } from '@/lib/similarQuestion';

export const dynamic = 'force-dynamic';

// GET /api/questions/similar
// Params: questionId, subTopic (required), topicId, difficulty, wasCorrect, exclude (comma-sep IDs)
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const questionId  = searchParams.get('questionId')  ?? '';
  const subTopic    = searchParams.get('subTopic')    ?? '';
  const topicId     = searchParams.get('topicId')     ?? '';
  const difficulty  = searchParams.get('difficulty')  ?? 'Medium';
  const wasCorrect  = searchParams.get('wasCorrect')  === 'true';
  const excludeIds  = (searchParams.get('exclude') ?? '').split(',').filter(Boolean);

  if (!subTopic) {
    return NextResponse.json({ error: 'subTopic required' }, { status: 400 });
  }

  const q = await findSimilarQuestion(
    { questionId, subTopic, topicId, difficulty, wasCorrect },
    excludeIds,
  );

  if (!q) {
    return NextResponse.json({ error: 'No similar question found' }, { status: 404 });
  }

  let stepByStep: unknown[] = [];
  try { stepByStep = JSON.parse(q.stepByStep); } catch { stepByStep = []; }

  return NextResponse.json({ ...q, stepByStep });
}

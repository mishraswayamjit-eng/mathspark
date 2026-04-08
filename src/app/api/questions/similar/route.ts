import { NextResponse } from 'next/server';
import { findSimilarQuestion } from '@/lib/similarQuestion';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

export const dynamic = 'force-dynamic';

// GET /api/questions/similar
// Params: questionId, subTopic (required), topicId, difficulty, wasCorrect, exclude (comma-sep IDs)
export async function GET(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const questionId  = searchParams.get('questionId')  ?? '';
    const subTopic    = searchParams.get('subTopic')    ?? '';
    const topicId     = searchParams.get('topicId')     ?? '';
    const difficulty  = searchParams.get('difficulty')  ?? 'Medium';
    const wasCorrect  = searchParams.get('wasCorrect')  === 'true';
    const excludeIds  = (searchParams.get('exclude') ?? '').split(',').filter(Boolean);

    if (!subTopic || subTopic.length > 100) {
      return NextResponse.json({ error: 'subTopic required (max 100 chars)' }, { status: 400 });
    }
    if (questionId.length > 50 || topicId.length > 30 || difficulty.length > 20) {
      return NextResponse.json({ error: 'Invalid parameter length' }, { status: 400 });
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

    // Omit correctAnswer — grading is done server-side via /api/attempts
    const { correctAnswer: _ca, ...rest } = q;
    return NextResponse.json({ ...rest, stepByStep });
  } catch (err) {
    console.error('[questions/similar] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

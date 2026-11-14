import { NextResponse } from 'next/server';
import { findSimilarQuestion } from '@/lib/similarQuestion';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { parseUnknownArray } from '@/lib/jsonFields';
import { logError } from '@/lib/logger';
import { withVisual } from '@/lib/figures/lookup';

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

    const stepByStep = parseUnknownArray(q.stepByStep);

    // correctAnswer is included, as in /api/questions/next: the practice screen
    // marks the answer on the spot (and would otherwise judge every "try a
    // similar one" answer a miss). /api/attempts still re-grades on the server,
    // so XP, mastery and progress never depend on this value.
    // The figure and step pictures ride along, as the steps themselves already do.
    return NextResponse.json(withVisual({ ...q, stepByStep }, { withSolution: true }));
  } catch (err) {
    logError('[questions/similar] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

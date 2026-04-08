import { NextResponse } from 'next/server';
import { getNextQuestion } from '@/lib/adaptive';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

// GET /api/questions/next?topicId=&subTopic=&exclude=
export async function GET(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    const { searchParams } = new URL(req.url);
    const topicId   = searchParams.get('topicId');
    const excludeParam = searchParams.get('exclude') ?? '';
    const excludeIds   = excludeParam ? excludeParam.split(',').filter(Boolean) : [];
    const subTopic     = searchParams.get('subTopic') ?? '';

    if (!topicId) {
      return NextResponse.json({ error: 'topicId required' }, { status: 400 });
    }

    const q = await getNextQuestion(studentId, topicId, excludeIds, subTopic);

    if (!q) {
      return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
    }

    let stepByStep: unknown[] = [];
    try { stepByStep = JSON.parse(q.stepByStep ?? '[]'); } catch { /* malformed seed data */ }
    // Strip correctAnswer — grading is done server-side via /api/attempts
    const { correctAnswer: _ca, ...rest } = q;
    return NextResponse.json({ ...rest, stepByStep });
  } catch (err) {
    console.error('[questions/next] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { getNextQuestion } from '@/lib/adaptive';

// GET /api/questions/next?topicId=&studentId=
// All session context (seen questions, streak) is derived from the DB.
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId   = searchParams.get('topicId');
  const studentId = searchParams.get('studentId');

  if (!topicId || !studentId) {
    return NextResponse.json({ error: 'topicId and studentId required' }, { status: 400 });
  }

  const q = await getNextQuestion(studentId, topicId);

  if (!q) {
    return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
  }

  return NextResponse.json({
    ...q,
    stepByStep: JSON.parse(q.stepByStep ?? '[]'),
  });
}

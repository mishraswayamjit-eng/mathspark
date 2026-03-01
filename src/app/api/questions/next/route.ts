import { NextResponse } from 'next/server';
import { getNextQuestion } from '@/lib/adaptive';

// GET /api/questions/next?topicId=&studentId=
// All session context (seen questions, streak) is derived from the DB.
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId   = searchParams.get('topicId');
  const studentId = searchParams.get('studentId');
  const excludeParam = searchParams.get('exclude') ?? '';
  const excludeIds   = excludeParam ? excludeParam.split(',').filter(Boolean) : [];

  if (!topicId || !studentId) {
    return NextResponse.json({ error: 'topicId and studentId required' }, { status: 400 });
  }

  const q = await getNextQuestion(studentId, topicId, excludeIds);

  if (!q) {
    return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
  }

  return NextResponse.json({
    ...q,
    stepByStep: JSON.parse(q.stepByStep ?? '[]'),
  });
}

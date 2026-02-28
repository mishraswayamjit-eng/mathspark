import { NextResponse } from 'next/server';
import { getNextQuestion } from '@/lib/adaptive';

// GET /api/questions/next?topicId=&studentId=&exclude=id1,id2&cw=0&cr=0
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId   = searchParams.get('topicId');
  const studentId = searchParams.get('studentId');

  if (!topicId || !studentId) {
    return NextResponse.json({ error: 'topicId and studentId required' }, { status: 400 });
  }

  const excludeRaw     = searchParams.get('exclude') ?? '';
  const seenIds        = excludeRaw ? excludeRaw.split(',').filter(Boolean) : [];
  const consecutiveWrong = parseInt(searchParams.get('cw') ?? '0', 10);
  const consecutiveRight = parseInt(searchParams.get('cr') ?? '0', 10);

  const q = await getNextQuestion(studentId, topicId, seenIds, consecutiveWrong, consecutiveRight);

  if (!q) {
    return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
  }

  // Parse stepByStep JSON before sending to client
  return NextResponse.json({
    ...q,
    stepByStep: JSON.parse(q.stepByStep ?? '[]'),
  });
}

import { NextResponse } from 'next/server';
import { getNextQuestion } from '@/lib/adaptive';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { parseUnknownArray } from '@/lib/jsonFields';
import { logError } from '@/lib/logger';

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

    const stepByStep = parseUnknownArray(q.stepByStep);
    // correctAnswer is included: adaptive practice grades per-question on the
    // client for instant feedback, offline play, option highlighting, and the
    // post-answer reveal. The authoritative record (XP, progress, mastery) is
    // still re-graded server-side in /api/attempts, which never trusts the
    // client's isCorrect flag.
    return NextResponse.json({ ...q, stepByStep });
  } catch (err) {
    logError('[questions/next] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

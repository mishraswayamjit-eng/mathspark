import { NextResponse } from 'next/server';
import { getNextQuestionWithLadder } from '@/lib/adaptive';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { parseUnknownArray } from '@/lib/jsonFields';
import { logError } from '@/lib/logger';
import { withVisual } from '@/lib/figures/lookup';

// GET /api/questions/next?topicId=&subTopic=&exclude=&confidence=
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
    // Anything other than the two known values is ignored.
    const confidenceParam = searchParams.get('confidence');
    const confidence = confidenceParam === 'low' || confidenceParam === 'high' ? confidenceParam : undefined;

    if (!topicId) {
      return NextResponse.json({ error: 'topicId required' }, { status: 400 });
    }

    const { question: q, ladder } = await getNextQuestionWithLadder(studentId, topicId, excludeIds, subTopic, confidence);

    if (!q) {
      return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
    }

    const stepByStep = parseUnknownArray(q.stepByStep);
    // correctAnswer is included: adaptive practice grades per-question on the
    // client for instant feedback, offline play, option highlighting, and the
    // post-answer reveal. The authoritative record (XP, progress, mastery) is
    // still re-graded server-side in /api/attempts, which never trusts the
    // client's isCorrect flag.
    // The figure and step pictures ride along: practice shows the solution after answering.
    const payload = withVisual({ ...q, stepByStep }, { withSolution: true });
    // `ladder` (where the child is in this topic: Warm-up → Build → Challenge →
    // Exam) is sent only for focused topic practice on a keyed grade; it was
    // worked out before this question is answered. Absent in every other case.
    return NextResponse.json(ladder ? { ...payload, ladder } : payload);
  } catch (err) {
    logError('[questions/next] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

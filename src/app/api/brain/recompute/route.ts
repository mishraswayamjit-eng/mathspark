import { NextResponse } from 'next/server';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

// POST /api/brain/recompute  { studentId }
// Called fire-and-forget from practice end, mock submit, etc.
export async function POST(req: Request) {
  try {
    const { studentId } = await req.json();
    if (!studentId || typeof studentId !== 'string') {
      return NextResponse.json({ error: 'studentId required' }, { status: 400 });
    }
    await recomputeStudentAnalytics(studentId);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[brain/recompute]', err);
    return NextResponse.json({ error: 'Failed to recompute' }, { status: 500 });
  }
}

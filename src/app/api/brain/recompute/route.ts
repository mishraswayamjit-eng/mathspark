import { NextResponse } from 'next/server';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

// POST /api/brain/recompute
export async function POST() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    await recomputeStudentAnalytics(studentId);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[brain/recompute]', err);
    return NextResponse.json({ error: 'Failed to recompute' }, { status: 500 });
  }
}

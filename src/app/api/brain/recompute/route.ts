import { NextResponse } from 'next/server';
import { recomputeStudentAnalytics } from '@/lib/brain/recompute';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';

export const dynamic = 'force-dynamic';
// NOTE: maxDuration is ignored on Vercel Hobby (10s hard limit). Only effective on Pro+.
export const maxDuration = 30;

// POST /api/brain/recompute
export async function POST() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    if (!checkRateLimit(`recompute:${studentId}`, 2, 60_000)) {
      return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }

    await recomputeStudentAnalytics(studentId);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[brain/recompute]', err);
    return NextResponse.json({ error: 'Failed to recompute' }, { status: 500 });
  }
}

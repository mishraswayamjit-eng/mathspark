import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { FREE_DAILY_MINUTES, isUnlimitedPlan, isPracticeAllowed } from '@/lib/usageLimits';

export const dynamic = 'force-dynamic';

// GET /api/usage/check?studentId=
// Returns current usage status without incrementing any counters.
// Used as a gate check before the practice session starts.
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const studentId = searchParams.get('studentId');
    if (!studentId) return NextResponse.json({ error: 'studentId required' }, { status: 400 });

    const student = await prisma.student.findUnique({
      where:  { id: studentId },
      select: {
        dailyUsageMinutes: true,
        lastActiveDate:    true,
        subscription: { select: { dailyLimitMinutes: true } },
      },
    });
    if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

    const today    = new Date();
    today.setUTCHours(0, 0, 0, 0);
    const todayStr = today.toISOString().slice(0, 10);
    const lastStr  = student.lastActiveDate
      ? new Date(student.lastActiveDate).toISOString().slice(0, 10)
      : '';

    // If last active was a previous day, today's usage resets to 0
    const used  = lastStr === todayStr ? student.dailyUsageMinutes : 0;
    const limit = student.subscription?.dailyLimitMinutes ?? FREE_DAILY_MINUTES;

    const allowed   = isUnlimitedPlan(limit) || isPracticeAllowed(used, limit);
    const remaining = isUnlimitedPlan(limit) ? null : Math.max(0, limit - used);

    return NextResponse.json({ allowed, used, limit, remaining });
  } catch (err) {
    console.error('[usage/check]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

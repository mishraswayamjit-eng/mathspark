import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { FREE_DAILY_MINUTES, UNLIMITED_THRESHOLD, isUnlimitedPlan, isPracticeAllowed } from '@/lib/usageLimits';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { MONETIZATION_ENABLED } from '@/lib/monetization';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

// GET /api/usage/check
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

    // Monetization OFF → everyone is effectively subscribed with unlimited usage.
    if (!MONETIZATION_ENABLED) {
      return NextResponse.json({
        allowed:   true,
        used:      0,
        limit:     UNLIMITED_THRESHOLD,
        remaining: null,
        trial:     { isSubscribed: true, lifetimeQuestions: 0, todayQuestions: 0 },
      });
    }

    const [student, lifetimeCount, todayAttemptCount] = await Promise.all([
      prisma.student.findUnique({
        where:  { id: studentId },
        select: {
          dailyUsageMinutes: true,
          lastActiveDate:    true,
          subscription: { select: { dailyLimitMinutes: true } },
        },
      }),
      prisma.attempt.count({ where: { studentId } }),
      prisma.attempt.count({
        where: {
          studentId,
          createdAt: { gte: (() => { const d = new Date(); d.setUTCHours(0,0,0,0); return d; })() },
        },
      }),
    ]);

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

    const trial = {
      isSubscribed:      student.subscription !== null,
      lifetimeQuestions: lifetimeCount,
      todayQuestions:    todayAttemptCount,
    };

    return NextResponse.json({ allowed, used, limit, remaining, trial });
  } catch (err) {
    logError('[usage/check]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

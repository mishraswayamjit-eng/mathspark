import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { FREE_DAILY_MINUTES, isUnlimitedPlan } from '@/lib/usageLimits';
import { validateStudentAccess } from '@/lib/validateStudent';

export const dynamic = 'force-dynamic';

// POST /api/usage/heartbeat
// Body: { studentId }
// Called every 60 seconds from practice pages to track daily usage.
export async function POST(req: Request) {
  try {
    const { studentId } = await req.json() as { studentId: string };
    if (!studentId) return NextResponse.json({ error: 'studentId required' }, { status: 400 });

    const accessErr = await validateStudentAccess(studentId);
    if (accessErr) return NextResponse.json({ error: accessErr }, { status: accessErr === 'Student not found' ? 404 : 403 });

    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);
    const todayStr = today.toISOString().slice(0, 10);

    // Upsert daily usage log (increment 1 minute per heartbeat)
    await prisma.usageLog.upsert({
      where:  { studentId_date: { studentId, date: today } },
      update: { minutesUsed: { increment: 1 } },
      create: { studentId, date: today, minutesUsed: 1 },
    });

    // Atomically read + update student daily counter to prevent race condition
    // on concurrent heartbeats that span a day boundary.
    const { newUsed, limit } = await prisma.$transaction(async (tx) => {
      const student = await tx.student.findUnique({
        where:  { id: studentId },
        select: {
          dailyUsageMinutes: true,
          lastActiveDate:    true,
          subscription:      { select: { dailyLimitMinutes: true } },
        },
      });
      if (!student) throw new Error('Student not found');

      const lastStr = student.lastActiveDate
        ? new Date(student.lastActiveDate).toISOString().slice(0, 10)
        : '';

      const isNewDay = lastStr !== todayStr;

      await tx.student.update({
        where: { id: studentId },
        data: isNewDay
          ? { dailyUsageMinutes: 1, aiChatMessagesUsedToday: 0, lastActiveDate: today }
          : { dailyUsageMinutes: { increment: 1 }, lastActiveDate: today },
      });

      const newUsed = isNewDay ? 1 : student.dailyUsageMinutes + 1;
      const limit   = student.subscription?.dailyLimitMinutes ?? FREE_DAILY_MINUTES;

      return { newUsed, limit };
    });

    if (isUnlimitedPlan(limit)) {
      return NextResponse.json({ allowed: true, used: newUsed, limit, remaining: null });
    }

    const remaining = Math.max(0, limit - newUsed);
    return NextResponse.json({ allowed: remaining > 0, used: newUsed, limit, remaining });
  } catch (err) {
    if ((err as Error).message === 'Student not found') {
      return NextResponse.json({ error: 'Student not found' }, { status: 404 });
    }
    console.error('[heartbeat]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

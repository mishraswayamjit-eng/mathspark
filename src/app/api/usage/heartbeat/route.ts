import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// POST /api/usage/heartbeat
// Body: { studentId }
// Called every 60 seconds from practice pages to track daily usage.
export async function POST(req: Request) {
  try {
    const { studentId } = await req.json() as { studentId: string };
    if (!studentId) return NextResponse.json({ error: 'studentId required' }, { status: 400 });

    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);

    // Upsert daily usage log (increment 1 minute per heartbeat)
    await prisma.usageLog.upsert({
      where:  { studentId_date: { studentId, date: today } },
      update: { minutesUsed: { increment: 1 } },
      create: { studentId, date: today, minutesUsed: 1 },
    });

    // Reset daily counter if date changed; otherwise increment
    const student = await prisma.student.findUnique({
      where:  { id: studentId },
      select: { dailyUsageMinutes: true, lastActiveDate: true, subscription: { select: { dailyLimitMinutes: true } } },
    });
    if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

    const lastActive = student.lastActiveDate ? new Date(student.lastActiveDate) : null;
    const todayStr   = today.toISOString().slice(0, 10);
    const lastStr    = lastActive?.toISOString().slice(0, 10) ?? '';

    if (lastStr !== todayStr) {
      // New day — reset counter
      await prisma.student.update({
        where: { id: studentId },
        data:  {
          dailyUsageMinutes:       1,
          aiChatMessagesUsedToday: 0,
          lastActiveDate:          today,
        },
      });
    } else {
      await prisma.student.update({
        where: { id: studentId },
        data:  { dailyUsageMinutes: { increment: 1 }, lastActiveDate: today },
      });
    }

    const limit     = student.subscription?.dailyLimitMinutes ?? 60;
    const newUsed   = lastStr !== todayStr ? 1 : (student.dailyUsageMinutes + 1);
    const remaining = Math.max(0, limit - newUsed);
    const allowed   = remaining > 0;

    return NextResponse.json({ allowed, used: newUsed, limit, remaining });
  } catch (err) {
    console.error('[heartbeat]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import bcrypt from 'bcryptjs';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

const TIER_TO_PLAN: Record<number, string> = {
  1: 'plan_starter_monthly',
  2: 'plan_advanced_monthly',
  3: 'plan_unlimited_monthly',
};

interface TestParent {
  id: string; name: string; email: string; phone: string;
}
interface TestStudent {
  id: string; name: string; grade: number; parentId: string;
  subscriptionTier: number;
}
interface TestOrder {
  id: string; parentId: string; studentId: string; subscriptionTier: number;
  amountPaise: number; currency: string; paymentMethod: string;
  razorpayOrderId: string; razorpayPaymentId: string;
  invoiceNumber: string; startsAt: string; expiresAt: string;
}
interface TestProgress {
  studentId: string; topicId: string; attempted: number; correct: number; mastery: string;
}
interface TestUsageLog {
  studentId: string; date: string; minutesUsed: number; questionsAttempted: number; aiChatMessages: number;
}
interface TestStreak {
  currentStreak: number; longestStreak: number; totalDaysPracticed: number;
}

// GET /api/seed-test?secret=xxx
export async function GET(req: Request) {
  const secret = process.env.SEED_SECRET;
  if (!secret) {
    return NextResponse.json({ error: 'SEED_SECRET not set.' }, { status: 500 });
  }
  const { searchParams } = new URL(req.url);
  if (searchParams.get('secret') !== secret) {
    return NextResponse.json({ error: 'Wrong secret.' }, { status: 401 });
  }

  try {
    const dataPath = path.join(process.cwd(), 'data', 'mathspark_test_seed.json');
    if (!fs.existsSync(dataPath)) {
      return NextResponse.json({ error: 'Test seed file not found at data/mathspark_test_seed.json' }, { status: 500 });
    }
    const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8')) as {
      parents:    TestParent[];
      students:   TestStudent[];
      orders:     TestOrder[];
      progress:   TestProgress[];
      usageLogs:  TestUsageLog[];
      streaks:    Record<string, TestStreak>;
      badges:     Record<string, string[]>;
    };

    // Hash 'test1234' once — all test parents share the same password
    const passwordHash = await bcrypt.hash('test1234', 12);

    // ── 1. Parents ────────────────────────────────────────────────────────────
    for (const p of data.parents) {
      await prisma.parent.upsert({
        where:  { id: p.id },
        update: { name: p.name, email: p.email, phone: p.phone, passwordHash },
        create: { id: p.id, name: p.name, email: p.email, phone: p.phone, passwordHash },
      });
    }

    // ── 2. Students ───────────────────────────────────────────────────────────
    for (const s of data.students) {
      const subscriptionId      = TIER_TO_PLAN[s.subscriptionTier];
      const streak              = data.streaks[s.id] ?? { currentStreak: 0, longestStreak: 0, totalDaysPracticed: 0 };
      const badges              = JSON.stringify(data.badges[s.id] ?? []);
      await prisma.student.upsert({
        where:  { id: s.id },
        update: {
          name: s.name, grade: s.grade, parentId: s.parentId, subscriptionId,
          currentStreak:      streak.currentStreak,
          longestStreak:      streak.longestStreak,
          totalDaysPracticed: streak.totalDaysPracticed,
          badges,
        },
        create: {
          id: s.id, name: s.name, grade: s.grade, parentId: s.parentId, subscriptionId,
          currentStreak:      streak.currentStreak,
          longestStreak:      streak.longestStreak,
          totalDaysPracticed: streak.totalDaysPracticed,
          badges,
        },
      });
    }

    // ── 3. Orders ─────────────────────────────────────────────────────────────
    for (const o of data.orders) {
      const subscriptionId = TIER_TO_PLAN[o.subscriptionTier];
      await prisma.order.upsert({
        where:  { id: o.id },
        update: {
          parentId: o.parentId, studentId: o.studentId, subscriptionId,
          amountPaise: o.amountPaise, currency: o.currency,
          paymentMethod: o.paymentMethod, paymentStatus: 'paid',
          razorpayOrderId: o.razorpayOrderId, razorpayPaymentId: o.razorpayPaymentId,
          invoiceNumber: o.invoiceNumber,
          startsAt: new Date(o.startsAt), expiresAt: new Date(o.expiresAt),
        },
        create: {
          id: o.id, parentId: o.parentId, studentId: o.studentId, subscriptionId,
          amountPaise: o.amountPaise, currency: o.currency,
          paymentMethod: o.paymentMethod, paymentStatus: 'paid',
          razorpayOrderId: o.razorpayOrderId, razorpayPaymentId: o.razorpayPaymentId,
          invoiceNumber: o.invoiceNumber,
          startsAt: new Date(o.startsAt), expiresAt: new Date(o.expiresAt),
        },
      });
    }

    // ── 4. Progress ───────────────────────────────────────────────────────────
    for (const pr of data.progress) {
      await prisma.progress.upsert({
        where:  { studentId_topicId: { studentId: pr.studentId, topicId: pr.topicId } },
        update: { attempted: pr.attempted, correct: pr.correct, mastery: pr.mastery },
        create: { studentId: pr.studentId, topicId: pr.topicId, attempted: pr.attempted, correct: pr.correct, mastery: pr.mastery },
      });
    }

    // ── 5. Usage logs ─────────────────────────────────────────────────────────
    for (const ul of data.usageLogs) {
      await prisma.usageLog.upsert({
        where:  { studentId_date: { studentId: ul.studentId, date: new Date(ul.date) } },
        update: { minutesUsed: ul.minutesUsed, questionsAttempted: ul.questionsAttempted, aiChatMessages: ul.aiChatMessages },
        create: { studentId: ul.studentId, date: new Date(ul.date), minutesUsed: ul.minutesUsed, questionsAttempted: ul.questionsAttempted, aiChatMessages: ul.aiChatMessages },
      });
    }

    return NextResponse.json({
      ok: true,
      seeded: {
        parents:   data.parents.length,
        students:  data.students.length,
        orders:    data.orders.length,
        progress:  data.progress.length,
        usageLogs: data.usageLogs.length,
      },
    });
  } catch (err) {
    console.error('[seed-test]', err);
    return NextResponse.json(
      { error: `Test seed failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

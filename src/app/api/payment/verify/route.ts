import { NextResponse } from 'next/server';
import crypto from 'crypto';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { validateBody, ValidationError } from '@/lib/validateBody';

function generateInvoiceNumber(count: number): string {
  const year = new Date().getFullYear();
  const seq  = String(count + 1).padStart(5, '0');
  return `MS-${year}-${seq}`;
}

// POST /api/payment/verify
// Body: { razorpayOrderId, razorpayPaymentId, razorpaySignature, subscriptionId, studentId }
export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const {
      razorpayOrderId,
      razorpayPaymentId,
      razorpaySignature,
      subscriptionId,
      studentId,
    } = validateBody<{
      razorpayOrderId: string;
      razorpayPaymentId: string;
      razorpaySignature: string;
      subscriptionId: string;
      studentId: string;
    }>(
      await req.json(),
      { razorpayOrderId: 'string', razorpayPaymentId: 'string', razorpaySignature: 'string', subscriptionId: 'string', studentId: 'string' },
    );

    // Verify Razorpay signature
    const secret    = process.env.RAZORPAY_KEY_SECRET ?? '';
    const body      = `${razorpayOrderId}|${razorpayPaymentId}`;
    const expected  = crypto.createHmac('sha256', secret).update(body).digest('hex');

    if (expected !== razorpaySignature) {
      return NextResponse.json({ error: 'Invalid payment signature.' }, { status: 400 });
    }

    // Verify student belongs to parent
    const student = await prisma.student.findFirst({
      where: { id: studentId, parentId: session.user.id },
      select: { id: true },
    });
    if (!student) return NextResponse.json({ error: 'Student not found.' }, { status: 404 });

    const plan = await prisma.subscription.findUnique({ where: { id: subscriptionId } });
    if (!plan) return NextResponse.json({ error: 'Plan not found.' }, { status: 404 });

    const now      = new Date();
    const expiresAt = new Date(now.getTime() + plan.durationDays * 24 * 60 * 60 * 1000);

    // Create order + activate subscription atomically.
    // Invoice number count is inside the transaction to prevent duplicates.
    const invoiceNumber = await prisma.$transaction(async (tx) => {
      const orderCount = await tx.order.count();
      const inv = generateInvoiceNumber(orderCount);

      await tx.order.create({
        data: {
          parentId:         session.user.id,
          subscriptionId,
          studentId,
          amountPaise:      plan.priceINR,
          paymentMethod:    'razorpay',
          paymentStatus:    'paid',
          razorpayOrderId,
          razorpayPaymentId,
          invoiceNumber:    inv,
          startsAt:         now,
          expiresAt,
        },
      });

      await tx.student.update({
        where: { id: studentId },
        data:  { subscriptionId },
      });

      return inv;
    });

    return NextResponse.json({ ok: true, invoiceNumber, expiresAt: expiresAt.toISOString() });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    console.error('[payment/verify]', err);
    return NextResponse.json({ error: 'Failed to verify payment.' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import Razorpay from 'razorpay';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';

// POST /api/payment/create-order
// Body: { subscriptionId, studentId }
export async function POST(req: Request) {
  // Fail fast if Razorpay credentials are missing — avoids creating "ghost" orders
  // with empty keys that would then fail signature verification on /verify.
  const razorpayKeyId     = process.env.RAZORPAY_KEY_ID;
  const razorpayKeySecret = process.env.RAZORPAY_KEY_SECRET;
  if (!razorpayKeyId || !razorpayKeySecret) {
    logError('[payment/create-order] Razorpay credentials missing');
    return NextResponse.json(
      { error: 'Payments are not configured. Please contact support.' },
      { status: 503 },
    );
  }
  // Lazy init — avoids constructor crash during Next.js build-time page collection
  const razorpay = new Razorpay({
    key_id:     razorpayKeyId,
    key_secret: razorpayKeySecret,
  });
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const userId = session.user.id;
  if (!checkRateLimit(`payment:${userId}`, 10, 60_000)) {
    return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
  }

  try {
    const { subscriptionId, studentId } = validateBody<{ subscriptionId: string; studentId: string }>(
      await req.json(),
      { subscriptionId: 'string', studentId: 'string' },
    );
    if (!subscriptionId || !studentId) {
      return NextResponse.json({ error: 'subscriptionId and studentId required.' }, { status: 400 });
    }

    // Verify student belongs to this parent
    const student = await prisma.student.findFirst({
      where: { id: studentId, parentId: userId },
      select: { id: true },
    });
    if (!student) {
      return NextResponse.json({ error: 'Student not found.' }, { status: 404 });
    }

    const plan = await prisma.subscription.findUnique({ where: { id: subscriptionId } });
    if (!plan || !plan.isActive) {
      return NextResponse.json({ error: 'Invalid subscription plan.' }, { status: 400 });
    }

    const order = await razorpay.orders.create({
      amount:   plan.priceINR,
      currency: 'INR',
      notes:    { subscriptionId, studentId, parentId: userId },
    });

    return NextResponse.json({
      orderId:    order.id,
      amount:     plan.priceINR,
      currency:   'INR',
      keyId:      razorpayKeyId,
      planName:   plan.name,
    });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    logError('[payment/create-order]', err);
    return NextResponse.json({ error: 'Failed to create payment order.' }, { status: 500 });
  }
}

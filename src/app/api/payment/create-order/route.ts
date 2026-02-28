import { NextResponse } from 'next/server';
import Razorpay from 'razorpay';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';

const razorpay = new Razorpay({
  key_id:     process.env.RAZORPAY_KEY_ID     ?? '',
  key_secret: process.env.RAZORPAY_KEY_SECRET ?? '',
});

// POST /api/payment/create-order
// Body: { subscriptionId, studentId }
export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const userId = session.user.id;
  if (!checkRateLimit(`payment:${userId}`, 10, 60_000)) {
    return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
  }

  try {
    const { subscriptionId, studentId } = await req.json() as { subscriptionId: string; studentId: string };
    if (!subscriptionId || !studentId) {
      return NextResponse.json({ error: 'subscriptionId and studentId required.' }, { status: 400 });
    }

    // Verify student belongs to this parent
    const student = await prisma.student.findFirst({
      where: { id: studentId, parentId: userId },
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
      keyId:      process.env.RAZORPAY_KEY_ID,
      planName:   plan.name,
    });
  } catch (err) {
    console.error('[payment/create-order]', err);
    return NextResponse.json({ error: 'Failed to create payment order.' }, { status: 500 });
  }
}

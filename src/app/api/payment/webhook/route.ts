import { NextResponse } from 'next/server';
import crypto from 'crypto';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// POST /api/payment/webhook
// Handles Razorpay webhook events
export async function POST(req: Request) {
  const body      = await req.text();
  const signature = req.headers.get('x-razorpay-signature') ?? '';
  const secret    = process.env.RAZORPAY_WEBHOOK_SECRET ?? '';

  // Verify webhook signature
  const expected = crypto.createHmac('sha256', secret).update(body).digest('hex');
  if (expected !== signature) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  try {
    const event = JSON.parse(body) as {
      event: string;
      payload: { payment: { entity: { id: string; order_id: string; status: string } } };
    };

    const payment = event.payload?.payment?.entity;
    if (!payment) return NextResponse.json({ ok: true });

    if (event.event === 'payment.captured') {
      // Mark order as paid if it exists
      await prisma.order.updateMany({
        where: { razorpayOrderId: payment.order_id },
        data:  { paymentStatus: 'paid', razorpayPaymentId: payment.id },
      });
    } else if (event.event === 'payment.failed') {
      await prisma.order.updateMany({
        where: { razorpayOrderId: payment.order_id },
        data:  { paymentStatus: 'failed' },
      });
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[payment/webhook]', err);
    return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
  }
}

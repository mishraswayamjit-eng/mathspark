import { NextResponse } from 'next/server';
import crypto from 'crypto';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { Resend } from 'resend';

export async function POST(req: Request) {
  // Lazy init — avoids "Missing API key" crash during Next.js build-time page collection
  const resend = new Resend(process.env.RESEND_API_KEY ?? '');
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0] ?? 'unknown';
  if (!checkRateLimit(`forgot:${ip}`, 5, 60_000)) {
    return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
  }

  try {
    const { email } = await req.json() as { email: string };
    if (!email?.trim()) {
      return NextResponse.json({ error: 'Email is required.' }, { status: 400 });
    }

    const emailClean = email.toLowerCase().trim();
    const parent = await prisma.parent.findUnique({ where: { email: emailClean } });

    // Always return success to prevent email enumeration
    if (!parent) {
      return NextResponse.json({ ok: true });
    }

    const token   = crypto.randomBytes(32).toString('hex');
    const expiry  = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

    await prisma.parent.update({
      where: { id: parent.id },
      data:  { resetToken: token, resetTokenExpiry: expiry },
    });

    const baseUrl = process.env.NEXTAUTH_URL ?? 'https://mathspark-five.vercel.app';
    const link    = `${baseUrl}/auth/reset-password?token=${token}`;

    await resend.emails.send({
      from:    'MathSpark <noreply@mathspark.app>',
      to:      [emailClean],
      subject: 'Reset your MathSpark password',
      html: `
        <p>Hi ${parent.name},</p>
        <p>Click the link below to reset your password. The link expires in 1 hour.</p>
        <p><a href="${link}" style="background:#58CC02;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;">Reset Password</a></p>
        <p>If you didn't request this, ignore this email.</p>
      `,
    });

    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: 'Something went wrong.' }, { status: 500 });
  }
}

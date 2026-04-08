import { NextResponse } from 'next/server';
import crypto from 'crypto';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';

export async function POST(req: Request) {
  // Rate limit: 10 attempts per IP per 15 minutes
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (!checkRateLimit(`reset-password:${ip}`, 10, 900_000)) {
    return NextResponse.json({ error: 'Too many requests. Please wait and try again.' }, { status: 429 });
  }

  try {
    const { token, password } = await req.json() as { token: string; password: string };

    if (!token || !password) {
      return NextResponse.json({ error: 'Token and password are required.' }, { status: 400 });
    }
    if (password.length < 8) {
      return NextResponse.json({ error: 'Password must be at least 8 characters.' }, { status: 400 });
    }

    // Hash the incoming token to compare against the stored hash
    const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

    const parent = await prisma.parent.findFirst({
      where: {
        resetToken:       tokenHash,
        resetTokenExpiry: { gt: new Date() },
      },
    });

    if (!parent) {
      return NextResponse.json({ error: 'Reset link is invalid or has expired.' }, { status: 400 });
    }

    const passwordHash = await bcrypt.hash(password, 12);
    await prisma.parent.update({
      where: { id: parent.id },
      data:  { passwordHash, resetToken: null, resetTokenExpiry: null },
    });

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error('[reset-password] Unexpected error:', err);
    return NextResponse.json({ error: 'Something went wrong.' }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { createStudentToken, COOKIE_NAME } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import bcrypt from 'bcryptjs';

export const dynamic = 'force-dynamic';

// POST /api/student/session — create student session (set httpOnly cookie)
export async function POST(req: Request) {
  // Rate limit: 10 per minute per IP
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (!checkRateLimit(`student-session:${ip}`, 10, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  let studentId: string;
  let pin: string | undefined;
  try {
    const parsed = validateBody<{ studentId: string; pin?: string }>(
      await req.json(),
      { studentId: 'string', pin: 'string?' },
    );
    studentId = parsed.studentId;
    pin = parsed.pin as string | undefined;
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
  }
  if (!studentId || studentId.length > 30) {
    return NextResponse.json({ error: 'Valid studentId required' }, { status: 400 });
  }

  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { id: true, name: true, grade: true, pinHash: true, parentId: true, deletedAt: true },
  });
  // Soft-deleted students are treated as not-found so they cannot log in.
  if (!student || student.deletedAt) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  // A parent authenticated via NextAuth who OWNS this child may start a session
  // without the child's PIN (legitimate proof of ownership). This also gives
  // legacy PIN-less accounts a secure recovery path: the parent logs in as the
  // child, then sets a PIN. Everyone else must present a valid PIN.
  const parentSession = await getServerSession(authOptions);
  const isOwningParent = Boolean(
    parentSession?.user?.id && student.parentId && parentSession.user.id === student.parentId,
  );

  if (!isOwningParent) {
    // Mandatory PIN: a self-serve session is ONLY ever issued after a verified
    // PIN check. This closes the account-takeover hole where any known studentId
    // yielded a session without proof of ownership.
    if (!student.pinHash) {
      return NextResponse.json(
        { error: 'This account needs a PIN. Ask a parent to set one.', requiresPinSetup: true },
        { status: 403 },
      );
    }
    if (!pin) {
      return NextResponse.json({ error: 'PIN required', requiresPin: true }, { status: 401 });
    }
    const pinValid = await bcrypt.compare(pin, student.pinHash);
    if (!pinValid) {
      return NextResponse.json({ error: 'Incorrect PIN' }, { status: 401 });
    }
  }

  const token = await createStudentToken(student.id);

  const res = NextResponse.json({
    success: true,
    name: student.name,
    grade: student.grade,
  });

  res.cookies.set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  });

  return res;
}

// DELETE /api/student/session — clear student session cookie (logout)
export async function DELETE() {
  const res = NextResponse.json({ success: true });

  res.cookies.set(COOKIE_NAME, '', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 0,
  });

  return res;
}

import { NextResponse } from 'next/server';
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
    select: { id: true, name: true, grade: true, pinHash: true },
  });
  if (!student) {
    return NextResponse.json({ error: 'Student not found' }, { status: 404 });
  }

  // If student has a PIN set, require it for login
  if (student.pinHash) {
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

import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';
import { validateBody, ValidationError } from '@/lib/validateBody';
import bcrypt from 'bcryptjs';

// PATCH /api/parent/children/[childId]   body: { pin: "1234" }
// The owning parent sets (or replaces) the child's 4-digit PIN. This is how a
// child added from the parent dashboard gets a PIN in the first place, and how
// a forgotten PIN is recovered. The old PIN is not needed: being signed in as
// the owning parent is the proof.
export async function PATCH(
  req: Request,
  { params }: { params: { childId: string } },
) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limit: 10 PIN changes per parent per hour
  if (!checkRateLimit(`set-child-pin:${session.user.id}`, 10, 3_600_000)) {
    return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
  }

  try {
    const { childId } = params;
    if (typeof childId !== 'string' || childId.length === 0 || childId.length > 50) {
      return NextResponse.json({ error: 'Invalid child ID' }, { status: 400 });
    }

    let rawBody: unknown;
    try {
      rawBody = await req.json();
    } catch {
      return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
    }
    const { pin } = validateBody<{ pin: string }>(rawBody, { pin: 'string' });
    if (!/^\d{4}$/.test(pin)) {
      return NextResponse.json({ error: 'PIN must be exactly 4 digits.' }, { status: 400 });
    }

    const pinHash = await bcrypt.hash(pin, 10);

    // updateMany enforces ownership atomically (same pattern as DELETE below).
    const { count } = await prisma.student.updateMany({
      where: { id: childId, parentId: session.user.id, deletedAt: null },
      data:  { pinHash },
    });
    if (count === 0) {
      return NextResponse.json({ error: 'Child not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    logError('[parent/children PATCH]', err);
    return NextResponse.json({ error: "We couldn't finish that. Please try again." }, { status: 500 });
  }
}

// DELETE /api/parent/children/[childId] — soft-delete a child the parent owns
export async function DELETE(
  _req: Request,
  { params }: { params: { childId: string } },
) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limit: 20 deletions per parent per hour
  if (!checkRateLimit(`delete-child:${session.user.id}`, 20, 3_600_000)) {
    return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
  }

  try {
    const { childId } = params;

    if (typeof childId !== 'string' || childId.length === 0 || childId.length > 50) {
      return NextResponse.json({ error: 'Invalid child ID' }, { status: 400 });
    }

    // Soft-delete only if the child belongs to this parent and isn't already deleted.
    // updateMany enforces ownership atomically and returns a count we can check.
    const { count } = await prisma.student.updateMany({
      where: { id: childId, parentId: session.user.id, deletedAt: null },
      data:  { deletedAt: new Date() },
    });

    if (count === 0) {
      return NextResponse.json({ error: 'Child not found' }, { status: 404 });
    }

    return NextResponse.json({ success: true });
  } catch (err) {
    logError('[parent/children DELETE]', err);
    return NextResponse.json({ error: "We couldn't finish that. Please try again." }, { status: 500 });
  }
}

import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';

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
    return NextResponse.json({ error: 'Something went wrong.' }, { status: 500 });
  }
}

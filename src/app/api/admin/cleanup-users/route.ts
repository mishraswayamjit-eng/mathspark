import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

// GET /api/admin/cleanup-users?secret=xxx
// Deletes all non-test students and parents (test IDs start with student_ / parent_)
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    // Count before deletion
    const totalStudents = await prisma.student.count();
    const totalParents  = await prisma.parent.count();

    // Delete non-test students (cascade handles attempts, progress, etc.)
    const deletedStudents = await prisma.student.deleteMany({
      where: {
        NOT: { id: { startsWith: 'student_' } },
      },
    });

    // Delete non-test parents (cascade handles orders, etc.)
    const deletedParents = await prisma.parent.deleteMany({
      where: {
        NOT: { id: { startsWith: 'parent_' } },
      },
    });

    return NextResponse.json({
      ok: true,
      before: { students: totalStudents, parents: totalParents },
      deleted: { students: deletedStudents.count, parents: deletedParents.count },
      remaining: {
        students: totalStudents - deletedStudents.count,
        parents:  totalParents  - deletedParents.count,
      },
    });
  } catch (err) {
    logError('[cleanup-users]', err);
    return NextResponse.json(
      { error: `Cleanup failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

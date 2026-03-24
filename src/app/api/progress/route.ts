import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

// GET /api/progress
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const progress = await prisma.progress.findMany({
      where: { studentId },
      include: { topic: true },
    });

    return NextResponse.json(progress);
  } catch (err) {
    console.error('[progress] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

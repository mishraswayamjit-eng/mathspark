import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

// GET /api/students/:id — authenticated students may read only their own record.
export async function GET(
  req: Request,
  { params }: { params: { id: string } },
) {
  const authId = await getAuthenticatedStudentId();
  if (!authId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  if (authId !== params.id) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (!checkRateLimit(`student-by-id:${authId}`, 30, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  const student = await prisma.student.findUnique({
    where: { id: params.id },
    select: {
      id: true,
      grade: true,
      displayName: true,
      avatarColor: true,
      createdAt: true,
    },
  });
  if (!student) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(student);
}

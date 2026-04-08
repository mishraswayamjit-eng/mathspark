import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';

// GET /api/students/:id — returns only safe public fields (no real name)
export async function GET(
  req: Request,
  { params }: { params: { id: string } },
) {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (!checkRateLimit(`student-by-id:${ip}`, 30, 60_000)) {
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

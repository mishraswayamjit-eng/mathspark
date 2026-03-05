import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/students/:id — returns only safe public fields
export async function GET(
  _req: Request,
  { params }: { params: { id: string } },
) {
  const student = await prisma.student.findUnique({
    where: { id: params.id },
    select: {
      id: true,
      name: true,
      grade: true,
      displayName: true,
      avatarColor: true,
      createdAt: true,
    },
  });
  if (!student) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(student);
}

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/students/:id
export async function GET(
  _req: Request,
  { params }: { params: { id: string } },
) {
  const student = await prisma.student.findUnique({ where: { id: params.id } });
  if (!student) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(student);
}

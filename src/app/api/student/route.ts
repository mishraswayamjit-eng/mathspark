import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// PATCH /api/student — update mutable student fields (parentEmail, name)
export async function PATCH(req: Request) {
  const body = await req.json() as { studentId?: string; parentEmail?: string; name?: string };
  const { studentId, parentEmail, name } = body;

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const data: Record<string, unknown> = {};
  if (typeof parentEmail !== 'undefined') data.parentEmail = parentEmail || null;
  if (typeof name !== 'undefined' && name.trim()) data.name = name.trim();

  if (Object.keys(data).length === 0) {
    return NextResponse.json({ error: 'No fields to update' }, { status: 400 });
  }

  await prisma.student.update({ where: { id: studentId }, data });
  return NextResponse.json({ success: true });
}

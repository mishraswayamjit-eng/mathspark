import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// POST /api/students   body: { name: string }
export async function POST(req: Request) {
  const { name } = await req.json();

  if (!name || typeof name !== 'string' || !name.trim()) {
    return NextResponse.json({ error: 'name is required' }, { status: 400 });
  }

  const student = await prisma.student.create({
    data: { name: name.trim() },
  });

  return NextResponse.json(student, { status: 201 });
}

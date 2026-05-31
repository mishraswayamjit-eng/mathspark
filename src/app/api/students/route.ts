import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const CreateStudentSchema = z.object({
  name: z.string().min(1).max(50).trim(),
});

// POST /api/students   body: { name: string }
export async function POST(req: Request) {
  try {
    const body = await req.json();

    const parsed = CreateStudentSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { name } = parsed.data;

    const student = await prisma.student.create({
      data: { name },
    });

    return NextResponse.json(student, { status: 201 });
  } catch (err) {
    console.error('[POST /api/students]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

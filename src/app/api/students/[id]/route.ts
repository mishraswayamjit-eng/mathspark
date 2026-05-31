import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/students/:id
export async function GET(
  _req: Request,
  { params }: { params: { id: string } },
) {
  try {
    const id = params.id;
    if (!id || typeof id !== 'string' || id.length < 1) {
      return NextResponse.json({ error: 'Invalid id' }, { status: 400 });
    }

    const student = await prisma.student.findUnique({ where: { id } });
    if (!student) return NextResponse.json({ error: 'Not found' }, { status: 404 });
    return NextResponse.json(student, {
      headers: {
        'Cache-Control': 'private, max-age=300, stale-while-revalidate=60',
      },
    });
  } catch (err) {
    console.error('[GET /api/students/:id]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

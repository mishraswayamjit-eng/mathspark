import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/progress?studentId=xxx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId is required' }, { status: 400 });
  }

  const progress = await prisma.progress.findMany({
    where: { studentId },
    include: { topic: true },
  });

  return NextResponse.json(progress);
}

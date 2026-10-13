import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// TEMP spot-check: GET /api/admin/inspect-textbook?secret=xxx[&ch=ch07][&limit=3]
// Filters grade-5 ipm_textbook rows by chapter token in the id (e.g. "ch07").
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const ch = searchParams.get('ch'); // e.g. "ch07"
  const limit = Math.max(1, Math.min(20, parseInt(searchParams.get('limit') ?? '3', 10)));

  const rows = await prisma.question.findMany({
    where: {
      topicId: 'grade5',
      source: 'ipm_textbook',
      ...(ch ? { id: { contains: `_${ch}_` } } : {}),
    },
    take: limit,
    orderBy: { id: 'asc' },
    select: {
      id: true,
      subTopic: true,
      difficulty: true,
      questionText: true,
      option1: true,
      option2: true,
      option3: true,
      option4: true,
      correctAnswer: true,
      hint1: true,
      hint2: true,
      hint3: true,
      stepByStep: true,
      misconceptionA: true,
      misconceptionB: true,
      misconceptionC: true,
      misconceptionD: true,
      source: true,
    },
  });

  // Distinct chapter tokens present, for navigation.
  const all = await prisma.question.findMany({
    where: { topicId: 'grade5', source: 'ipm_textbook' },
    select: { id: true },
  });
  const chapters = Array.from(
    new Set(all.map((r) => r.id.match(/_(ch\d+)_/)?.[1]).filter(Boolean)),
  ).sort();

  return NextResponse.json({ chapters, returned: rows.length, rows });
}

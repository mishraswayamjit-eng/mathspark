import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// TEMP spot-check: GET /api/admin/inspect-textbook?secret=xxx[&limit=5][&id=IPMTB_...]
// Returns full grade-5 ipm_textbook rows (all fields incl. teaching layer) for QA.
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const id = searchParams.get('id');
  const limit = Math.max(1, Math.min(20, parseInt(searchParams.get('limit') ?? '5', 10)));

  const rows = await prisma.question.findMany({
    where: id
      ? { id }
      : { topicId: 'grade5', source: 'ipm_textbook' },
    take: id ? 1 : limit,
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

  const total = await prisma.question.count({
    where: { topicId: 'grade5', source: 'ipm_textbook' },
  });

  return NextResponse.json({ total, returned: rows.length, rows });
}

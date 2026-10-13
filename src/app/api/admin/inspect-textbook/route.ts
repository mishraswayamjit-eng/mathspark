import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// TEMP QA: GET /api/admin/inspect-textbook?secret=xxx
//   → all grade-5 ipm_textbook rows: { id, subTopic, questionText } (compact)
// PATCH /api/admin/inspect-textbook?secret=xxx  body { id, subTopic }
//   → re-tag a single row's subTopic.
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const rows = await prisma.question.findMany({
    where: { topicId: 'grade5', source: 'ipm_textbook' },
    orderBy: { id: 'asc' },
    select: { id: true, subTopic: true, questionText: true },
  });

  return NextResponse.json({ total: rows.length, rows });
}

export async function PATCH(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  let id: string;
  let subTopic: string;
  try {
    const body = await req.json();
    id = String(body.id);
    subTopic = String(body.subTopic);
    if (!id || !subTopic) throw new Error('missing');
  } catch {
    return NextResponse.json({ error: 'Body requires { id, subTopic }' }, { status: 400 });
  }

  const before = await prisma.question.findUnique({
    where: { id },
    select: { id: true, subTopic: true, source: true },
  });
  if (!before || before.source !== 'ipm_textbook') {
    return NextResponse.json({ error: 'Not an ipm_textbook row' }, { status: 404 });
  }

  await prisma.question.update({ where: { id }, data: { subTopic } });

  return NextResponse.json({ id, from: before.subTopic, to: subTopic });
}

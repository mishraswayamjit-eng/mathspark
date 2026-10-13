import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// TEMP QA:
//   GET  ?secret=xxx&ch=ch20        → full rows for a chapter (all fields)
//   DELETE ?secret=xxx  body {id}   → delete one ipm_textbook row + dependents
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const ch = searchParams.get('ch');
  const rows = await prisma.question.findMany({
    where: {
      topicId: 'grade5',
      source: 'ipm_textbook',
      ...(ch ? { id: { contains: `_${ch}_` } } : {}),
    },
    orderBy: { id: 'asc' },
    select: {
      id: true,
      difficulty: true,
      questionText: true,
      option1: true,
      option2: true,
      option3: true,
      option4: true,
      correctAnswer: true,
      stepByStep: true,
    },
  });

  return NextResponse.json({ returned: rows.length, rows });
}

export async function DELETE(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  let id: string;
  try {
    const body = await req.json();
    id = String(body.id);
    if (!id) throw new Error('missing');
  } catch {
    return NextResponse.json({ error: 'Body requires { id }' }, { status: 400 });
  }

  const row = await prisma.question.findUnique({
    where: { id },
    select: { id: true, source: true },
  });
  if (!row || row.source !== 'ipm_textbook') {
    return NextResponse.json({ error: 'Not an ipm_textbook row' }, { status: 404 });
  }

  // Question FKs have no cascade — delete dependents first.
  const [attempts, mockResponses, questions] = await prisma.$transaction([
    prisma.attempt.deleteMany({ where: { questionId: id } }),
    prisma.mockTestResponse.deleteMany({ where: { questionId: id } }),
    prisma.question.deleteMany({ where: { id } }),
  ]);

  return NextResponse.json({
    id,
    deletedQuestions: questions.count,
    deletedAttempts: attempts.count,
    deletedMockResponses: mockResponses.count,
  });
}

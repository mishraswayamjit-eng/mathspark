/**
 * TEMPORARY admin route — find ipm_textbook rows with leaked model self-talk in
 * stepByStep and delete them (answers are verified, but delivery is unsalvageable
 * by truncation). GET = dry-run; DELETE = apply. Remove after use.
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';
export const maxDuration = 60;

const SELF_TALK =
  /\b(wait|hmm+)\b|let me (re-?check|check|verify|double[\s-]?check)|re-?examin/i;

interface Step {
  step: number;
  text: string;
  latex?: string;
}

function hasSelfTalk(raw: unknown): boolean {
  let parsed: unknown;
  try {
    parsed = JSON.parse(typeof raw === 'string' ? raw : '[]');
  } catch {
    return false;
  }
  if (!Array.isArray(parsed)) return false;
  return (parsed as Step[]).some(
    (s) => s && typeof s === 'object' && SELF_TALK.test(String(s.text ?? '')),
  );
}

async function affectedIds(topicId: string, source: string): Promise<string[]> {
  const rows = await prisma.question.findMany({
    where: { topicId, source },
    select: { id: true, stepByStep: true },
  });
  return rows.filter((r) => hasSelfTalk(r.stepByStep)).map((r) => r.id);
}

export async function GET(req: NextRequest) {
  const p = req.nextUrl.searchParams;
  if (!verifySecret(p.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const topicId = p.get('topicId') ?? 'grade5';
  const source = p.get('source') ?? 'ipm_textbook';
  const ids = await affectedIds(topicId, source);
  return NextResponse.json({ mode: 'dry-run', topicId, source, affectedCount: ids.length, ids });
}

export async function DELETE(req: NextRequest) {
  const p = req.nextUrl.searchParams;
  if (!verifySecret(p.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const topicId = p.get('topicId') ?? 'grade5';
  const source = p.get('source') ?? 'ipm_textbook';
  const ids = await affectedIds(topicId, source);

  if (ids.length === 0) {
    return NextResponse.json({ mode: 'delete', matched: 0, deletedQuestions: 0 });
  }

  const [attempts, mockResponses, questions] = await prisma.$transaction([
    prisma.attempt.deleteMany({ where: { questionId: { in: ids } } }),
    prisma.mockTestResponse.deleteMany({ where: { questionId: { in: ids } } }),
    prisma.question.deleteMany({ where: { id: { in: ids } } }),
  ]);

  return NextResponse.json({
    mode: 'delete',
    matched: ids.length,
    deletedQuestions: questions.count,
    deletedAttempts: attempts.count,
    deletedMockResponses: mockResponses.count,
    ids,
  });
}

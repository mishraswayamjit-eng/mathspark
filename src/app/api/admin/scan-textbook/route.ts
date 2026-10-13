/**
 * TEMPORARY admin route — scan ipm_textbook rows for leaked model self-talk in
 * stepByStep (same symptom found in ai_generated). Read-only dry-run. Remove after use.
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

function stepsWithSelfTalk(raw: unknown): string[] {
  let parsed: unknown;
  try {
    parsed = JSON.parse(typeof raw === 'string' ? raw : '[]');
  } catch {
    return [];
  }
  if (!Array.isArray(parsed)) return [];
  const hits: string[] = [];
  for (const s of parsed as Step[]) {
    const text = s && typeof s === 'object' ? String(s.text ?? '') : '';
    if (SELF_TALK.test(text)) hits.push(text);
  }
  return hits;
}

export async function GET(req: NextRequest) {
  const secret = req.nextUrl.searchParams.get('secret') ?? '';
  if (!verifySecret(secret)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const topicId = req.nextUrl.searchParams.get('topicId') ?? 'grade5';
  const source = req.nextUrl.searchParams.get('source') ?? 'ipm_textbook';

  const rows = await prisma.question.findMany({
    where: { topicId, source },
    select: { id: true, stepByStep: true },
  });

  const affected: { id: string; hits: string[] }[] = [];
  for (const r of rows) {
    const hits = stepsWithSelfTalk(r.stepByStep);
    if (hits.length) affected.push({ id: r.id, hits });
  }

  return NextResponse.json({
    mode: 'scan',
    topicId,
    source,
    scanned: rows.length,
    affectedCount: affected.length,
    sample: affected.slice(0, 20),
  });
}

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';

// ── GET /api/admin/inspect-generated?secret=xxx[&topicId=grade5][&source=ai_generated][&subTopic=ratio][&limit=10] ──
// TEMPORARY read-only spot-check endpoint: returns sample questions (full content)
// so generated rows can be audited for correctness. Remove after spot-check.

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const topicId = searchParams.get('topicId') ?? 'grade5';
  const source = searchParams.get('source') ?? 'ai_generated';
  const subTopic = searchParams.get('subTopic');
  const limit = Math.min(Math.max(parseInt(searchParams.get('limit') ?? '10', 10), 1), 50);

  try {
    const rows = await prisma.question.findMany({
      where: {
        topicId,
        source,
        ...(subTopic
          ? { subTopic: { contains: subTopic, mode: 'insensitive' as const } }
          : {}),
      },
      take: limit,
      orderBy: { id: 'desc' },
      select: {
        id: true,
        subTopic: true,
        difficulty: true,
        questionText: true,
        questionLatex: true,
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
      },
    });

    const total = await prisma.question.count({ where: { topicId, source } });

    return NextResponse.json({ topicId, source, total, returned: rows.length, rows });
  } catch (err) {
    return NextResponse.json(
      { error: `Inspect failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

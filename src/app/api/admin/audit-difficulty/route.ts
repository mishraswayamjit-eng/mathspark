import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { scoreQuestion } from '@/lib/difficultyScorer';

export const dynamic = 'force-dynamic';

const PAGE_SIZE = 500;

function authorize(req: NextRequest): boolean {
  const secret = process.env.SEED_SECRET;
  if (!secret) return false;
  const { searchParams } = new URL(req.url);
  return searchParams.get('secret') === secret;
}

// ── GET: Paginated dry-run / apply ────────────────────────────────────
//
// Usage (client loops until done=true):
//   GET /api/admin/audit-difficulty?secret=xxx&page=0           → dry run
//   GET /api/admin/audit-difficulty?secret=xxx&page=0&apply=1   → apply fixes
//
// Each page fetches PAGE_SIZE questions, scores them, optionally writes
// fixes, and returns cumulative stats + done/nextPage for the loop.

export async function GET(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const page    = parseInt(searchParams.get('page') ?? '0', 10);
  const apply   = searchParams.get('apply') === '1';
  const topic   = searchParams.get('topic') || undefined;

  try {
    // Count total questions (only on page 0, client caches it)
    const total = page === 0
      ? await prisma.question.count({ where: topic ? { topicId: topic } : undefined })
      : 0;

    // Fetch one page of questions
    const questions = await prisma.question.findMany({
      where: topic ? { topicId: topic } : undefined,
      select: {
        id: true,
        topicId: true,
        difficulty: true,
        questionText: true,
        topic: { select: { grade: true } },
      },
      skip: page * PAGE_SIZE,
      take: PAGE_SIZE,
      orderBy: { id: 'asc' },
    });

    // Score this batch
    const scored = questions.map((q) =>
      scoreQuestion({
        id: q.id,
        topicId: q.topicId,
        difficulty: q.difficulty,
        questionText: q.questionText,
        grade: q.topic.grade,
      }),
    );

    const mismatches = scored.filter((s) => s.changed);

    // If applying, update mismatches in this batch
    let updated = 0;
    if (apply && mismatches.length > 0) {
      await prisma.$transaction(
        mismatches.map((m) =>
          prisma.question.update({
            where: { id: m.id },
            data: { difficulty: m.newDifficulty },
          }),
        ),
      );
      updated = mismatches.length;
    }

    // Transition summary for this batch
    const summary: Record<string, number> = {};
    for (const m of mismatches) {
      const key = `${m.oldDifficulty}\u2192${m.newDifficulty}`;
      summary[key] = (summary[key] || 0) + 1;
    }

    // Sample mismatches (up to 10 per page, client accumulates)
    const samples = mismatches.slice(0, 10).map((m) => {
      const q = questions.find((q) => q.id === m.id);
      const fullText = q?.questionText ?? '';
      return {
        id: m.id,
        topic: m.topicId,
        text: fullText.length > 120 ? fullText.slice(0, 120) + '...' : fullText,
        was: m.oldDifficulty,
        now: m.newDifficulty,
        score: m.score,
      };
    });

    const done = questions.length < PAGE_SIZE;

    return NextResponse.json({
      done,
      nextPage: done ? page : page + 1,
      pageScored: scored.length,
      pageMismatches: mismatches.length,
      pageUpdated: updated,
      summary,
      samples,
      ...(page === 0 ? { total } : {}),
    });
  } catch (err) {
    console.error('audit-difficulty error:', err);
    return NextResponse.json(
      { error: `Internal error: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

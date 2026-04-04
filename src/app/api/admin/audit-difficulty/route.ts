import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { scoreQuestion, ScoredQuestion } from '@/lib/difficultyScorer';

// Allow up to 60s for scoring 12k+ questions
export const maxDuration = 60;

function authorize(req: NextRequest): boolean {
  const secret = process.env.SEED_SECRET;
  if (!secret) return false;
  const { searchParams } = new URL(req.url);
  return searchParams.get('secret') === secret;
}

// ── GET: Dry-run report ────────────────────────────────────────────────

export async function GET(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const topicFilter = searchParams.get('topic');

  try {
    const questions = await prisma.question.findMany({
      where: topicFilter ? { topicId: topicFilter } : undefined,
      select: {
        id: true,
        topicId: true,
        difficulty: true,
        questionText: true,
        topic: { select: { grade: true } },
      },
    });

    // Build a lookup map for sample text (avoids O(n²) find calls)
    const textMap = new Map<string, string>();
    for (const q of questions) {
      textMap.set(q.id, q.questionText);
    }

    const scored: ScoredQuestion[] = questions.map((q) =>
      scoreQuestion({
        id: q.id,
        topicId: q.topicId,
        difficulty: q.difficulty,
        questionText: q.questionText,
        grade: q.topic.grade,
      }),
    );

    const mismatches = scored.filter((s) => s.changed);

    // Summary: count transitions
    const summary: Record<string, number> = {};
    for (const m of mismatches) {
      const key = `${m.oldDifficulty}\u2192${m.newDifficulty}`;
      summary[key] = (summary[key] || 0) + 1;
    }

    // By topic
    const byTopic: Record<string, { total: number; changes: number }> = {};
    for (const s of scored) {
      if (!byTopic[s.topicId]) byTopic[s.topicId] = { total: 0, changes: 0 };
      byTopic[s.topicId].total++;
      if (s.changed) byTopic[s.topicId].changes++;
    }

    // Sample mismatches (up to 50)
    const samples = mismatches.slice(0, 50).map((m) => {
      const fullText = textMap.get(m.id) ?? '';
      return {
        id: m.id,
        topic: m.topicId,
        text: fullText.length > 120 ? fullText.slice(0, 120) + '...' : fullText,
        was: m.oldDifficulty,
        now: m.newDifficulty,
        score: m.score,
      };
    });

    return NextResponse.json({
      total: scored.length,
      mismatches: mismatches.length,
      summary,
      byTopic,
      samples,
    });
  } catch (err) {
    console.error('audit-difficulty GET error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

// ── POST: Apply reclassification ───────────────────────────────────────

const BATCH_SIZE = 500;

export async function POST(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const questions = await prisma.question.findMany({
      select: {
        id: true,
        topicId: true,
        difficulty: true,
        questionText: true,
        topic: { select: { grade: true } },
      },
    });

    const mismatches = questions
      .map((q) =>
        scoreQuestion({
          id: q.id,
          topicId: q.topicId,
          difficulty: q.difficulty,
          questionText: q.questionText,
          grade: q.topic.grade,
        }),
      )
      .filter((s) => s.changed);

    if (mismatches.length === 0) {
      return NextResponse.json({ updated: 0 });
    }

    // Batch update in transactions of BATCH_SIZE
    let updated = 0;
    for (let i = 0; i < mismatches.length; i += BATCH_SIZE) {
      const batch = mismatches.slice(i, i + BATCH_SIZE);
      await prisma.$transaction(
        batch.map((m) =>
          prisma.question.update({
            where: { id: m.id },
            data: { difficulty: m.newDifficulty },
          }),
        ),
      );
      updated += batch.length;
    }

    return NextResponse.json({ updated });
  } catch (err) {
    console.error('audit-difficulty POST error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}

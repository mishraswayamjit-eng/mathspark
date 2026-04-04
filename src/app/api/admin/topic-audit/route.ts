import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsForGrade } from '@/data/topicTree';

export const dynamic = 'force-dynamic';

function authorize(req: NextRequest): boolean {
  const secret = process.env.SEED_SECRET;
  if (!secret) return false;
  const { searchParams } = new URL(req.url);
  return searchParams.get('secret') === secret;
}

// ── GET /api/admin/topic-audit?secret=xxx[&grade=4] ─────────────────────────
// Returns per-topic: total count, usable count, difficulty breakdown

export async function GET(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const gradeParam = searchParams.get('grade');
  const grades = gradeParam ? [parseInt(gradeParam, 10)] : [2, 3, 4, 5, 6, 7, 8, 9];

  try {
    const report: Record<string, {
      topics: Array<{
        topicId: string;
        name: string;
        subTopicKey?: string;
        examWeight: number;
        total: number;
        usable: number;
        easy: number;
        medium: number;
        hard: number;
        blueprintNeed: number;
        coverage: string;
      }>;
      totalQuestions: number;
      totalUsable: number;
    }> = {};

    for (const grade of grades) {
      const topics = getTopicsForGrade(grade);
      const topicResults: typeof report[string]['topics'] = [];
      let gradeTotalQ = 0;
      let gradeTotalU = 0;

      // Get all questions for this grade's DB topic IDs in one query
      const dbTopicIds = [...new Set(topics.map(t => t.dbTopicId))];
      const allQuestions = await prisma.question.findMany({
        where: { topicId: { in: dbTopicIds } },
        select: { topicId: true, subTopic: true, difficulty: true, questionText: true, correctAnswer: true, option1: true, option2: true, option3: true, option4: true },
      });

      for (const topic of topics) {
        // Skip IPM past paper pools from audit
        if (topic.id.endsWith('_ipm')) continue;

        // Filter questions for this topic
        let topicQs = allQuestions.filter(q => q.topicId === topic.dbTopicId);

        // If subTopicKey exists, further filter by subTopic ILIKE
        if (topic.subTopicKey) {
          const key = topic.subTopicKey.toLowerCase();
          topicQs = topicQs.filter(q =>
            (q.subTopic ?? '').toLowerCase().includes(key)
          );
        }

        const total = topicQs.length;

        // Count usable (non-empty fields)
        const usable = topicQs.filter(q =>
          q.questionText && q.correctAnswer && q.option1 && q.option2 && q.option3 && q.option4
        ).length;

        const easy = topicQs.filter(q => q.difficulty === 'Easy').length;
        const medium = topicQs.filter(q => q.difficulty === 'Medium').length;
        const hard = topicQs.filter(q => q.difficulty === 'Hard').length;

        // Blueprint need: for Grade 4, use the fixed blueprint count; for others, estimate from examWeight
        const blueprintNeed = Math.max(2, Math.round(topic.examWeight * 40));

        let coverage = 'ok';
        if (usable < blueprintNeed) coverage = 'low';
        if (usable < blueprintNeed * 3) coverage = 'thin'; // want at least 3x for variety
        if (usable >= blueprintNeed * 5) coverage = 'rich';
        if (usable === 0) coverage = 'empty';

        topicResults.push({
          topicId: topic.dbTopicId,
          name: topic.name,
          subTopicKey: topic.subTopicKey,
          examWeight: topic.examWeight,
          total,
          usable,
          easy,
          medium,
          hard,
          blueprintNeed,
          coverage,
        });

        gradeTotalQ += total;
        gradeTotalU += usable;
      }

      report[`grade${grade}`] = {
        topics: topicResults,
        totalQuestions: gradeTotalQ,
        totalUsable: gradeTotalU,
      };
    }

    return NextResponse.json(report);
  } catch (err) {
    return NextResponse.json(
      { error: `Audit failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}

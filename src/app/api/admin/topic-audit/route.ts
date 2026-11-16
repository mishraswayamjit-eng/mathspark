import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsForGrade } from '@/data/topicTree';
import { verifySecret } from '@/lib/adminAuth';
import { matchesSubTopicKey } from '@/lib/sharedUtils';
import { aiSourceFilter } from '@/lib/db';
import seedIdList from '@/data/bank/seedIds.json';

// The ids in the seed file (built by scripts/bank/build_seed_ids.py). A
// question in the database whose id is not here exists only in the database.
const SEED_IDS: { [id: string]: true } = {};
for (let i = 0; i < (seedIdList as string[]).length; i++) SEED_IDS[(seedIdList as string[])[i]] = true;

/** How the whole bank of one grade is made up, counting each question once. */
interface BankReport {
  total: number;
  inSeedFile: number;
  databaseOnly: number;
  /** Questions no topic of the grade picks up: they only appear in mixed practice. */
  reachedByNoTopic: number;
  /** Questions picked up by more than one topic. */
  reachedBySeveral: number;
  bySource: Array<{
    source: string;
    total: number;
    inSeedFile: number;
    databaseOnly: number;
    reachedByNoTopic: number;
    /** False when this source is switched off for practice (see aiSourceFilter). */
    servedInPractice: boolean;
  }>;
  /** The commonest sub-topic labels no topic picks up, largest first. */
  unreachedLabels: Array<{ label: string; total: number; databaseOnly: number }>;
}

export const dynamic = 'force-dynamic';

function authorize(req: NextRequest): boolean {
  const { searchParams } = new URL(req.url);
  return verifySecret(searchParams.get('secret'));
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
      bank: BankReport;
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
      const dbTopicIds = Array.from(new Set(topics.map(t => t.dbTopicId)));
      const allQuestions = await prisma.question.findMany({
        where: { topicId: { in: dbTopicIds } },
        select: { id: true, source: true, topicId: true, subTopic: true, difficulty: true, questionText: true, correctAnswer: true, option1: true, option2: true, option3: true, option4: true },
      });

      for (const topic of topics) {
        // Skip IPM past paper pools from audit
        if (topic.id.endsWith('_ipm')) continue;

        // Filter questions for this topic
        let topicQs = allQuestions.filter(q => q.topicId === topic.dbTopicId);

        // If subTopicKey exists, further filter by word-boundary subTopic match
        if (topic.subTopicKey) {
          const key = topic.subTopicKey;
          topicQs = topicQs.filter(q => matchesSubTopicKey(q.subTopic, key));
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

      // The whole bank of the grade, each question counted once.
      const switchedOff = aiSourceFilter().source?.notIn ?? [];
      const keys: string[] = [];
      topics.forEach((t) => {
        if (!t.id.endsWith('_ipm') && t.subTopicKey && keys.indexOf(t.subTopicKey) === -1) keys.push(t.subTopicKey);
      });
      const sources: { [source: string]: { total: number; inSeedFile: number; databaseOnly: number; reachedByNoTopic: number } } = {};
      const labels: { [label: string]: { total: number; databaseOnly: number } } = {};
      let inSeedFile = 0;
      let reachedByNoTopic = 0;
      let reachedBySeveral = 0;
      for (let i = 0; i < allQuestions.length; i++) {
        const q = allQuestions[i];
        const inSeed = SEED_IDS[q.id] === true;
        // A grade with no sub-topic keys (Grade 4 chapters) reaches every question through its chapter.
        let hits = keys.length === 0 ? 1 : 0;
        for (let k = 0; k < keys.length; k++) {
          if (matchesSubTopicKey(q.subTopic, keys[k])) hits++;
        }
        const src = q.source || '(none)';
        if (!sources[src]) sources[src] = { total: 0, inSeedFile: 0, databaseOnly: 0, reachedByNoTopic: 0 };
        sources[src].total++;
        if (inSeed) { sources[src].inSeedFile++; inSeedFile++; } else { sources[src].databaseOnly++; }
        if (hits > 1) reachedBySeveral++;
        if (hits === 0) {
          reachedByNoTopic++;
          sources[src].reachedByNoTopic++;
          const label = q.subTopic || '(no label)';
          if (!labels[label]) labels[label] = { total: 0, databaseOnly: 0 };
          labels[label].total++;
          if (!inSeed) labels[label].databaseOnly++;
        }
      }
      const bank: BankReport = {
        total: allQuestions.length,
        inSeedFile,
        databaseOnly: allQuestions.length - inSeedFile,
        reachedByNoTopic,
        reachedBySeveral,
        bySource: Object.keys(sources)
          .map((source) => ({
            source,
            total: sources[source].total,
            inSeedFile: sources[source].inSeedFile,
            databaseOnly: sources[source].databaseOnly,
            reachedByNoTopic: sources[source].reachedByNoTopic,
            servedInPractice: switchedOff.indexOf(source) === -1,
          }))
          .sort((x, y) => y.total - x.total),
        unreachedLabels: Object.keys(labels)
          .map((label) => ({ label, total: labels[label].total, databaseOnly: labels[label].databaseOnly }))
          .sort((x, y) => y.total - x.total)
          .slice(0, 30),
      };

      report[`grade${grade}`] = {
        bank,
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

import { prisma } from './db';
import type { Difficulty } from '@/types';
import { getUnmetPrerequisites } from './prerequisites';

type QuestionResult = (Awaited<ReturnType<typeof prisma.question.findFirst>> & {
  prerequisiteRedirect?: string; // topicId that student should tackle first
}) | null;

const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

function shift(d: Difficulty, delta: number): Difficulty {
  const idx = Math.max(0, Math.min(2, DIFFICULTIES.indexOf(d) + delta));
  return DIFFICULTIES[idx];
}

function shuffle<T>(arr: T[]): void {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

async function pickFromDifficulty(
  topicId: string,
  exclude: string[],
  difficulty: Difficulty,
) {
  const pool = await prisma.question.findMany({
    where: { topicId, id: { notIn: exclude }, difficulty },
    take: 20,
  });
  shuffle(pool);
  return pool[0] ?? null;
}

/**
 * Adaptive next-question picker.
 *
 * Rules (from CLAUDE.md):
 *  - 3 wrong in a row → drop difficulty 1 level
 *  - 5 right in a row → raise difficulty 1 level
 *  - Never repeat a question in the same session (seenIds)
 *  - Base difficulty derived from current mastery level
 *
 * ZPD distribution (applied after streak adjustment):
 *  - 70%  → base difficulty (current level / ZPD)
 *  - 20%  → SRS review band: surface a mastered topic due for review
 *  - 10%  → one level above base (stretch)
 *
 * Prerequisite check:
 *  - If the student has never attempted a prerequisite topic, serve an Easy
 *    question from that topic first (soft redirect — not a hard block).
 */
export async function getNextQuestion(
  studentId: string,
  topicId: string,
  seenIds: string[]        = [],
  consecutiveWrong: number = 0,
  consecutiveRight: number = 0,
): Promise<QuestionResult> {
  // Check prerequisites before serving the requested topic
  const unmetPrereqs = await getUnmetPrerequisites(studentId, topicId);
  if (unmetPrereqs.length > 0) {
    const prereqTopicId = unmetPrereqs[0];
    // Serve an Easy question from the first unmet prerequisite topic
    const prereqQuestion = await prisma.question.findFirst({
      where: { topicId: prereqTopicId, difficulty: 'Easy' },
      orderBy: { id: 'asc' },
    });
    if (prereqQuestion) {
      return { ...prereqQuestion, prerequisiteRedirect: prereqTopicId };
    }
    // If no Easy questions found, try any question from the prereq topic
    const fallbackQuestion = await prisma.question.findFirst({
      where: { topicId: prereqTopicId },
      orderBy: { id: 'asc' },
    });
    if (fallbackQuestion) {
      return { ...fallbackQuestion, prerequisiteRedirect: prereqTopicId };
    }
  }

  const progress = await prisma.progress.findUnique({
    where: { studentId_topicId: { studentId, topicId } },
  });

  // Derive base difficulty from mastery
  let base: Difficulty = 'Medium';
  if (!progress || progress.mastery === 'NotStarted') base = 'Easy';
  else if (progress.mastery === 'Mastered') base = 'Hard';

  // Streak adjustments
  if (consecutiveWrong >= 3) base = shift(base, -1);
  else if (consecutiveRight >= 5) base = shift(base, 1);

  const exclude = seenIds.length > 0 ? seenIds : [];

  // ZPD roll: 0–0.69 → base, 0.70–0.89 → SRS review band, 0.90–0.99 → stretch (base+1)
  const roll = Math.random();
  let targetDiff: Difficulty;
  if (roll < 0.70) {
    targetDiff = base;
  } else if (roll < 0.90) {
    // SRS Review Band (20% chance): surface a mastered topic due for review
    const reviewProgress = await prisma.progress.findFirst({
      where: {
        studentId,
        mastery: 'Mastered',
        nextReviewAt: { lte: new Date() },
        topicId: { not: topicId }, // different topic
      },
      orderBy: { nextReviewAt: 'asc' }, // most overdue first
    });

    if (reviewProgress) {
      const reviewPool = await prisma.question.findMany({
        where: {
          topicId: reviewProgress.topicId,
          id: { notIn: exclude },
        },
        take: 10,
      });
      shuffle(reviewPool);
      if (reviewPool.length > 0) return reviewPool[0];
    }
    // Fall through to base difficulty if no SRS review found
    targetDiff = base;
  } else {
    targetDiff = shift(base, +1); // stretch
  }

  // Try the rolled difficulty band first
  if (targetDiff !== base) {
    const question = await pickFromDifficulty(topicId, exclude, targetDiff);
    if (question) return question;
  }

  // Fall back to base difficulty
  const baseQuestion = await pickFromDifficulty(topicId, exclude, base);
  if (baseQuestion) return baseQuestion;

  // Final fallback: any unseen question in the topic
  const pool = await prisma.question.findMany({
    where: { topicId, id: { notIn: exclude } },
    take: 20,
  });
  shuffle(pool);
  return pool[0] ?? null;
}

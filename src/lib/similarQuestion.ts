import { prisma } from './db';

type Difficulty = 'Easy' | 'Medium' | 'Hard';
const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

export interface FindSimilarParams {
  questionId: string;
  subTopic:   string;
  topicId:    string;
  difficulty: string;
  wasCorrect: boolean;
}

function pickRandom<T>(arr: T[]): T | null {
  if (arr.length === 0) return null;
  return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * Find the best "repeat similar" question for a student.
 *
 * Priority order:
 *  1. Same subTopic + auto_generated  (number-swapped variants — ideal)
 *  2. Same subTopic + hand_crafted    (same concept, full solution)
 *  3. Same topicId  + similar difficulty ±1 (broader topic fallback)
 *  4. null — nothing suitable found
 *
 * Difficulty adjustment:
 *  - Student was WRONG → serve same or one level EASIER (reinforce)
 *  - Student was RIGHT → serve same or one level HARDER (challenge)
 */
export async function findSimilarQuestion(
  params: FindSimilarParams,
  excludeIds: string[],
) {
  const { questionId, subTopic, topicId, difficulty, wasCorrect } = params;

  // Build exclusion list (always exclude the original question)
  const excluded = Array.from(new Set<string>([questionId, ...excludeIds]));

  // Compute allowed difficulty range
  const origIdx = DIFFICULTIES.indexOf(difficulty as Difficulty);
  const lo = wasCorrect ? origIdx       : Math.max(origIdx - 1, 0);
  const hi = wasCorrect ? Math.min(origIdx + 1, 2) : origIdx;
  const allowedDiff = DIFFICULTIES.slice(lo, hi + 1);

  // Priority 1 — same subTopic, auto_generated (number-swapped variants)
  const p1 = await prisma.question.findMany({
    where: {
      subTopic,
      source:     'auto_generated',
      difficulty: { in: allowedDiff },
      id:         { notIn: excluded },
    },
    take: 20,
  });
  if (p1.length > 0) return pickRandom(p1);

  // Priority 2 — same subTopic, hand_crafted
  const p2 = await prisma.question.findMany({
    where: {
      subTopic,
      source:     'hand_crafted',
      difficulty: { in: allowedDiff },
      id:         { notIn: excluded },
    },
    take: 10,
  });
  if (p2.length > 0) return pickRandom(p2);

  // Priority 3 — same topic, similar difficulty (±1 level)
  const p3 = await prisma.question.findMany({
    where: {
      topicId,
      difficulty: { in: allowedDiff },
      id:         { notIn: excluded },
    },
    take: 20,
  });
  if (p3.length > 0) return pickRandom(p3);

  return null;
}

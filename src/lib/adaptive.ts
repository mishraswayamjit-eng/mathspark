import { prisma } from './db';
import type { Difficulty } from '@/types';

const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

function shift(d: Difficulty, delta: number): Difficulty {
  const idx = Math.max(0, Math.min(2, DIFFICULTIES.indexOf(d) + delta));
  return DIFFICULTIES[idx];
}

/**
 * Adaptive next-question picker.
 *
 * Rules (from CLAUDE.md):
 *  - 3 wrong in a row → drop difficulty 1 level
 *  - 5 right in a row → raise difficulty 1 level
 *  - Never repeat a question in the same session (seenIds)
 *  - Base difficulty derived from current mastery level
 */
export async function getNextQuestion(
  studentId: string,
  topicId: string,
  seenIds: string[]        = [],
  consecutiveWrong: number = 0,
  consecutiveRight: number = 0,
) {
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

  // Try target difficulty first
  const question = await prisma.question.findFirst({
    where: { topicId, id: { notIn: exclude }, difficulty: base },
    orderBy: { id: 'asc' },
  });
  if (question) return question;

  // Fallback: any unseen question from this topic
  return prisma.question.findFirst({
    where: { topicId, id: { notIn: exclude } },
    orderBy: { id: 'asc' },
  });
}

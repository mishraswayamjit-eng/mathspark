import { prisma } from './db';
import type { MasteryLevel } from '@/types';

/**
 * Recalculate mastery from the student's last 10 attempts on a topic.
 *   >= 80% correct → Mastered
 *   >= 40% correct → Practicing
 *   <  40% correct → NotStarted
 */
export async function calculateMastery(
  studentId: string,
  topicId: string,
): Promise<MasteryLevel> {
  const recent = await prisma.attempt.findMany({
    where: {
      studentId,
      question: { topicId },
    },
    orderBy: { createdAt: 'desc' },
    take: 10,
  });

  if (recent.length === 0) return 'NotStarted';

  const ratio = recent.filter((a) => a.isCorrect).length / recent.length;
  if (ratio >= 0.8) return 'Mastered';
  if (ratio >= 0.4) return 'Practicing';
  return 'NotStarted';
}

/**
 * Recalculate and persist mastery + aggregate counts for a student/topic pair.
 * Also exported as updateMastery to match the spec interface.
 */
export async function updateProgress(studentId: string, topicId: string): Promise<void> {
  const [mastery, all] = await Promise.all([
    calculateMastery(studentId, topicId),
    prisma.attempt.findMany({
      where: { studentId, question: { topicId } },
      select: { isCorrect: true },
    }),
  ]);

  const attempted = all.length;
  const correct   = all.filter((a) => a.isCorrect).length;

  await prisma.progress.upsert({
    where:  { studentId_topicId: { studentId, topicId } },
    update: { attempted, correct, mastery },
    create: { studentId, topicId, attempted, correct, mastery },
  });
}

/** Alias matching the task spec. */
export const updateMastery = updateProgress;

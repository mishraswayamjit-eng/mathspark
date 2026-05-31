import { prisma } from './db';
import type { MasteryLevel } from '@/types';

/**
 * Recalculate and persist mastery + aggregate counts for a student/topic pair.
 * Single DB fetch: all attempts ordered newest-first; mastery derived from the
 * most-recent 10, all-time totals derived from the full set.
 */
export async function updateProgress(studentId: string, topicId: string): Promise<void> {
  // Single fetch: all attempts for this student+topic, newest first
  const all = await prisma.attempt.findMany({
    where: { studentId, question: { topicId } },
    orderBy: { createdAt: 'desc' },
    select: { isCorrect: true },
  });

  // Mastery from last 10
  const recent = all.slice(0, 10);
  const mastery: MasteryLevel = recent.length === 0
    ? 'NotStarted'
    : recent.filter((a) => a.isCorrect).length / recent.length >= 0.8
      ? 'Mastered'
      : recent.filter((a) => a.isCorrect).length / recent.length >= 0.4
        ? 'Practicing'
        : 'NotStarted';

  // All-time counts
  const attempted = all.length;
  const correct   = all.filter((a) => a.isCorrect).length;

  await prisma.progress.upsert({
    where:  { studentId_topicId: { studentId, topicId } },
    update: { attempted, correct, mastery },
    create: { studentId, topicId, attempted, correct, mastery },
  });
}

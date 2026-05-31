import { prisma } from './db';
import type { MasteryLevel } from '@/types';

export async function calculateMastery(studentId: string, topicId: string): Promise<MasteryLevel> {
  const recent = await prisma.attempt.findMany({
    where: { studentId, question: { topicId } },
    orderBy: { createdAt: 'desc' },
    take: 10,
    select: { isCorrect: true },
  });
  if (recent.length === 0) return 'NotStarted';
  const ratio = recent.filter((a) => a.isCorrect).length / recent.length;
  return ratio >= 0.8 ? 'Mastered' : ratio >= 0.4 ? 'Practicing' : 'NotStarted';
}

export async function updateProgress(studentId: string, topicId: string): Promise<void> {
  const mastery = await calculateMastery(studentId, topicId);

  const all = await prisma.attempt.findMany({
    where: { studentId, question: { topicId } },
    select: { isCorrect: true },
  });

  const attempted = all.length;
  const correct   = all.filter((a) => a.isCorrect).length;

  // Compute SRS fields
  let nextReviewAt: Date | null = null;
  let reviewInterval = 1;

  if (mastery === 'Mastered') {
    // Fetch current progress to see if already mastered (to increment interval)
    const current = await prisma.progress.findUnique({
      where: { studentId_topicId: { studentId, topicId } },
      select: { mastery: true, reviewInterval: true },
    });

    if (current?.mastery === 'Mastered') {
      // Already mastered — increment interval (1 → 3 → 7 → 14 → 30, capped)
      const intervals = [1, 3, 7, 14, 30];
      const currentIdx = intervals.indexOf(current.reviewInterval ?? 1);
      reviewInterval = intervals[Math.min(currentIdx + 1, intervals.length - 1)];
    } else {
      // Newly mastered — start at 1 day
      reviewInterval = 1;
    }

    nextReviewAt = new Date(Date.now() + reviewInterval * 24 * 60 * 60 * 1000);
  }

  await prisma.progress.upsert({
    where:  { studentId_topicId: { studentId, topicId } },
    update: { attempted, correct, mastery, nextReviewAt, reviewInterval },
    create: { studentId, topicId, attempted, correct, mastery, nextReviewAt, reviewInterval },
  });
}

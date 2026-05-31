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

  await prisma.progress.upsert({
    where:  { studentId_topicId: { studentId, topicId } },
    update: { attempted, correct, mastery },
    create: { studentId, topicId, attempted, correct, mastery },
  });
}

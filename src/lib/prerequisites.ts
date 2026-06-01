import { prisma } from './db';
import type { MasteryLevel } from '@/types';

// Topic prerequisite graph: key → list of topics that must not be NotStarted
export const PREREQUISITES: Record<string, string[]> = {
  'ch07-08': ['ch01-05'],
  'ch09-10': ['ch01-05', 'ch06'],
  'ch11':    ['ch07-08'],
  'ch12':    ['ch11'],
  'ch13':    ['ch09-10'],
  'ch14':    ['ch13'],
  'ch15':    ['ch09-10'],
  'ch16':    ['ch09-10'],
  'ch19':    ['ch18'],
  'ch20':    ['ch18'],
  'ch21':    ['ch18'],
};

// Returns prerequisites that are still NotStarted/not attempted
export async function getUnmetPrerequisites(
  studentId: string,
  topicId: string,
): Promise<string[]> {
  const prereqs = PREREQUISITES[topicId] ?? [];
  if (prereqs.length === 0) return [];

  const progress = await prisma.progress.findMany({
    where: { studentId, topicId: { in: prereqs } },
    select: { topicId: true, mastery: true, attempted: true },
  });

  const progressMap: Record<string, { mastery: MasteryLevel; attempted: number }> = {};
  for (const p of progress) {
    progressMap[p.topicId] = { mastery: p.mastery as MasteryLevel, attempted: p.attempted };
  }

  // A prerequisite is "unmet" if the student has never attempted it
  return prereqs.filter((p) => !progressMap[p] || progressMap[p].attempted === 0);
}

// Synchronous variant for client components that already have mastery data in memory.
// masteryMap: topicId → mastery level string ('NotStarted' | 'Practicing' | 'Mastered')
export function getUnmetPrerequisiteIds(
  topicId: string,
  masteryMap: Record<string, string>,
): string[] {
  const prereqs = PREREQUISITES[topicId] ?? [];
  return prereqs.filter((p) => !masteryMap[p] || masteryMap[p] === 'NotStarted');
}

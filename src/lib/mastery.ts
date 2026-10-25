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
    select: { isCorrect: true },
  });

  if (recent.length === 0) return 'NotStarted';

  const ratio = recent.filter((a) => a.isCorrect).length / recent.length;
  if (ratio >= 0.8) return 'Mastered';
  if (ratio >= 0.4) return 'Practicing';
  return 'NotStarted';
}

// Coalesce concurrent recomputes per (student, topic). `updateProgress` is
// fired fire-and-forget on every attempt, so a burst of rapid answers would
// otherwise stampede the DB with many redundant full-table recounts. While one
// recompute is in flight we only mark the key dirty; the running pass then does
// exactly one trailing recompute so the final persisted counts still reflect
// the latest attempts (never a stale overwrite). Keyed per warm instance.
const inFlightProgress = new Map<string, boolean>(); // key -> dirty

async function recomputeProgress(studentId: string, topicId: string): Promise<void> {
  const where = { studentId, question: { topicId } };

  const [recent, attempted, correct] = await prisma.$transaction([
    prisma.attempt.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: 10,
      select: { isCorrect: true },
    }),
    prisma.attempt.count({ where }),
    prisma.attempt.count({ where: { studentId, question: { topicId }, isCorrect: true } }),
  ]);

  // Derive mastery from recent 10 attempts
  let mastery: MasteryLevel = 'NotStarted';
  if (recent.length > 0) {
    const ratio = recent.filter((a) => a.isCorrect).length / recent.length;
    if (ratio >= 0.8) mastery = 'Mastered';
    else if (ratio >= 0.4) mastery = 'Practicing';
  }

  await prisma.progress.upsert({
    where:  { studentId_topicId: { studentId, topicId } },
    update: { attempted, correct, mastery },
    create: { studentId, topicId, attempted, correct, mastery },
  });
}

/**
 * Recalculate and persist mastery + aggregate counts for a student/topic pair.
 * Uses a single batched transaction (3 queries → 1 round-trip) + 1 upsert.
 * Concurrent calls for the same (student, topic) are coalesced into one running
 * recompute plus a single trailing pass (see `inFlightProgress`).
 */
export async function updateProgress(studentId: string, topicId: string): Promise<void> {
  const key = `${studentId}::${topicId}`;

  // A recompute is already running for this key — mark dirty and let it catch up.
  if (inFlightProgress.has(key)) {
    inFlightProgress.set(key, true);
    return;
  }

  inFlightProgress.set(key, false);
  try {
    do {
      // Clear the dirty flag before computing; any call that arrives during the
      // recompute will set it again, triggering exactly one more pass.
      inFlightProgress.set(key, false);
      await recomputeProgress(studentId, topicId);
    } while (inFlightProgress.get(key));
  } finally {
    inFlightProgress.delete(key);
  }
}

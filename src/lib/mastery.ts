import { prisma } from './db';
import type { MasteryLevel } from '@/types';

/**
 * Recalculate mastery from the student's last 10 attempts on a topic.
 *   >= 80% correct → Mastered
 *   >= 40% correct → Practicing
 *   <  40% correct → NotStarted
 */
// India has one time zone and no daylight saving: UTC + 5:30.
const IST_OFFSET_MS = 330 * 60 * 1000;

/** How many recent attempts are read to find the last 10 first tries. */
const RECENT_READ = 40;

/** One recent attempt, as read for mastery. */
interface RecentAttempt {
  isCorrect: boolean;
  questionId?: string;
  createdAt?: Date | string;
}

/** The calendar day in India an attempt was made on, e.g. "2026-11-17". */
function indiaDay(when: Date | string): string {
  return new Date(new Date(when).getTime() + IST_OFFSET_MS).toISOString().slice(0, 10);
}

/**
 * The last 10 attempts that count for mastery, from a newest-first list.
 *
 * Only the FIRST attempt at a question on a given India-time day counts. Later
 * tries at the same question that day (the review round, "review mistakes")
 * are made after the correct answer has been shown, so they say little about
 * what the child knows. A row without a question id or a time is always kept.
 */
export function lastTenFirstTries<T extends RecentAttempt>(newestFirst: T[]): T[] {
  const seen: Record<string, boolean> = Object.create(null);
  const kept: T[] = [];
  // Oldest first, so the first try of the day is the one that is kept.
  for (let i = newestFirst.length - 1; i >= 0; i--) {
    const a = newestFirst[i];
    if (a.questionId && a.createdAt) {
      const key = a.questionId + '|' + indiaDay(a.createdAt);
      if (seen[key]) continue;
      seen[key] = true;
    }
    kept.push(a);
  }
  return kept.slice(-10);
}

export async function calculateMastery(
  studentId: string,
  topicId: string,
): Promise<MasteryLevel> {
  const read = await prisma.attempt.findMany({
    where: {
      studentId,
      question: { topicId },
    },
    orderBy: { createdAt: 'desc' },
    take: RECENT_READ,
    select: { isCorrect: true, questionId: true, createdAt: true },
  });
  const recent = lastTenFirstTries(read);

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

  const [read, attempted, correct] = await prisma.$transaction([
    prisma.attempt.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: RECENT_READ,
      select: { isCorrect: true, questionId: true, createdAt: true },
    }),
    prisma.attempt.count({ where }),
    prisma.attempt.count({ where: { studentId, question: { topicId }, isCorrect: true } }),
  ]);

  // Derive mastery from the last 10 first tries (see lastTenFirstTries)
  const recent = lastTenFirstTries(read);
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

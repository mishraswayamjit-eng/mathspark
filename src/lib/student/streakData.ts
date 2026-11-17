// SERVER ONLY: talks to the database. Never import this from a client component.
//
// The one query every streak is counted from. Earlier each screen counted its
// streak from whatever attempts it had already loaded (the newest 100, or the
// oldest 300), so a child who answers many questions a day saw a streak that
// stopped growing, and different screens showed different numbers.

import { prisma } from '@/lib/db';
import { MS_PER_DAY } from '@/lib/timeConstants';
import { computeStreak } from '@/lib/sharedUtils';

/** How far back a streak is counted. A streak cannot be longer than this. */
export const STREAK_LOOKBACK_DAYS = 366;
/**
 * Upper bound on rows read (each row is one timestamp). About 16 answers a day,
 * every day, for the whole look-back. Rows are newest first, so if a child ever
 * goes over it only the far end of a very long streak is cut short.
 */
export const STREAK_MAX_ROWS = 6000;

/** When the child answered, newest first: nothing but the time of each answer. */
export function loadStreakAttempts(
  studentId: string,
  now: Date = new Date(),
): Promise<Array<{ createdAt: Date }>> {
  return prisma.attempt.findMany({
    where: {
      studentId,
      createdAt: { gte: new Date(now.getTime() - STREAK_LOOKBACK_DAYS * MS_PER_DAY) },
    },
    select: { createdAt: true },
    orderBy: { createdAt: 'desc' },
    take: STREAK_MAX_ROWS,
  });
}

/** Days practised in a row for one child (India-time days; see `computeStreak`). */
export async function loadStreakDays(studentId: string, now: Date = new Date()): Promise<number> {
  const attempts = await loadStreakAttempts(studentId, now);
  return computeStreak(attempts, false, now);
}

/**
 * Shared dashboard computation helpers used by /api/dashboard and /api/home.
 */
import type { RecentSession } from '@/types';
import { istDayNumber, istDayStart } from '@/lib/sharedUtils';
import { MS_PER_DAY } from '@/lib/timeConstants';

// Day number 0 (1 January 1970) was a Thursday.
const WEEKDAY_SHORT = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

/**
 * The first instant of the 7-day window the weekly chart covers (India-time
 * days, today included). Use it as the lower bound of the attempts query.
 */
export function weeklyWindowStart(now: Date = new Date()): Date {
  return new Date(istDayStart(now).getTime() - 6 * MS_PER_DAY);
}

/**
 * Compute weekly chart data: attempts per day for the last 7 India-time days.
 * Feed it every attempt since `weeklyWindowStart()`, not a fixed number of
 * rows: a row limit cuts the bars short for a child who answers a lot.
 * @param onlyCorrect If true, count only correct attempts
 */
export function computeWeeklyData(
  attempts: Array<{ createdAt: Date; isCorrect?: boolean }>,
  onlyCorrect = false,
  now: Date = new Date(),
) {
  const today = istDayNumber(now);
  const counts: Record<number, number> = {};
  for (let i = 0; i < attempts.length; i++) {
    const a = attempts[i];
    if (onlyCorrect && !a.isCorrect) continue;
    const day = istDayNumber(a.createdAt);
    counts[day] = (counts[day] || 0) + 1;
  }
  const out: Array<{ date: string; count: number }> = [];
  for (let back = 6; back >= 0; back--) {
    const day = today - back;
    out.push({
      date:  WEEKDAY_SHORT[(((day + 4) % 7) + 7) % 7],
      count: counts[day] || 0,
    });
  }
  return out;
}

/**
 * Compute recent activity: last N (topicId x calendar-day) sessions.
 */
export function computeRecentActivity(
  attempts: Array<{ isCorrect: boolean; createdAt: Date; question: { topicId: string } }>,
  topicMap: Map<string, string>,
  limit = 5,
): RecentSession[] {
  const groups = new Map<string, { topicId: string; attempted: number; correct: number; latest: Date }>();

  for (const a of attempts) {
    const topicId = a.question.topicId;
    const dayKey  = istDayNumber(a.createdAt);
    const key     = `${topicId}__${dayKey}`;

    if (!groups.has(key)) {
      groups.set(key, { topicId, attempted: 0, correct: 0, latest: new Date(a.createdAt) });
    }
    const g = groups.get(key)!;
    g.attempted++;
    if (a.isCorrect) g.correct++;
    const at = new Date(a.createdAt);
    if (at > g.latest) g.latest = at;
  }

  return Array.from(groups.values())
    .sort((a, b) => b.latest.getTime() - a.latest.getTime())
    .slice(0, limit)
    .map((g) => ({
      topicId:   g.topicId,
      topicName: topicMap.get(g.topicId) ?? g.topicId,
      attempted: g.attempted,
      correct:   g.correct,
      createdAt: g.latest.toISOString(),
    }));
}

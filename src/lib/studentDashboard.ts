/**
 * Shared dashboard computation helpers used by /api/dashboard and /api/home.
 */
import type { RecentSession } from '@/types';

/**
 * Compute weekly chart data: attempts per day for last 7 days.
 * @param onlyCorrect If true, count only correct attempts
 */
export function computeWeeklyData(
  attempts: Array<{ createdAt: Date; isCorrect?: boolean }>,
  onlyCorrect = false,
) {
  const today = new Date();
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(d.getDate() - (6 - i));
    const dateStr = d.toDateString();
    return {
      date:  d.toLocaleDateString('en-IN', { weekday: 'short' }),
      count: attempts.filter((a) => {
        if (onlyCorrect && !a.isCorrect) return false;
        return new Date(a.createdAt).toDateString() === dateStr;
      }).length,
    };
  });
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
    const dayKey  = new Date(a.createdAt).toDateString();
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

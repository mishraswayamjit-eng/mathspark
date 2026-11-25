import { isCleanWord } from '@/lib/profanityFilter';

/** Canonical topic ordering for consistent display across all pages */
export const TOPIC_ORDER: readonly string[] = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

// ── India-time days ───────────────────────────────────────────────────────────
// The children are in India (UTC+5:30); the server's own clock is not. Every
// "today", "this week" and streak is counted in India-time calendar days.

const IST_OFFSET_MS = 5.5 * 3_600_000;
const DAY_MS = 86_400_000;

/**
 * The India-time calendar day a moment falls on, as a whole number of days
 * since 1 January 1970. Two moments are on the same India day exactly when
 * their numbers are equal, and yesterday is the number minus one.
 */
export function istDayNumber(when: Date | string | number): number {
  return Math.floor((new Date(when).getTime() + IST_OFFSET_MS) / DAY_MS);
}

/**
 * The key of the daily `UsageLog` row for the India-time day `when` falls on:
 * that calendar date at 00:00 UTC, which is what the `date` column (a plain
 * date) stores. Every reader and writer of the daily log must use this, so the
 * day's XP cap, minutes and chat count all roll over at midnight in India,
 * together with streaks, review XP and the adaptive "today".
 */
export function usageDayKey(when: Date | string | number = new Date()): Date {
  return new Date(istDayNumber(when) * DAY_MS);
}

/** The first instant (as a UTC Date) of the India-time day that `when` falls on. */
export function istDayStart(when: Date | string | number): Date {
  return new Date(istDayNumber(when) * DAY_MS - IST_OFFSET_MS);
}

/**
 * Days practised in a row, in India-time days.
 *
 * The run ends today when the child has practised today. When they have not
 * yet, it ends YESTERDAY: a streak is not shown as lost just because today's
 * first answer has not been given yet. It is 0 only when neither today nor
 * yesterday has an attempt.
 *
 * Feed it attempts that are not cut off after a fixed number of rows (see
 * `loadStreakAttempts` in src/lib/student/streakData.ts): the streak can never
 * be longer than the days the given attempts cover.
 *
 * @param attempts - Array of items with createdAt dates (and optionally isCorrect)
 * @param filterCorrect - If true, only count days with at least 1 correct attempt
 * @param now - The current moment (for tests)
 */
export function computeStreak(
  attempts: Array<{ createdAt: Date; isCorrect?: boolean }>,
  filterCorrect = false,
  now: Date = new Date(),
): number {
  if (attempts.length === 0) return 0;

  const days: Record<number, boolean> = {};
  for (let i = 0; i < attempts.length; i++) {
    const a = attempts[i];
    if (filterCorrect && !a.isCorrect) continue;
    const day = istDayNumber(a.createdAt);
    if (!isNaN(day)) days[day] = true;
  }

  const today = istDayNumber(now);
  let day = days[today] ? today : today - 1;
  let streak = 0;
  while (days[day]) {
    streak++;
    day--;
  }
  return streak;
}

/**
 * Match a question's `subTopic` against a topic node's `subTopicKey` using a
 * word-boundary (prefix) test instead of a raw substring. This prevents
 * cross-contamination where a key appears INSIDE a larger word — e.g. the key
 * "ratio" must not match "Ope(ratio)ns" / "Mensu(ratio)n", and "angle" must not
 * match "Tri(angle)s". The key must start the string or follow a non-alphanumeric
 * character; it need NOT end on a boundary, so stems like "divisib" still match
 * "divisibility" and "square" still matches "squares". An empty key matches all
 * (mirrors the "no filter" case). Case-insensitive.
 */
export function matchesSubTopicKey(
  subTopic: string | null | undefined,
  key: string,
): boolean {
  if (!key) return true;
  const hay = (subTopic ?? '').toLowerCase();
  const needle = key.toLowerCase();
  for (let from = 0; ; ) {
    const idx = hay.indexOf(needle, from);
    if (idx === -1) return false;
    if (idx === 0 || !/[a-z0-9]/.test(hay[idx - 1])) return true;
    from = idx + 1;
  }
}

/**
 * Whether a `gradeRange` tag covers a given grade. Content data files tag entries
 * with either an inclusive `[min, max]` pair (strategies, skill-drill levels) or
 * an enumerated grade list (stories) — both are always contiguous, so a single
 * `min..max` span test is correct for either shape. Untagged entries (missing or
 * short `gradeRange`) are treated as grade-agnostic and always match, preserving
 * the pre-filter behaviour for content that was never tagged.
 */
export function gradeInRange(gradeRange: unknown, grade: number): boolean {
  if (!Array.isArray(gradeRange)) return true;
  const nums = gradeRange.filter((n): n is number => typeof n === 'number');
  if (nums.length < 2) return true;
  return Math.min(...nums) <= grade && grade <= Math.max(...nums);
}

/**
 * Resolve a leaderboard/report display name: prefer student.displayName,
 * otherwise fall back to the first token of the full name.
 */
export function getDisplayName(name: string, displayName?: string | null): string {
  if (displayName) return displayName;
  // The first name is typed freely at sign-up and is not filtered there, so it
  // is not shown to other children when the whole word is a blocked one.
  const first = name.split(' ')[0];
  return isCleanWord(first) ? first : 'Student';
}

/**
 * Build a `Map<topicId, topicName>` from a topic list.
 * Used by dashboard/home/report routes for O(1) topic-name lookup.
 */
export function buildTopicNameMap(
  topics: ReadonlyArray<{ id: string; name: string }>,
): Map<string, string> {
  return new Map(topics.map((t) => [t.id, t.name]));
}

/**
 * Build a `Map<T[K], T>` keyed by the named field. Generic equivalent of
 * `new Map(items.map(i => [i.keyField, i]))` used across dashboard/report
 * routes to index Prisma rows by topicId / cardId / etc.
 */
export function buildLookupMap<T, K extends keyof T>(
  items: ReadonlyArray<T>,
  keyField: K,
): Map<T[K], T> {
  return new Map(items.map((item) => [item[keyField], item]));
}

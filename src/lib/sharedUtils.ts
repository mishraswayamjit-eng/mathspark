/** Canonical topic ordering for consistent display across all pages */
export const TOPIC_ORDER: readonly string[] = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

/**
 * Compute consecutive day streak counting backwards from today.
 * @param attempts - Array of items with createdAt dates (and optionally isCorrect)
 * @param filterCorrect - If true, only count days with at least 1 correct attempt
 */
export function computeStreak(
  attempts: Array<{ createdAt: Date; isCorrect?: boolean }>,
  filterCorrect = false,
): number {
  if (attempts.length === 0) return 0;

  const filtered = filterCorrect
    ? attempts.filter((a) => a.isCorrect)
    : attempts;

  const days = new Set(
    filtered.map((a) => new Date(a.createdAt).toDateString()),
  );

  const today = new Date();
  let streak = 0;
  for (let i = 0; i < 365; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    if (days.has(d.toDateString())) streak++;
    else break;
  }
  return streak;
}

/**
 * Resolve a leaderboard/report display name: prefer student.displayName,
 * otherwise fall back to the first token of the full name.
 */
export function getDisplayName(name: string, displayName?: string | null): string {
  return displayName ?? name.split(' ')[0];
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

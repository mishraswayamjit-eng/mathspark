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

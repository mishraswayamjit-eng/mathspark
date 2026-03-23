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

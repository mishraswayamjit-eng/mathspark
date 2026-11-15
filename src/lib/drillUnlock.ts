/**
 * Which skill-drill levels are open to a child.
 *
 * One rule, used by both the skill-drill hub and the level page so they always
 * agree. Pure: it only reads the progress kept on the device and the list of
 * levels the child is shown. Safe to import into a client component.
 *
 * A child is only shown the levels made for their grade (the API leaves the
 * others out), so the levels they see may start at L2 and may skip a level that
 * has no sessions. A level is open when:
 *   - it is the lowest level the child is shown (there is nothing before it
 *     that they could finish first), or
 *   - the device has it marked as unlocked, or
 *   - the best score on the level shown just before it is DRILL_UNLOCK_SCORE
 *     or more.
 */

export interface DrillLevelProgress {
  bestScore: number;
  /** Session number → best score. */
  sessions: Record<string, number>;
  unlocked: boolean;
}

export const DRILL_LEVEL_IDS: string[] = ['L1', 'L2', 'L3', 'L4', 'L5'];

/** Score (out of 10) on one level that opens the next. */
export const DRILL_UNLOCK_SCORE = 8;

/** The levels a child is shown for one topic, lowest first: listed for their grade and with sessions. */
export function availableDrillLevels(
  levels: Record<string, { sessionsAvailable: number }> | null | undefined,
): string[] {
  const out: string[] = [];
  if (!levels) return out;
  for (let i = 0; i < DRILL_LEVEL_IDS.length; i++) {
    const info = levels[DRILL_LEVEL_IDS[i]];
    if (info && info.sessionsAvailable > 0) out.push(DRILL_LEVEL_IDS[i]);
  }
  return out;
}

export function isDrillLevelOpen(
  levelId: string,
  available: string[],
  topicProgress: Record<string, DrillLevelProgress>,
): boolean {
  const stored = topicProgress[levelId];
  if (stored && stored.unlocked) return true;

  const idx = available.indexOf(levelId);
  // Not a level this child is shown (or the list is not known): only L1 is open.
  if (idx === -1) return levelId === 'L1';
  if (idx === 0) return true;

  const before = topicProgress[available[idx - 1]];
  return !!before && before.bestScore >= DRILL_UNLOCK_SCORE;
}

/** The highest open level the child is shown; the lowest one when nothing else is open. */
export function highestOpenDrillLevel(
  available: string[],
  topicProgress: Record<string, DrillLevelProgress>,
): string {
  let highest = available.length > 0 ? available[0] : 'L1';
  for (let i = 0; i < available.length; i++) {
    if (isDrillLevelOpen(available[i], available, topicProgress)) highest = available[i];
  }
  return highest;
}

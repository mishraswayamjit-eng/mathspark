// ── Flashcard XP Economy ─────────────────────────────────────────────────────
// Drives the reward loop: earn XP per card, bonus for streaks & milestones.

// ── Constants ────────────────────────────────────────────────────────────────

const BASE_CARD_XP = 5;       // XP for a correct card answer
const LEVEL_UP_BONUS = 10;    // extra XP when Leitner box increases
const MASTERY_BONUS = 25;     // extra XP when card reaches box 5 (Master)
const STRONG_BONUS = 5;       // extra XP when card reaches box 4 (Expert)
const ANTI_SPAM_MS = 1000;    // ignore answers faster than 1s

// ── Streak milestones ────────────────────────────────────────────────────────

export interface StreakMilestone {
  days: number;
  emoji: string;
  title: string;
  description: string;
  xpBonus: number;            // one-time XP bonus when milestone is hit
}

export const STREAK_MILESTONES: StreakMilestone[] = [
  { days: 3,  emoji: '🔥',  title: '3-Day Streak!',    description: 'Great start — keep going!',    xpBonus: 15 },
  { days: 7,  emoji: '🌟',  title: 'Weekly Champion!',  description: 'A whole week of practice!',    xpBonus: 35 },
  { days: 14, emoji: '💎',  title: '2-Week Legend!',     description: 'Consistency is your superpower', xpBonus: 75 },
  { days: 21, emoji: '🏆',  title: '3-Week Master!',    description: 'You\'re unstoppable!',         xpBonus: 100 },
  { days: 30, emoji: '👑',  title: 'Monthly Champion!',  description: '30 days of dedication!',      xpBonus: 200 },
];

// ── Daily streak multiplier ──────────────────────────────────────────────────

/** Multiplier applied to session XP based on consecutive study days */
export function getStreakMultiplier(dailyStreak: number): number {
  if (dailyStreak >= 30) return 1.5;
  if (dailyStreak >= 14) return 1.3;
  if (dailyStreak >= 7)  return 1.2;
  if (dailyStreak >= 3)  return 1.1;
  return 1.0;
}

// ── Per-card XP ──────────────────────────────────────────────────────────────

export interface CardXPResult {
  xp: number;
  breakdown: {
    base: number;
    levelUpBonus: number;
    masteryBonus: number;
  };
}

/**
 * Compute XP earned for a single flashcard answer.
 * @param correct     Whether the answer was correct
 * @param leveledUp   Whether the Leitner box increased
 * @param reachedMastery Whether the card reached box 5
 * @param reachedStrong  Whether the card reached box 4
 * @param timeTakenMs Time taken to answer (anti-spam)
 */
export function computeCardXP(
  correct: boolean,
  leveledUp: boolean,
  reachedMastery: boolean,
  reachedStrong: boolean,
  timeTakenMs?: number,
): CardXPResult {
  // Anti-spam: too fast = no XP
  if (timeTakenMs !== undefined && timeTakenMs < ANTI_SPAM_MS) {
    return { xp: 0, breakdown: { base: 0, levelUpBonus: 0, masteryBonus: 0 } };
  }

  if (!correct) {
    return { xp: 0, breakdown: { base: 0, levelUpBonus: 0, masteryBonus: 0 } };
  }

  const base = BASE_CARD_XP;
  const levelUpB = leveledUp ? LEVEL_UP_BONUS : 0;
  const masteryB = reachedMastery ? MASTERY_BONUS : reachedStrong ? STRONG_BONUS : 0;

  return {
    xp: base + levelUpB + masteryB,
    breakdown: { base, levelUpBonus: levelUpB, masteryBonus: masteryB },
  };
}

// ── Session XP ───────────────────────────────────────────────────────────────

/**
 * Compute total XP for a completed flashcard session.
 * @param cardsCorrect Number of correct answers
 * @param cardsReviewed Total cards reviewed
 * @param dailyStreak  Current consecutive study days
 * @param bonusXP      Extra XP from level-ups/masteries already awarded per-card
 */
export function computeSessionXP(
  cardsCorrect: number,
  cardsReviewed: number,
  dailyStreak: number,
  bonusXP: number = 0,
): { totalXP: number; baseXP: number; streakMultiplier: number; streakBonus: number } {
  const baseXP = cardsCorrect * BASE_CARD_XP + bonusXP;
  const multiplier = getStreakMultiplier(dailyStreak);
  const totalXP = Math.round(baseXP * multiplier);
  const streakBonus = totalXP - baseXP;

  return { totalXP, baseXP, streakMultiplier: multiplier, streakBonus };
}

// ── Milestone helpers ────────────────────────────────────────────────────────

/** Get the milestone just achieved (exact match on days) */
export function getAchievedMilestone(dailyStreak: number): StreakMilestone | null {
  return STREAK_MILESTONES.find((m) => m.days === dailyStreak) ?? null;
}

/** Get the next milestone to work toward */
export function getNextMilestone(dailyStreak: number): StreakMilestone | null {
  return STREAK_MILESTONES.find((m) => m.days > dailyStreak) ?? null;
}

/** Get progress toward next milestone as 0–1 */
export function getMilestoneProgress(dailyStreak: number): {
  current: number;
  target: number;
  progress: number;
  milestone: StreakMilestone | null;
} {
  const next = getNextMilestone(dailyStreak);
  if (!next) {
    // All milestones achieved
    return { current: dailyStreak, target: dailyStreak, progress: 1, milestone: null };
  }

  // Find previous milestone (or 0)
  const prevMilestones = STREAK_MILESTONES.filter((m) => m.days <= dailyStreak);
  const prevDays = prevMilestones.length > 0
    ? prevMilestones[prevMilestones.length - 1].days
    : 0;

  const range = next.days - prevDays;
  const current = dailyStreak - prevDays;

  return {
    current: dailyStreak,
    target: next.days,
    progress: range > 0 ? Math.min(1, current / range) : 0,
    milestone: next,
  };
}

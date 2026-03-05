import { describe, it, expect } from 'vitest';
import {
  computeCardXP,
  computeSessionXP,
  getStreakMultiplier,
  getAchievedMilestone,
  getNextMilestone,
  getMilestoneProgress,
  STREAK_MILESTONES,
} from '../flashcardXP';

describe('computeCardXP', () => {
  it('wrong answer → 0 XP', () => {
    const result = computeCardXP(false, false, false, false);
    expect(result.xp).toBe(0);
  });

  it('correct answer → base XP (5)', () => {
    const result = computeCardXP(true, false, false, false);
    expect(result.xp).toBe(5);
    expect(result.breakdown.base).toBe(5);
  });

  it('correct + level up → 5 + 10 = 15', () => {
    const result = computeCardXP(true, true, false, false);
    expect(result.xp).toBe(15);
    expect(result.breakdown.levelUpBonus).toBe(10);
  });

  it('correct + mastery (box 5) → 5 + 25 = 30', () => {
    const result = computeCardXP(true, false, true, false);
    expect(result.xp).toBe(30);
    expect(result.breakdown.masteryBonus).toBe(25);
  });

  it('correct + strong (box 4) → 5 + 5 = 10', () => {
    const result = computeCardXP(true, false, false, true);
    expect(result.xp).toBe(10);
    expect(result.breakdown.masteryBonus).toBe(5);
  });

  it('correct + level up + mastery → 5 + 10 + 25 = 40', () => {
    const result = computeCardXP(true, true, true, false);
    expect(result.xp).toBe(40);
  });

  it('anti-spam: answer < 1s → 0 XP', () => {
    const result = computeCardXP(true, false, false, false, 500);
    expect(result.xp).toBe(0);
  });

  it('correct with valid time → normal XP', () => {
    const result = computeCardXP(true, false, false, false, 3000);
    expect(result.xp).toBe(5);
  });
});

describe('computeSessionXP', () => {
  it('0 correct → 0 XP', () => {
    const result = computeSessionXP(0, 5, 1);
    expect(result.totalXP).toBe(0);
    expect(result.baseXP).toBe(0);
  });

  it('5 correct, no streak bonus', () => {
    const result = computeSessionXP(5, 10, 1);
    expect(result.baseXP).toBe(25);
    expect(result.totalXP).toBe(25);
    expect(result.streakMultiplier).toBe(1.0);
  });

  it('5 correct with 3-day streak → 1.1x', () => {
    const result = computeSessionXP(5, 10, 3);
    expect(result.streakMultiplier).toBe(1.1);
    expect(result.totalXP).toBe(Math.round(25 * 1.1));
  });

  it('includes bonusXP in base', () => {
    const result = computeSessionXP(2, 5, 1, 20);
    expect(result.baseXP).toBe(30); // 2*5 + 20
    expect(result.totalXP).toBe(30);
  });
});

describe('getStreakMultiplier', () => {
  it('0 days → 1.0', () => {
    expect(getStreakMultiplier(0)).toBe(1.0);
  });
  it('3 days → 1.1', () => {
    expect(getStreakMultiplier(3)).toBe(1.1);
  });
  it('7 days → 1.2', () => {
    expect(getStreakMultiplier(7)).toBe(1.2);
  });
  it('14 days → 1.3', () => {
    expect(getStreakMultiplier(14)).toBe(1.3);
  });
  it('30 days → 1.5', () => {
    expect(getStreakMultiplier(30)).toBe(1.5);
  });
  it('2 days → 1.0', () => {
    expect(getStreakMultiplier(2)).toBe(1.0);
  });
});

describe('getAchievedMilestone', () => {
  it('0 → null', () => {
    expect(getAchievedMilestone(0)).toBeNull();
  });
  it('3 → fire milestone', () => {
    const m = getAchievedMilestone(3);
    expect(m).not.toBeNull();
    expect(m!.days).toBe(3);
    expect(m!.emoji).toBe('🔥');
  });
  it('30 → crown milestone', () => {
    const m = getAchievedMilestone(30);
    expect(m).not.toBeNull();
    expect(m!.emoji).toBe('👑');
  });
  it('4 → null (not an exact milestone)', () => {
    expect(getAchievedMilestone(4)).toBeNull();
  });
});

describe('getMilestoneProgress', () => {
  it('0 days → progress toward 3-day', () => {
    const result = getMilestoneProgress(0);
    expect(result.milestone).not.toBeNull();
    expect(result.target).toBe(3);
    expect(result.progress).toBe(0);
  });
  it('1 day → 1/3 progress', () => {
    const result = getMilestoneProgress(1);
    expect(result.progress).toBeCloseTo(1 / 3);
  });
  it('past all milestones → progress 1', () => {
    const result = getMilestoneProgress(31);
    expect(result.progress).toBe(1);
    expect(result.milestone).toBeNull();
  });
});

describe('getNextMilestone', () => {
  it('0 days → next is 3-day', () => {
    const m = getNextMilestone(0);
    expect(m!.days).toBe(3);
  });
  it('30 days → null (all achieved)', () => {
    expect(getNextMilestone(30)).toBeNull();
  });
});

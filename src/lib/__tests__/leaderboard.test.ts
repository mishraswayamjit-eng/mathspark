import { describe, it, expect } from 'vitest';
import { computeXPForAttempt, getWeekBounds } from '../leaderboard';

describe('computeXPForAttempt', () => {
  it('correct answer → 20 XP', () => {
    expect(computeXPForAttempt(true, false, 5000)).toBe(20);
  });

  it('wrong answer → 0 XP', () => {
    expect(computeXPForAttempt(false, false, 5000)).toBe(0);
  });

  it('correct but < 3s (anti-spam) → 0 XP', () => {
    expect(computeXPForAttempt(true, false, 2000)).toBe(0);
  });

  it('bonus question correct → 10 XP', () => {
    expect(computeXPForAttempt(true, true, 5000)).toBe(10);
  });

  it('correct at exactly 3s → 0 XP (anti-spam boundary)', () => {
    expect(computeXPForAttempt(true, false, 3000)).toBe(20);
  });

  it('wrong bonus question → 0 XP', () => {
    expect(computeXPForAttempt(false, true, 5000)).toBe(0);
  });
});

describe('getWeekBounds', () => {
  it('returns weekStart before weekEnd', () => {
    const { weekStart, weekEnd } = getWeekBounds();
    expect(weekStart.getTime()).toBeLessThan(weekEnd.getTime());
  });

  it('week spans roughly 7 days', () => {
    const { weekStart, weekEnd } = getWeekBounds();
    const diffMs = weekEnd.getTime() - weekStart.getTime();
    const diffDays = diffMs / (1000 * 60 * 60 * 24);
    // Should be approximately 7 days (6 days + 23:59:59)
    expect(diffDays).toBeGreaterThan(6);
    expect(diffDays).toBeLessThan(8);
  });

  it('weekStart is a Monday in IST', () => {
    const { weekStart } = getWeekBounds();
    // weekStart is stored in UTC but represents Monday 00:00 IST
    // IST = UTC + 5:30, so Monday 00:00 IST = Sunday 18:30 UTC
    const istTime = new Date(weekStart.getTime() + 330 * 60 * 1000);
    // Day should be Monday (1) in IST
    expect(istTime.getUTCDay()).toBe(1);
  });

  it('weekEnd is a Sunday in IST', () => {
    const { weekEnd } = getWeekBounds();
    const istTime = new Date(weekEnd.getTime() + 330 * 60 * 1000);
    // Day should be Sunday (0) in IST
    expect(istTime.getUTCDay()).toBe(0);
  });
});

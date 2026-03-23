import { describe, it, expect } from 'vitest';
import {
  isUnlimitedPlan,
  remainingMinutes,
  isPracticeAllowed,
  usagePct,
  usageBarColor,
  formatMinutes,
  UNLIMITED_THRESHOLD,
} from '../usageLimits';

describe('isUnlimitedPlan', () => {
  it('returns true for 0 (no limit)', () => {
    expect(isUnlimitedPlan(0)).toBe(true);
  });
  it('returns true for 1440 (24h = unlimited threshold)', () => {
    expect(isUnlimitedPlan(1440)).toBe(true);
  });
  it('returns false for 60 (starter)', () => {
    expect(isUnlimitedPlan(60)).toBe(false);
  });
  it('returns true for negative values', () => {
    expect(isUnlimitedPlan(-1)).toBe(true);
  });
  it('returns true for values above threshold', () => {
    expect(isUnlimitedPlan(UNLIMITED_THRESHOLD + 1)).toBe(true);
  });
});

describe('remainingMinutes', () => {
  it('returns Infinity for unlimited plans', () => {
    expect(remainingMinutes(50, 1440)).toBe(Infinity);
  });
  it('returns correct remaining for partial usage', () => {
    expect(remainingMinutes(30, 60)).toBe(30);
  });
  it('returns 0 when over limit', () => {
    expect(remainingMinutes(90, 60)).toBe(0);
  });
  it('returns 0 when exactly at limit', () => {
    expect(remainingMinutes(60, 60)).toBe(0);
  });
});

describe('isPracticeAllowed', () => {
  it('returns true for unlimited plans', () => {
    expect(isPracticeAllowed(999, 1440)).toBe(true);
  });
  it('returns true when usage is under limit', () => {
    expect(isPracticeAllowed(29, 60)).toBe(true);
  });
  it('returns false when at limit', () => {
    expect(isPracticeAllowed(60, 60)).toBe(false);
  });
  it('returns false when over limit', () => {
    expect(isPracticeAllowed(61, 60)).toBe(false);
  });
});

describe('usagePct', () => {
  it('returns 0 for unlimited plans', () => {
    expect(usagePct(50, 1440)).toBe(0);
  });
  it('returns 50 for half used', () => {
    expect(usagePct(30, 60)).toBe(50);
  });
  it('caps at 100 when over limit', () => {
    expect(usagePct(120, 60)).toBe(100);
  });
  it('returns 0 for no usage', () => {
    expect(usagePct(0, 60)).toBe(0);
  });
});

describe('usageBarColor', () => {
  it('returns red at 100%', () => {
    expect(usageBarColor(100)).toBe('bg-red-500');
  });
  it('returns amber at 80%', () => {
    expect(usageBarColor(80)).toBe('bg-amber-500');
  });
  it('returns green at 50%', () => {
    expect(usageBarColor(50)).toBe('bg-duo-green');
  });
  it('returns amber at 75%', () => {
    expect(usageBarColor(75)).toBe('bg-amber-500');
  });
});

describe('formatMinutes', () => {
  it('formats 0 as "0 min"', () => {
    expect(formatMinutes(0)).toBe('0 min');
  });
  it('formats 45 as "45 min"', () => {
    expect(formatMinutes(45)).toBe('45 min');
  });
  it('formats 60 as "1 hr"', () => {
    expect(formatMinutes(60)).toBe('1 hr');
  });
  it('formats 90 as "1 hr 30 min"', () => {
    expect(formatMinutes(90)).toBe('1 hr 30 min');
  });
  it('formats negative as "0 min"', () => {
    expect(formatMinutes(-5)).toBe('0 min');
  });
});

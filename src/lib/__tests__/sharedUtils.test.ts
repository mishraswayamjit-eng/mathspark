import { describe, it, expect } from 'vitest';
import { computeStreak, istDayNumber, istDayStart } from '../sharedUtils';

// India is UTC+5:30, so an India-time day runs from 18:30Z to 18:30Z.
const at = (iso: string) => ({ createdAt: new Date(iso) });
const right = (iso: string) => ({ createdAt: new Date(iso), isCorrect: true });
const missed = (iso: string) => ({ createdAt: new Date(iso), isCorrect: false });

// 11 November 2026, 10:30 in India.
const NOW = new Date('2026-11-11T05:00:00Z');

describe('India-time days', () => {
  it('puts a late-evening UTC moment on the next India day', () => {
    // 19:00Z on the 10th is 00:30 on the 11th in India.
    expect(istDayNumber(new Date('2026-11-10T19:00:00Z'))).toBe(istDayNumber(NOW));
    // 18:00Z on the 10th is 23:30 on the 10th in India.
    expect(istDayNumber(new Date('2026-11-10T18:00:00Z'))).toBe(istDayNumber(NOW) - 1);
  });

  it('starts the India day at 18:30Z the evening before', () => {
    expect(istDayStart(NOW).toISOString()).toBe('2026-11-10T18:30:00.000Z');
  });
});

describe('computeStreak', () => {
  it('is 0 with no attempts', () => {
    expect(computeStreak([], false, NOW)).toBe(0);
  });

  it('counts days in a row ending today', () => {
    const attempts = [at('2026-11-11T04:00:00Z'), at('2026-11-10T10:00:00Z'), at('2026-11-09T10:00:00Z')];
    expect(computeStreak(attempts, false, NOW)).toBe(3);
  });

  it('keeps the run that ended yesterday when today has no attempt yet', () => {
    const attempts = [at('2026-11-10T10:00:00Z'), at('2026-11-09T10:00:00Z')];
    expect(computeStreak(attempts, false, NOW)).toBe(2);
  });

  it('is 0 when neither today nor yesterday was practised', () => {
    expect(computeStreak([at('2026-11-09T10:00:00Z'), at('2026-11-08T10:00:00Z')], false, NOW)).toBe(0);
  });

  it('stops at a gap', () => {
    const attempts = [at('2026-11-11T04:00:00Z'), at('2026-11-10T10:00:00Z'), at('2026-11-08T10:00:00Z')];
    expect(computeStreak(attempts, false, NOW)).toBe(2);
  });

  it('counts a day once however many answers it has', () => {
    const attempts = [at('2026-11-11T04:00:00Z'), at('2026-11-11T03:00:00Z'), at('2026-11-11T02:00:00Z')];
    expect(computeStreak(attempts, false, NOW)).toBe(1);
  });

  it('uses India days, not UTC days', () => {
    // 20:00Z on the 9th is 01:30 on the 10th in India: that is yesterday.
    const attempts = [at('2026-11-11T04:00:00Z'), at('2026-11-09T20:00:00Z')];
    expect(computeStreak(attempts, false, NOW)).toBe(2);
  });

  it('can count only days with a correct answer', () => {
    const attempts = [right('2026-11-11T04:00:00Z'), missed('2026-11-10T10:00:00Z'), right('2026-11-09T10:00:00Z')];
    expect(computeStreak(attempts, true, NOW)).toBe(1);
    expect(computeStreak(attempts, false, NOW)).toBe(3);
  });
});

import { describe, it, expect } from 'vitest';
import {
  getSpeedMultiplier,
  getComboMultiplier,
  calculatePoints,
} from '../quizBlitz';

describe('getSpeedMultiplier', () => {
  it('< 3s → 2.0x', () => {
    expect(getSpeedMultiplier(2000)).toBe(2.0);
  });
  it('5s → 1.5x', () => {
    expect(getSpeedMultiplier(5000)).toBe(1.5);
  });
  it('8s → 1.0x', () => {
    expect(getSpeedMultiplier(8000)).toBe(1.0);
  });
  it('12s → 0.5x', () => {
    expect(getSpeedMultiplier(12000)).toBe(0.5);
  });
  it('exactly 3s → 1.5x', () => {
    expect(getSpeedMultiplier(3000)).toBe(1.5);
  });
  it('exactly 7s → 1.0x', () => {
    expect(getSpeedMultiplier(7000)).toBe(1.0);
  });
  it('exactly 10s → 0.5x', () => {
    expect(getSpeedMultiplier(10000)).toBe(0.5);
  });
});

describe('getComboMultiplier', () => {
  it('0 combo → 1.0x', () => {
    expect(getComboMultiplier(0)).toBe(1.0);
  });
  it('3 combo → 1.2x', () => {
    expect(getComboMultiplier(3)).toBe(1.2);
  });
  it('5 combo → 1.5x', () => {
    expect(getComboMultiplier(5)).toBe(1.5);
  });
  it('7 combo → 2.0x', () => {
    expect(getComboMultiplier(7)).toBe(2.0);
  });
  it('2 combo → 1.0x', () => {
    expect(getComboMultiplier(2)).toBe(1.0);
  });
  it('10 combo → 2.0x', () => {
    expect(getComboMultiplier(10)).toBe(2.0);
  });
});

describe('calculatePoints', () => {
  it('fast correct = high points', () => {
    // 2s + 5 combo = 10 * 2.0 * 1.5 = 30
    expect(calculatePoints(2000, 5)).toBe(30);
  });
  it('slow correct = lower points', () => {
    // 12s + 0 combo = 10 * 0.5 * 1.0 = 5
    expect(calculatePoints(12000, 0)).toBe(5);
  });
  it('medium speed + high combo', () => {
    // 5s + 7 combo = 10 * 1.5 * 2.0 = 30
    expect(calculatePoints(5000, 7)).toBe(30);
  });
  it('base case: no speed bonus, no combo', () => {
    // 8s + 0 combo = 10 * 1.0 * 1.0 = 10
    expect(calculatePoints(8000, 0)).toBe(10);
  });
});

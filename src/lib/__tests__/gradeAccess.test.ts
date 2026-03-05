import { describe, it, expect } from 'vitest';
import { getAccessibleGrades, isGradeAccessible, getTopicGrade } from '../gradeAccess';

describe('getAccessibleGrades', () => {
  it('free tier (0): grade 4 → full access to own + below', () => {
    const result = getAccessibleGrades(4, 0);
    expect(result.fullAccess).toContain(4);
    expect(result.fullAccess).toContain(2);
    expect(result.fullAccess).toContain(3);
    expect(result.sampleOnly).toEqual([]);
  });

  it('starter tier (1): grade 4 → full own+below, sample [5]', () => {
    const result = getAccessibleGrades(4, 1);
    expect(result.fullAccess).toContain(4);
    expect(result.fullAccess).toContain(2);
    expect(result.fullAccess).toContain(3);
    expect(result.sampleOnly).toEqual([5]);
  });

  it('advanced tier (2): grade 4 → full access +2 grades above', () => {
    const result = getAccessibleGrades(4, 2);
    expect(result.fullAccess).toContain(4);
    expect(result.fullAccess).toContain(5);
    expect(result.fullAccess).toContain(6);
    expect(result.sampleOnly).toEqual([]);
  });

  it('unlimited tier (3): any grade → full 2-9', () => {
    const result = getAccessibleGrades(4, 3);
    expect(result.fullAccess).toEqual([2, 3, 4, 5, 6, 7, 8, 9]);
    expect(result.sampleOnly).toEqual([]);
  });

  it('grade 9 + starter → no sample (can\'t go higher)', () => {
    const result = getAccessibleGrades(9, 1);
    expect(result.fullAccess).toContain(9);
    expect(result.sampleOnly).toEqual([]);
  });

  it('grade 2 + free → full [2] only', () => {
    const result = getAccessibleGrades(2, 0);
    expect(result.fullAccess).toEqual([2]);
    expect(result.sampleOnly).toEqual([]);
  });
});

describe('isGradeAccessible', () => {
  it('own grade is always full access for free tier', () => {
    const result = isGradeAccessible(4, 4, 0);
    expect(result.full).toBe(true);
    expect(result.sample).toBe(false);
    expect(result.locked).toBe(false);
  });

  it('higher grade is locked for free tier', () => {
    const result = isGradeAccessible(5, 4, 0);
    expect(result.locked).toBe(true);
  });

  it('higher grade is sample for starter', () => {
    const result = isGradeAccessible(5, 4, 1);
    expect(result.sample).toBe(true);
    expect(result.full).toBe(false);
  });

  it('all grades accessible for unlimited', () => {
    const result = isGradeAccessible(9, 4, 3);
    expect(result.full).toBe(true);
  });
});

describe('getTopicGrade', () => {
  it('grade4 → 4', () => {
    expect(getTopicGrade('grade4')).toBe(4);
  });

  it('grade9 → 9', () => {
    expect(getTopicGrade('grade9')).toBe(9);
  });

  it('ch11 → 4 (curriculum chapter defaults to 4)', () => {
    expect(getTopicGrade('ch11')).toBe(4);
  });

  it('dh → 4', () => {
    expect(getTopicGrade('dh')).toBe(4);
  });
});

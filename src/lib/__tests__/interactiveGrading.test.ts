import { describe, it, expect } from 'vitest';
import {
  validateInteractiveAnswer,
  isTileBuildCorrect,
  isNumberLineCorrect,
} from '../interactiveGrading';

describe('tileBuild grading', () => {
  const config = { solution: ['3', '8', '4'] };

  it('accepts the exact solution', () => {
    expect(isTileBuildCorrect(config, ['3', '8', '4'])).toBe(true);
    expect(validateInteractiveAnswer('tileBuild', config, JSON.stringify(['3', '8', '4']))).toBe(true);
  });

  it('rejects a different order, a short answer and a non-array', () => {
    expect(validateInteractiveAnswer('tileBuild', config, JSON.stringify(['8', '3', '4']))).toBe(false);
    expect(validateInteractiveAnswer('tileBuild', config, JSON.stringify(['3', '8']))).toBe(false);
    expect(validateInteractiveAnswer('tileBuild', config, JSON.stringify('384'))).toBe(false);
    expect(validateInteractiveAnswer('tileBuild', config, 'not json')).toBe(false);
  });

  it('accepts a listed alternative only', () => {
    const swap = { solution: ['2', '5'], alsoCorrect: [['5', '2']] };
    expect(isTileBuildCorrect(swap, ['5', '2'])).toBe(true);
    expect(isTileBuildCorrect(swap, ['2', '2'])).toBe(false);
  });
});

describe('numberLine grading', () => {
  const tenths = { min: 0, step: 0.1, correctValue: 0.7 };

  it('accepts the correct snap point despite float noise', () => {
    expect(isNumberLineCorrect(tenths, 0.7)).toBe(true);
    expect(isNumberLineCorrect(tenths, 0.1 * 7)).toBe(true);
    expect(validateInteractiveAnswer('numberLine', tenths, '0.7')).toBe(true);
  });

  it('rejects neighbouring points and non-numbers', () => {
    expect(isNumberLineCorrect(tenths, 0.6)).toBe(false);
    expect(isNumberLineCorrect(tenths, 0.8)).toBe(false);
    expect(validateInteractiveAnswer('numberLine', tenths, '"0.7"')).toBe(false);
    expect(validateInteractiveAnswer('numberLine', tenths, 'null')).toBe(false);
  });

  it('works on quarter steps', () => {
    const quarters = { min: 0, step: 0.25, correctValue: 0.75 };
    expect(isNumberLineCorrect(quarters, 0.75)).toBe(true);
    expect(isNumberLineCorrect(quarters, 1)).toBe(false);
  });
});

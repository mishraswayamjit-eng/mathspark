import { describe, it, expect } from 'vitest';
import { toSpeech, hintsToSpeech } from '../speech/mathToSpeech';

describe('toSpeech', () => {
  it('reads plain fractions', () => {
    expect(toSpeech('3/8')).toBe('3 over 8');
    expect(toSpeech('1/2')).toBe('one half');
    expect(toSpeech('3/4')).toBe('three quarters');
  });

  it('reads a LaTeX equation with fractions', () => {
    expect(toSpeech('\\frac{1}{2}m + 1 = \\frac{1}{4}m - 3'))
      .toBe('one half m plus 1 equals one quarter m minus 3');
  });

  it('reads powers, roots and rupees', () => {
    expect(toSpeech('x^2 + 5')).toBe('x squared plus 5');
    expect(toSpeech('\\sqrt{9}')).toBe('the square root of 9');
    expect(toSpeech('Her total bill is ₹133.')).toBe('Her total bill is 133 rupees.');
  });

  it('reads operators', () => {
    expect(toSpeech('6 × 7 = 42')).toBe('6 times 7 equals 42');
    expect(toSpeech('12 ÷ 4')).toBe('12 divided by 4');
    expect(toSpeech('9 - 4')).toBe('9 minus 4');
  });

  it('leaves hyphenated words alone', () => {
    expect(toSpeech('a 3-digit number')).toBe('a 3-digit number');
  });

  it('never reads emoji', () => {
    expect(toSpeech('Great job! ⭐')).toBe('Great job!');
    expect(toSpeech('You got it! 🎯')).toBe('You got it!');
  });

  it('returns an empty string for missing text', () => {
    expect(toSpeech('')).toBe('');
    expect(toSpeech(undefined)).toBe('');
  });
});

describe('hintsToSpeech', () => {
  it('joins hints as separate sentences', () => {
    expect(hintsToSpeech(['Count the parts', 'Then shade 3.'])).toBe('Count the parts. Then shade 3.');
  });
});

import { describe, it, expect } from 'vitest';
import {
  tidyQuestionText,
  questionTextSize,
  topicChipLabel,
  SHORT_QUESTION_MAX,
  MEDIUM_QUESTION_MAX,
} from '../questionDisplay';

describe('tidyQuestionText', () => {
  it('takes out an emoji that only decorates, and closes the space it leaves', () => {
    expect(tidyQuestionText('Meera lights lamps for Diwali 🪔 . How many lamps does she light?'))
      .toBe('Meera lights lamps for Diwali. How many lamps does she light?');
    expect(tidyQuestionText('Ravi shares the sweets with his friends 🍬.'))
      .toBe('Ravi shares the sweets with his friends.');
    expect(tidyQuestionText('How many lamps are there in all? 🎉'))
      .toBe('How many lamps are there in all?');
  });

  it('takes out an emoji that carries a variation selector', () => {
    const heart = String.fromCharCode(0x2764, 0xfe0f);
    expect(tidyQuestionText('Asha makes cards for her class ' + heart + '.'))
      .toBe('Asha makes cards for her class.');
  });

  it('keeps an emoji that stands for a thing in the sentence', () => {
    const kept = [
      'How many 🍎 are there?',
      'How many 🍎?',
      'Riya has 3 🍎.',
      'Riya has 3 ripe 🍎.',
      'She ate the ripe 🍎.',
      '🍎 + 🍌 = ?',
      'If 🍎 = 5 and 🍌 = 3, what is 🍎 + 🍌?',
      '🍎 costs ₹5. What do 4 cost?',
      '🍎🍎🍎 How many apples?',
      'Each 🍎 costs ₹5.',
    ];
    for (let i = 0; i < kept.length; i++) {
      expect(tidyQuestionText(kept[i])).toBe(kept[i]);
    }
  });

  it('keeps every emoji when one of them means something', () => {
    const text = 'Riya loves apples 🍎. She has 4 🍎.';
    expect(tidyQuestionText(text)).toBe(text);
  });

  it('leaves shapes, suits and signs that are not picture emoji', () => {
    const kept = ['Count the ⬛ squares.', 'Draw a ♥.', 'Tick ✓ the right one.', '5 ➕ 3 = ?', '2 → 4 → 8'];
    for (let i = 0; i < kept.length; i++) {
      expect(tidyQuestionText(kept[i])).toBe(kept[i]);
    }
  });

  it('closes a space before a full stop, comma, question mark or exclamation mark', () => {
    expect(tidyQuestionText('What is the area of the field ?')).toBe('What is the area of the field?');
    expect(tidyQuestionText('Anu has pens , pencils and books .')).toBe('Anu has pens, pencils and books.');
    expect(tidyQuestionText('A rope is 3/4 m long. How long are 20 ropes in m ?'))
      .toBe('A rope is 3/4 m long. How long are 20 ropes in m?');
    expect(tidyQuestionText('The bill is ₹250 .')).toBe('The bill is ₹250.');
    expect(tidyQuestionText('He paid ₹250 . How much is left?')).toBe('He paid ₹250. How much is left?');
  });

  it('never changes digits, maths signs, ratios, decimals, blanks or lists', () => {
    const kept = [
      'The ratio is 3 : 4',
      'What is 12 . 5 + 3?',
      'What comes next: 2, 4, 6 ...',
      'Write 1 , 2 , 3 in words',
      'Fill in: 7 × ___ . Then add 2',
      '₹1,250.50 − ₹250 = ?',
      '3/4 + 1/4 = ?',
      '25% of 80 kg',
      '5 cm × 4 cm = __ cm²',
    ];
    for (let i = 0; i < kept.length; i++) {
      expect(tidyQuestionText(kept[i])).toBe(kept[i]);
    }
  });

  it('returns text holding LaTeX untouched', () => {
    const latex = 'Find \\frac{1}{2} of 10 sweets 🍬 .';
    expect(tidyQuestionText(latex)).toBe(latex);
  });

  it('copes with empty text', () => {
    expect(tidyQuestionText('')).toBe('');
    expect(tidyQuestionText('🎉')).toBe('🎉');
  });
});

describe('questionTextSize', () => {
  it('sets a short question large, a word problem a step smaller', () => {
    expect(questionTextSize('What is 7 × 8?')).toBe('short');
    expect(questionTextSize(new Array(SHORT_QUESTION_MAX + 1).join('a'))).toBe('short');
    expect(questionTextSize(new Array(SHORT_QUESTION_MAX + 2).join('a'))).toBe('medium');
    expect(questionTextSize(new Array(MEDIUM_QUESTION_MAX + 1).join('a'))).toBe('medium');
    expect(questionTextSize(new Array(MEDIUM_QUESTION_MAX + 2).join('a'))).toBe('long');
  });

  it('does not count LaTeX markup as reading', () => {
    expect(questionTextSize('\\frac{1}{2} + \\frac{1}{4} = ?')).toBe('short');
  });
});

describe('topicChipLabel', () => {
  it('drops the grade prefix', () => {
    expect(topicChipLabel('Grade 5 — Numbers (place value)')).toBe('Numbers (place value)');
    expect(topicChipLabel('Grade 6 - HCF & LCM')).toBe('HCF & LCM');
    expect(topicChipLabel('Fractions')).toBe('Fractions');
  });

  it('drops a trailing bracket only when the name is too long to show whole', () => {
    expect(topicChipLabel('Grade 5 — Area & Perimeter (rectangles, squares and triangles)'))
      .toBe('Area & Perimeter');
  });

  it('copes with empty or prefix-only names', () => {
    expect(topicChipLabel('')).toBe('');
    expect(topicChipLabel('Grade 5 — ')).toBe('Grade 5 —');
  });
});

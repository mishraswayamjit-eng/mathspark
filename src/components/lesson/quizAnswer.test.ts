import { describe, it, expect } from 'vitest';
import { answerFormatHint, foldAnswer, isQuizAnswerRight } from './quizAnswer';

describe('isQuizAnswerRight', () => {
  it('ignores case, spacing and a closing full stop', () => {
    expect(isQuizAnswerRight('  25 ', '25')).toBe(true);
    expect(isQuizAnswerRight('YES', 'Yes')).toBe(true);
    expect(isQuizAnswerRight('7 : 00  am', '7:00 AM')).toBe(true);
    expect(isQuizAnswerRight('1 / 2', '1/2')).toBe(true);
    expect(isQuizAnswerRight('12.', '12')).toBe(true);
  });

  it('never accepts an empty answer', () => {
    expect(isQuizAnswerRight('', '5')).toBe(false);
    expect(isQuizAnswerRight('   ', '5')).toBe(false);
  });

  it('compares numbers as numbers', () => {
    expect(isQuizAnswerRight('.5', '0.5')).toBe(true);
    expect(isQuizAnswerRight('3.50', '3.5')).toBe(true);
    expect(isQuizAnswerRight('007', '7')).toBe(true);
    expect(isQuizAnswerRight('-3', '−3')).toBe(true);
    expect(isQuizAnswerRight('0.05', '0.5')).toBe(false);
    expect(isQuizAnswerRight('3', '-3')).toBe(false);
  });

  it('ignores commas inside a number', () => {
    expect(isQuizAnswerRight('19,800', '19800')).toBe(true);
    expect(isQuizAnswerRight('2,34,500', '234500')).toBe(true);
    expect(isQuizAnswerRight('400250', '4,00,250')).toBe(true);
    expect(isQuizAnswerRight('19,801', '19800')).toBe(false);
  });

  it('accepts an equivalent fraction but not another form of the number', () => {
    expect(isQuizAnswerRight('2/4', '1/2')).toBe(true);
    expect(isQuizAnswerRight('3/9', '1/3')).toBe(true);
    expect(isQuizAnswerRight('2/3', '1/2')).toBe(false);
    expect(isQuizAnswerRight('0.5', '1/2')).toBe(false);
    expect(isQuizAnswerRight('1/2', '0.5')).toBe(false);
    expect(isQuizAnswerRight('11/3', '3 2/3')).toBe(false);
    expect(isQuizAnswerRight('3  2/3', '3 2/3')).toBe(true);
    expect(isQuizAnswerRight('3 4/6', '3 2/3')).toBe(true);
  });

  it('accepts the same numbers with or without the units', () => {
    expect(isQuizAnswerRight('25', '25 minutes')).toBe(true);
    expect(isQuizAnswerRight('25 min', '25 minutes')).toBe(true);
    expect(isQuizAnswerRight('25 mins', '25 minutes')).toBe(true);
    expect(isQuizAnswerRight('3 h 15 min', '3 hours 15 minutes')).toBe(true);
    expect(isQuizAnswerRight('3 hrs and 15 minutes', '3 hours 15 minutes')).toBe(true);
    expect(isQuizAnswerRight('6 weeks 3 days', '6 weeks 3 days')).toBe(true);
    expect(isQuizAnswerRight('8100', '8100 seconds')).toBe(true);
    expect(isQuizAnswerRight('40', '40%')).toBe(true);
    expect(isQuizAnswerRight('40 percent', '40%')).toBe(true);
    expect(isQuizAnswerRight('10886 m', '10886')).toBe(true);
  });

  it('never accepts a different number, or the numbers in another order', () => {
    expect(isQuizAnswerRight('26', '25 minutes')).toBe(false);
    expect(isQuizAnswerRight('15 hours 3 minutes', '3 hours 15 minutes')).toBe(false);
    expect(isQuizAnswerRight('3 hours', '3 hours 15 minutes')).toBe(false);
    expect(isQuizAnswerRight('0.4', '40%')).toBe(false);
    expect(isQuizAnswerRight('9', '9:00')).toBe(false);
    expect(isQuizAnswerRight('6.45', '6:45')).toBe(false);
    expect(isQuizAnswerRight('5 tenths', '0.5')).toBe(false);
    expect(isQuizAnswerRight('2 thousand', '2')).toBe(false);
    expect(isQuizAnswerRight('40%', '40')).toBe(false);
  });

  it('does not let a different word through', () => {
    expect(isQuizAnswerRight('15 July', '15 August')).toBe(false);
    expect(isQuizAnswerRight('15th August', '15 August')).toBe(true);
    expect(isQuizAnswerRight('15 Aug', '15 August')).toBe(true);
    expect(isQuizAnswerRight('15', '15 August')).toBe(false);
    // One or two letters do not name a month or a day: "a" fits April too.
    expect(isQuizAnswerRight('15 a', '15 August')).toBe(false);
    expect(isQuizAnswerRight('15 at', '15 August')).toBe(false);
    expect(isQuizAnswerRight('15 j', '15 June')).toBe(false);
    expect(isQuizAnswerRight('15 ju', '15 July')).toBe(false);
    expect(isQuizAnswerRight('15 jun', '15 June')).toBe(true);
    expect(isQuizAnswerRight('thu', 'Thursday 3')).toBe(false);
    expect(isQuizAnswerRight('3 thurs', '3 Thursday')).toBe(true);
    expect(isQuizAnswerRight('5 sept', '5 September')).toBe(true);
    expect(isQuizAnswerRight('25 hours', '25 minutes')).toBe(false);
  });

  it('needs AM or PM when the answer has one', () => {
    expect(isQuizAnswerRight('7:00 am', '7:00 AM')).toBe(true);
    expect(isQuizAnswerRight('7:00 a.m.', '7:00 AM')).toBe(true);
    expect(isQuizAnswerRight('7:00 pm', '7:00 AM')).toBe(false);
    expect(isQuizAnswerRight('7:00', '7:00 AM')).toBe(false);
  });

  it('takes the yes or no of a "Yes, because" answer', () => {
    const answer = 'No, because 1900 is divisible by 100 but not by 400';
    expect(isQuizAnswerRight('No', answer)).toBe(true);
    expect(isQuizAnswerRight('no, it is not', answer)).toBe(true);
    expect(isQuizAnswerRight('Yes', answer)).toBe(false);
    expect(isQuizAnswerRight('not sure', answer)).toBe(false);
    expect(isQuizAnswerRight('no', 'Yes')).toBe(false);
  });

  it('matches a list item by item, in order', () => {
    expect(isQuizAnswerRight('1/5,1/3,1/2', '1/5, 1/3, 1/2')).toBe(true);
    expect(isQuizAnswerRight('1/5 , 1/3 , 1/2', '1/5, 1/3, 1/2')).toBe(true);
    expect(isQuizAnswerRight('1/2, 1/3, 1/5', '1/5, 1/3, 1/2')).toBe(false);
    expect(isQuizAnswerRight('1/5, 1/3', '1/5, 1/3, 1/2')).toBe(false);
  });
});

describe('foldAnswer', () => {
  it('folds case, spaces, minus signs and a closing full stop', () => {
    expect(foldAnswer('  3  Hours 15 Minutes. ')).toBe('3 hours 15 minutes');
    expect(foldAnswer('−3')).toBe('-3');
    expect(foldAnswer('₹250')).toBe('250');
  });
});

describe('answerFormatHint', () => {
  it('blanks the numbers and keeps the units', () => {
    expect(answerFormatHint('25 minutes')).toBe('__ minutes');
    expect(answerFormatHint('3 hours 15 minutes')).toBe('__ hours __ minutes');
    expect(answerFormatHint('9:00')).toBe('__:__');
    expect(answerFormatHint('12.5%')).toBe('__%');
  });

  it('never gives away AM or PM', () => {
    expect(answerFormatHint('7:00 AM')).toBe('__:__ AM or PM');
    expect(answerFormatHint('6:15 PM')).toBe('__:__ AM or PM');
  });

  it('gives no hint for a bare number, a fraction, or words that are part of the answer', () => {
    expect(answerFormatHint('25')).toBeNull();
    expect(answerFormatHint('1/4')).toBeNull();
    expect(answerFormatHint('3 2/3')).toBeNull();
    expect(answerFormatHint('15 August')).toBeNull();
    expect(answerFormatHint('Yes')).toBeNull();
    expect(answerFormatHint('No, because 1900 is divisible by 100 but not by 400')).toBeNull();
  });
});

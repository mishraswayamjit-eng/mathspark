/**
 * Marking a typed answer in a concept-lesson quiz.
 *
 * The stored answer is one string ("25 minutes", "1/2", "19800", "No, because
 * ..."). A child who knows the answer should not be held back by how it is
 * typed, so the comparison is tolerant about form and strict about value:
 *
 *   - case, extra spaces, a closing full stop and spaces round "/" and ":" do
 *     not matter;
 *   - commas inside a number do not matter ("19,800" is 19800);
 *   - numbers are compared as numbers (".5" is 0.5, "3.50" is 3.5);
 *   - an equivalent fraction is accepted ("2/4" for "1/2"), but a decimal is
 *     not accepted for a fraction, nor an improper fraction for a mixed number,
 *     because the form is then what the question asks for;
 *   - where the answer is a number with a unit or words ("3 hours 15 minutes"),
 *     the same numbers in the same order are accepted with or without the
 *     units (but a month or weekday in the answer must be typed too); words the child does type must match the answer's own words
 *     ("min" for "minutes", but not "July" for "August" or "PM" for "AM");
 *   - an answer that starts "Yes," or "No," is right when the child's answer
 *     starts with the same word.
 *
 * A different number is never accepted. Pure functions: no DOM, no React.
 * This only decides what the quiz screen shows; see the lesson progress route
 * for what is recorded.
 */

interface Rational {
  n: number;
  d: number;
}

type PureKind = 'num' | 'frac' | 'mixed';

interface PureValue extends Rational {
  kind: PureKind;
}

/** Lower case, single spaces, plain minus and apostrophe, no rupee sign, no closing full stop. */
export function foldAnswer(text: string): string {
  return String(text === null || text === undefined ? '' : text)
    .replace(/[−–—]/g, '-')
    .replace(/[‘’]/g, "'")
    .replace(/₹/g, ' ')
    .toLowerCase()
    .replace(/\ba\.m\.?/g, 'am')
    .replace(/\bp\.m\.?/g, 'pm')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[.!]+$/, '')
    .trim();
}

/** "19,800" and "2,34,500" without their commas. A comma between two list items is left alone. */
function stripNumberCommas(text: string): string {
  return text.replace(/(\d),(?=\d{2,3}(?!\d))/g, '$1');
}

/** No spaces round "/" and ":" ("1 / 2" is "1/2", "7 : 30" is "7:30"). */
function tighten(text: string): string {
  return text.replace(/\s*([\/:])\s*/g, '$1');
}

/** "0.50" as 50 over 100. Exact for the sizes a quiz uses. */
function parseDecimal(whole: string, fraction: string): Rational {
  return { n: Number((whole || '0') + fraction), d: Math.pow(10, fraction.length) };
}

function sameValue(a: Rational, b: Rational): boolean {
  if (!(a.d > 0) || !(b.d > 0)) return false;
  return a.n * b.d === b.n * a.d;
}

/** A whole answer that is one number, one fraction or one mixed number; otherwise null. */
function parsePure(text: string): PureValue | null {
  let m = /^([+-]?)(\d*)(?:\.(\d+))?$/.exec(text);
  if (m && (m[2] !== '' || m[3] !== undefined)) {
    const value = parseDecimal(m[2], m[3] || '');
    return { n: m[1] === '-' ? -value.n : value.n, d: value.d, kind: 'num' };
  }
  m = /^([+-]?)(\d+)\/(\d+)$/.exec(text);
  if (m) {
    const d = Number(m[3]);
    if (!(d > 0)) return null;
    const n = Number(m[2]);
    return { n: m[1] === '-' ? -n : n, d: d, kind: 'frac' };
  }
  m = /^([+-]?)(\d+) (\d+)\/(\d+)$/.exec(text);
  if (m) {
    const d = Number(m[4]);
    if (!(d > 0)) return null;
    const n = Number(m[2]) * d + Number(m[3]);
    return { n: m[1] === '-' ? -n : n, d: d, kind: 'mixed' };
  }
  return null;
}

/** Every number in the text, in order. "3/4" is one number; "7:30" is two. */
function numberTokens(text: string): Rational[] {
  const out: Rational[] = [];
  const re = /(\d+)(?:\.(\d+))?(?:\/(\d+))?|\.(\d+)/g;
  let m = re.exec(text);
  while (m) {
    let value: Rational;
    if (m[4] !== undefined) {
      value = parseDecimal('0', m[4]);
    } else {
      value = parseDecimal(m[1], m[2] || '');
      if (m[3] !== undefined) value = { n: value.n, d: value.d * Number(m[3]) };
    }
    // A minus sign straight before the number, at the start or after a space, makes it negative.
    const at = m.index;
    if (at > 0 && text.charAt(at - 1) === '-' && (at === 1 || text.charAt(at - 2) === ' ')) {
      value = { n: -value.n, d: value.d };
    }
    out.push(value);
    m = re.exec(text);
  }
  return out;
}

// Little words that carry no meaning in an answer.
const FILLER = ['and', 'the', 'of', 'a', 'an', 'is', 'it', 'at', 'in', 'on', 'about', 'equals', 'answer', 'to'];
// Words that are the point of the answer: when the stored answer has one, the child's must too.
const REQUIRED = ['am', 'pm', 'yes', 'no'];
// Words that say WHICH one (a month, a weekday): when the stored answer has one, a bare number
// is not enough ("15" is not "15 August").
const NAMING = [
  'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
  'november', 'december', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
];
// Words that change the size of a number. Never ignored after a bare number.
const MAGNITUDE = [
  'ten', 'tens', 'hundred', 'hundreds', 'thousand', 'thousands', 'lakh', 'lakhs', 'crore', 'crores',
  'million', 'millions', 'tenth', 'tenths', 'hundredth', 'hundredths', 'thousandth', 'thousandths',
  'dozen', 'dozens', 'half', 'halves', 'quarter', 'quarters', 'percent', 'times',
];

/** The words of an answer, without filler. "%" counts as the word "percent"; "15th" has no word. */
function wordTokens(text: string): string[] {
  const found = text
    .replace(/%/g, ' percent ')
    .replace(/(\d)(st|nd|rd|th)\b/g, '$1 ')
    .match(/[a-z]+/g);
  const out: string[] = [];
  if (!found) return out;
  for (let i = 0; i < found.length; i++) {
    if (FILLER.indexOf(found[i]) === -1) out.push(found[i]);
  }
  return out;
}

function isSubsequence(short: string, long: string): boolean {
  let at = 0;
  for (let i = 0; i < long.length && at < short.length; i++) {
    if (long.charAt(i) === short.charAt(at)) at += 1;
  }
  return at === short.length;
}

/** True when the child's word is the stored word, a short form of it ("min", "hrs"), or its plural. */
function wordsAlike(typed: string, stored: string): boolean {
  if (typed === stored) return true;
  if (typed.charAt(0) !== stored.charAt(0)) return false;
  if (isSubsequence(typed, stored)) return true;
  return stored.length >= 2 && typed.indexOf(stored) === 0 && typed.length - stored.length <= 2;
}

function has(list: string[], word: string): boolean {
  return list.indexOf(word) !== -1;
}

/** One answer against one stored answer (no lists, no yes/no). Both already folded. */
function matchOne(typedFolded: string, storedFolded: string): boolean {
  const typed = tighten(stripNumberCommas(typedFolded));
  const stored = tighten(stripNumberCommas(storedFolded));
  if (typed === '' || stored === '') return false;
  if (typed === stored) return true;

  // The stored answer is a bare number, fraction or mixed number.
  const storedPure = parsePure(stored);
  if (storedPure) {
    const typedPure = parsePure(typed);
    if (typedPure) return typedPure.kind === storedPure.kind && sameValue(typedPure, storedPure);
    // A bare number with a unit typed after it ("10886 m").
    if (storedPure.kind !== 'num') return false;
    const m = /^([+-]?(?:\d+(?:\.\d+)?|\.\d+)) ?([^\d]+)$/.exec(typed);
    if (!m) return false;
    const value = parsePure(m[1]);
    if (!value || value.kind !== 'num' || !sameValue(value, storedPure)) return false;
    const unitWords = wordTokens(m[2]);
    for (let i = 0; i < unitWords.length; i++) {
      if (has(MAGNITUDE, unitWords[i])) return false;
    }
    return true;
  }

  // The stored answer has numbers with units or words round them.
  const storedNumbers = numberTokens(stored);
  if (storedNumbers.length === 0) return false;
  const typedNumbers = numberTokens(typed);
  if (typedNumbers.length !== storedNumbers.length) return false;
  for (let i = 0; i < storedNumbers.length; i++) {
    if (!sameValue(typedNumbers[i], storedNumbers[i])) return false;
  }

  const storedWords = wordTokens(stored);
  const typedWords = wordTokens(typed);
  for (let i = 0; i < storedWords.length; i++) {
    if (has(REQUIRED, storedWords[i]) && !has(typedWords, storedWords[i])) return false;
    if (has(NAMING, storedWords[i])) {
      let named = false;
      for (let k = 0; k < typedWords.length; k++) {
        if (wordsAlike(typedWords[k], storedWords[i])) {
          named = true;
          break;
        }
      }
      if (!named) return false;
    }
  }
  for (let i = 0; i < typedWords.length; i++) {
    let alike = false;
    for (let k = 0; k < storedWords.length; k++) {
      if (wordsAlike(typedWords[i], storedWords[k])) {
        alike = true;
        break;
      }
    }
    if (!alike) return false;
  }
  return true;
}

/** True when what the child typed is the stored answer, allowing for how it is written. */
export function isQuizAnswerRight(typed: string, answer: string): boolean {
  const a = foldAnswer(typed);
  const b = foldAnswer(answer);
  if (a === '' || b === '') return false;
  if (a === b) return true;

  // "Yes, because ..." / "No, because ...": the yes or no is the answer.
  const lead = /^(yes|no)\b/.exec(b);
  if (lead) {
    const mine = /^(yes|no)\b/.exec(a);
    return !!mine && mine[1] === lead[1];
  }

  // A list ("1/5, 1/3, 1/2"): the same items in the same order.
  if (/,\s/.test(b)) {
    const want = b.split(',');
    const got = a.split(',');
    if (want.length === got.length) {
      let all = true;
      for (let i = 0; i < want.length; i++) {
        if (!matchOne(got[i].trim(), want[i].trim())) {
          all = false;
          break;
        }
      }
      if (all) return true;
    }
  }

  return matchOne(a, b);
}

// Unit words that can be shown in a format hint without giving anything away.
const UNIT_WORDS = [
  'second', 'seconds', 'minute', 'minutes', 'hour', 'hours', 'day', 'days', 'week', 'weeks',
  'month', 'months', 'year', 'years', 'mm', 'cm', 'm', 'km', 'g', 'kg', 'ml', 'l',
  'metre', 'metres', 'litre', 'litres', 'gram', 'grams', 'rupee', 'rupees', 'paise', 'degrees', 'and',
];

/**
 * How to write the answer, when it carries a unit: "__ hours __ minutes",
 * "__:__", "__:__ AM or PM", "__%". The numbers are blanked, and nothing is
 * returned when the words of the answer are more than units (a month, "Yes").
 */
export function answerFormatHint(answer: string): string | null {
  const text = String(answer === null || answer === undefined ? '' : answer).replace(/\s+/g, ' ').trim();
  if (!/\d/.test(text)) return null;
  const words = text.toLowerCase().match(/[a-z]+/g) || [];
  for (let i = 0; i < words.length; i++) {
    if (words[i] !== 'am' && words[i] !== 'pm' && UNIT_WORDS.indexOf(words[i]) === -1) return null;
  }
  const hasMark = text.indexOf(':') !== -1 || text.indexOf('%') !== -1;
  if (words.length === 0 && !hasMark) return null;
  return text
    .replace(/\d+(?:\.\d+)?/g, '__')
    .replace(/\b(am|pm)\b/gi, 'AM or PM');
}

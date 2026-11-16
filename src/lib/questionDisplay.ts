// How a question is shown on screen: a light tidy of its wording, a size for
// its text, and a short name for its topic chip.
//
// Display only. Nothing here changes what is stored, graded or read aloud, and
// nothing here ever touches a digit, a maths sign, a currency sign, a fraction,
// a unit or LaTeX. When a rule is not sure, it leaves the text exactly as it is.
//
// This file is plain ASCII: every special character is given by its code, so
// nothing here depends on how the file is saved.

// -- Emoji --------------------------------------------------------------------
// Picture emoji only, matched as explicit surrogate pairs (no `u` flag):
//   U+1F300 to U+1F3FF   high D83C, low DF00-DFFF
//   U+1F400 to U+1F64F   high D83D, low DC00-DE4F
//   U+1F680 to U+1F6FF   high D83D, low DE80-DEFF
//   U+1F900 to U+1F9FF   high D83E, low DD00-DDFF
//   U+1FA70 to U+1FAFF   high D83E, low DE70-DEFF
// plus a short list of single-unit ones: star U+2B50, sparkles U+2728, heart
// U+2764, sun U+2600, smiley U+263A, football U+26BD. Each may be followed by
// the variation selector U+FE0F. Left out on purpose: coloured squares and
// circles, playing cards, card suits, ticks and crosses, the heavy
// plus/minus/divide signs, arrows and the mathematical alphabets, all of which
// a question may really be about.
const EMOJI_SOURCE =
  '(?:\\uD83C[\\uDF00-\\uDFFF]|\\uD83D[\\uDC00-\\uDE4F\\uDE80-\\uDEFF]|\\uD83E[\\uDD00-\\uDDFF\\uDE70-\\uDEFF]|[\\u2B50\\u2728\\u2764\\u2600\\u263A\\u26BD])\\uFE0F?';

/** The "show as emoji" mark that may trail an emoji (U+FE0F). */
const VARIATION_SELECTOR = String.fromCharCode(0xfe0f);
/** Joins several emoji into one picture (U+200D). */
const ZERO_WIDTH_JOINER = String.fromCharCode(0x200d);
/** U+00A0. */
const NO_BREAK_SPACE = String.fromCharCode(0xa0);
/** Em dash and en dash (U+2014, U+2013). */
const LONG_DASHES = String.fromCharCode(0x2014, 0x2013);

/** More emoji than this and the question is probably made of pictures: leave it alone. */
const MAX_DECORATIVE_EMOJI = 2;

/**
 * Words that, straight before an emoji, mean the emoji is standing in for a
 * thing in the sentence ("how many [apple]?", "each [apple] costs"), so it must stay.
 */
const WORDS_BEFORE_A_PICTURE_NOUN = [
  'how', 'many', 'much', 'each', 'every', 'the', 'a', 'an', 'of', 'per', 'some', 'these', 'those',
  'this', 'that', 'more', 'fewer', 'less', 'is', 'are', 'was', 'were', 'and', 'or', 'with', 'has',
  'have', 'had', 'in', 'on', 'by', 'to', 'for', 'both', 'all', 'no', 'any', 'which', 'what',
  'whose', 'his', 'her', 'their', 'my', 'your', 'our', 'its', 'than', 'as', 'equals', 'plus',
  'minus', 'times', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
  'red', 'blue', 'green', 'yellow', 'big', 'small', 'new', 'old',
];

/** Two words back, these mean the same ("the ripe [apple]", "many ripe [apple]"). A number does too. */
const WORDS_TWO_BEFORE_A_PICTURE_NOUN = [
  'how', 'many', 'much', 'each', 'every', 'the', 'a', 'an', 'some', 'these', 'those', 'this',
  'that', 'more', 'fewer', 'both', 'all', 'no', 'any', 'one', 'two', 'three', 'four', 'five',
  'six', 'seven', 'eight', 'nine', 'ten',
];

function isBlank(ch: string): boolean {
  return ch === ' ' || ch === '\t' || ch === '\n' || ch === '\r' || ch === NO_BREAK_SPACE;
}

function isLetter(ch: string): boolean {
  return /[A-Za-z]/.test(ch);
}

interface EmojiHit {
  start: number;
  end: number;
  /** The emoji without its trailing variation selector. */
  glyph: string;
}

function findEmoji(text: string): EmojiHit[] {
  const hits: EmojiHit[] = [];
  const re = new RegExp(EMOJI_SOURCE, 'g');
  let m = re.exec(text);
  while (m !== null) {
    hits.push({
      start: m.index,
      end: m.index + m[0].length,
      glyph: m[0].split(VARIATION_SELECTOR).join(''),
    });
    m = re.exec(text);
  }
  return hits;
}

/**
 * True when the emoji at `hit` is only decoration: it trails a word or a
 * finished sentence, and is followed by punctuation or nothing.
 */
function isDecorative(text: string, hit: EmojiHit): boolean {
  // What follows (after spaces) must be the end, or sentence punctuation.
  let next = hit.end;
  while (next < text.length && isBlank(text.charAt(next))) next += 1;
  if (next < text.length && '.,!?;:)'.indexOf(text.charAt(next)) === -1) return false;

  // What comes before (after spaces) must be a word or the end of a sentence.
  let prev = hit.start - 1;
  while (prev >= 0 && isBlank(text.charAt(prev))) prev -= 1;
  if (prev < 0) return false; // an emoji that opens the text may be its subject
  const before = text.charAt(prev);
  if ('.!?'.indexOf(before) !== -1) return true; // after a finished sentence
  if (!isLetter(before)) return false; // a digit, a sign, a bracket: it means something

  // The word straight before it.
  let wordStart = prev;
  while (wordStart > 0 && isLetter(text.charAt(wordStart - 1))) wordStart -= 1;
  const word = text.slice(wordStart, prev + 1).toLowerCase();
  if (WORDS_BEFORE_A_PICTURE_NOUN.indexOf(word) !== -1) return false;
  // Part of something longer than a plain word ("5kg", "x-axis"): leave it.
  if (wordStart > 0 && !isBlank(text.charAt(wordStart - 1))) return false;

  // The token before that word: a number or a counting word means "3 ripe [apple]".
  let tokenEnd = wordStart - 1;
  while (tokenEnd >= 0 && isBlank(text.charAt(tokenEnd))) tokenEnd -= 1;
  if (tokenEnd >= 0) {
    let tokenStart = tokenEnd;
    while (tokenStart > 0 && !isBlank(text.charAt(tokenStart - 1))) tokenStart -= 1;
    const token = text.slice(tokenStart, tokenEnd + 1).toLowerCase();
    if (/[0-9]/.test(token)) return false;
    if (WORDS_TWO_BEFORE_A_PICTURE_NOUN.indexOf(token) !== -1) return false;
  }
  return true;
}

function removeDecorativeEmoji(text: string): string {
  const hits = findEmoji(text);
  if (hits.length === 0 || hits.length > MAX_DECORATIVE_EMOJI) return text;
  // Joined emoji are one picture made of several: leave them.
  if (text.indexOf(ZERO_WIDTH_JOINER) !== -1) return text;
  // The same picture twice is being counted or compared, not decorating.
  if (hits.length === 2 && hits[0].glyph === hits[1].glyph) return text;
  // All or nothing: one emoji that means something keeps every emoji in place.
  for (let i = 0; i < hits.length; i++) {
    if (!isDecorative(text, hits[i])) return text;
  }

  let out = '';
  let cursor = 0;
  for (let i = 0; i < hits.length; i++) {
    // Take the spaces in front of the emoji away with it.
    let cut = hits[i].start;
    while (cut > cursor && isBlank(text.charAt(cut - 1))) cut -= 1;
    out += text.slice(cursor, cut);
    cursor = hits[i].end;
  }
  out += text.slice(cursor);
  return out.replace(/\s+$/, '') === '' ? text : out;
}

// -- Spaces before punctuation ------------------------------------------------

/**
 * "for Diwali ." becomes "for Diwali." Only before . , ? ! ; and only where the
 * mark closes a word: a colon is never touched (ratios such as 3 : 4), and a
 * number is only closed up where the mark plainly ends the sentence.
 */
function closeSpacesBeforePunctuation(text: string): string {
  return text.replace(
    /([A-Za-z0-9)%])[ \t]+([.,?!;])(?=\s|$|["')])/g,
    function (match: string, before: string, mark: string, offset: number, whole: string): string {
      if (/[0-9]/.test(before)) {
        if (mark === ',' || mark === ';') return match; // "2 , 3" may be a list or a point: leave it
        if (mark === '.') {
          // Only a full stop that ends the sentence: nothing after it, or a new word.
          const after = whole.slice(offset + match.length);
          if (!/^\s*$/.test(after) && !/^\s+[A-Za-z]/.test(after)) return match;
        }
      }
      return before + mark;
    },
  );
}

/**
 * The question's wording, tidied for the screen: decorative emoji taken out
 * and stray spaces before punctuation closed up. Text holding LaTeX (a
 * backslash) is returned untouched.
 */
export function tidyQuestionText(text: string): string {
  if (!text) return text;
  if (text.indexOf('\\') !== -1) return text;
  return closeSpacesBeforePunctuation(removeDecorativeEmoji(text));
}

// -- Text size ----------------------------------------------------------------

export type QuestionTextSize = 'short' | 'medium' | 'long';

/** Up to this many characters: a one-line or two-line question, set large. */
export const SHORT_QUESTION_MAX = 60;
/** Up to this many characters: the standard question size. Longer is a word problem, set a step smaller. */
export const MEDIUM_QUESTION_MAX = 180;

/** Which of three sizes the question text is set in, by how much there is to read. */
export function questionTextSize(text: string): QuestionTextSize {
  // LaTeX commands and braces are markup, not reading.
  const plain = text.replace(/\\[a-zA-Z]+/g, '').replace(/[{}$]/g, '').replace(/\s+/g, ' ').trim();
  if (plain.length <= SHORT_QUESTION_MAX) return 'short';
  if (plain.length <= MEDIUM_QUESTION_MAX) return 'medium';
  return 'long';
}

// -- Topic chip ---------------------------------------------------------------

/** A topic name longer than this loses its trailing bracket ("Area & Perimeter (rectangles, ...)"). */
export const TOPIC_LABEL_MAX = 30;

/** "Grade 5 - " at the start of a topic name, with an em dash, en dash, hyphen or colon. */
const GRADE_PREFIX = new RegExp('^(?:Grade|Class)\\s*\\d+\\s*[' + LONG_DASHES + ':-]\\s*', 'i');

/**
 * The topic's name for the chip above a question: without the "Grade 5 - "
 * prefix, and without a trailing bracket when the whole name would be too long
 * to show, so it is never cut off mid-bracket.
 */
export function topicChipLabel(subTopic: string): string {
  const original = (subTopic || '').trim();
  let label = original.replace(GRADE_PREFIX, '').trim();
  if (label.length > TOPIC_LABEL_MAX) {
    const withoutBracket = label.replace(/\s*\([^()]*\)\s*$/, '').trim();
    if (withoutBracket) label = withoutBracket;
  }
  return label || original;
}

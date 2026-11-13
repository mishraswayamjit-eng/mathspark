/**
 * Turns verified question / hint / step text (plain text mixed with LaTeX) into
 * a sentence a text-to-speech voice can read naturally.
 *
 * This only changes how verified content is *spoken*. It never computes or
 * alters an answer, so it sits on the "delivery" side of the truth-vs-delivery
 * rule. Pure and deterministic: no browser APIs, safe to unit-test and to reuse
 * when narration audio is generated offline.
 *
 * Regexes deliberately avoid the `u`/`s` flags, named groups and lookbehind:
 * the project compiles to the default ES5 target.
 */

import type { StepItem } from '@/types';

/**
 * The fields narration needs. Both the client `Question` type and a raw
 * database row satisfy this, so the app and the offline narration export
 * produce exactly the same words.
 */
export interface NarrationQuestion {
  questionText: string;
  questionLatex?: string | null;
  option1: string;
  option2: string;
  option3: string;
  option4: string;
  correctAnswer: string;
  interactionType?: string | null;
}

const COMMON_FRACTIONS: Record<string, string> = {
  '1/2': 'one half',
  '1/3': 'one third',
  '2/3': 'two thirds',
  '1/4': 'one quarter',
  '3/4': 'three quarters',
};

function fractionWords(num: string, den: string): string {
  const n = num.trim();
  const d = den.trim();
  const known = COMMON_FRACTIONS[`${n}/${d}`];
  return known ? ` ${known} ` : ` ${n} over ${d} `;
}

/** Replace `\frac{a}{b}` (innermost first, so nested fractions resolve). */
function speakLatexFractions(input: string): string {
  let out = input;
  for (let i = 0; i < 6; i++) {
    const next = out.replace(
      /\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g,
      (_m, a: string, b: string) => fractionWords(a, b),
    );
    if (next === out) break;
    out = next;
  }
  return out;
}

function speakPower(exp: string): string {
  const e = exp.trim();
  if (e === '2') return ' squared ';
  if (e === '3') return ' cubed ';
  return ` to the power ${e} `;
}

/** Convert one piece of text (may contain LaTeX) to speakable English. */
export function toSpeech(input: string | null | undefined): string {
  if (!input) return '';
  let s = String(input);

  // ── LaTeX structure ──────────────────────────────────────────────────────
  s = s.replace(/_{2,}/g, ' blank ');                 // fill-in-the-blank lines (before subscripts)
  s = s.replace(/\\\\/g, '. ');                       // line break
  s = s.replace(/\\(?:text|mathrm|mathbf|textbf|mathit|operatorname)\s*\{([^{}]*)\}/g, ' $1 ');
  // Powers and subscripts first, so a fraction or root containing them has no inner braces left.
  s = s.replace(/\^\s*\{?\s*\\circ\s*\}?/g, ' degrees ');
  s = s.replace(/\^\s*\{([^{}]*)\}/g, (_m, e: string) => speakPower(e));
  s = s.replace(/\^\s*(\d+|[a-zA-Z])/g, (_m, e: string) => speakPower(e));
  s = s.replace(/_\s*\{([^{}]*)\}/g, ' $1 ');
  s = s.replace(/_\s*(\d+|[a-zA-Z])/g, ' $1 ');
  s = speakLatexFractions(s);
  s = s.replace(/\\sqrt\s*\[\s*3\s*\]\s*\{([^{}]*)\}/g, ' the cube root of $1 ');
  s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, ' the square root of $1 ');

  // ── LaTeX commands ───────────────────────────────────────────────────────
  s = s.replace(/\\(?:times|cdot)\b/g, ' times ');
  s = s.replace(/\\div\b/g, ' divided by ');
  s = s.replace(/\\pm\b/g, ' plus or minus ');
  s = s.replace(/\\(?:leq|le)\b/g, ' is less than or equal to ');
  s = s.replace(/\\(?:geq|ge)\b/g, ' is greater than or equal to ');
  s = s.replace(/\\(?:neq|ne)\b/g, ' is not equal to ');
  s = s.replace(/\\lt\b/g, ' is less than ');
  s = s.replace(/\\gt\b/g, ' is greater than ');
  s = s.replace(/\\approx\b/g, ' is about ');
  s = s.replace(/\\(?:rightarrow|to|Rightarrow|implies)\b/g, ' gives ');
  s = s.replace(/\\(alpha|beta|gamma|theta)\b/g, ' $1 ');
  s = s.replace(/\\angle\b/g, ' angle ');
  s = s.replace(/\\triangle\b/g, ' triangle ');
  s = s.replace(/\\(?:degree|circ)\b/g, ' degrees ');
  s = s.replace(/\\pi\b/g, ' pi ');
  s = s.replace(/\\%/g, ' percent ');
  s = s.replace(/\\(?:left|right|displaystyle|quad|qquad)\b/g, ' ');
  s = s.replace(/\\[,;:! ()[\]]/g, ' ');             // spacing commands and \( \) \[ \] delimiters
  s = s.replace(/\\[a-zA-Z]+/g, ' ');                 // any command left over
  s = s.replace(/[{}$]/g, ' ');

  // ── Money, percent, degrees ──────────────────────────────────────────────
  s = s.replace(/₹\s*(\d+(?:,\d+)*(?:\.\d+)?)/g, ' $1 rupees ');
  s = s.replace(/₹\s*([a-zA-Z])\b/g, ' $1 rupees ');
  s = s.replace(/₹/g, ' rupees ');
  s = s.replace(/%/g, ' percent ');
  s = s.replace(/°/g, ' degrees ');

  // ── Plain-text fractions and powers ──────────────────────────────────────
  s = s.replace(/(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)/g, (_m, a: string, b: string) => fractionWords(a, b));
  s = s.replace(/²/g, ' squared ');
  s = s.replace(/³/g, ' cubed ');
  s = s.replace(/√/g, ' the square root of ');
  s = s.replace(/π/g, ' pi ');

  // ── Operators and relations ──────────────────────────────────────────────
  s = s.replace(/[×✕]/g, ' times ');
  s = s.replace(/÷/g, ' divided by ');
  s = s.replace(/≤/g, ' is less than or equal to ');
  s = s.replace(/≥/g, ' is greater than or equal to ');
  s = s.replace(/≠/g, ' is not equal to ');
  s = s.replace(/≈/g, ' is about ');
  s = s.replace(/→|->|=>/g, ' gives ');               // arrows, before < > = are read
  s = s.replace(/<=/g, ' is less than or equal to ');
  s = s.replace(/>=/g, ' is greater than or equal to ');
  s = s.replace(/</g, ' is less than ');
  s = s.replace(/>/g, ' is greater than ');
  s = s.replace(/=/g, ' equals ');
  s = s.replace(/\+/g, ' plus ');
  s = s.replace(/(\d)\s*\*\s*(\d)/g, '$1 times $2');
  s = s.replace(/□/g, ' blank ');
  s = s.replace(/△/g, ' triangle ');
  s = s.replace(/(\d)\s*–\s*(\d)/g, '$1 to $2');      // en dash between numbers is a range
  s = s.replace(/−/g, ' minus ');                     // U+2212 true minus sign
  // ASCII hyphen: read as minus only where it is clearly maths, so "3-digit",
  // "3-D" and "Not quite - try again" are left alone.
  s = s.replace(/(^|[\s(])-\s*(\d)/g, '$1 minus $2');                         // -5, (-3)
  s = s.replace(/(equals\s+|\(\s*)-\s*([a-zA-Z]\b)/g, '$1 minus $2');         // = -y (the = is already "equals")
  s = s.replace(/(\d|\))-(\d)/g, '$1 minus $2');                              // 9-4
  s = s.replace(/(\d[a-zA-Z]|\b[a-zA-Z])-(\d)/g, '$1 minus $2');              // 2n-3, x-5
  s = s.replace(/(\d[a-zA-Z]|\d|\)|\b[a-zA-Z])\s-\s(\d|\(|[a-zA-Z]\b)/g, '$1 minus $2'); // 2m - 3, a - b

  // ── Emoji and decoration (never read aloud) ──────────────────────────────
  s = s.replace(/[\uD83C-\uDBFF][\uDC00-\uDFFF]/g, ' ');
  s = s.replace(/[\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]/g, ' ');

  return s.replace(/\s+/g, ' ').replace(/\s+([.,?!])/g, '$1').trim();
}

/** Join spoken sentences, making sure each one ends with a pause. */
function joinSentences(parts: string[]): string {
  const out: string[] = [];
  for (let i = 0; i < parts.length; i++) {
    const p = parts[i].trim();
    if (!p) continue;
    out.push(/[.?!]$/.test(p) ? p : `${p}.`);
  }
  return out.join(' ');
}

/** The question, then its four options (options are skipped for interactive questions). */
export function questionToSpeech(q: NarrationQuestion): string {
  const parts: string[] = [toSpeech(q.questionText)];
  if (q.questionLatex) parts.push(toSpeech(q.questionLatex));
  if (!q.interactionType) {
    parts.push(`Option A: ${toSpeech(q.option1)}`);
    parts.push(`Option B: ${toSpeech(q.option2)}`);
    parts.push(`Option C: ${toSpeech(q.option3)}`);
    parts.push(`Option D: ${toSpeech(q.option4)}`);
  }
  return joinSentences(parts);
}

/** One solution step: its sentence, then its maths line if it has one. */
export function stepToSpeech(step: StepItem): string {
  const parts: string[] = [toSpeech(step.text)];
  if (step.latex) parts.push(toSpeech(step.latex));
  return joinSentences(parts);
}

/**
 * What the solution walkthrough says for step `index` (0-based). The last
 * step also announces the verified answer.
 */
export function walkthroughStepSpeech(q: NarrationQuestion, steps: StepItem[], index: number): string {
  let text = stepToSpeech(steps[index]);
  if (index >= steps.length - 1) {
    const options = [q.option1, q.option2, q.option3, q.option4];
    const answerIdx = ['A', 'B', 'C', 'D'].indexOf(q.correctAnswer);
    if (answerIdx !== -1) {
      text = `${text} The answer is ${q.correctAnswer}: ${toSpeech(options[answerIdx])}.`;
    }
  }
  return text;
}

/** The hints currently on screen, in order. */
export function hintsToSpeech(hints: string[]): string {
  const parts: string[] = [];
  for (let i = 0; i < hints.length; i++) parts.push(toSpeech(hints[i]));
  return joinSentences(parts);
}

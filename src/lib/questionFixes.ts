/**
 * Corrected question content, laid over what the database returns.
 *
 * Fixes to hints, steps, answer-choice wording and question wording are
 * authored offline, checked by `scripts/fixes/check.py` (every written-out sum
 * true, the steps ending on the keyed answer, no hint stating it) and built
 * into the data file by `python scripts/fixes/apply.py --write`. The same run
 * updates the seed file, so the database catches up at the next re-seed; this
 * overlay makes the fixes reach children as soon as the app is deployed.
 *
 * It never changes which choice is correct. Grading reads the answer key from
 * the database and is untouched.
 *
 * Server only: import from API routes, so the data stays out of the browser.
 */

import fixes from '@/data/questionFixes/fixes.json';

interface StepFix { step: number; text: string; latex?: string }

interface QuestionFix {
  questionText?: string;
  options?: string[];
  hints?: string[];
  steps?: StepFix[];
}

const ALL = fixes as unknown as Record<string, QuestionFix>;

/**
 * Returns the question with its corrected fields, or the same object when it
 * has no fix. A field is only replaced when the object already carries it, so
 * a route that withholds hints or steps keeps withholding them.
 *
 * `withSolution: false` (a test in progress) applies wording fixes only.
 */
export function withFixes<T extends { id: string }>(question: T, opts: { withSolution: boolean }): T {
  if (!Object.prototype.hasOwnProperty.call(ALL, question.id)) return question;
  const fix = ALL[question.id];
  const out = { ...question } as T & Record<string, unknown>;
  const has = (key: string): boolean => Object.prototype.hasOwnProperty.call(out, key);
  const set = (key: string, value: unknown): void => { (out as Record<string, unknown>)[key] = value; };

  if (typeof fix.questionText === 'string' && has('questionText')) set('questionText', fix.questionText);
  if (Array.isArray(fix.options) && fix.options.length === 4) {
    for (let i = 0; i < 4; i++) {
      if (has(`option${i + 1}`)) set(`option${i + 1}`, fix.options[i]);
    }
  }
  if (opts.withSolution) {
    if (Array.isArray(fix.hints) && fix.hints.length === 3) {
      for (let i = 0; i < 3; i++) {
        if (has(`hint${i + 1}`)) set(`hint${i + 1}`, fix.hints[i]);
      }
    }
    // Only where the route has already parsed the steps into a list.
    if (Array.isArray(fix.steps) && Array.isArray(out.stepByStep)) {
      set('stepByStep', fix.steps);
    }
  }
  return out;
}

/**
 * Server-side lookup of the visuals attached to a question.
 *
 * The data is built offline by `python scripts/figures/validate.py --build`
 * (which refuses to write unless every figure passes its checks) and is keyed
 * by question id. Import this from API routes only, so the data stays out of
 * the browser bundle.
 */

import figures from '@/data/questionFigures/figures.json';
import speech from '@/data/questionSpeech/speech.json';
import type { QuestionSpeech } from '@/types';
import type { ServedVisual } from './types';
import { withFixes } from '@/lib/questionFixes';

const ALL = figures as unknown as Record<string, ServedVisual>;
// Authored narration, built by `python scripts/speech/validate.py --build`.
const SPEECH = speech as unknown as Record<string, QuestionSpeech>;

/**
 * The visual for one question, or undefined if it has none.
 *
 * `withSolution: false` returns the before-answering figure only. Use it
 * wherever the solution must stay hidden: mock tests and past papers in
 * progress. Step figures and computed steps show worked values.
 */
export function visualFor(questionId: string, opts: { withSolution: boolean }): ServedVisual | undefined {
  if (!Object.prototype.hasOwnProperty.call(ALL, questionId)) return undefined;
  const v = ALL[questionId];
  if (opts.withSolution) return v;
  return v.figure ? { figure: v.figure } : undefined;
}

/**
 * The narration for one question, or undefined if none has been written.
 * With `withSolution: false` only the question and its choices are returned:
 * hint and step narration says the working aloud.
 */
export function speechFor(questionId: string, opts: { withSolution: boolean }): QuestionSpeech | undefined {
  if (!Object.prototype.hasOwnProperty.call(SPEECH, questionId)) return undefined;
  const s = SPEECH[questionId];
  if (!s || typeof s.q !== 'string') return undefined;
  if (opts.withSolution) return s;
  return { q: s.q, options: s.options, hints: [], steps: [] };
}

/**
 * Applies any corrected content to a question, then adds `visual` and `speech`
 * when it has them. Returns a new object. Every route that serves a question
 * to a screen goes through here, so fixes, figures and narration always
 * travel together and describe the same text.
 */
export function withVisual<T extends { id: string }>(
  question: T,
  opts: { withSolution: boolean },
): T & { visual?: ServedVisual; speech?: QuestionSpeech } {
  const fixed = withFixes(question, opts);
  const visual = visualFor(question.id, opts);
  const spoken = speechFor(question.id, opts);
  if (!visual && !spoken) return fixed;
  const out: T & { visual?: ServedVisual; speech?: QuestionSpeech } = { ...fixed };
  if (visual) out.visual = visual;
  if (spoken) out.speech = spoken;
  return out;
}

/** Ids of every question that has a visual, in a steady order (for the review gallery). */
export function visualQuestionIds(): string[] {
  return Object.keys(ALL).sort();
}

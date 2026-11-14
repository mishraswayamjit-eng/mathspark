/**
 * Server-side lookup of the visuals attached to a question.
 *
 * The data is built offline by `python scripts/figures/validate.py --build`
 * (which refuses to write unless every figure passes its checks) and is keyed
 * by question id. Import this from API routes only, so the data stays out of
 * the browser bundle.
 */

import figures from '@/data/questionFigures/figures.json';
import type { ServedVisual } from './types';

const ALL = figures as unknown as Record<string, ServedVisual>;

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

/** Adds `visual` to a question object when it has one. Returns a new object. */
export function withVisual<T extends { id: string }>(question: T, opts: { withSolution: boolean }): T & { visual?: ServedVisual } {
  const visual = visualFor(question.id, opts);
  return visual ? { ...question, visual } : question;
}

/** Ids of every question that has a visual, in a steady order (for the review gallery). */
export function visualQuestionIds(): string[] {
  return Object.keys(ALL).sort();
}

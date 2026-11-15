/**
 * Server-side lookup of the teach-mode lesson for a question.
 *
 * The data is built offline by `python scripts/teach/validate.py --build`,
 * which refuses to write unless every lesson passes its checks. Import this
 * from API routes only, so the lessons stay out of the browser bundle.
 */

import scripts from '@/data/teach/scripts.json';
import type { TeachBeat } from './types';

/** What a screen receives: the beats of the lesson. */
export interface ServedTeachScript {
  beats: TeachBeat[];
}

const ALL = scripts as unknown as Record<string, ServedTeachScript>;

/** The lesson for one question, or undefined if none has been written. */
export function teachFor(questionId: string): ServedTeachScript | undefined {
  if (!Object.prototype.hasOwnProperty.call(ALL, questionId)) return undefined;
  const s = ALL[questionId];
  return s && Array.isArray(s.beats) && s.beats.length > 0 ? s : undefined;
}

/** True when a lesson exists, without sending it. */
export function hasTeachScript(questionId: string): boolean {
  return teachFor(questionId) !== undefined;
}

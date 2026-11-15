/**
 * Teach mode ("Explain it to me"): a teacher's lesson for one question.
 *
 * A lesson is a list of beats. In each beat the teacher SAYS one or two short
 * sentences while the board DOES something: a new line of working is written,
 * an arc shows a number multiplying into a bracket, a term is struck out with
 * what was done written above it, the answer is ringed. Some beats stop and
 * ASK the child to predict the next move before it is shown.
 *
 * THE CONTRACT. Three things are built against this file and must agree:
 *   - the board renderer and lesson player   src/components/teach/
 *   - the offline lesson scripts              data/teach/parts/*.json  (checked by scripts/teach/validate.py)
 *   - the route that serves a lesson          src/app/api/teach/
 * Change a type here and scripts/teach/validate.py must change with it.
 *
 * Lessons are written offline and checked before they ship: every line of
 * maths on the board is verified (an equation must hold at the answer; a sum
 * must be true), and the lesson must end on the question's keyed answer.
 * Nothing here is generated while a child uses the app, and nothing here feeds
 * grading, XP or mastery.
 */

import type { FigureSpec } from '@/lib/figures/types';

/** Which pen a line is written with. */
export type BoardTone =
  | 'given'    // the question as printed: dark ink
  | 'work'     // the teacher's working: blue pen
  | 'answer';  // the final answer: blue pen, drawn larger

/**
 * A place on a line: a piece of the line's own text. `nth` picks the 1st, 2nd...
 * occurrence when the text appears more than once (default 1).
 * Example: on the line "10x − 34 = 3x + 15", { text: "3x" } is the term on the right.
 */
export interface BoardTarget {
  text: string;
  nth?: number;
}

/**
 * Something the teacher does on the board. Ops in one beat happen in order,
 * spread over the time it takes to say the beat.
 */
export type BoardOp =
  /**
   * Write a new line under the last one. `text` is plain maths notation, the
   * way it would be written by hand: "4(3x − 5) − 2(x + 7) = 3x + 15",
   * "12x − 20 − 2x − 14 = 3x + 15", "3/4 + 1/8 = 7/8", "25% of 240 = 60".
   * With `label: true` the line is words, not maths ("Area = length × breadth").
   */
  | { op: 'write'; id: string; text: string; tone?: BoardTone; label?: boolean }
  /**
   * An arc drawn over a line from one place to one or more others: the
   * "multiply into the bracket" mark. from "4", to ["3x", "5"].
   */
  | { op: 'arc'; line: string; from: BoardTarget; to: BoardTarget[] }
  /**
   * Cross a place out, with a small note written above it saying what was done
   * ("− 3x", "+ 34"). Used when a term is moved or cancelled.
   */
  | { op: 'strike'; line: string; target: BoardTarget; note?: string }
  /** A small note above or below a place, without crossing it out. */
  | { op: 'note'; line: string; target: BoardTarget; text: string; place?: 'above' | 'below' }
  /** Draw attention to a place. */
  | { op: 'mark'; line: string; target: BoardTarget; shape: 'underline' | 'circle' | 'box' }
  /**
   * "Do the same to both sides": writes `text` under each side of the equation
   * on that line ("− 3x" under both sides).
   */
  | { op: 'both'; line: string; text: string }
  /** Divide both sides: draws a bar under each side with `by` beneath it. */
  | { op: 'divide'; line: string; by: string }
  /** Group several places with a bracket underneath and a label ("like terms", "10x"). */
  | { op: 'group'; line: string; targets: BoardTarget[]; label?: string }
  /** Show a figure from the figure library beside the working (a bar model, a triangle, a place-value chart). */
  | { op: 'figure'; id: string; spec: FigureSpec }
  /** Wipe the board (rare: only when a lesson moves to a fresh part). */
  | { op: 'clear' };

/**
 * A point where the teacher stops and the child takes a turn.
 *   choose  the child taps one of two to four choices; `answer` is the index of the right one.
 *           `ifNot` is what the teacher says after a miss, before carrying on (never "wrong").
 *   think   an open question with no checking: the child taps "I've got an idea" when ready.
 */
export type BeatAsk =
  | { kind: 'choose'; choices: string[]; answer: number; ifNot: string }
  | { kind: 'think' };

export interface TeachBeat {
  /**
   * What the teacher says: one or two short spoken sentences, in words a voice
   * can say (no symbols). This is also shown as the caption.
   */
  say: string;
  /** What happens on the board while it is said. */
  board?: BoardOp[];
  /** Stop here for the child's turn, after `say` has been spoken. */
  ask?: BeatAsk;
}

/** A lesson for one question. Stored offline, keyed by question id. */
export interface TeachScript {
  /**
   * How the lesson's maths is checked offline. For an equation: the letter and
   * its value at the answer, e.g. { variable: "x", value: "7" }. Leave out
   * when the working has no unknown.
   */
  check?: { variable: string; value: string };
  /** Six to sixteen beats. */
  beats: TeachBeat[];
  /** 'rule': produced by a template rule. 'authored': written for this one question. */
  origin: 'rule' | 'authored';
}

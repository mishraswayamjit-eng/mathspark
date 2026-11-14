/**
 * Hands-on lessons: shapes cut into pieces that a child colours to show a fraction.
 *
 * A piece is worth its area, worked out from its corners, so a figure can mix
 * big and small pieces and still be checked exactly. All arithmetic is in whole
 * numbers (twice the area of a polygon on a whole-number grid is a whole number).
 *
 * The lesson content is authored and machine-checked offline by
 * scripts/build_hands_on_fractions.py. Nothing here is generated at runtime, and
 * these lessons do not feed XP, mastery or grading.
 */

import data from '@/data/handsOn/fractions.json';

export interface PartitionFigure {
  w: number;
  h: number;
  /** Each piece is a list of [x, y] corners on the grid. */
  pieces: number[][][];
  /** The outer shape, when it is not the full w by h rectangle. */
  outline?: number[][];
}

export interface ShownFigure {
  figure: string;
  shaded: number[];
  label: string;
}

export type LessonScreen =
  | { kind: 'do'; figure: string; target: number[]; prompt: string; say: string; why: string }
  | { kind: 'check'; figure: string; target: number[]; prompt: string; why: string }
  | { kind: 'see'; text: string; say: string; show: ShownFigure[] };

export interface HandsOnLesson {
  id: string;
  title: string;
  blurb: string;
  grades: number[];
  screens: LessonScreen[];
}

const FIGURES = data.figures as unknown as Record<string, PartitionFigure>;
export const HANDS_ON_TOPIC: string = data.topic;
export const HANDS_ON_LESSONS = data.lessons as unknown as HandsOnLesson[];

export function getFigure(name: string): PartitionFigure | null {
  return Object.prototype.hasOwnProperty.call(FIGURES, name) ? FIGURES[name] : null;
}

export function getLesson(id: string): HandsOnLesson | null {
  for (let i = 0; i < HANDS_ON_LESSONS.length; i++) {
    if (HANDS_ON_LESSONS[i].id === id) return HANDS_ON_LESSONS[i];
  }
  return null;
}

export function nextLessonId(id: string): string | null {
  for (let i = 0; i < HANDS_ON_LESSONS.length - 1; i++) {
    if (HANDS_ON_LESSONS[i].id === id) return HANDS_ON_LESSONS[i + 1].id;
  }
  return null;
}

// ── Whole-number geometry ────────────────────────────────────────────────────

/** Twice the area of a polygon. */
function area2(points: number[][]): number {
  let total = 0;
  for (let i = 0; i < points.length; i++) {
    const a = points[i];
    const b = points[(i + 1) % points.length];
    total += a[0] * b[1] - b[0] * a[1];
  }
  return Math.abs(total);
}

export function pieceValues(fig: PartitionFigure): number[] {
  const out: number[] = [];
  for (let i = 0; i < fig.pieces.length; i++) out.push(area2(fig.pieces[i]));
  return out;
}

function gcd(a: number, b: number): number {
  let x = Math.abs(a);
  let y = Math.abs(b);
  while (y) {
    const t = y;
    y = x % y;
    x = t;
  }
  return x || 1;
}

export interface Amount {
  /** Coloured value and whole value, in the same units. */
  coloured: number;
  whole: number;
}

export function colouredAmount(fig: PartitionFigure, shaded: boolean[]): Amount {
  const values = pieceValues(fig);
  let coloured = 0;
  let whole = 0;
  for (let i = 0; i < values.length; i++) {
    whole += values[i];
    if (shaded[i]) coloured += values[i];
  }
  return { coloured, whole };
}

/** True when exactly n/d of the figure is coloured. */
export function meetsTarget(fig: PartitionFigure, shaded: boolean[], n: number, d: number): boolean {
  const a = colouredAmount(fig, shaded);
  return a.coloured * d === n * a.whole;
}

/**
 * The coloured amount as a fraction the child will recognise: over the target's
 * bottom number when that comes out whole, otherwise in lowest terms.
 */
export function colouredFraction(fig: PartitionFigure, shaded: boolean[], d: number): string {
  const a = colouredAmount(fig, shaded);
  if (a.coloured === 0) return 'nothing';
  if (a.coloured === a.whole) return 'the whole shape';
  if ((a.coloured * d) % a.whole === 0) return `${(a.coloured * d) / a.whole}/${d}`;
  const g = gcd(a.coloured, a.whole);
  return `${a.coloured / g}/${a.whole / g}`;
}

/** One way to colour n/d of the figure, or null if the pieces cannot make it. */
export function solveTarget(fig: PartitionFigure, n: number, d: number): boolean[] | null {
  const values = pieceValues(fig);
  let whole = 0;
  for (let i = 0; i < values.length; i++) whole += values[i];
  if ((n * whole) % d !== 0) return null;
  const goal = (n * whole) / d;

  // last[s] = the piece that first reached the sum s (-1: not reached, -2: the empty start).
  const last: number[] = [];
  for (let s = 0; s <= goal; s++) last.push(-1);
  last[0] = -2;
  for (let i = 0; i < values.length; i++) {
    for (let s = goal; s >= values[i]; s--) {
      if (last[s] === -1 && last[s - values[i]] !== -1) last[s] = i;
    }
  }
  if (last[goal] === -1) return null;

  const out: boolean[] = [];
  for (let i = 0; i < values.length; i++) out.push(false);
  let s = goal;
  while (s > 0) {
    const piece = last[s];
    out[piece] = true;
    s -= values[piece];
  }
  return out;
}

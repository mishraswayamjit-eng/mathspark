/**
 * The teacher's board, worked out from the list of ops: which rows are on the
 * board (lines of working and figures), which marks sit on which line, and
 * which characters of a line each mark points at. Pure: no DOM, no React.
 */

import type { BoardOp, BoardTarget, BoardTone } from '@/lib/teach/types';
import type { FigureSpec } from '@/lib/figures/types';

/** A box on screen, in pixels, measured from the top-left corner of its row. */
export interface Rect {
  x: number;
  y: number;
  w: number;
  h: number;
}

/** A run of characters in a line's text: [start, end). */
export interface Span {
  start: number;
  end: number;
}

export interface LineRow {
  kind: 'line';
  /** Stable React key and DOM handle: the index of the op that wrote it. */
  key: string;
  id: string;
  opIndex: number;
  text: string;
  tone: BoardTone;
  label: boolean;
  /** Index of the equals sign the line is centred on, or -1. */
  eq: number;
  /** True when a mark is written under this line, so it needs room below. */
  below: boolean;
}

export interface FigureRow {
  kind: 'figure';
  key: string;
  id: string;
  opIndex: number;
  spec: FigureSpec;
}

export type BoardRow = LineRow | FigureRow;

/** Every op that marks an existing line. */
export type MarkOp = Extract<BoardOp, { line: string }>;

export interface BoardMark {
  opIndex: number;
  rowKey: string;
  op: MarkOp;
}

export interface BoardModel {
  rows: BoardRow[];
  marks: BoardMark[];
  /** The row the newest op touched: the one to keep in view. */
  focusKey: string | null;
  /** The lines in order, for the text alternative. */
  spoken: string;
}

/** The equals sign a line is centred on: the first one that is not part of <=, >=, != or ==. */
export function equalsIndex(text: string): number {
  for (let i = 0; i < text.length; i++) {
    if (text.charAt(i) !== '=') continue;
    const before = i > 0 ? text.charAt(i - 1) : '';
    const after = text.charAt(i + 1);
    if (before === '<' || before === '>' || before === '!' || before === '=' || after === '=') continue;
    return i;
  }
  return -1;
}

function trimSpan(text: string, start: number, end: number): Span | null {
  let s = start;
  let e = end;
  while (s < e && text.charAt(s) === ' ') s++;
  while (e > s && text.charAt(e - 1) === ' ') e--;
  return s < e ? { start: s, end: e } : null;
}

/**
 * Where a target sits in a line's text. Occurrences are counted the way
 * scripts/teach/validate.py counts them: plain, non-overlapping, left to right.
 * Returns null when the text is not there.
 */
export function findTarget(text: string, target: BoardTarget | null | undefined): Span | null {
  if (!target || typeof target.text !== 'string' || target.text === '') return null;
  const nth = typeof target.nth === 'number' && target.nth >= 1 ? Math.floor(target.nth) : 1;
  let from = 0;
  let at = -1;
  for (let k = 0; k < nth; k++) {
    at = text.indexOf(target.text, from);
    if (at < 0) return null;
    from = at + target.text.length;
  }
  return trimSpan(text, at, at + target.text.length);
}

/** The two sides of the equation on a line (or the whole line when it has no equals sign). */
export function sideSpans(row: LineRow): Array<Span | null> {
  if (row.eq < 0) return [trimSpan(row.text, 0, row.text.length)];
  return [trimSpan(row.text, 0, row.eq), trimSpan(row.text, row.eq + 1, row.text.length)];
}

/**
 * The places a mark needs measured, in a fixed order per op:
 *   arc            [from, ...to]
 *   strike/note/mark  [target]
 *   both/divide    [left side, right side]
 *   group          [...targets]
 */
export function markSpans(row: LineRow, op: MarkOp): Array<Span | null> {
  const out: Array<Span | null> = [];
  switch (op.op) {
    case 'arc': {
      out.push(findTarget(row.text, op.from));
      const to = Array.isArray(op.to) ? op.to : [];
      for (let i = 0; i < to.length; i++) out.push(findTarget(row.text, to[i]));
      return out;
    }
    case 'strike':
    case 'note':
    case 'mark':
      out.push(findTarget(row.text, op.target));
      return out;
    case 'both':
    case 'divide':
      return sideSpans(row);
    case 'group': {
      const targets = Array.isArray(op.targets) ? op.targets : [];
      for (let i = 0; i < targets.length; i++) out.push(findTarget(row.text, targets[i]));
      return out;
    }
    default:
      return out;
  }
}

function writesBelow(op: MarkOp): boolean {
  if (op.op === 'both' || op.op === 'divide' || op.op === 'group') return true;
  if (op.op === 'note') return op.place === 'below';
  return false;
}

/** Replays the ops into what is on the board now. Unknown or malformed ops are skipped. */
export function buildModel(ops: BoardOp[]): BoardModel {
  let rows: BoardRow[] = [];
  let marks: BoardMark[] = [];
  let byId: Record<string, LineRow> = {};
  let focusKey: string | null = null;

  const list = Array.isArray(ops) ? ops : [];
  for (let i = 0; i < list.length; i++) {
    const op = list[i];
    if (!op || typeof op !== 'object') continue;
    if (op.op === 'clear') {
      rows = [];
      marks = [];
      byId = {};
      focusKey = null;
    } else if (op.op === 'write') {
      if (typeof op.text !== 'string' || typeof op.id !== 'string') continue;
      const row: LineRow = {
        kind: 'line',
        key: 'r' + i,
        id: op.id,
        opIndex: i,
        text: op.text,
        tone: op.tone === 'given' || op.tone === 'answer' ? op.tone : 'work',
        label: op.label === true,
        eq: equalsIndex(op.text),
        below: false,
      };
      rows.push(row);
      byId[op.id] = row;
      focusKey = row.key;
    } else if (op.op === 'figure') {
      if (!op.spec || typeof op.spec !== 'object') continue;
      const key = 'r' + i;
      const figureId = String(op.id);
      // A figure drawn again under the same id is the same picture moved on a
      // step (pieces labelled, a part highlighted): it takes the old one's
      // place instead of appearing a second time further down the board.
      let replaced = false;
      for (let r = 0; r < rows.length; r++) {
        const existing = rows[r];
        if (existing.kind === 'figure' && existing.id === figureId) {
          rows[r] = { kind: 'figure', key: key, id: figureId, opIndex: i, spec: op.spec };
          replaced = true;
          break;
        }
      }
      if (!replaced) rows.push({ kind: 'figure', key: key, id: figureId, opIndex: i, spec: op.spec });
      focusKey = key;
    } else if (typeof op.line === 'string') {
      if (!Object.prototype.hasOwnProperty.call(byId, op.line)) continue;
      const row = byId[op.line];
      marks.push({ opIndex: i, rowKey: row.key, op: op });
      if (writesBelow(op)) row.below = true;
      focusKey = row.key;
    }
  }

  const spokenLines: string[] = [];
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    if (row.kind === 'line') spokenLines.push(row.text);
  }

  return {
    rows: rows,
    marks: marks,
    focusKey: focusKey,
    spoken: spokenLines.join('. '),
  };
}

/** When a new op starts appearing and how long it takes, in milliseconds. */
export interface Timing {
  delay: number;
  dur: number;
}

/**
 * New ops (index >= animateFrom) share the beat equally, one after another.
 * Ops already on the board get null: they are simply shown.
 */
export function timingFor(opIndex: number, animateFrom: number, total: number, beatMs: number): Timing | null {
  if (opIndex < animateFrom || opIndex >= total) return null;
  const count = Math.max(1, total - Math.max(0, animateFrom));
  const ms = typeof beatMs === 'number' && beatMs > 0 ? beatMs : 0;
  const slot = Math.max(260, ms / count);
  return {
    delay: Math.round((opIndex - Math.max(0, animateFrom)) * slot),
    dur: Math.round(Math.min(1600, Math.max(220, slot * 0.85))),
  };
}

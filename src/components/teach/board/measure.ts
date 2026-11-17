/**
 * Lays the lines out and finds where each mark goes, by measuring the real
 * text in the browser.
 *
 * Each line is a real piece of text in the page: one, or three (left side,
 * equals sign, right side), spans inside a `[data-text]` element. To find a
 * place on a line we take the character range of the target in the line's
 * text, make a DOM Range over exactly those characters of the span's text
 * node, and ask the browser for its box. So positions come from the browser's
 * own text layout: they follow the font, its kerning, the size the line was
 * fitted to, and the board's width.
 *
 * This module sets `font-size` and `left` on the `[data-text]` elements
 * directly and returns the same numbers, which the board then also renders,
 * so the two always agree.
 */

import { clamp } from './geometry';
import { markSpans } from './model';
import type { BoardModel, LineRow, Rect, Span } from './model';

export interface RowLayout {
  /** Font size of the line, in pixels. */
  f: number;
  /** How far the line is pushed in from the left edge of the board, in pixels. */
  left: number;
  /** True for a line of words too long for the board: it fills the width and wraps. */
  wrap: boolean;
}

export interface BoardLayout {
  /** Width of the writing area, in pixels. */
  width: number;
  /** The board's base font size, in pixels. */
  base: number;
  rows: Record<string, RowLayout>;
  /** For each mark (by op index): the boxes of its places, in the order `markSpans` gives them. */
  rects: Record<number, Array<Rect | null>>;
}

/** Where the equals signs line up, as a fraction of the board's width. Left sides are usually the longer ones. */
const AXIS = 0.54;

/** A line of words (a label) is never shrunk below this size, in pixels: it wraps instead. */
const MIN_LABEL_FONT = 14;

function round2(value: number): number {
  return Math.round(value * 100) / 100;
}

export function toneScale(row: LineRow): number {
  if (row.tone === 'answer') return 1.3;
  if (row.label) return 0.82;
  return 1;
}

/** The base font size for a board this wide: about 20px on a phone, 30px on a tablet pane. */
export function baseFont(width: number): number {
  return round2(clamp(width * 0.068, 20, 30));
}

function segmentStarts(row: LineRow): number[] {
  return row.eq >= 0 ? [0, row.eq, row.eq + 1] : [0];
}

/** The box round characters [span.start, span.end) of a line, relative to `origin`. */
function spanRect(textEl: Element, row: LineRow, span: Span, origin: DOMRect): Rect | null {
  const segs = textEl.querySelectorAll('[data-seg]');
  const starts = segmentStarts(row);
  let left = Infinity;
  let top = Infinity;
  let right = -Infinity;
  let bottom = -Infinity;
  for (let i = 0; i < segs.length && i < starts.length; i++) {
    const node = segs[i].firstChild;
    if (!node || node.nodeType !== 3) continue;
    const length = (node.nodeValue || '').length;
    const s = Math.max(span.start, starts[i]) - starts[i];
    const e = Math.min(span.end, starts[i] + length) - starts[i];
    if (e <= s) continue;
    const range = document.createRange();
    range.setStart(node, s);
    range.setEnd(node, e);
    const box = range.getBoundingClientRect();
    if (box.width <= 0 && box.height <= 0) continue;
    if (box.left < left) left = box.left;
    if (box.top < top) top = box.top;
    if (box.right > right) right = box.right;
    if (box.bottom > bottom) bottom = box.bottom;
  }
  if (right <= left || bottom <= top) return null;
  return { x: left - origin.left, y: top - origin.top, w: right - left, h: bottom - top };
}

/**
 * Fits every line to the board and measures every mark's places.
 * Returns null when the board has no width yet (not on screen).
 */
export function measureBoard(root: HTMLElement, model: BoardModel): BoardLayout | null {
  const width = root.clientWidth;
  if (!(width > 0)) return null;
  const base = baseFont(width);
  const axis = width * AXIS;

  const rowEls: Record<string, HTMLElement> = {};
  const found = root.querySelectorAll<HTMLElement>('[data-row]');
  for (let i = 0; i < found.length; i++) {
    const key = found[i].getAttribute('data-row');
    if (key) rowEls[key] = found[i];
  }

  const textEls: Record<string, HTMLElement> = {};
  const lineRows: Record<string, LineRow> = {};
  const rows: Record<string, RowLayout> = {};

  // 1. Size and place each line. A line never depends on another line, so
  //    writing a new one cannot move the ones above it.
  for (let i = 0; i < model.rows.length; i++) {
    const row = model.rows[i];
    if (row.kind !== 'line') continue;
    const rowEl = rowEls[row.key];
    if (!rowEl) continue;
    const textEl = rowEl.querySelector<HTMLElement>('[data-text]');
    if (!textEl) continue;
    textEls[row.key] = textEl;
    lineRows[row.key] = row;

    const natural = round2(base * toneScale(row));
    let f = natural;
    let wrap = false;
    // Measure the line as one unbroken line first, whatever it was last time.
    textEl.style.whiteSpace = '';
    textEl.style.width = '';
    textEl.style.textAlign = '';
    textEl.style.fontSize = f + 'px';
    textEl.style.left = '0px';
    let w = textEl.getBoundingClientRect().width;
    if (w > width) {
      const fitted = round2(Math.max(natural * 0.5, natural * (width / w) * 0.985));
      if (row.label && fitted < MIN_LABEL_FONT) {
        // A line of words too long for the board: it keeps its size and runs
        // on to a second line, rather than shrinking until it cannot be read.
        wrap = true;
        textEl.style.whiteSpace = 'pre-wrap';
        textEl.style.width = width + 'px';
        textEl.style.textAlign = 'center';
        w = width;
      } else {
        // Too long for the board: this one line is written smaller.
        f = fitted;
        textEl.style.fontSize = f + 'px';
        w = textEl.getBoundingClientRect().width;
      }
    }

    let left = (width - w) / 2;
    if (!wrap && row.eq >= 0) {
      const segs = textEl.querySelectorAll('[data-seg]');
      if (segs.length >= 2) {
        const textBox = textEl.getBoundingClientRect();
        const eqBox = segs[1].getBoundingClientRect();
        left = axis - (eqBox.left + eqBox.width / 2 - textBox.left);
      }
    }
    // Keep the whole line on the board, even if that pulls its equals sign off the shared axis.
    left = round2(clamp(left, 0, Math.max(0, width - w)));
    textEl.style.left = left + 'px';
    rows[row.key] = { f: f, left: left, wrap: wrap };
  }

  // 2. With every line in its final place, measure the marks.
  const rects: Record<number, Array<Rect | null>> = {};
  for (let i = 0; i < model.marks.length; i++) {
    const mark = model.marks[i];
    const rowEl = rowEls[mark.rowKey];
    const textEl = textEls[mark.rowKey];
    const row = lineRows[mark.rowKey];
    if (!rowEl || !textEl || !row) continue;
    const origin = rowEl.getBoundingClientRect();
    const spans = markSpans(row, mark.op);
    const boxes: Array<Rect | null> = [];
    for (let j = 0; j < spans.length; j++) {
      const span = spans[j];
      boxes.push(span ? spanRect(textEl, row, span, origin) : null);
    }
    rects[mark.opIndex] = boxes;
  }

  return { width: width, base: base, rows: rows, rects: rects };
}

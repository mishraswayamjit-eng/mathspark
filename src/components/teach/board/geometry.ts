/**
 * The shapes a teacher draws on the board, as SVG path data. All coordinates
 * are pixels inside one row. Every path is a single stroke (or a stroke with
 * short sub-strokes) so it can be drawn from its start to its end.
 */

import type { Rect } from './model';

function n(value: number): string {
  return String(Math.round(value * 10) / 10);
}

export function clamp(value: number, low: number, high: number): number {
  return Math.min(high, Math.max(low, value));
}

/**
 * Where the ink of a piece of text is, inside its measured box. A text box is
 * as tall as the font's ascent plus descent; capitals and digits fill roughly
 * the band from 20% to 80% of it.
 */
export function inkTop(r: Rect): number {
  return r.y + r.h * 0.2;
}

export function inkBase(r: Rect): number {
  return r.y + r.h * 0.8;
}

export function midX(r: Rect): number {
  return r.x + r.w / 2;
}

/** An arc over the line from x1 to x2, starting and ending at height y, with a small arrowhead at the end. */
export function arcPath(x1: number, x2: number, y: number, fontPx: number): string {
  const dx = x2 - x1;
  const rise = clamp(Math.abs(dx) * 0.32, fontPx * 0.28, fontPx * 0.62);
  const cx = (x1 + x2) / 2;
  const cy = y - 2 * rise;
  // Direction the pen is moving in as it lands.
  let tx = x2 - cx;
  let ty = y - cy;
  const len = Math.sqrt(tx * tx + ty * ty) || 1;
  tx /= len;
  ty /= len;
  const head = Math.max(6, fontPx * 0.26);
  const spread = 0.52;
  const cos = Math.cos(spread);
  const sin = Math.sin(spread);
  const bx = -tx;
  const by = -ty;
  const ax1 = x2 + head * (bx * cos - by * sin);
  const ay1 = y + head * (bx * sin + by * cos);
  const ax2 = x2 + head * (bx * cos + by * sin);
  const ay2 = y + head * (-bx * sin + by * cos);
  return (
    'M' + n(x1) + ' ' + n(y) +
    ' Q' + n(cx) + ' ' + n(cy) + ' ' + n(x2) + ' ' + n(y) +
    ' M' + n(x2) + ' ' + n(y) + ' L' + n(ax1) + ' ' + n(ay1) +
    ' M' + n(x2) + ' ' + n(y) + ' L' + n(ax2) + ' ' + n(ay2)
  );
}

/** A diagonal stroke through a place, from bottom left to top right. */
export function strikePath(r: Rect): string {
  return 'M' + n(r.x - 3) + ' ' + n(inkBase(r) + 2) + ' L' + n(r.x + r.w + 3) + ' ' + n(inkTop(r) - 2);
}

/** A straight-ish stroke from x0 to x1 at height y, with the slight sag of a line drawn by hand. */
export function linePath(x0: number, x1: number, y: number): string {
  return 'M' + n(x0) + ' ' + n(y) + ' Q' + n((x0 + x1) / 2) + ' ' + n(y + 1.8) + ' ' + n(x1) + ' ' + n(y - 0.6);
}

/** A box round a place, drawn in one go with corners that do not quite meet. */
export function boxPath(r: Rect, fontPx: number): string {
  const pad = fontPx * 0.16;
  const x0 = r.x - pad - 2;
  const x1 = r.x + r.w + pad + 2;
  const y0 = inkTop(r) - pad;
  const y1 = inkBase(r) + pad;
  return (
    'M' + n(x0) + ' ' + n(y0) +
    ' L' + n(x1 + 1) + ' ' + n(y0 - 1) +
    ' L' + n(x1) + ' ' + n(y1 + 1) +
    ' L' + n(x0 - 1) + ' ' + n(y1) +
    ' L' + n(x0) + ' ' + n(y0 - 2.5)
  );
}

/**
 * A ring round a place, the way a hand draws one: it starts at the upper left,
 * goes once round and a little further, and drifts inwards so the end overlaps
 * the start without meeting it.
 */
export function ringPath(r: Rect, fontPx: number): string {
  const cx = midX(r);
  const cy = (inkTop(r) + inkBase(r)) / 2;
  const rx = r.w / 2 + fontPx * 0.5;
  const ry = (inkBase(r) - inkTop(r)) / 2 + fontPx * 0.3;
  const steps = 64;
  let d = '';
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const angle = ((-200 + 400 * t) * Math.PI) / 180;
    const k = 1.05 - 0.09 * t + 0.02 * Math.sin(t * 9);
    const x = cx + rx * k * Math.cos(angle);
    const y = cy + ry * k * Math.sin(angle);
    d += (i === 0 ? 'M' : ' L') + n(x) + ' ' + n(y);
  }
  return d;
}

/** A short stroke straight down from (x, y0) to (x, y1). */
export function stemPath(x: number, y0: number, y1: number): string {
  return 'M' + n(x) + ' ' + n(y0) + ' L' + n(x) + ' ' + n(y1);
}

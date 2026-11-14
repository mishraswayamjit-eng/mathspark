'use client';

import type { ReactNode } from 'react';
import { C } from '@/components/visuals/parts';

/**
 * Shared pieces for the question-figure renderer: colours, the outer frame
 * (label for screen readers + the note line), SVG text with a halo, and the
 * small geometry helpers every kind uses.
 *
 * Bearings are in degrees clockwise from the top (north), as on a compass or
 * a clock face.
 */

export { C };

export interface Pt { x: number; y: number }
export type Anchor = 'start' | 'middle' | 'end';
export interface KindProps<T> { spec: T; className?: string }

/** Outline width, and the width of a highlighted part. */
export const INK_W = 2.5;
export const HI_W = 5;

/** Every SVG figure scales to its container, up to a sensible width. */
export const SVG_CLASS = 'block w-full max-w-[380px] mx-auto h-auto';

// ── Defensive readers ────────────────────────────────────────────────────────

/** True when `key` is listed in a figure's `highlight`. */
export function isOn(highlight: string[] | undefined, key: string): boolean {
  if (!Array.isArray(highlight)) return false;
  for (let i = 0; i < highlight.length; i++) {
    if (highlight[i] === key) return true;
  }
  return false;
}

/** A label as a trimmed string; '' when missing. */
export function text(v: unknown): string {
  if (typeof v === 'string') return v.trim();
  if (typeof v === 'number' && isFinite(v)) return String(v);
  return '';
}

export function num(v: unknown, fallback: number): number {
  return typeof v === 'number' && isFinite(v) ? v : fallback;
}

export function clamp(n: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, n));
}

export function list<T>(v: T[] | null | undefined): T[] {
  return Array.isArray(v) ? v : [];
}

/** A number without trailing noise: 2500, 0.025, 1.5. */
export function tidy(n: number): string {
  return String(Math.round(n * 1e6) / 1e6);
}

/** Rough width of bold text in SVG units. */
export function estWidth(s: string, size?: number): number {
  return s.length * (size === undefined ? 13 : size) * 0.58;
}

/** "a", "a and b", "a, b and c". */
export function sayList(items: string[]): string {
  if (items.length === 0) return '';
  if (items.length === 1) return items[0];
  return `${items.slice(0, items.length - 1).join(', ')} and ${items[items.length - 1]}`;
}

// ── Geometry ─────────────────────────────────────────────────────────────────

function fx(n: number): string {
  return n.toFixed(1);
}

export function pointsAttr(pts: Pt[]): string {
  const out: string[] = [];
  for (let i = 0; i < pts.length; i++) out.push(`${fx(pts[i].x)},${fx(pts[i].y)}`);
  return out.join(' ');
}

/** The point `r` away from (cx, cy) at a bearing. */
export function at(cx: number, cy: number, r: number, bearing: number): Pt {
  const a = (bearing * Math.PI) / 180;
  return { x: cx + r * Math.sin(a), y: cy - r * Math.cos(a) };
}

/** A filled wedge from bearing b1 clockwise round to b2 (b2 > b1). */
export function wedgePath(cx: number, cy: number, r: number, b1: number, b2: number): string {
  const span = b2 - b1;
  if (span >= 359.9) {
    return `M ${fx(cx - r)} ${fx(cy)} A ${r} ${r} 0 1 1 ${fx(cx + r)} ${fx(cy)} A ${r} ${r} 0 1 1 ${fx(cx - r)} ${fx(cy)} Z`;
  }
  const p = at(cx, cy, r, b1);
  const q = at(cx, cy, r, b2);
  return `M ${fx(cx)} ${fx(cy)} L ${fx(p.x)} ${fx(p.y)} A ${r} ${r} 0 ${span > 180 ? 1 : 0} 1 ${fx(q.x)} ${fx(q.y)} Z`;
}

/** An open arc of `degrees` (under 360) starting at bearing `from`. */
export function arcPath(cx: number, cy: number, r: number, from: number, degrees: number, clockwise: boolean): string {
  const p = at(cx, cy, r, from);
  const q = at(cx, cy, r, clockwise ? from + degrees : from - degrees);
  return `M ${fx(p.x)} ${fx(p.y)} A ${r} ${r} 0 ${degrees > 180 ? 1 : 0} ${clockwise ? 1 : 0} ${fx(q.x)} ${fx(q.y)}`;
}

/** A small solid arrowhead with its middle at `p`, pointing along a bearing. */
export function headPoints(p: Pt, bearing: number, size: number): string {
  const a = (bearing * Math.PI) / 180;
  const tx = Math.sin(a);
  const ty = -Math.cos(a);
  return pointsAttr([
    { x: p.x + tx * size, y: p.y + ty * size },
    { x: p.x - tx * size * 0.6 - ty * size * 0.8, y: p.y - ty * size * 0.6 + tx * size * 0.8 },
    { x: p.x - tx * size * 0.6 + ty * size * 0.8, y: p.y - ty * size * 0.6 - tx * size * 0.8 },
  ]);
}

/** Where to put a label beside the middle of an edge, given the edge's outward direction. */
export function besideEdge(p: Pt, q: Pt, nx: number, ny: number, off: number): { x: number; y: number; anchor: Anchor } {
  return {
    x: (p.x + q.x) / 2 + nx * off,
    y: (p.y + q.y) / 2 + ny * off + 4.5,
    anchor: nx > 0.35 ? 'start' : nx < -0.35 ? 'end' : 'middle',
  };
}

// ── Drawing ──────────────────────────────────────────────────────────────────

/** SVG text at the house weight. The white halo keeps it readable over lines. */
export function Label({ x, y, children, anchor, size, fill, halo }: {
  x: number;
  y: number;
  children: ReactNode;
  anchor?: Anchor;
  size?: number;
  fill?: string;
  /** Pass false for text that sits on a filled shape. */
  halo?: boolean;
}) {
  const plain = halo === false;
  return (
    <text
      x={x}
      y={y}
      textAnchor={anchor === undefined ? 'middle' : anchor}
      fontSize={size === undefined ? 13 : size}
      fontWeight={800}
      fill={fill === undefined ? C.ink : fill}
      stroke={plain ? 'none' : C.card}
      strokeWidth={plain ? 0 : 4}
      strokeLinejoin="round"
      paintOrder="stroke"
    >
      {children}
    </text>
  );
}

/**
 * The outer element of every figure: one image for screen readers, described
 * in words, with the optional note as a centred line in a soft block.
 */
export function Frame({ label, note, className, children }: {
  label: string;
  note?: string;
  className?: string;
  children: ReactNode;
}) {
  const noteText = text(note);
  return (
    <div role="img" aria-label={noteText ? `${label}. ${noteText}` : label} className={`w-full ${className === undefined ? '' : className}`}>
      {children}
      {noteText !== '' && (
        <p className="mt-2 bg-soft rounded-control px-3 py-2 text-[14px] leading-snug font-bold text-ink text-center" aria-hidden="true">
          {noteText}
        </p>
      )}
    </div>
  );
}

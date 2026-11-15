'use client';

import type { CSSProperties, ReactNode } from 'react';
import { C } from '@/components/visuals/parts';
import { arcPath, boxPath, inkBase, inkTop, linePath, midX, ringPath, stemPath, strikePath } from './geometry';
import type { BoardMark, Rect, Timing } from './model';

const PEN = C.action;
const GOLD = C.star;
const QUIET = C.muted;
const STROKE = 2.75;

/** The animation for one part of a mark: the mark's time is shared equally between its parts, in order. */
function anim(name: string, t: Timing | null, part: number, parts: number): CSSProperties | undefined {
  if (!t) return undefined;
  const each = t.dur / Math.max(1, parts);
  return {
    animation: name + ' ' + Math.round(each) + 'ms ease-out ' + Math.round(t.delay + each * part) + 'ms both',
  };
}

interface StrokeProps {
  d: string;
  color: string;
  t: Timing | null;
  part: number;
  parts: number;
}

/** One pen stroke, drawn from its start to its end when it is new. */
function Stroke({ d, color, t, part, parts }: StrokeProps) {
  const style = anim('wb-draw', t, part, parts);
  return (
    <path
      d={d}
      fill="none"
      stroke={color}
      strokeWidth={STROKE}
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      className={style ? 'wb-anim wb-dash' : undefined}
      style={style}
    />
  );
}

interface SmallProps {
  x: number;
  y: number;
  text: string;
  color: string;
  size: number;
  t: Timing | null;
  part: number;
  parts: number;
}

/** Small writing next to a place, centred on x with its baseline at y. A white edge keeps it readable over other marks. */
function Small({ x, y, text, color, size, t, part, parts }: SmallProps) {
  const style = anim('wb-fade', t, part, parts);
  return (
    <text
      x={x}
      y={y}
      textAnchor="middle"
      fontSize={size}
      fontWeight={600}
      fill={color}
      stroke="#ffffff"
      strokeWidth={3}
      strokeLinejoin="round"
      paintOrder="stroke"
      className={style ? 'wb-anim' : undefined}
      style={style}
    >
      {text}
    </text>
  );
}

function present(rects: Array<Rect | null>): Rect[] {
  const out: Rect[] = [];
  for (let i = 0; i < rects.length; i++) {
    const r = rects[i];
    if (r) out.push(r);
  }
  return out;
}

/**
 * Draws one mark from the measured boxes of its places. `f` is the font size
 * of the line it sits on and `m` the size of small writing. Returns null when
 * a place it needs was not found, so that mark is simply left out.
 */
function renderMark(mark: BoardMark, rects: Array<Rect | null>, f: number, m: number, t: Timing | null): ReactNode {
  const op = mark.op;
  switch (op.op) {
    case 'arc': {
      const from = rects[0];
      if (!from) return null;
      const tos = present(rects.slice(1));
      if (tos.length === 0) return null;
      return tos.map((to, i) => (
        <Stroke
          key={i}
          d={arcPath(midX(from), midX(to), Math.min(inkTop(from), inkTop(to)) - 3, f)}
          color={PEN}
          t={t}
          part={i}
          parts={tos.length}
        />
      ));
    }
    case 'strike': {
      const r = rects[0];
      if (!r) return null;
      const note = typeof op.note === 'string' && op.note !== '' ? op.note : null;
      const parts = note ? 2 : 1;
      return (
        <>
          <Stroke d={strikePath(r)} color={PEN} t={t} part={0} parts={parts} />
          {note && <Small x={midX(r)} y={inkTop(r) - f * 0.16} text={note} color={PEN} size={m} t={t} part={1} parts={parts} />}
        </>
      );
    }
    case 'note': {
      const r = rects[0];
      if (!r || typeof op.text !== 'string') return null;
      const y = op.place === 'below' ? inkBase(r) + f * 0.2 + m * 0.8 : inkTop(r) - f * 0.16;
      return <Small x={midX(r)} y={y} text={op.text} color={QUIET} size={m} t={t} part={0} parts={1} />;
    }
    case 'mark': {
      const r = rects[0];
      if (!r) return null;
      let d = linePath(r.x - 2, r.x + r.w + 2, inkBase(r) + f * 0.14 + 1);
      if (op.shape === 'circle') d = ringPath(r, f);
      else if (op.shape === 'box') d = boxPath(r, f);
      return <Stroke d={d} color={GOLD} t={t} part={0} parts={1} />;
    }
    case 'both': {
      const sides = present(rects);
      if (sides.length === 0 || typeof op.text !== 'string') return null;
      return sides.map((r, i) => (
        <Small
          key={i}
          x={midX(r)}
          y={inkBase(r) + f * 0.22 + m * 0.8}
          text={op.text}
          color={PEN}
          size={m}
          t={t}
          part={i}
          parts={sides.length}
        />
      ));
    }
    case 'divide': {
      const sides = present(rects);
      if (sides.length === 0) return null;
      const by = String(op.by);
      const parts = sides.length * 2;
      return sides.map((r, i) => {
        const barY = inkBase(r) + f * 0.2;
        return (
          <g key={i}>
            <Stroke d={linePath(r.x - 4, r.x + r.w + 4, barY)} color={PEN} t={t} part={i * 2} parts={parts} />
            <Small x={midX(r)} y={barY + m * 0.95 + 2} text={by} color={PEN} size={m} t={t} part={i * 2 + 1} parts={parts} />
          </g>
        );
      });
    }
    case 'group': {
      const places = present(rects).sort((a, b) => a.x - b.x);
      if (places.length === 0) return null;
      let y0 = 0;
      for (let i = 0; i < places.length; i++) y0 = Math.max(y0, inkBase(places[i]) + f * 0.16);
      const many = places.length > 1;
      const rail = y0 + 7;
      let d = '';
      for (let i = 0; i < places.length; i++) {
        const r = places[i];
        d += (d ? ' ' : '') + linePath(r.x, r.x + r.w, y0);
        if (many) d += ' ' + stemPath(midX(r), y0, rail);
      }
      const first = midX(places[0]);
      const last = midX(places[places.length - 1]);
      if (many) d += ' M' + first + ' ' + rail + ' L' + last + ' ' + rail;
      const label = typeof op.label === 'string' && op.label !== '' ? op.label : null;
      const parts = label ? 2 : 1;
      return (
        <>
          <Stroke d={d} color={PEN} t={t} part={0} parts={parts} />
          {label && (
            <Small
              x={(first + last) / 2}
              y={(many ? rail : y0) + m * 0.9 + 3}
              text={label}
              color={PEN}
              size={m}
              t={t}
              part={1}
              parts={parts}
            />
          )}
        </>
      );
    }
    default:
      return null;
  }
}

export interface RowMarksProps {
  /** The marks on this one line, in the order they were made. */
  marks: BoardMark[];
  /** Measured boxes for every mark on the board, by op index; null before the first measurement. */
  rects: Record<number, Array<Rect | null>> | null;
  /** Font size of the line, in pixels. */
  f: number;
  /** The board's base font size, in pixels. */
  base: number;
  timing: (opIndex: number) => Timing | null;
}

/** Everything drawn on one line: an overlay the size of the row, in the row's own pixel coordinates. */
export default function RowMarks({ marks, rects, f, base, timing }: RowMarksProps) {
  if (!rects || marks.length === 0) return null;
  const m = Math.max(13, Math.round(base * 0.6));
  const items: ReactNode[] = [];
  for (let i = 0; i < marks.length; i++) {
    const mark = marks[i];
    const boxes: Array<Rect | null> | undefined = rects[mark.opIndex];
    if (!boxes) continue;
    const node = renderMark(mark, boxes, f, m, timing(mark.opIndex));
    if (node) items.push(<g key={mark.opIndex}>{node}</g>);
  }
  if (items.length === 0) return null;
  return (
    <svg
      className="absolute left-0 top-0 w-full h-full overflow-visible pointer-events-none font-display"
      aria-hidden="true"
      focusable="false"
    >
      {items}
    </svg>
  );
}

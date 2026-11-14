'use client';

import type { ReactNode } from 'react';
import type { AnglesFigure, ClockFigure, CompassFigure } from '@/lib/figures/types';
import type { Pt, KindProps } from './shared';
import { C, Frame, Label, SVG_CLASS, INK_W, isOn, text, num, clamp, list, pointsAttr, at, wedgePath, arcPath, headPoints, estWidth, sayList, tidy } from './shared';

// ══ Angles at a point ════════════════════════════════════════════════════════

interface Wedge { b1: number; b2: number; label: string; index: number }

function drawnSize(part: { label: string; size?: number } | undefined): number {
  return part && typeof part.size === 'number' && isFinite(part.size) && part.size > 0 ? part.size : 0;
}

/** Degrees to draw each part: stated sizes are kept, the rest share what is left of `total`. */
function shareOut(parts: Array<{ label: string; size?: number }>, total: number): number[] {
  const n = parts.length;
  let known = 0;
  let unknown = 0;
  const sizes: number[] = [];
  for (let i = 0; i < n; i++) {
    const s = drawnSize(parts[i]);
    sizes.push(s);
    if (s > 0) known += s;
    else unknown++;
  }
  const left = total - known;
  if (unknown > 0 && left >= unknown * 8) {
    return sizes.map((s) => (s > 0 ? s : left / unknown));
  }
  if (unknown === 0 && Math.abs(left) < 0.5) return sizes;
  // The stated sizes do not fit: keep their proportions and fill the whole turn.
  const stand = known > 0 ? known / (n - unknown) : 1;
  let sum = 0;
  const rough = sizes.map((s) => {
    const v = s > 0 ? s : stand;
    sum += v;
    return v;
  });
  return rough.map((v) => (v * total) / (sum || 1));
}

const ANGLE_WORDS: Record<string, string> = {
  single: 'An angle',
  onLine: 'Angles on a straight line, from left to right',
  inRightAngle: 'Angles that together make a right angle',
  aroundPoint: 'Angles around a point, clockwise from the top',
  crossing: 'Two straight lines crossing. The angles, clockwise from the top',
};

export function AnglesKind({ spec, className }: KindProps<AnglesFigure>) {
  const parts = list(spec.parts);
  const n = parts.length;
  if (n === 0) return null;
  const hl = spec.highlight;
  const layout = Object.prototype.hasOwnProperty.call(ANGLE_WORDS, spec.layout) ? spec.layout : 'single';
  const L = 118;
  const wedges: Wedge[] = [];
  const rays: number[] = [];

  if (layout === 'crossing') {
    let top = drawnSize(parts[0]) || drawnSize(parts[2]);
    if (!top) {
      const side = drawnSize(parts[1]) || drawnSize(parts[3]);
      top = side ? 180 - side : 64;
    }
    const h = clamp(top, 20, 160) / 2;
    const bounds = [[-h, h], [h, 180 - h], [180 - h, 180 + h], [180 + h, 360 - h]];
    for (let i = 0; i < Math.min(n, 4); i++) {
      wedges.push({ b1: bounds[i][0], b2: bounds[i][1], label: text(parts[i] && parts[i].label), index: i });
    }
    rays.push(h, 180 - h, 180 + h, 360 - h);
  } else if (layout === 'single') {
    const size = clamp(drawnSize(parts[0]) || 50, 5, 355);
    wedges.push({ b1: 90 - size, b2: 90, label: text(parts[0] && parts[0].label), index: 0 });
    rays.push(90 - size, 90);
  } else {
    const total = layout === 'onLine' ? 180 : layout === 'inRightAngle' ? 90 : 360;
    const sizes = shareOut(parts, total);
    let cur = layout === 'onLine' ? 270 : 0;
    rays.push(cur);
    for (let i = 0; i < n; i++) {
      wedges.push({ b1: cur, b2: cur + sizes[i], label: text(parts[i] && parts[i].label), index: i });
      cur += sizes[i];
      if (!(layout === 'aroundPoint' && i === n - 1)) rays.push(cur);
    }
  }

  // Work around the vertex at (0, 0), then frame what was drawn.
  let minX = 0;
  let maxX = 0;
  let minY = 0;
  let maxY = 0;
  function reach(p: Pt, rx: number, ry: number) {
    minX = Math.min(minX, p.x - rx);
    maxX = Math.max(maxX, p.x + rx);
    minY = Math.min(minY, p.y - ry);
    maxY = Math.max(maxY, p.y + ry);
  }

  const lines: ReactNode[] = [];
  for (let i = 0; i < rays.length; i++) {
    const end = at(0, 0, L, rays[i]);
    reach(end, 2, 2);
    lines.push(<line key={i} x1={0} y1={0} x2={end.x.toFixed(1)} y2={end.y.toFixed(1)} stroke={C.ink} strokeWidth={INK_W} strokeLinecap="round" />);
  }

  const fills: ReactNode[] = [];
  const labels: ReactNode[] = [];
  const said: string[] = [];
  for (let i = 0; i < wedges.length; i++) {
    const w = wedges[i];
    const on = isOn(hl, `p${w.index}`);
    const span = w.b2 - w.b1;
    fills.push(
      <path key={i} d={wedgePath(0, 0, on ? 34 : 28, w.b1, w.b2)} fill={on ? C.action : C.star} fillOpacity={on || i % 2 === 0 ? 1 : 0.55}
        stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />,
    );
    if (w.label !== '') {
      const halfSin = span < 180 ? Math.sin((span * Math.PI) / 360) : 1;
      const d = clamp(16 / (halfSin || 1) + estWidth(w.label) / 4, 50, 94);
      const p = at(0, 0, d, (w.b1 + w.b2) / 2);
      reach(p, estWidth(w.label) / 2 + 2, 9);
      labels.push(<Label key={i} x={p.x} y={p.y + 4.5} fill={on ? C.action : C.ink}>{w.label}</Label>);
      said.push(w.label);
    }
  }

  const aria = said.length ? `${ANGLE_WORDS[layout]}: ${sayList(said)}` : ANGLE_WORDS[layout];
  const vbX = (minX + maxX) / 2 - 160;
  const vbY = minY - 14;
  const vbH = maxY - minY + 28;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`${vbX.toFixed(1)} ${vbY.toFixed(1)} 320 ${vbH.toFixed(1)}`} className={SVG_CLASS} aria-hidden="true">
        {fills}
        {layout === 'inRightAngle' && <path d="M 0 -11 L 11 -11 L 11 0" fill="none" stroke={C.ink} strokeWidth={1.5} />}
        {lines}
        <circle cx={0} cy={0} r={4} fill={C.ink} />
        {labels}
      </svg>
    </Frame>
  );
}

// ══ Clock ════════════════════════════════════════════════════════════════════

export function ClockKind({ spec, className }: KindProps<ClockFigure>) {
  const hl = spec.highlight;
  const hour = ((Math.round(num(spec.hour, 12)) % 12) + 12) % 12;
  const minute = clamp(Math.round(num(spec.minute, 0)), 0, 59);
  const cx = 160;
  const cy = 118;
  const R = 100;
  const hourAt = hour * 30 + minute * 0.5;
  const minuteAt = minute * 6;
  const hourOn = isOn(hl, 'hour');
  const minuteOn = isOn(hl, 'minute');
  const angleOn = isOn(hl, 'angle');

  const face: ReactNode[] = [];
  for (let i = 0; i < 60; i++) {
    const big = i % 5 === 0;
    const a = at(cx, cy, big ? R - 10 : R - 5, i * 6);
    const b = at(cx, cy, R - 1, i * 6);
    face.push(<line key={`t${i}`} x1={a.x.toFixed(1)} y1={a.y.toFixed(1)} x2={b.x.toFixed(1)} y2={b.y.toFixed(1)} stroke={big ? C.ink : C.muted} strokeWidth={big ? 2 : 1} />);
  }
  for (let i = 1; i <= 12; i++) {
    const p = at(cx, cy, R - 24, i * 30);
    face.push(<Label key={`n${i}`} x={p.x} y={p.y + 4.5} halo={false}>{i}</Label>);
  }

  // The smaller angle between the hands.
  const gap = (minuteAt - hourAt + 360) % 360;
  const from = gap <= 180 ? hourAt : minuteAt;
  const span = gap <= 180 ? gap : 360 - gap;
  const hourEnd = at(cx, cy, 50, hourAt);
  const minuteEnd = at(cx, cy, 74, minuteAt);

  let aria = `A clock showing ${hour === 0 ? 12 : hour}:${minute < 10 ? '0' : ''}${minute}`;
  if (spec.showAngle === true) aria += ', with the angle between the hands shaded';

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox="0 0 320 236" className={SVG_CLASS} aria-hidden="true">
        <circle cx={cx} cy={cy} r={R} fill={C.card} stroke={C.ink} strokeWidth={INK_W} />
        {spec.showAngle === true && span > 0.5 && (
          <path d={wedgePath(cx, cy, angleOn ? 40 : 34, from, from + span)} fill={angleOn ? C.action : C.star} fillOpacity={angleOn ? 0.85 : 1}
            stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />
        )}
        {face}
        <line x1={cx} y1={cy} x2={minuteEnd.x.toFixed(1)} y2={minuteEnd.y.toFixed(1)} stroke={minuteOn ? C.action : C.ink} strokeWidth={minuteOn ? 5 : 3.5} strokeLinecap="round" />
        <line x1={cx} y1={cy} x2={hourEnd.x.toFixed(1)} y2={hourEnd.y.toFixed(1)} stroke={hourOn ? C.action : C.ink} strokeWidth={hourOn ? 7 : 5.5} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={5.5} fill={C.ink} />
      </svg>
    </Frame>
  );
}

// ══ Compass ══════════════════════════════════════════════════════════════════

const COMPASS_POINTS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
const COMPASS_WORDS = ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'];

/** A straight arrow from the centre, as one outlined shape. */
function arrowShape(cx: number, cy: number, bearing: number, length: number, half: number): string {
  const a = (bearing * Math.PI) / 180;
  const ux = Math.sin(a);
  const uy = -Math.cos(a);
  const sx = Math.cos(a);
  const sy = Math.sin(a);
  const neck = length - 17;
  const wide = half + 6.5;
  const local = [[0, half], [neck, half], [neck, wide], [length, 0], [neck, -wide], [neck, -half], [0, -half]];
  const pts: Pt[] = [];
  for (let i = 0; i < local.length; i++) {
    pts.push({ x: cx + ux * local[i][0] + sx * local[i][1], y: cy + uy * local[i][0] + sy * local[i][1] });
  }
  return pointsAttr(pts);
}

export function CompassKind({ spec, className }: KindProps<CompassFigure>) {
  const hl = spec.highlight;
  const cx = 160;
  const cy = 131;
  const idx = COMPASS_POINTS.indexOf(spec.facing);
  const start = idx >= 0 ? idx * 45 : 0;
  const turns = list(spec.turns);

  const rose: Pt[] = [];
  for (let i = 0; i < 16; i++) {
    rose.push(at(cx, cy, i % 4 === 0 ? 96 : i % 2 === 0 ? 62 : 20, i * 22.5));
  }

  const said: string[] = [];
  const arcs: ReactNode[] = [];
  let cur = start;
  let drawn = 0;
  for (let i = 0; i < turns.length; i++) {
    const t = turns[i];
    const degrees = Math.abs(num(t ? t.degrees : 0, 0));
    if (!t || degrees <= 0) continue;
    const clockwise = t.direction !== 'anticlockwise';
    const on = isOn(hl, `t${i}`);
    const r = Math.min(80, 36 + drawn * 11);
    const end = clockwise ? cur + degrees : cur - degrees;
    const colour = on ? C.action : C.ink;
    const tip = at(cx, cy, r, end);
    arcs.push(
      <g key={i}>
        {degrees >= 360 ? (
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={colour} strokeWidth={on ? 4.5 : INK_W} />
        ) : (
          <path d={arcPath(cx, cy, r, cur, degrees, clockwise)} fill="none" stroke={colour} strokeWidth={on ? 4.5 : INK_W} strokeLinecap="round" />
        )}
        <polygon points={headPoints(tip, clockwise ? end + 90 : end - 90, on ? 8.5 : 7)} fill={colour} stroke={colour} strokeWidth={1} strokeLinejoin="round" />
      </g>,
    );
    said.push(`a turn of ${tidy(degrees)} degrees ${clockwise ? 'clockwise' : 'anticlockwise'}`);
    cur = end;
    drawn++;
  }

  const startOn = isOn(hl, 'start');
  const endOn = isOn(hl, 'end');
  let aria = `A compass with north at the top. An arrow faces ${idx >= 0 ? COMPASS_WORDS[idx] : 'north'}`;
  if (said.length) aria += `. Then ${said.join(', then ')}`;
  if (spec.showEnd === true) aria += '. A gold arrow shows the direction faced at the end';

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox="0 0 320 262" className={SVG_CLASS} aria-hidden="true">
        <polygon points={pointsAttr(rose)} fill={C.soft} stroke={C.line} strokeWidth={2} strokeLinejoin="round" />
        {COMPASS_POINTS.map((name, i) => {
          const main = i % 2 === 0;
          const p = at(cx, cy, main ? 112 : 80, i * 45);
          return (
            <Label key={name} x={p.x} y={p.y + (main ? 5 : 4)} size={main ? 14 : 11} fill={main ? C.ink : C.muted} halo={false}>{name}</Label>
          );
        })}
        <polygon points={arrowShape(cx, cy, start, 90, startOn ? 4 : 2.5)} fill={startOn ? C.action : C.ink}
          stroke={startOn ? C.action : C.ink} strokeWidth={1.5} strokeLinejoin="round" />
        {arcs}
        {spec.showEnd === true && (
          <polygon points={arrowShape(cx, cy, cur, 90, endOn ? 4.5 : 3.5)} fill={endOn ? C.action : C.star}
            stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />
        )}
        <circle cx={cx} cy={cy} r={5} fill={C.ink} />
      </svg>
    </Frame>
  );
}

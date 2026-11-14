'use client';

import React, { useRef, useState } from 'react';
import type { VisualSpec } from '@/lib/visuals/spec';
import { C, range, fmt, Stat, Working, Slider, Toggle } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

interface Pt { x: number; y: number }

const POLYGON_NAMES: Record<number, string> = {
  3: 'triangle', 4: 'square', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon',
  9: 'nonagon', 10: 'decagon', 11: 'hendecagon', 12: 'dodecagon',
};

function pointsAttr(pts: Pt[]): string {
  return pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
}

/** A filled wedge marking the angle at `v` between the directions to `p` and `q`. */
function anglePath(v: Pt, p: Pt, q: Pt, r: number): string {
  const l1 = Math.hypot(p.x - v.x, p.y - v.y) || 1;
  const l2 = Math.hypot(q.x - v.x, q.y - v.y) || 1;
  const d1 = { x: (p.x - v.x) / l1, y: (p.y - v.y) / l1 };
  const d2 = { x: (q.x - v.x) / l2, y: (q.y - v.y) / l2 };
  const sweep = d1.x * d2.y - d1.y * d2.x > 0 ? 1 : 0;
  return `M ${v.x} ${v.y} L ${v.x + r * d1.x} ${v.y + r * d1.y} A ${r} ${r} 0 0 ${sweep} ${v.x + r * d2.x} ${v.y + r * d2.y} Z`;
}

/** The angle at `v` in whole degrees. */
function angleAt(v: Pt, p: Pt, q: Pt): number {
  const ax = p.x - v.x;
  const ay = p.y - v.y;
  const bx = q.x - v.x;
  const by = q.y - v.y;
  const cos = (ax * bx + ay * by) / ((Math.hypot(ax, ay) || 1) * (Math.hypot(bx, by) || 1));
  return (Math.acos(Math.min(1, Math.max(-1, cos))) * 180) / Math.PI;
}

function round1(n: number): string {
  return String(Math.round(n * 10) / 10);
}

// ══ Regular polygon and its angles ═══════════════════════════════════════════

export function PolygonVisual({ spec }: { spec: Of<'polygon'> }) {
  const [n, setN] = useState(spec.sides);
  const cx = 150;
  const cy = 128;
  const R = 100;
  const pts: Pt[] = range(n).map((i) => {
    const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
    return { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) };
  });
  const each = ((n - 2) * 180) / n;
  const wedge = n <= 6 ? 26 : 18;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 256" className="w-full max-w-[340px] mx-auto h-auto" role="img"
        aria-label={`Regular ${POLYGON_NAMES[n]} with ${n} sides`}>
        <polygon points={pointsAttr(pts)} fill={C.card} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        {pts.map((v, i) => {
          const prev = pts[(i + n - 1) % n];
          const next = pts[(i + 1) % n];
          // Label sits a little inside the corner, towards the centre.
          const k = n <= 6 ? 0.56 : 0.66;
          return (
            <g key={i}>
              <path d={anglePath(v, prev, next, wedge)} fill={C.star} stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />
              {n <= 8 && (
                <text x={cx + (v.x - cx) * k} y={cy + (v.y - cy) * k + 4} textAnchor="middle" fontSize={n <= 6 ? 13 : 11} fontWeight={800} fill={C.ink}>
                  {round1(each)}°
                </text>
              )}
            </g>
          );
        })}
      </svg>
      <Slider label="Number of sides" value={n} min={3} max={12} onChange={setN} display={`${n} (${POLYGON_NAMES[n]})`} />
      <div className="flex flex-wrap gap-2">
        <Stat label="Each angle" value={`${round1(each)}°`} />
        <Stat label="All angles together" value={`${fmt((n - 2) * 180)}°`} />
      </div>
      <Working>
        ({n} − 2) × 180° = {fmt((n - 2) * 180)}°, shared between {n} equal angles: {fmt((n - 2) * 180)}° ÷ {n} = {round1(each)}°
      </Working>
    </div>
  );
}

// ══ Shapes around a point ════════════════════════════════════════════════════

/** A regular n-gon with one corner at `a`, its first edge leaving at `startDeg`. */
function polygonAt(a: Pt, n: number, side: number, startDeg: number): Pt[] {
  const pts: Pt[] = [a];
  let heading = (startDeg * Math.PI) / 180;
  const turn = (2 * Math.PI) / n;
  for (let i = 1; i < n; i++) {
    const last = pts[i - 1];
    pts.push({ x: last.x + side * Math.cos(heading), y: last.y + side * Math.sin(heading) });
    heading += turn;
  }
  return pts;
}

const TILE_OPTIONS = [
  { value: '3', label: 'Triangles' },
  { value: '4', label: 'Squares' },
  { value: '5', label: 'Pentagons' },
  { value: '6', label: 'Hexagons' },
];

export function TilingVisual({ spec }: { spec: Of<'tiling'> }) {
  const [n, setN] = useState(spec.sides);
  const each = ((n - 2) * 180) / n;
  const most = Math.floor(360 / each + 0.0001);
  const [count, setCount] = useState(Math.min(spec.count, most));
  const a: Pt = { x: 150, y: 132 };
  const side = n === 3 ? 84 : n === 4 ? 72 : n === 5 ? 58 : 52;
  const total = count * each;
  const gap = 360 - total;
  const name = POLYGON_NAMES[n];

  const btn = 'flex-1 min-h-[48px] rounded-control border-2 border-ink bg-white text-ink font-extrabold text-[14px] px-2 shadow-hard-sm disabled:opacity-40 disabled:shadow-none active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]';

  let message = `${count} × ${round1(each)}° = ${round1(total)}°`;
  if (count === 0) message = `Add a ${name}. Each of its angles is ${round1(each)}°`;
  else if (Math.abs(gap) < 0.01) message += '. They close up exactly: a full turn of 360° with no gap';
  else if (count === most) message += `. There is a gap of ${round1(gap)}°, too small for another ${name}`;
  else message += `. ${round1(gap)}° still to fill`;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 264" className="w-full max-w-[340px] mx-auto h-auto" role="img"
        aria-label={`${count} ${name}s meeting at a point`}>
        {range(count).map((j) => (
          <polygon
            key={`${n}-${j}`}
            points={pointsAttr(polygonAt(a, n, side, j * each - 90))}
            fill={C.star}
            fillOpacity={j % 2 === 0 ? 1 : 0.6}
            stroke={C.ink}
            strokeWidth={2.5}
            strokeLinejoin="round"
            className="animate-card-pop"
          />
        ))}
        <circle cx={a.x} cy={a.y} r={5} fill={C.ink} />
        <text x={a.x + 9} y={a.y - 8} fontSize={14} fontWeight={800} fill={C.ink}>A</text>
      </svg>

      <Toggle
        options={TILE_OPTIONS}
        value={String(n)}
        onChange={(v) => { setN(Number(v)); setCount(1); }}
      />
      <div className="flex gap-2">
        <button type="button" className={btn} disabled={count >= most} onClick={() => setCount(count + 1)}>
          Add a {name}
        </button>
        <button type="button" className={btn} disabled={count <= 0} onClick={() => setCount(count - 1)}>
          Take one away
        </button>
      </div>
      <Working>{message}</Working>
    </div>
  );
}

// ══ Triangle ═════════════════════════════════════════════════════════════════

function startTriangle(angleA: number, angleB: number): Pt[] {
  const a: Pt = { x: 50, y: 210 };
  const b: Pt = { x: 250, y: 210 };
  const A = (angleA * Math.PI) / 180;
  const B = (angleB * Math.PI) / 180;
  const Cang = Math.PI - A - B;
  let ac = (200 * Math.sin(B)) / Math.sin(Cang);
  let c: Pt = { x: a.x + ac * Math.cos(A), y: a.y - ac * Math.sin(A) };
  // Keep the top corner on the board.
  if (c.y < 24) {
    const k = (a.y - 24) / (a.y - c.y);
    ac *= k;
    c = { x: a.x + ac * Math.cos(A), y: a.y - ac * Math.sin(A) };
    b.x = a.x + 200 * k;
  }
  return [a, b, c];
}

function triangleName(angles: number[]): string {
  const sorted = angles.slice().sort((x, y) => x - y);
  const byAngle = sorted[2] === 90 ? 'right-angled' : sorted[2] > 90 ? 'obtuse-angled' : 'acute-angled';
  const bySide = sorted[0] === sorted[2] ? 'equilateral' : sorted[0] === sorted[1] || sorted[1] === sorted[2] ? 'isosceles' : 'scalene';
  return bySide === 'equilateral' ? 'an equilateral triangle' : `${byAngle === 'acute-angled' ? 'an' : 'a'} ${byAngle}, ${bySide} triangle`.replace('a obtuse', 'an obtuse');
}

export function TriangleVisual({ spec }: { spec: Of<'triangle'> }) {
  const [pts, setPts] = useState<Pt[]>(() => startTriangle(spec.angleA, spec.angleB));
  const svgRef = useRef<SVGSVGElement | null>(null);
  const grabbed = useRef<number>(-1);
  const labels = ['A', 'B', 'C'];

  function toView(clientX: number, clientY: number): Pt | null {
    const svg = svgRef.current;
    if (!svg) return null;
    const rect = svg.getBoundingClientRect();
    if (rect.width === 0) return null;
    return {
      x: Math.min(288, Math.max(12, ((clientX - rect.left) / rect.width) * 300)),
      y: Math.min(228, Math.max(16, ((clientY - rect.top) / rect.height) * 240)),
    };
  }

  function down(e: React.PointerEvent<SVGSVGElement>) {
    const p = toView(e.clientX, e.clientY);
    if (!p) return;
    let best = -1;
    let bestD = 46;
    for (let i = 0; i < 3; i++) {
      const d = Math.hypot(pts[i].x - p.x, pts[i].y - p.y);
      if (d < bestD) { best = i; bestD = d; }
    }
    grabbed.current = best;
    if (best !== -1) e.currentTarget.setPointerCapture(e.pointerId);
  }

  function move(e: React.PointerEvent<SVGSVGElement>) {
    const i = grabbed.current;
    if (i === -1) return;
    const p = toView(e.clientX, e.clientY);
    if (!p) return;
    const next = pts.map((q, k) => (k === i ? p : q));
    // Refuse a flattened triangle (twice the area under 1500 square units).
    const area2 = Math.abs((next[1].x - next[0].x) * (next[2].y - next[0].y) - (next[2].x - next[0].x) * (next[1].y - next[0].y));
    if (area2 > 1500) setPts(next);
  }

  // Whole-degree angles that always add to exactly 180.
  const a = Math.round(angleAt(pts[0], pts[1], pts[2]));
  const b = Math.round(angleAt(pts[1], pts[0], pts[2]));
  const angles = [a, b, 180 - a - b];
  const mid = { x: (pts[0].x + pts[1].x + pts[2].x) / 3, y: (pts[0].y + pts[1].y + pts[2].y) / 3 };

  return (
    <div className="space-y-3">
      <svg
        ref={svgRef}
        viewBox="0 0 300 240"
        className="w-full max-w-[360px] mx-auto h-auto select-none"
        style={{ touchAction: 'none', cursor: 'grab' }}
        role="img"
        aria-label={`Triangle with angles ${angles[0]}, ${angles[1]} and ${angles[2]} degrees`}
        onPointerDown={down}
        onPointerMove={move}
        onPointerUp={() => { grabbed.current = -1; }}
        onPointerCancel={() => { grabbed.current = -1; }}
      >
        <polygon points={pointsAttr(pts)} fill={C.card} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        {pts.map((v, i) => {
          const p = pts[(i + 1) % 3];
          const q = pts[(i + 2) % 3];
          const tones = [C.star, C.action, C.success];
          return (
            <g key={i}>
              <path d={anglePath(v, p, q, 26)} fill={tones[i]} fillOpacity={0.85} stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />
              <text x={v.x + (mid.x - v.x) * 0.36} y={v.y + (mid.y - v.y) * 0.36 + 4} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.ink}>
                {angles[i]}°
              </text>
              <circle cx={v.x} cy={v.y} r={9} fill={C.card} stroke={C.ink} strokeWidth={2.5} />
              <text x={v.x + (v.x - mid.x) * 0.16} y={v.y + (v.y - mid.y) * 0.16 + (v.y < mid.y ? -12 : 22)} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.muted}>
                {labels[i]}
              </text>
            </g>
          );
        })}
      </svg>
      <Working>
        {angles[0]}° + {angles[1]}° + {angles[2]}° = 180°. This is {triangleName(angles)}
      </Working>
      <p className="text-caption text-ink-muted text-center">Drag any corner. The three angles always make 180°</p>
    </div>
  );
}

// ══ Circle ═══════════════════════════════════════════════════════════════════

export function CircleVisual({ spec }: { spec: Of<'circle'> }) {
  const [r, setR] = useState(spec.radius);
  const [mode, setMode] = useState<'circumference' | 'area'>('circumference');
  const unit = spec.unit ?? 'units';
  const px = 24 + r * 4;
  const cx = 150;
  const cy = 118;
  const circumference = Math.round(2 * 3.14 * r * 100) / 100;
  const area = Math.round(3.14 * r * r * 100) / 100;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 236" className="w-full max-w-[340px] mx-auto h-auto" role="img" aria-label={`Circle of radius ${r}`}>
        <circle cx={cx} cy={cy} r={px} fill={mode === 'area' ? C.star : C.card} fillOpacity={mode === 'area' ? 0.55 : 1}
          stroke={mode === 'circumference' ? C.action : C.ink} strokeWidth={mode === 'circumference' ? 5 : 2.5}
          style={{ transition: 'r 0.2s' }} />
        <line x1={cx - px} y1={cy} x2={cx} y2={cy} stroke={C.muted} strokeWidth={2} strokeDasharray="5 5" />
        <line x1={cx} y1={cy} x2={cx + px} y2={cy} stroke={C.ink} strokeWidth={3} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={4.5} fill={C.ink} />
        <text x={cx + px / 2} y={cy - 8} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.ink}>r = {r}</text>
        <text x={cx} y={cy + px + 20} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.muted}>diameter = {2 * r} {unit}</text>
      </svg>
      <Toggle
        options={[{ value: 'circumference', label: 'Circumference' }, { value: 'area', label: 'Area' }]}
        value={mode}
        onChange={setMode}
      />
      <Slider label="Radius" value={r} min={1} max={20} onChange={setR} display={`${r} ${unit}`} />
      <Working>
        {mode === 'circumference'
          ? `Circumference = 2 × π × r ≈ 2 × 3.14 × ${r} = ${fmt(circumference)} ${unit}`
          : `Area = π × r × r ≈ 3.14 × ${r} × ${r} = ${fmt(area)} square ${unit}`}
      </Working>
    </div>
  );
}

// ══ Bar chart ════════════════════════════════════════════════════════════════

export function BarChartVisual({ spec }: { spec: Of<'barChart'> }) {
  const [picked, setPicked] = useState<number | null>(null);
  const [mean, setMean] = useState(spec.showMean === true);
  const unit = spec.unit ? ` ${spec.unit}` : '';
  let sum = 0;
  let top = 0;
  for (let i = 0; i < spec.bars.length; i++) {
    sum += spec.bars[i].value;
    if (spec.bars[i].value > top) top = spec.bars[i].value;
  }
  const scale = top > 0 ? top : 1;
  const average = Math.round((sum / spec.bars.length) * 100) / 100;

  let line = 'Tap a bar to read its value';
  if (mean) line = `Average = ${fmt(sum)} ÷ ${spec.bars.length} = ${fmt(average)}${unit}`;
  else if (picked !== null) line = `${spec.bars[picked].label}: ${fmt(spec.bars[picked].value)}${unit}`;

  return (
    <div className="space-y-3">
      <div className="relative h-48 border-b-2 border-l-2 border-ink flex items-end gap-2 px-2">
        {mean && (
          <div
            className="absolute left-0 right-0 border-t-2 border-dashed border-action z-10 pointer-events-none"
            style={{ bottom: `${(average / scale) * 92}%` }}
            aria-hidden="true"
          />
        )}
        {spec.bars.map((bar, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setPicked(picked === i ? null : i)}
            aria-pressed={picked === i}
            aria-label={`${bar.label}: ${bar.value}${unit}`}
            className={`flex-1 min-w-0 min-h-0 rounded-t-note border-2 border-b-0 border-ink transition-[height,opacity] duration-300 flex items-start justify-center pt-1 text-[13px] font-extrabold text-ink ${
              picked !== null && picked !== i ? 'opacity-50' : ''
            }`}
            style={{ height: `${Math.max(4, (bar.value / scale) * 92)}%`, backgroundColor: C.star }}
          >
            {fmt(bar.value)}
          </button>
        ))}
      </div>
      <div className="flex gap-2 px-2 pl-[10px]">
        {spec.bars.map((bar, i) => (
          <span key={i} className="flex-1 min-w-0 text-center text-caption text-ink-muted truncate">{bar.label}</span>
        ))}
      </div>
      <Toggle
        options={[{ value: 'bars', label: 'Values' }, { value: 'mean', label: 'Average' }]}
        value={mean ? 'mean' : 'bars'}
        onChange={(v) => setMean(v === 'mean')}
      />
      <Working>{line}</Working>
    </div>
  );
}

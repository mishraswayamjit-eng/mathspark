'use client';

import React, { useRef, useState } from 'react';
import type { VisualSpec, SymmetryShape, QuadKind } from '@/lib/visuals/spec';
import { C, range, fmt, Stat, Working, Slider, Toggle, Picker } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

interface Pt { x: number; y: number }

function pointsAttr(pts: Pt[]): string {
  return pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
}

function regular(n: number, cx: number, cy: number, r: number): Pt[] {
  return range(n).map((i) => {
    const a = (-90 + (i * 360) / n) * (Math.PI / 180);
    return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
  });
}

// ══ Lines of symmetry ════════════════════════════════════════════════════════

interface SymmetryInfo {
  label: string;
  points: Pt[];
  /** Mirror lines, as angles in degrees through the centre (150, 110). 90 is vertical. */
  lines: number[];
  /** How many times it fits onto itself in one full turn. */
  turns: number;
}

function regularInfo(label: string, n: number): SymmetryInfo {
  return { label, points: regular(n, 150, 110, 88), lines: range(n).map((k) => 90 + (k * 180) / n), turns: n };
}

const SYMMETRY: Record<SymmetryShape, SymmetryInfo> = {
  equilateral:   { label: 'Equilateral triangle', points: regular(3, 150, 122, 96), lines: [], turns: 3 },
  isosceles:     { label: 'Isosceles triangle', points: [{ x: 150, y: 22 }, { x: 215, y: 198 }, { x: 85, y: 198 }], lines: [90], turns: 1 },
  scalene:       { label: 'Scalene triangle', points: [{ x: 95, y: 40 }, { x: 245, y: 190 }, { x: 60, y: 190 }], lines: [], turns: 1 },
  square:        regularInfo('Square', 4),
  rectangle:     { label: 'Rectangle', points: [{ x: 50, y: 50 }, { x: 250, y: 50 }, { x: 250, y: 170 }, { x: 50, y: 170 }], lines: [0, 90], turns: 2 },
  rhombus:       { label: 'Rhombus', points: [{ x: 150, y: 20 }, { x: 225, y: 110 }, { x: 150, y: 200 }, { x: 75, y: 110 }], lines: [0, 90], turns: 2 },
  parallelogram: { label: 'Parallelogram', points: [{ x: 95, y: 55 }, { x: 255, y: 55 }, { x: 205, y: 165 }, { x: 45, y: 165 }], lines: [], turns: 2 },
  kite:          { label: 'Kite', points: [{ x: 150, y: 18 }, { x: 215, y: 82 }, { x: 150, y: 204 }, { x: 85, y: 82 }], lines: [90], turns: 1 },
  pentagon:      regularInfo('Regular pentagon', 5),
  hexagon:       regularInfo('Regular hexagon', 6),
  octagon:       regularInfo('Regular octagon', 8),
};
// A square is drawn flat, and an equilateral triangle's mirror lines pass through its own centre.
SYMMETRY.square.points = [{ x: 70, y: 30 }, { x: 230, y: 30 }, { x: 230, y: 190 }, { x: 70, y: 190 }];
SYMMETRY.square.lines = [0, 45, 90, 135];

const SYMMETRY_ORDER: SymmetryShape[] = ['equilateral', 'isosceles', 'scalene', 'square', 'rectangle', 'rhombus', 'parallelogram', 'kite', 'pentagon', 'hexagon', 'octagon'];

export function SymmetryVisual({ spec }: { spec: Of<'symmetry'> }) {
  const [shape, setShape] = useState<SymmetryShape>(spec.shape);
  const [show, setShow] = useState<'hide' | 'show'>('show');
  const info = SYMMETRY[shape];
  const centre: Pt = shape === 'equilateral' ? { x: 150, y: 122 } : { x: 150, y: 110 };
  const lines = shape === 'equilateral' ? [90, 30, 150] : info.lines;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 226" className="w-full max-w-[340px] mx-auto h-auto" role="img" aria-label={`${info.label} with ${lines.length} lines of symmetry`}>
        <polygon points={pointsAttr(info.points)} fill={C.star} fillOpacity={0.55} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        {show === 'show' && lines.map((deg, i) => {
          const a = (deg * Math.PI) / 180;
          return (
            <line
              key={i}
              x1={centre.x - 125 * Math.cos(a)} y1={centre.y + 125 * Math.sin(a)}
              x2={centre.x + 125 * Math.cos(a)} y2={centre.y - 125 * Math.sin(a)}
              stroke={C.action} strokeWidth={2.5} strokeDasharray="7 5" strokeLinecap="round"
            />
          );
        })}
      </svg>
      <Picker label="Shape" options={SYMMETRY_ORDER.map((s) => ({ value: s, label: SYMMETRY[s].label }))} value={shape} onChange={setShape} />
      <Toggle options={[{ value: 'show', label: 'Show mirror lines' }, { value: 'hide', label: 'Hide them' }]} value={show} onChange={setShow} />
      <div className="flex gap-2">
        <Stat label="Lines of symmetry" value={lines.length} />
        <Stat label="Fits itself in a full turn" value={`${info.turns} time${info.turns === 1 ? '' : 's'}`} />
      </div>
      <Working>
        {lines.length === 0
          ? `A ${info.label.toLowerCase()} has no line of symmetry: no fold makes the two halves match.`
          : `Fold along a dashed line and the two halves match exactly. A ${info.label.toLowerCase()} has ${lines.length} such line${lines.length === 1 ? '' : 's'}.`}
      </Working>
    </div>
  );
}

// ══ Cuboid: volume and surface area ══════════════════════════════════════════

export function CuboidVisual({ spec }: { spec: Of<'cuboid'> }) {
  const [l, setL] = useState(spec.length);
  const [w, setW] = useState(spec.width);
  const [h, setH] = useState(spec.height);
  const [mode, setMode] = useState<'volume' | 'surface'>('volume');
  const unit = spec.unit ?? 'cm';
  const cos = 0.866;
  const u = Math.min(26, 230 / ((l + w) * cos), 180 / ((l + w) * 0.5 + h));
  const ox = 150 - ((l - w) * cos * u) / 2;
  const oy = 16 + h * u;
  const P = (x: number, y: number, z: number): Pt => ({ x: ox + (x - y) * cos * u, y: oy + (x + y) * 0.5 * u - z * u });
  const seg = (a: Pt, b: Pt, key: string) => <line key={key} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={C.ink} strokeWidth={1.2} />;
  const grid: React.ReactNode[] = [];
  for (let i = 1; i < l; i++) { grid.push(seg(P(i, 0, h), P(i, w, h), `tx${i}`)); grid.push(seg(P(i, w, 0), P(i, w, h), `fx${i}`)); }
  for (let i = 1; i < w; i++) { grid.push(seg(P(0, i, h), P(l, i, h), `ty${i}`)); grid.push(seg(P(l, i, 0), P(l, i, h), `ry${i}`)); }
  for (let i = 1; i < h; i++) { grid.push(seg(P(0, w, i), P(l, w, i), `fz${i}`)); grid.push(seg(P(l, 0, i), P(l, w, i), `rz${i}`)); }
  const volume = l * w * h;
  const surface = 2 * (l * w + w * h + l * h);

  return (
    <div className="space-y-3">
      <svg viewBox={`0 0 300 ${Math.ceil(oy + (l + w) * 0.5 * u + 14)}`} className="w-full max-w-[340px] mx-auto h-auto" role="img" aria-label={`A cuboid ${l} by ${w} by ${h}`}>
        <polygon points={pointsAttr([P(0, 0, h), P(l, 0, h), P(l, w, h), P(0, w, h)])} fill={C.hint} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        <polygon points={pointsAttr([P(0, w, h), P(l, w, h), P(l, w, 0), P(0, w, 0)])} fill={C.star} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        <polygon points={pointsAttr([P(l, 0, h), P(l, w, h), P(l, w, 0), P(l, 0, 0)])} fill={C.star} fillOpacity={0.6} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        {grid}
      </svg>
      <Toggle options={[{ value: 'volume', label: 'Volume' }, { value: 'surface', label: 'Surface area' }]} value={mode} onChange={setMode} />
      <Slider label="Length" value={l} min={1} max={8} onChange={setL} display={`${l} ${unit}`} />
      <Slider label="Width" value={w} min={1} max={8} onChange={setW} display={`${w} ${unit}`} />
      <Slider label="Height" value={h} min={1} max={8} onChange={setH} display={`${h} ${unit}`} />
      <Working>
        {mode === 'volume'
          ? `One layer holds ${l} × ${w} = ${l * w} cubes, and there are ${h} layer${h === 1 ? '' : 's'}: ${l} × ${w} × ${h} = ${fmt(volume)} cubic ${unit}${l === w && w === h ? ' (a cube)' : ''}`
          : `Six faces in three matching pairs: 2 × (${l}×${w} + ${w}×${h} + ${l}×${h}) = 2 × ${l * w + w * h + l * h} = ${fmt(surface)} square ${unit}`}
      </Working>
    </div>
  );
}

// ══ Coordinate grid ══════════════════════════════════════════════════════════

export function CoordinateGridVisual({ spec }: { spec: Of<'coordinateGrid'> }) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [mine, setMine] = useState<{ x: number; y: number } | null>(null);
  let negative = false;
  for (let i = 0; i < spec.points.length; i++) if (spec.points[i].x < 0 || spec.points[i].y < 0) negative = true;
  const lo = negative ? -8 : 0;
  const hi = negative ? 8 : 10;
  const size = 260;
  const pad = 20;
  const step = size / (hi - lo);
  const X = (v: number) => pad + (v - lo) * step;
  const Y = (v: number) => pad + (hi - v) * step;

  function tap(e: React.PointerEvent<SVGSVGElement>) {
    const svg = svgRef.current;
    if (!svg) return;
    const box = svg.getBoundingClientRect();
    const scale = (size + pad * 2) / box.width;
    const gx = Math.round(((e.clientX - box.left) * scale - pad) / step + lo);
    const gy = Math.round(hi - ((e.clientY - box.top) * scale - pad) / step);
    if (gx < lo || gx > hi || gy < lo || gy > hi) return;
    setMine({ x: gx, y: gy });
  }

  const quadrant = (p: { x: number; y: number }): string => {
    if (p.x === 0 && p.y === 0) return 'the origin';
    if (p.y === 0) return 'on the x-axis';
    if (p.x === 0) return 'on the y-axis';
    if (p.x > 0) return p.y > 0 ? 'in the first quadrant' : 'in the fourth quadrant';
    return p.y > 0 ? 'in the second quadrant' : 'in the third quadrant';
  };

  return (
    <div className="space-y-3">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${size + pad * 2} ${size + pad * 2}`}
        className="w-full max-w-[340px] mx-auto h-auto touch-none cursor-crosshair"
        role="img"
        aria-label="Coordinate grid. Tap to place a point."
        onPointerDown={tap}
      >
        {range(hi - lo + 1).map((i) => {
          const v = lo + i;
          return (
            <g key={i}>
              <line x1={X(v)} y1={Y(lo)} x2={X(v)} y2={Y(hi)} stroke={v === 0 ? C.ink : C.line} strokeWidth={v === 0 ? 2.5 : 1} />
              <line x1={X(lo)} y1={Y(v)} x2={X(hi)} y2={Y(v)} stroke={v === 0 ? C.ink : C.line} strokeWidth={v === 0 ? 2.5 : 1} />
              {v !== 0 && v % 2 === 0 && (
                <>
                  <text x={X(v)} y={Y(0) + 13} textAnchor="middle" fontSize={9} fontWeight={800} fill={C.muted}>{v}</text>
                  <text x={X(0) - 5} y={Y(v) + 3} textAnchor="end" fontSize={9} fontWeight={800} fill={C.muted}>{v}</text>
                </>
              )}
            </g>
          );
        })}
        {spec.join && spec.points.length > 1 && (
          <polygon points={pointsAttr(spec.points.map((p) => ({ x: X(p.x), y: Y(p.y) })))} fill={C.star} fillOpacity={0.35} stroke={C.ink} strokeWidth={2} strokeLinejoin="round" />
        )}
        {spec.points.map((p, i) => (
          <g key={i}>
            <circle cx={X(p.x)} cy={Y(p.y)} r={5.5} fill={C.star} stroke={C.ink} strokeWidth={2} />
            <text x={X(p.x) + 8} y={Y(p.y) - 8} fontSize={11} fontWeight={800} fill={C.ink}>{p.label ? `${p.label} ` : ''}({p.x}, {p.y})</text>
          </g>
        ))}
        {mine && <circle cx={X(mine.x)} cy={Y(mine.y)} r={6.5} fill={C.action} stroke={C.ink} strokeWidth={2} />}
      </svg>
      <Working>
        {mine
          ? `Your point is (${mine.x}, ${mine.y}): ${Math.abs(mine.x)} ${mine.x < 0 ? 'left' : 'right'} and ${Math.abs(mine.y)} ${mine.y < 0 ? 'down' : 'up'} from the origin. It is ${quadrant(mine)}.`
          : 'Tap the grid to place a point. The first number is how far across (x); the second is how far up (y).'}
      </Working>
    </div>
  );
}

// ══ Quadrilaterals ═══════════════════════════════════════════════════════════

interface QuadInfo { label: string; points: Pt[]; angles: number[]; facts: string[] }

const QUADS: Record<QuadKind, QuadInfo> = {
  square: {
    label: 'Square', points: [{ x: 75, y: 30 }, { x: 225, y: 30 }, { x: 225, y: 180 }, { x: 75, y: 180 }], angles: [90, 90, 90, 90],
    facts: ['All four sides are equal', 'All four angles are 90°', 'Opposite sides are parallel', 'Diagonals are equal and cross at 90°'],
  },
  rectangle: {
    label: 'Rectangle', points: [{ x: 45, y: 50 }, { x: 255, y: 50 }, { x: 255, y: 165 }, { x: 45, y: 165 }], angles: [90, 90, 90, 90],
    facts: ['Opposite sides are equal and parallel', 'All four angles are 90°', 'Diagonals are equal and cut each other in half'],
  },
  parallelogram: {
    label: 'Parallelogram', points: [{ x: 95, y: 50 }, { x: 265, y: 50 }, { x: 205, y: 165 }, { x: 35, y: 165 }], angles: [118, 62, 118, 62],
    facts: ['Opposite sides are equal and parallel', 'Opposite angles are equal', 'Angles next to each other add to 180°', 'Diagonals cut each other in half'],
  },
  rhombus: {
    label: 'Rhombus', points: [{ x: 150, y: 22 }, { x: 240, y: 108 }, { x: 150, y: 194 }, { x: 60, y: 108 }], angles: [93, 87, 93, 87],
    facts: ['All four sides are equal', 'Opposite sides are parallel', 'Opposite angles are equal', 'Diagonals cross at 90° and cut each other in half'],
  },
  trapezium: {
    label: 'Trapezium', points: [{ x: 105, y: 50 }, { x: 205, y: 50 }, { x: 260, y: 165 }, { x: 40, y: 165 }], angles: [119, 116, 64, 61],
    facts: ['Exactly one pair of opposite sides is parallel', 'Each angle on the top side and the angle below it add to 180°'],
  },
  kite: {
    label: 'Kite', points: [{ x: 150, y: 20 }, { x: 220, y: 85 }, { x: 150, y: 200 }, { x: 80, y: 85 }], angles: [94, 102, 62, 102],
    facts: ['Two pairs of equal sides that sit next to each other', 'One pair of opposite angles is equal', 'Diagonals cross at 90°'],
  },
};

const QUAD_ORDER: QuadKind[] = ['square', 'rectangle', 'parallelogram', 'rhombus', 'trapezium', 'kite'];

export function QuadrilateralVisual({ spec }: { spec: Of<'quadrilateral'> }) {
  const [kind, setKind] = useState<QuadKind>(spec.kind);
  const [diagonals, setDiagonals] = useState<'off' | 'on'>('off');
  const q = QUADS[kind];
  const mid = { x: (q.points[0].x + q.points[2].x) / 2, y: (q.points[0].y + q.points[2].y) / 2 };

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 220" className="w-full max-w-[340px] mx-auto h-auto" role="img" aria-label={q.label}>
        <polygon points={pointsAttr(q.points)} fill={C.star} fillOpacity={0.55} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
        {diagonals === 'on' && (
          <>
            <line x1={q.points[0].x} y1={q.points[0].y} x2={q.points[2].x} y2={q.points[2].y} stroke={C.action} strokeWidth={2.5} strokeDasharray="7 5" />
            <line x1={q.points[1].x} y1={q.points[1].y} x2={q.points[3].x} y2={q.points[3].y} stroke={C.action} strokeWidth={2.5} strokeDasharray="7 5" />
          </>
        )}
        {q.points.map((p, i) => (
          // Pull each label a little towards the middle so it sits inside its corner.
          <text key={i} x={p.x + (mid.x - p.x) * 0.24} y={p.y + (mid.y - p.y) * 0.24 + 4} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.ink}>
            {q.angles[i]}°
          </text>
        ))}
      </svg>
      <Picker label="Shape" options={QUAD_ORDER.map((k) => ({ value: k, label: QUADS[k].label }))} value={kind} onChange={setKind} />
      <Toggle options={[{ value: 'off', label: 'Sides and angles' }, { value: 'on', label: 'Show diagonals' }]} value={diagonals} onChange={setDiagonals} />
      <ul className="bg-soft rounded-control px-4 py-3 space-y-1">
        {q.facts.map((f) => (
          <li key={f} className="text-[14px] font-bold text-ink flex gap-2"><span aria-hidden="true">•</span>{f}</li>
        ))}
      </ul>
      <Working>
        {q.angles.join('° + ')}° = 360°. The four angles of every quadrilateral add to 360°.
      </Working>
    </div>
  );
}

// ══ Parallel lines and a transversal ═════════════════════════════════════════

export function ParallelLinesVisual({ spec }: { spec: Of<'parallelLines'> }) {
  const [deg, setDeg] = useState(spec.angle);
  const a = (deg * Math.PI) / 180;
  const other = 180 - deg;
  // The transversal passes through (150, 110) and meets the lines y = 65 and y = 155.
  const xAt = (y: number) => 150 + (110 - y) / Math.tan(a);
  const crossings = [{ x: xAt(65), y: 65 }, { x: xAt(155), y: 155 }];
  const far = 100 / Math.sin(a);

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 220" className="w-full max-w-[340px] mx-auto h-auto" role="img" aria-label={`Two parallel lines crossed by a line at ${deg} degrees`}>
        <line x1={150 - far * Math.cos(a)} y1={110 + far * Math.sin(a)} x2={150 + far * Math.cos(a)} y2={110 - far * Math.sin(a)} stroke={C.action} strokeWidth={3} strokeLinecap="round" />
        {crossings.map((p, i) => (
          <g key={i}>
            <line x1={12} y1={p.y} x2={288} y2={p.y} stroke={C.ink} strokeWidth={3} strokeLinecap="round" />
            <text x={p.x + 30} y={p.y - 9} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.ink}>{deg}°</text>
            <text x={p.x - 30} y={p.y - 9} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.muted}>{other}°</text>
            <text x={p.x - 30} y={p.y + 19} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.ink}>{deg}°</text>
            <text x={p.x + 30} y={p.y + 19} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.muted}>{other}°</text>
            <circle cx={p.x} cy={p.y} r={4} fill={C.star} stroke={C.ink} strokeWidth={2} />
          </g>
        ))}
        <text x={282} y={58} textAnchor="end" fontSize={11} fontWeight={800} fill={C.muted}>parallel</text>
        <text x={282} y={172} textAnchor="end" fontSize={11} fontWeight={800} fill={C.muted}>parallel</text>
      </svg>
      <Slider label="Tilt the crossing line" value={deg} min={30} max={150} step={5} onChange={setDeg} display={`${deg}°`} />
      <div className="flex gap-2">
        <Stat label="Dark angles" value={`${deg}°`} />
        <Stat label="Grey angles" value={`${other}°`} />
      </div>
      <Working>
        The same angles appear at both crossings because the lines are parallel (corresponding angles). Angles on a straight line add to 180°: {deg}° + {other}° = 180°. Angles opposite each other at a crossing are equal.
      </Working>
    </div>
  );
}

'use client';

import type { ReactNode } from 'react';
import type { TriangleFigure, RectangleFigure, PolygonFigure, CircleFigure, GridFigure } from '@/lib/figures/types';
import type { Pt, KindProps } from './shared';
import { C, Frame, Label, SVG_CLASS, INK_W, HI_W, isOn, text, num, clamp, list, pointsAttr, besideEdge, estWidth } from './shared';

/** A filled wedge marking the angle at `v` between the directions to `p` and `q`. */
function cornerWedge(v: Pt, p: Pt, q: Pt, r: number): string {
  const l1 = Math.hypot(p.x - v.x, p.y - v.y) || 1;
  const l2 = Math.hypot(q.x - v.x, q.y - v.y) || 1;
  const d1 = { x: (p.x - v.x) / l1, y: (p.y - v.y) / l1 };
  const d2 = { x: (q.x - v.x) / l2, y: (q.y - v.y) / l2 };
  const sweep = d1.x * d2.y - d1.y * d2.x > 0 ? 1 : 0;
  return `M ${v.x} ${v.y} L ${(v.x + r * d1.x).toFixed(1)} ${(v.y + r * d1.y).toFixed(1)} A ${r} ${r} 0 0 ${sweep} ${(v.x + r * d2.x).toFixed(1)} ${(v.y + r * d2.y).toFixed(1)} Z`;
}

/** The unit direction, square to edge p-q, that points away from `inside`. */
function awayFrom(p: Pt, q: Pt, inside: Pt): Pt {
  const dx = q.x - p.x;
  const dy = q.y - p.y;
  const len = Math.hypot(dx, dy) || 1;
  let nx = -dy / len;
  let ny = dx / len;
  if ((inside.x - (p.x + q.x) / 2) * nx + (inside.y - (p.y + q.y) / 2) * ny > 0) {
    nx = -nx;
    ny = -ny;
  }
  return { x: nx, y: ny };
}

/** Where a label goes inside the corner at `v`: along the line that halves the angle. */
function insideCorner(v: Pt, p: Pt, q: Pt, label: string): Pt {
  const l1 = Math.hypot(p.x - v.x, p.y - v.y) || 1;
  const l2 = Math.hypot(q.x - v.x, q.y - v.y) || 1;
  const u1 = { x: (p.x - v.x) / l1, y: (p.y - v.y) / l1 };
  const u2 = { x: (q.x - v.x) / l2, y: (q.y - v.y) / l2 };
  const bx = u1.x + u2.x;
  const by = u1.y + u2.y;
  const bl = Math.hypot(bx, by) || 1;
  const half = Math.acos(clamp(u1.x * u2.x + u1.y * u2.y, -1, 1)) / 2;
  const d = clamp(15 / (Math.sin(half) || 1) + estWidth(label) / 4, 32, 62);
  return { x: v.x + (bx / bl) * d, y: v.y + (by / bl) * d + 4.5 };
}

// ══ Triangle ═════════════════════════════════════════════════════════════════

/** Corners A (top), B (bottom left), C (bottom right) for each shape. */
const TRIANGLES: Record<string, Pt[]> = {
  scalene: [{ x: 195, y: 46 }, { x: 60, y: 190 }, { x: 270, y: 190 }],
  right: [{ x: 125, y: 44 }, { x: 125, y: 190 }, { x: 285, y: 190 }],
  isosceles: [{ x: 180, y: 36 }, { x: 115, y: 190 }, { x: 245, y: 190 }],
  equilateral: [{ x: 180, y: 34 }, { x: 90, y: 190 }, { x: 270, y: 190 }],
};

const TRIANGLE_WORDS: Record<string, string> = {
  scalene: 'A triangle',
  right: 'A right-angled triangle with its right angle at the bottom left',
  isosceles: 'An isosceles triangle',
  equilateral: 'An equilateral triangle',
};

export function TriangleKind({ spec, className }: KindProps<TriangleFigure>) {
  const shape = Object.prototype.hasOwnProperty.call(TRIANGLES, spec.shape) ? spec.shape : 'scalene';
  const pts = TRIANGLES[shape];
  const A = pts[0];
  const B = pts[1];
  const Cc = pts[2];
  const mid: Pt = { x: (A.x + B.x + Cc.x) / 3, y: (A.y + B.y + Cc.y) / 3 };
  const hl = spec.highlight;
  const filled = isOn(hl, 'fill');
  const sides = spec.sides || {};
  const angles = spec.angles || {};

  const edges = [
    { key: 'ab', name: 'left side', p: A, q: B, label: text(sides.ab) },
    { key: 'bc', name: 'bottom side', p: B, q: Cc, label: text(sides.bc) },
    { key: 'ca', name: 'right side', p: Cc, q: A, label: text(sides.ca) },
  ];
  const corners = [
    { key: 'a', name: 'top angle', v: A, p: B, q: Cc, label: text(angles.a) },
    { key: 'b', name: 'bottom left angle', v: B, p: Cc, q: A, label: text(angles.b) },
    { key: 'c', name: 'bottom right angle', v: Cc, p: A, q: B, label: text(angles.c) },
  ];
  const hasHeight = typeof spec.height === 'string';
  const heightLabel = text(spec.height);
  const heightOn = isOn(hl, 'height');
  const foot: Pt = { x: A.x, y: B.y };

  const words: string[] = [];
  for (let i = 0; i < edges.length; i++) {
    if (edges[i].label) words.push(`${edges[i].name} ${edges[i].label}`);
  }
  for (let i = 0; i < corners.length; i++) {
    if (corners[i].label) words.push(`${corners[i].name} ${corners[i].label}`);
  }
  if (hasHeight) words.push(heightLabel ? `dashed height ${heightLabel}` : 'a dashed height');
  if (spec.enclose === true) words.push('a dashed rectangle drawn around it');
  const aria = words.length ? `${TRIANGLE_WORDS[shape]}: ${words.join(', ')}` : TRIANGLE_WORDS[shape];

  const marks: ReactNode[] = [];
  const angleLabels: ReactNode[] = [];
  for (let i = 0; i < corners.length; i++) {
    const c = corners[i];
    const on = isOn(hl, c.key);
    if (shape === 'right' && c.key === 'b') {
      marks.push(
        <path key={c.key} d={`M ${B.x + 13} ${B.y} L ${B.x + 13} ${B.y - 13} L ${B.x} ${B.y - 13}`} fill="none"
          stroke={on ? C.action : C.ink} strokeWidth={on ? 3.5 : 2} strokeLinejoin="round" />,
      );
    } else if (c.label !== '' || on) {
      marks.push(
        <path key={c.key} d={cornerWedge(c.v, c.p, c.q, on ? 24 : 20)} fill={on ? C.action : C.star}
          stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />,
      );
    }
    if (c.label !== '') {
      const at = insideCorner(c.v, c.p, c.q, c.label);
      angleLabels.push(
        <Label key={c.key} x={at.x} y={at.y} fill={on ? C.action : C.ink} halo={!filled}>{c.label}</Label>,
      );
    }
  }

  const left = Math.min(A.x, B.x);
  const right = Math.max(A.x, Cc.x);

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox="0 0 360 222" className={SVG_CLASS} aria-hidden="true">
        {spec.enclose === true && (
          <rect x={left} y={A.y} width={right - left} height={B.y - A.y} fill="none" stroke={C.muted} strokeWidth={2} strokeDasharray="6 5" />
        )}
        <polygon points={pointsAttr(pts)} fill={filled ? C.star : C.card} stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
        {marks}
        {hasHeight && (
          <g>
            <line x1={A.x} y1={A.y} x2={foot.x} y2={foot.y} stroke={heightOn ? C.action : C.ink} strokeWidth={heightOn ? 4 : 2} strokeDasharray="6 5" />
            {shape !== 'right' && (
              <path d={`M ${foot.x + 9} ${foot.y} L ${foot.x + 9} ${foot.y - 9} L ${foot.x} ${foot.y - 9}`} fill="none" stroke={C.ink} strokeWidth={1.5} />
            )}
          </g>
        )}
        {edges.map((e) => (isOn(hl, e.key) ? (
          <line key={e.key} x1={e.p.x} y1={e.p.y} x2={e.q.x} y2={e.q.y} stroke={C.action} strokeWidth={HI_W} strokeLinecap="round" />
        ) : null))}
        {edges.map((e) => {
          if (e.label === '') return null;
          const n = awayFrom(e.p, e.q, mid);
          const at = besideEdge(e.p, e.q, n.x, n.y, 15);
          return (
            <Label key={e.key} x={at.x} y={at.y} anchor={at.anchor} fill={isOn(hl, e.key) ? C.action : C.ink}>{e.label}</Label>
          );
        })}
        {hasHeight && heightLabel !== '' && (
          <Label
            x={shape === 'right' ? A.x + 10 : A.x - 9}
            y={A.y + (B.y - A.y) * 0.62}
            anchor={shape === 'right' ? 'start' : 'end'}
            fill={heightOn ? C.action : C.ink}
            halo={!filled}
          >
            {heightLabel}
          </Label>
        )}
        {angleLabels}
      </svg>
    </Frame>
  );
}

// ══ Rectangle ════════════════════════════════════════════════════════════════

export function RectangleKind({ spec, className }: KindProps<RectangleFigure>) {
  const hl = spec.highlight;
  const grid = spec.grid && typeof spec.grid === 'object' ? spec.grid : undefined;
  const cols = grid ? clamp(Math.round(num(grid.cols, 0)), 0, 12) : 0;
  const rows = grid ? clamp(Math.round(num(grid.rows, 0)), 0, 12) : 0;
  const hasGrid = cols >= 1 && rows >= 1;
  const square = spec.square === true;

  // Unit squares must stay square, so a grid sets the proportion.
  let p = square ? 1 : 1.6;
  if (hasGrid) p = cols / rows;
  else if (typeof spec.proportion === 'number' && isFinite(spec.proportion)) p = clamp(spec.proportion, 1, 3);

  const w = Math.min(190, 140 * p);
  const h = w / p;
  const x0 = 207 - w / 2;
  const y0 = 40;
  const length = text(spec.length);
  const breadth = text(spec.breadth);
  const inside = text(spec.inside);
  const filled = isOn(hl, 'fill');
  const lengthOn = isOn(hl, 'length');
  const breadthOn = isOn(hl, 'breadth');
  const borderOn = isOn(hl, 'border');

  const words: string[] = [];
  if (length) words.push(`top side ${length}`);
  if (breadth) words.push(`left side ${breadth}`);
  if (hasGrid) words.push(`divided into ${rows} rows of ${cols} unit squares`);
  if (inside) words.push(`with ${inside} written inside`);
  const name = square ? 'A square' : 'A rectangle';
  const aria = words.length ? `${name}: ${words.join(', ')}` : name;

  const lines: ReactNode[] = [];
  if (hasGrid) {
    for (let c = 1; c < cols; c++) {
      const x = x0 + (c * w) / cols;
      lines.push(<line key={`c${c}`} x1={x} y1={y0} x2={x} y2={y0 + h} stroke={C.ink} strokeWidth={1} />);
    }
    for (let r = 1; r < rows; r++) {
      const y = y0 + (r * h) / rows;
      lines.push(<line key={`r${r}`} x1={x0} y1={y} x2={x0 + w} y2={y} stroke={C.ink} strokeWidth={1} />);
    }
  }

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${(y0 + h + 18).toFixed(0)}`} className={SVG_CLASS} aria-hidden="true">
        <rect x={x0} y={y0} width={w} height={h} fill={filled ? C.star : C.card}
          stroke={borderOn ? C.action : C.ink} strokeWidth={borderOn ? HI_W : INK_W} strokeLinejoin="round" />
        {lines}
        {lengthOn && <line x1={x0} y1={y0} x2={x0 + w} y2={y0} stroke={C.action} strokeWidth={HI_W} strokeLinecap="round" />}
        {breadthOn && <line x1={x0} y1={y0} x2={x0} y2={y0 + h} stroke={C.action} strokeWidth={HI_W} strokeLinecap="round" />}
        {length !== '' && (
          <Label x={x0 + w / 2} y={y0 - 12} fill={lengthOn ? C.action : C.ink}>{length}</Label>
        )}
        {breadth !== '' && (
          <Label x={x0 - 11} y={y0 + h / 2 + 4.5} anchor="end" fill={breadthOn ? C.action : C.ink}>{breadth}</Label>
        )}
        {inside !== '' && (
          <Label x={x0 + w / 2} y={y0 + h / 2 + 4.5} size={estWidth(inside) > w - 12 ? 11 : 13} halo={!filled && hasGrid}>{inside}</Label>
        )}
      </svg>
    </Frame>
  );
}

// ══ Polygon ══════════════════════════════════════════════════════════════════

export function PolygonKind({ spec, className }: KindProps<PolygonFigure>) {
  const raw = list(spec.points);
  const n = raw.length;
  if (n < 3) return null;
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (let i = 0; i < n; i++) {
    const p = raw[i];
    if (!Array.isArray(p) || typeof p[0] !== 'number' || typeof p[1] !== 'number' || !isFinite(p[0]) || !isFinite(p[1])) return null;
    minX = Math.min(minX, p[0]);
    maxX = Math.max(maxX, p[0]);
    minY = Math.min(minY, p[1]);
    maxY = Math.max(maxY, p[1]);
  }
  const bw = maxX - minX;
  const bh = maxY - minY;
  if (bw <= 0 || bh <= 0) return null;

  const s = Math.min(190 / bw, 150 / bh, 34);
  const ox = 180 - (bw * s) / 2;
  const top = 36;
  const pts: Pt[] = [];
  for (let i = 0; i < n; i++) pts.push({ x: ox + (raw[i][0] - minX) * s, y: top + (raw[i][1] - minY) * s });

  // Which way round the corners run decides which side of an edge is outside.
  let area = 0;
  for (let i = 0; i < n; i++) {
    const a = pts[i];
    const b = pts[(i + 1) % n];
    area += a.x * b.y - b.x * a.y;
  }
  const sign = area >= 0 ? 1 : -1;
  const normals: Pt[] = [];
  for (let i = 0; i < n; i++) {
    const a = pts[i];
    const b = pts[(i + 1) % n];
    const len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
    normals.push({ x: (sign * (b.y - a.y)) / len, y: (-sign * (b.x - a.x)) / len });
  }

  const hl = spec.highlight;
  const filled = isOn(hl, 'fill');
  const edgeLabels = list(spec.edges);
  const cornerLabels = list(spec.corners);
  const rightAngles = list(spec.rightAngles);
  const dashed = list(spec.dashed);

  const said: string[] = [];
  const body: ReactNode[] = [];

  for (let i = 0; i < n; i++) {
    const a = pts[i];
    const b = pts[(i + 1) % n];
    const on = isOn(hl, `e${i}`);
    if (on) {
      body.push(<line key={`eh${i}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={C.action} strokeWidth={HI_W} strokeLinecap="round" />);
    }
    const label = text(edgeLabels[i]);
    if (label !== '') {
      const at = besideEdge(a, b, normals[i].x, normals[i].y, 14);
      body.push(<Label key={`el${i}`} x={at.x} y={at.y} anchor={at.anchor} fill={on ? C.action : C.ink}>{label}</Label>);
      said.push(`a side labelled ${label}`);
    }
  }

  for (let k = 0; k < rightAngles.length; k++) {
    const i = rightAngles[k];
    if (typeof i !== 'number' || i < 0 || i >= n || Math.floor(i) !== i) continue;
    const v = pts[i];
    const prev = pts[(i + n - 1) % n];
    const next = pts[(i + 1) % n];
    const l1 = Math.hypot(prev.x - v.x, prev.y - v.y) || 1;
    const l2 = Math.hypot(next.x - v.x, next.y - v.y) || 1;
    const u = { x: ((prev.x - v.x) / l1) * 10, y: ((prev.y - v.y) / l1) * 10 };
    const t = { x: ((next.x - v.x) / l2) * 10, y: ((next.y - v.y) / l2) * 10 };
    body.push(
      <path key={`ra${k}`} d={`M ${(v.x + u.x).toFixed(1)} ${(v.y + u.y).toFixed(1)} L ${(v.x + u.x + t.x).toFixed(1)} ${(v.y + u.y + t.y).toFixed(1)} L ${(v.x + t.x).toFixed(1)} ${(v.y + t.y).toFixed(1)}`}
        fill="none" stroke={C.ink} strokeWidth={1.5} />,
    );
  }
  if (rightAngles.length > 0) said.push('right angles marked with small squares');

  for (let k = 0; k < dashed.length; k++) {
    const d = dashed[k];
    if (!d || typeof d.from !== 'number' || typeof d.to !== 'number') continue;
    if (d.from < 0 || d.from >= n || d.to < 0 || d.to >= n || Math.floor(d.from) !== d.from || Math.floor(d.to) !== d.to || d.from === d.to) continue;
    const a = pts[d.from];
    const b = pts[d.to];
    const label = text(d.label);
    body.push(<line key={`d${k}`} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={C.muted} strokeWidth={2} strokeDasharray="6 5" />);
    if (label !== '') {
      body.push(<Label key={`dl${k}`} x={(a.x + b.x) / 2} y={(a.y + b.y) / 2 + 4.5} halo={!filled}>{label}</Label>);
      said.push(`a dashed line labelled ${label}`);
    } else {
      said.push('a dashed line');
    }
  }

  for (let i = 0; i < n; i++) {
    const label = text(cornerLabels[i]);
    if (label === '') continue;
    const before = normals[(i + n - 1) % n];
    const after = normals[i];
    let dx = before.x + after.x;
    let dy = before.y + after.y;
    const dl = Math.hypot(dx, dy);
    if (dl < 0.01) {
      dx = after.x;
      dy = after.y;
    } else {
      dx /= dl;
      dy /= dl;
    }
    body.push(
      <Label key={`cl${i}`} x={pts[i].x + dx * 15} y={pts[i].y + dy * 15 + 4.5} anchor={dx > 0.35 ? 'start' : dx < -0.35 ? 'end' : 'middle'}>{label}</Label>,
    );
    said.push(`a corner labelled ${label}`);
  }

  const aria = said.length ? `A shape with ${n} straight sides: ${said.join(', ')}` : `A shape with ${n} straight sides`;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 360 ${(top + bh * s + 36).toFixed(0)}`} className={SVG_CLASS} aria-hidden="true">
        <polygon points={pointsAttr(pts)} fill={filled ? C.star : C.card} stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
        {body}
      </svg>
    </Frame>
  );
}

// ══ Circle ═══════════════════════════════════════════════════════════════════

export function CircleKind({ spec, className }: KindProps<CircleFigure>) {
  const hl = spec.highlight;
  const cx = 160;
  const cy = 106;
  const R = 80;
  const hasRadius = typeof spec.radius === 'string';
  const hasDiameter = typeof spec.diameter === 'string';
  const radius = text(spec.radius);
  const diameter = text(spec.diameter);
  const radiusOn = isOn(hl, 'radius');
  const diameterOn = isOn(hl, 'diameter');
  const edgeOn = isOn(hl, 'edge');
  const filled = isOn(hl, 'fill');

  const words: string[] = [];
  if (hasRadius) words.push(radius ? `radius ${radius}` : 'its radius drawn');
  if (hasDiameter) words.push(diameter ? `diameter ${diameter}` : 'its diameter drawn');
  const aria = words.length ? `A circle: ${words.join(', ')}` : 'A circle';

  // With a diameter across the middle, the radius goes straight up instead.
  const radiusEnd: Pt = hasDiameter ? { x: cx, y: cy - R } : { x: cx + R, y: cy };

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox="0 0 320 212" className={SVG_CLASS} aria-hidden="true">
        <circle cx={cx} cy={cy} r={R} fill={filled ? C.star : C.card} stroke={edgeOn ? C.action : C.ink} strokeWidth={edgeOn ? HI_W : INK_W} />
        {hasDiameter && (
          <line x1={cx - R} y1={cy} x2={cx + R} y2={cy} stroke={diameterOn ? C.action : C.ink} strokeWidth={diameterOn ? HI_W : INK_W} strokeLinecap="round" />
        )}
        {hasRadius && (
          <line x1={cx} y1={cy} x2={radiusEnd.x} y2={radiusEnd.y} stroke={radiusOn ? C.action : C.ink} strokeWidth={radiusOn ? HI_W : INK_W} strokeLinecap="round" />
        )}
        {(hasRadius || hasDiameter) && <circle cx={cx} cy={cy} r={4.5} fill={C.ink} />}
        {hasDiameter && diameter !== '' && (
          <Label x={cx} y={cy + 22} fill={diameterOn ? C.action : C.ink} halo={!filled}>{diameter}</Label>
        )}
        {hasRadius && radius !== '' && (hasDiameter ? (
          <Label x={cx + 9} y={cy - R / 2 + 4.5} anchor="start" fill={radiusOn ? C.action : C.ink} halo={!filled}>{radius}</Label>
        ) : (
          <Label x={cx + R / 2} y={cy - 10} fill={radiusOn ? C.action : C.ink} halo={!filled}>{radius}</Label>
        ))}
      </svg>
    </Frame>
  );
}

// ══ Grid of unit squares ═════════════════════════════════════════════════════

export function GridKind({ spec, className }: KindProps<GridFigure>) {
  const rows = clamp(Math.round(num(spec.rows, 0)), 0, 12);
  const cols = clamp(Math.round(num(spec.cols, 0)), 0, 12);
  if (rows < 1 || cols < 1) return null;
  const cell = Math.min(28, 288 / cols, 224 / rows);
  const x0 = 160 - (cols * cell) / 2;
  const y0 = 10;
  const shaded = list(spec.shaded);

  const squares: ReactNode[] = [];
  const seen: Record<string, boolean> = {};
  let count = 0;
  for (let i = 0; i < shaded.length; i++) {
    const cellAt = shaded[i];
    if (!Array.isArray(cellAt)) continue;
    const r = cellAt[0];
    const c = cellAt[1];
    if (typeof r !== 'number' || typeof c !== 'number' || Math.floor(r) !== r || Math.floor(c) !== c) continue;
    if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
    const key = `${r}-${c}`;
    if (seen[key]) continue;
    seen[key] = true;
    count++;
    squares.push(<rect key={key} x={x0 + c * cell} y={y0 + r * cell} width={cell} height={cell} fill={C.action} />);
  }

  const lines: ReactNode[] = [];
  for (let c = 1; c < cols; c++) {
    lines.push(<line key={`c${c}`} x1={x0 + c * cell} y1={y0} x2={x0 + c * cell} y2={y0 + rows * cell} stroke={C.ink} strokeWidth={1.5} />);
  }
  for (let r = 1; r < rows; r++) {
    lines.push(<line key={`r${r}`} x1={x0} y1={y0 + r * cell} x2={x0 + cols * cell} y2={y0 + r * cell} stroke={C.ink} strokeWidth={1.5} />);
  }
  const dots: ReactNode[] = [];
  if (spec.dots === true) {
    for (let r = 1; r < rows; r++) {
      for (let c = 1; c < cols; c++) {
        dots.push(<circle key={`${r}-${c}`} cx={x0 + c * cell} cy={y0 + r * cell} r={3.2} fill={C.ink} />);
      }
    }
  }

  let aria = `A grid of unit squares, ${rows} rows by ${cols} columns`;
  if (count > 0) aria += `, with ${count} ${count === 1 ? 'square' : 'squares'} shaded`;
  if (spec.dots === true) aria += ', with a dot at each crossing inside';

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${(rows * cell + 20).toFixed(0)}`} className={SVG_CLASS} aria-hidden="true">
        <rect x={x0} y={y0} width={cols * cell} height={rows * cell} fill={C.card} />
        {squares}
        {lines}
        <rect x={x0} y={y0} width={cols * cell} height={rows * cell} fill="none" stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
        {dots}
      </svg>
    </Frame>
  );
}

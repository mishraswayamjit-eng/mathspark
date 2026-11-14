'use client';

import React, { useRef, useState } from 'react';
import type { VisualSpec } from '@/lib/visuals/spec';
import { C, range, gcd, fmt, Stat, Working, Slider, Toggle } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

// ══ Balance scale ════════════════════════════════════════════════════════════

interface Sides { lx: number; lu: number; rx: number; ru: number }

function sideText(x: number, units: number, v: string): string {
  const parts: string[] = [];
  if (x > 0) parts.push(x === 1 ? v : `${x}${v}`);
  if (units > 0 || x === 0) parts.push(String(units));
  return parts.join(' + ');
}

function Pan({ x, units, v }: { x: number; units: number; v: string }) {
  return (
    <div className="flex-1 min-w-0">
      <div className="min-h-[92px] bg-soft border-2 border-line rounded-tile p-2 flex flex-wrap gap-1.5 content-end justify-center">
        {range(x).map((i) => (
          <span key={`x${i}`} className="w-9 h-9 rounded-[6px] bg-action border-2 border-ink text-white font-extrabold flex items-center justify-center">{v}</span>
        ))}
        {range(units).map((i) => (
          <span key={`u${i}`} className="w-5 h-5 rounded-full bg-star border-2 border-ink" aria-hidden="true" />
        ))}
      </div>
      <div className="h-2 bg-ink rounded-b-note mx-3" aria-hidden="true" />
      <p className="text-label text-ink text-center mt-1">{sideText(x, units, v)}</p>
    </div>
  );
}

export function BalanceVisual({ spec }: { spec: Of<'balance'> }) {
  const start: Sides = { lx: spec.leftX, lu: spec.leftUnits, rx: spec.rightX, ru: spec.rightUnits };
  const [s, setS] = useState<Sides>(start);
  const [note, setNote] = useState('Do the same to both sides to keep the scale level');
  const v = spec.variable ?? 'x';

  // One side holds only x-boxes, the other only weights: the weights can be shared out.
  const leftOnlyX = s.lx > 1 && s.lu === 0 && s.rx === 0;
  const rightOnlyX = s.rx > 1 && s.ru === 0 && s.lx === 0;
  const boxes = leftOnlyX ? s.lx : rightOnlyX ? s.rx : 0;
  const weights = leftOnlyX ? s.ru : rightOnlyX ? s.lu : 0;
  const canShare = boxes > 1 && weights % boxes === 0;

  const solved = (s.lx === 1 && s.lu === 0 && s.rx === 0) || (s.rx === 1 && s.ru === 0 && s.lx === 0);
  const answer = s.lx === 1 ? s.ru : s.lu;

  const btn = 'flex-1 min-h-[48px] rounded-control border-2 border-ink bg-white text-ink font-extrabold text-[14px] px-2 shadow-hard-sm disabled:opacity-40 disabled:shadow-none active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]';

  return (
    <div className="space-y-3">
      <div className="flex items-start gap-2">
        <Pan x={s.lx} units={s.lu} v={v} />
        <span className="font-display text-heading text-ink pt-8" aria-label="equals">=</span>
        <Pan x={s.rx} units={s.ru} v={v} />
      </div>

      <Working>{solved ? `${v} = ${answer} 🎉` : note}</Working>

      <div className="flex flex-wrap gap-2">
        <button type="button" className={btn} disabled={s.lu < 1 || s.ru < 1}
          onClick={() => { setS({ lx: s.lx, lu: s.lu - 1, rx: s.rx, ru: s.ru - 1 }); setNote('Took 1 from both sides. Still level!'); }}>
          Take 1 from each side
        </button>
        <button type="button" className={btn} disabled={s.lx < 1 || s.rx < 1}
          onClick={() => { setS({ lx: s.lx - 1, lu: s.lu, rx: s.rx - 1, ru: s.ru }); setNote(`Took one ${v} from both sides. Still level!`); }}>
          Take one {v} from each side
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        <button type="button" className={btn} disabled={!canShare}
          onClick={() => {
            const each = weights / boxes;
            setS(leftOnlyX ? { lx: 1, lu: 0, rx: 0, ru: each } : { lx: 0, lu: each, rx: 1, ru: 0 });
            setNote(`Shared ${weights} equally between ${boxes} boxes: ${weights} ÷ ${boxes} = ${each}`);
          }}>
          Share equally
        </button>
        <button type="button" className={btn}
          onClick={() => { setS(start); setNote('Do the same to both sides to keep the scale level'); }}>
          Start again
        </button>
      </div>
    </div>
  );
}

// ══ Rectangle: area and perimeter ════════════════════════════════════════════

export function RectangleVisual({ spec }: { spec: Of<'rectangle'> }) {
  const [w, setW] = useState(spec.width);
  const [h, setH] = useState(spec.height);
  const [mode, setMode] = useState<'area' | 'perimeter'>('area');
  const unit = spec.unit ?? 'units';
  const cell = Math.min(300 / w, 190 / h, 34);
  const pw = w * cell;
  const ph = h * cell;

  return (
    <div className="space-y-3">
      <div className="flex justify-center">
        <svg viewBox={`0 0 ${pw + 44} ${ph + 36}`} width={pw + 44} height={ph + 36} className="max-w-full h-auto" role="img"
          aria-label={`Rectangle ${w} by ${h}`}>
          <g transform="translate(30 6)">
            <rect x={0} y={0} width={pw} height={ph} fill={mode === 'area' ? C.actionSoft : C.card} />
            {range(w + 1).map((i) => (
              <line key={`v${i}`} x1={i * cell} y1={0} x2={i * cell} y2={ph} stroke={C.line} strokeWidth={1} />
            ))}
            {range(h + 1).map((i) => (
              <line key={`h${i}`} x1={0} y1={i * cell} x2={pw} y2={i * cell} stroke={C.line} strokeWidth={1} />
            ))}
            <rect x={0} y={0} width={pw} height={ph} fill="none" stroke={mode === 'perimeter' ? C.action : C.ink} strokeWidth={mode === 'perimeter' ? 5 : 2.5} />
            <text x={pw / 2} y={ph + 20} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.ink}>{w} {unit}</text>
            <text x={-8} y={ph / 2 + 4} textAnchor="end" fontSize={13} fontWeight={800} fill={C.ink}>{h}</text>
          </g>
        </svg>
      </div>

      <Toggle
        options={[{ value: 'area', label: 'Area' }, { value: 'perimeter', label: 'Perimeter' }]}
        value={mode}
        onChange={setMode}
      />
      <div className="grid grid-cols-2 gap-4">
        <Slider label="Length" value={w} min={1} max={20} onChange={setW} />
        <Slider label="Breadth" value={h} min={1} max={20} onChange={setH} />
      </div>
      <Working>
        {mode === 'area'
          ? `Area = length × breadth = ${w} × ${h} = ${w * h} square ${unit}`
          : `Perimeter = 2 × (length + breadth) = 2 × (${w} + ${h}) = ${2 * (w + h)} ${unit}`}
      </Working>
    </div>
  );
}

// ══ Angle maker ══════════════════════════════════════════════════════════════

function angleKind(d: number): string {
  if (d === 0) return 'a zero angle';
  if (d < 90) return 'an acute angle (less than 90°)';
  if (d === 90) return 'a right angle (exactly 90°)';
  if (d < 180) return 'an obtuse angle (between 90° and 180°)';
  if (d === 180) return 'a straight angle (exactly 180°)';
  if (d < 360) return 'a reflex angle (more than 180°)';
  return 'a complete turn (360°)';
}

export function AngleVisual({ spec }: { spec: Of<'angle'> }) {
  const [deg, setDeg] = useState(spec.degrees);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const dragging = useRef(false);
  const cx = 150;
  const cy = 130;
  const arm = 110;
  const rad = (deg * Math.PI) / 180;
  const ex = cx + arm * Math.cos(rad);
  const ey = cy - arm * Math.sin(rad);
  const ar = 36;

  function turnTo(clientX: number, clientY: number) {
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    if (rect.width === 0) return;
    const x = ((clientX - rect.left) / rect.width) * 300 - cx;
    const y = cy - ((clientY - rect.top) / rect.height) * 250;
    let d = Math.round((Math.atan2(y, x) * 180) / Math.PI);
    if (d < 0) d += 360;
    // Snap to the nearest 5° so tidy angles are easy to land on.
    setDeg(Math.round(d / 5) * 5);
  }

  return (
    <div className="space-y-2">
      <svg
        ref={svgRef}
        viewBox="0 0 300 250"
        className="w-full h-auto select-none"
        style={{ touchAction: 'none', cursor: 'pointer' }}
        role="img"
        aria-label={`Angle of ${deg} degrees`}
        onPointerDown={(e) => { dragging.current = true; e.currentTarget.setPointerCapture(e.pointerId); turnTo(e.clientX, e.clientY); }}
        onPointerMove={(e) => { if (dragging.current) turnTo(e.clientX, e.clientY); }}
        onPointerUp={() => { dragging.current = false; }}
        onPointerCancel={() => { dragging.current = false; }}
      >
        {/* Angle arc */}
        {deg >= 360 ? (
          <circle cx={cx} cy={cy} r={ar} fill={C.actionSoft} stroke={C.action} strokeWidth={2.5} />
        ) : deg > 0 ? (
          <path
            d={`M ${cx} ${cy} L ${cx + ar} ${cy} A ${ar} ${ar} 0 ${deg > 180 ? 1 : 0} 0 ${cx + ar * Math.cos(rad)} ${cy - ar * Math.sin(rad)} Z`}
            fill={C.actionSoft} stroke={C.action} strokeWidth={2.5} strokeLinejoin="round"
          />
        ) : null}
        {/* Fixed arm and turning arm */}
        <line x1={cx} y1={cy} x2={cx + arm} y2={cy} stroke={C.ink} strokeWidth={4} strokeLinecap="round" />
        <line x1={cx} y1={cy} x2={ex} y2={ey} stroke={C.ink} strokeWidth={4} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={6} fill={C.ink} />
        <circle cx={ex} cy={ey} r={12} fill={C.action} stroke={C.ink} strokeWidth={2.5} />
        <text x={cx} y={cy + 34} textAnchor="middle" fontSize={22} fontWeight={800} fill={C.ink}>{deg}°</text>
      </svg>
      <Slider label="Turn the arm" value={deg} min={0} max={360} step={5} onChange={setDeg} display={`${deg}°`} />
      <Working>{deg}° is {angleKind(deg)}</Working>
    </div>
  );
}

// ══ Hundred grid ═════════════════════════════════════════════════════════════

export function PercentGridVisual({ spec }: { spec: Of<'percentGrid'> }) {
  const [p, setP] = useState(spec.percent);
  const g = gcd(p, 100);
  const cell = 24;

  return (
    <div className="space-y-3">
      <div className="flex justify-center">
        <svg viewBox={`0 0 ${cell * 10 + 4} ${cell * 10 + 4}`} className="w-full max-w-[260px] h-auto" role="img"
          aria-label={`${p} squares out of 100 shaded`}>
          {range(100).map((i) => (
            <rect
              key={i}
              x={2 + (i % 10) * cell}
              y={2 + Math.floor(i / 10) * cell}
              width={cell}
              height={cell}
              fill={i < p ? C.action : C.card}
              stroke={C.line}
              strokeWidth={1}
              onClick={() => setP(i + 1 === p ? i : i + 1)}
              style={{ cursor: 'pointer' }}
            />
          ))}
          <rect x={2} y={2} width={cell * 10} height={cell * 10} fill="none" stroke={C.ink} strokeWidth={2.5} />
        </svg>
      </div>
      <Slider label="Shaded squares" value={p} min={0} max={100} onChange={setP} display={`${p} of 100`} />
      <div className="flex flex-wrap gap-2">
        <Stat label="Percent" value={`${p}%`} />
        <Stat label="Fraction" value={p === 0 ? '0' : `${p / g}/${100 / g}`} />
        <Stat label="Decimal" value={(p / 100).toFixed(2)} />
      </div>
    </div>
  );
}

// ══ Measuring jar ════════════════════════════════════════════════════════════

export function ContainerVisual({ spec }: { spec: Of<'container'> }) {
  const sliderStep = spec.capacity / 20;
  const [filled, setFilled] = useState(spec.filled);
  const unit = spec.unit ?? '';
  const ratio = Math.min(1, Math.max(0, filled / spec.capacity));
  const jarH = 180;
  const jarW = 110;
  const level = jarH * ratio;
  const show = (v: number) => `${fmt(v)}${unit ? ` ${unit}` : ''}`;

  return (
    <div className="space-y-3">
      <div className="flex justify-center">
        <svg viewBox={`0 0 ${jarW + 90} ${jarH + 24}`} className="w-full max-w-[260px] h-auto" role="img"
          aria-label={`Jar holding ${show(filled)} of ${show(spec.capacity)}`}>
          <g transform="translate(14 12)">
            <rect x={0} y={jarH - level} width={jarW} height={level} fill={C.actionSoft} />
            {level > 0 && <line x1={0} y1={jarH - level} x2={jarW} y2={jarH - level} stroke={C.action} strokeWidth={3} />}
            <path d={`M 0 0 L 0 ${jarH} L ${jarW} ${jarH} L ${jarW} 0`} fill="none" stroke={C.ink} strokeWidth={3} strokeLinejoin="round" strokeLinecap="round" />
            {[0, 0.25, 0.5, 0.75, 1].map((t) => (
              <g key={t}>
                <line x1={jarW} y1={jarH - jarH * t} x2={jarW + 10} y2={jarH - jarH * t} stroke={C.ink} strokeWidth={2} />
                <text x={jarW + 16} y={jarH - jarH * t + 4} fontSize={12} fontWeight={800} fill={C.ink}>{fmt(spec.capacity * t)}</text>
              </g>
            ))}
          </g>
        </svg>
      </div>
      <Slider label="Fill the jar" value={filled} min={0} max={spec.capacity} step={sliderStep} onChange={setFilled} display={show(filled)} />
      <div className="flex flex-wrap gap-2">
        <Stat label="Filled" value={show(filled)} />
        <Stat label="Space left" value={show(spec.capacity - filled)} />
        <Stat label="How full" value={`${Math.round(ratio * 100)}%`} />
      </div>
    </div>
  );
}

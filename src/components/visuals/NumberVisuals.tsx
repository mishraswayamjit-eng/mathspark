'use client';

import React, { useRef, useState } from 'react';
import type { VisualSpec, BarModelBar } from '@/lib/visuals/spec';
import { C, range, fmt, Working, Stepper, Slider } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

// ══ Fractions ════════════════════════════════════════════════════════════════

function startCells(parts: number, shaded: number): boolean[] {
  return range(parts).map((i) => i < shaded);
}

function FractionShape({ shape, cells, onToggle, fill, name }: {
  shape: 'bar' | 'circle'; cells: boolean[]; onToggle: (i: number) => void; fill: string; name: string;
}) {
  const n = cells.length;

  if (shape === 'circle') {
    const cx = 80;
    const cy = 80;
    const r = 70;
    return (
      <svg viewBox="0 0 160 160" className="w-40 h-40 mx-auto select-none" role="group" aria-label={name}>
        {n === 1 ? (
          <circle cx={cx} cy={cy} r={r} fill={cells[0] ? fill : C.card} stroke={C.ink} strokeWidth={2.5}
            onClick={() => onToggle(0)} style={{ cursor: 'pointer' }} />
        ) : cells.map((on, i) => {
          const a0 = (2 * Math.PI * i) / n - Math.PI / 2;
          const a1 = (2 * Math.PI * (i + 1)) / n - Math.PI / 2;
          const d = `M ${cx} ${cy} L ${cx + r * Math.cos(a0)} ${cy + r * Math.sin(a0)} A ${r} ${r} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${cx + r * Math.cos(a1)} ${cy + r * Math.sin(a1)} Z`;
          return (
            <path key={i} d={d} fill={on ? fill : C.card} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round"
              onClick={() => onToggle(i)} style={{ cursor: 'pointer' }} />
          );
        })}
      </svg>
    );
  }

  return (
    <div className="flex w-full h-14 rounded-note border-2 border-ink overflow-hidden" role="group" aria-label={name}>
      {cells.map((on, i) => (
        <button
          key={i}
          type="button"
          onClick={() => onToggle(i)}
          aria-pressed={on}
          aria-label={`Part ${i + 1} of ${n}`}
          className="flex-1 min-h-0 border-r-2 border-ink last:border-r-0 transition-colors"
          style={{ backgroundColor: on ? fill : C.card }}
        />
      ))}
    </div>
  );
}

export function FractionVisual({ spec }: { spec: Of<'fraction'> }) {
  const [a, setA] = useState<boolean[]>(() => startCells(spec.parts, spec.shaded));
  const [b, setB] = useState<boolean[] | null>(() => (spec.compare ? startCells(spec.compare.parts, spec.compare.shaded) : null));

  const toggle = (cells: boolean[], i: number) => cells.map((on, k) => (k === i ? !on : on));
  const count = (cells: boolean[]) => cells.filter(Boolean).length;

  const aN = count(a);
  const aD = a.length;
  let verdict = `${aN} of the ${aD} equal parts are shaded: ${aN}/${aD}`;
  if (b) {
    const bN = count(b);
    const bD = b.length;
    // Compare by cross-multiplying, so no rounding is involved.
    const left = aN * bD;
    const right = bN * aD;
    verdict = left === right
      ? `${aN}/${aD} and ${bN}/${bD} are equal`
      : left > right
        ? `${aN}/${aD} is bigger than ${bN}/${bD}`
        : `${aN}/${aD} is smaller than ${bN}/${bD}`;
  }

  return (
    <div className="space-y-3">
      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="flex-1"><FractionShape shape={spec.shape} cells={a} onToggle={(i) => setA(toggle(a, i))} fill={C.action} name="First fraction" /></div>
          <span className="font-display text-heading text-ink w-14 text-center">{aN}/{aD}</span>
        </div>
        {b && (
          <div className="flex items-center gap-3">
            <div className="flex-1"><FractionShape shape={spec.shape} cells={b} onToggle={(i) => setB(toggle(b, i))} fill={C.star} name="Second fraction" /></div>
            <span className="font-display text-heading text-ink w-14 text-center">{count(b)}/{b.length}</span>
          </div>
        )}
      </div>
      <Working>{verdict}</Working>
      <p className="text-caption text-ink-muted text-center">Tap a part to shade it or clear it</p>
    </div>
  );
}

// ══ Number line ══════════════════════════════════════════════════════════════

const NL_W = 340;
const NL_PAD = 22;
const NL_Y = 62;

export function NumberLineVisual({ spec }: { spec: Of<'numberLine'> }) {
  const steps = Math.max(1, Math.round((spec.max - spec.min) / spec.step));
  const stepText = String(spec.step);
  const decimals = stepText.indexOf('.') === -1 ? 0 : stepText.length - stepText.indexOf('.') - 1;
  const labelEvery = Math.max(1, Math.ceil(steps / 10));
  const toPos = (v: number) => Math.min(steps, Math.max(0, Math.round((v - spec.min) / spec.step)));
  const valueAt = (p: number) => Number((spec.min + p * spec.step).toFixed(decimals));
  const xAt = (p: number) => NL_PAD + (p / steps) * (NL_W - NL_PAD * 2);

  const [pos, setPos] = useState<number>(() => toPos(spec.point !== undefined ? spec.point : spec.jumpTo !== undefined ? spec.jumpTo : spec.min));
  const svgRef = useRef<SVGSVGElement | null>(null);
  const dragging = useRef(false);

  function moveTo(clientX: number) {
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    if (rect.width === 0) return;
    const viewX = ((clientX - rect.left) / rect.width) * NL_W;
    setPos(Math.min(steps, Math.max(0, Math.round(((viewX - NL_PAD) / (NL_W - NL_PAD * 2)) * steps))));
  }

  const hasJump = spec.jumpFrom !== undefined && spec.jumpTo !== undefined && spec.jumpFrom !== spec.jumpTo;
  const jf = hasJump ? toPos(spec.jumpFrom as number) : 0;
  const jt = hasJump ? toPos(spec.jumpTo as number) : 0;
  const jumpSize = hasJump ? Number(((spec.jumpTo as number) - (spec.jumpFrom as number)).toFixed(decimals)) : 0;

  return (
    <div className="space-y-2">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${NL_W} 104`}
        className="w-full h-auto select-none"
        style={{ touchAction: 'none', cursor: 'pointer' }}
        role="img"
        aria-label={`Number line from ${spec.min} to ${spec.max}`}
        onPointerDown={(e) => { dragging.current = true; e.currentTarget.setPointerCapture(e.pointerId); moveTo(e.clientX); }}
        onPointerMove={(e) => { if (dragging.current) moveTo(e.clientX); }}
        onPointerUp={() => { dragging.current = false; }}
        onPointerCancel={() => { dragging.current = false; }}
      >
        {/* Hop */}
        {hasJump && (
          <g>
            <path
              d={`M ${xAt(jf)} ${NL_Y - 6} Q ${(xAt(jf) + xAt(jt)) / 2} ${NL_Y - 58} ${xAt(jt)} ${NL_Y - 6}`}
              fill="none" stroke={C.star} strokeWidth={3} strokeLinecap="round" strokeDasharray="6 5"
            />
            <text x={(xAt(jf) + xAt(jt)) / 2} y={NL_Y - 38} textAnchor="middle" fontSize={14} fontWeight={800} fill={C.ink}>
              {jumpSize > 0 ? `+${jumpSize}` : `−${Math.abs(jumpSize)}`}
            </text>
          </g>
        )}

        <line x1={NL_PAD} y1={NL_Y} x2={NL_W - NL_PAD} y2={NL_Y} stroke={C.ink} strokeWidth={3} strokeLinecap="round" />
        {range(steps + 1).map((p) => {
          const major = p % labelEvery === 0 || p === steps;
          return (
            <g key={p}>
              <line x1={xAt(p)} y1={NL_Y - (major ? 9 : 5)} x2={xAt(p)} y2={NL_Y + (major ? 9 : 5)} stroke={major ? C.ink : C.muted} strokeWidth={major ? 2 : 1.5} />
              {major && (
                <text x={xAt(p)} y={NL_Y + 28} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.ink}>{valueAt(p)}</text>
              )}
            </g>
          );
        })}
        <circle cx={xAt(pos)} cy={NL_Y} r={11} fill={C.action} stroke={C.ink} strokeWidth={2.5} />
      </svg>
      <Working>The point is at {valueAt(pos)}</Working>
      <p className="text-caption text-ink-muted text-center">Drag the point along the line</p>
    </div>
  );
}

// ══ Place-value blocks ═══════════════════════════════════════════════════════

const PLACES = [
  { name: 'thousands', worth: 1000, box: 'w-9 h-9', tone: 'bg-action' },
  { name: 'hundreds',  worth: 100,  box: 'w-7 h-7', tone: 'bg-star' },
  { name: 'tens',      worth: 10,   box: 'w-2.5 h-7', tone: 'bg-success' },
  { name: 'ones',      worth: 1,    box: 'w-2.5 h-2.5', tone: 'bg-ink' },
];

export function PlaceValueVisual({ spec }: { spec: Of<'placeValue'> }) {
  const [digits, setDigits] = useState<number[]>(() => [
    Math.floor(spec.number / 1000) % 10,
    Math.floor(spec.number / 100) % 10,
    Math.floor(spec.number / 10) % 10,
    spec.number % 10,
  ]);

  const total = digits[0] * 1000 + digits[1] * 100 + digits[2] * 10 + digits[3];
  const expanded = PLACES
    .map((p, i) => digits[i] * p.worth)
    .filter((v) => v > 0)
    .map((v) => fmt(v))
    .join(' + ');

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-4 gap-2">
        {PLACES.map((p, i) => (
          <div key={p.name} className="bg-soft border-2 border-line rounded-tile p-2 min-h-[112px]">
            <p className="text-caption text-ink-muted text-center capitalize">{p.name}</p>
            <div className="flex flex-wrap gap-1 justify-center mt-2">
              {range(digits[i]).map((k) => (
                <span key={k} className={`${p.box} ${p.tone} rounded-[3px] border border-ink`} aria-hidden="true" />
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-2 gap-x-4 gap-y-2">
        {PLACES.map((p, i) => (
          <Stepper
            key={p.name}
            label={p.name}
            value={digits[i]}
            min={0}
            max={9}
            onChange={(v) => setDigits(digits.map((d, k) => (k === i ? v : d)))}
          />
        ))}
      </div>
      <Working>{expanded ? `${expanded} = ${fmt(total)}` : '0'}</Working>
    </div>
  );
}

// ══ Dot array ════════════════════════════════════════════════════════════════

export function ArrayVisual({ spec }: { spec: Of<'array'> }) {
  const [rows, setRows] = useState(spec.rows);
  const [cols, setCols] = useState(spec.cols);
  const cell = Math.min(26, Math.floor(312 / Math.max(rows, cols)));
  const total = rows * cols;

  return (
    <div className="space-y-3">
      <div className="flex justify-center">
        <svg
          width={cols * cell + 8}
          height={rows * cell + 8}
          viewBox={`0 0 ${cols * cell + 8} ${rows * cell + 8}`}
          className="max-w-full h-auto"
          role="img"
          aria-label={`${rows} rows of ${cols} dots`}
        >
          <rect x={1} y={1} width={cols * cell + 6} height={rows * cell + 6} rx={10} fill={C.soft} stroke={C.line} strokeWidth={2} />
          {range(rows).map((r) => range(cols).map((c) => (
            <circle key={`${r}-${c}`} cx={4 + c * cell + cell / 2} cy={4 + r * cell + cell / 2} r={cell * 0.34}
              fill={r === 0 || c === 0 ? C.action : C.actionSoft} stroke={C.ink} strokeWidth={1.5} />
          )))}
        </svg>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <Slider label="Rows" value={rows} min={1} max={12} onChange={setRows} />
        <Slider label="In each row" value={cols} min={1} max={12} onChange={setCols} />
      </div>
      <Working>
        {rows} rows of {cols} = {rows} × {cols} = {total}
        {rows === cols && rows > 1 ? ` (a square number: ${rows}²)` : ''}
      </Working>
    </div>
  );
}

// ══ Bar model ════════════════════════════════════════════════════════════════

function barTotal(bar: BarModelBar): number {
  let sum = 0;
  for (let i = 0; i < bar.segments.length; i++) sum += bar.segments[i].value;
  return sum;
}

/** Width weight of a piece: unknown pieces take the average size of the known ones. */
function weightOf(bar: BarModelBar, index: number): number {
  const seg = bar.segments[index];
  if (seg.value > 0) return seg.value;
  const known = bar.segments.filter((s) => s.value > 0);
  return known.length > 0 ? barTotal(bar) / known.length : 1;
}

const PIECE_TONES = ['bg-action text-white', 'bg-star text-ink', 'bg-success text-white'];

export function BarModelVisual({ spec }: { spec: Of<'barModel'> }) {
  const [picked, setPicked] = useState<string | null>(null);
  const unit = spec.unit ?? '';
  const withUnit = (v: number) => (unit === '₹' || unit === '$' ? `${unit}${fmt(v)}` : `${fmt(v)}${unit ? ` ${unit}` : ''}`);

  const weights = spec.bars.map((bar) => {
    let sum = 0;
    for (let i = 0; i < bar.segments.length; i++) sum += weightOf(bar, i);
    return sum;
  });
  const widest = Math.max.apply(null, weights);

  let pickedText = 'Tap a piece to see what it stands for';
  if (picked) {
    const [b, s] = picked.split('-').map(Number);
    const seg = spec.bars[b] && spec.bars[b].segments[s];
    if (seg) {
      pickedText = seg.unknown
        ? `${seg.label && seg.label !== '?' ? `${seg.label}: ` : ''}this is the piece we are finding`
        : `${seg.label ? `${seg.label}: ` : ''}${withUnit(seg.value)}`;
    }
  }

  return (
    <div className="space-y-3">
      {spec.bars.map((bar, b) => {
        const hasUnknown = bar.segments.some((s) => s.unknown);
        return (
          <div key={b}>
            <div className="flex items-baseline justify-between mb-1">
              <span className="text-label text-ink">{bar.label ?? ''}</span>
              {!hasUnknown && <span className="text-caption text-ink-muted">Total {withUnit(barTotal(bar))}</span>}
            </div>
            <div className="flex h-14 rounded-note border-2 border-ink overflow-hidden" style={{ width: `${Math.max(20, (weights[b] / widest) * 100)}%` }}>
              {bar.segments.map((seg, s) => {
                const id = `${b}-${s}`;
                const tone = seg.unknown ? 'bg-hint text-hint-ink' : PIECE_TONES[b % PIECE_TONES.length];
                return (
                  <button
                    key={s}
                    type="button"
                    onClick={() => setPicked(picked === id ? null : id)}
                    aria-pressed={picked === id}
                    className={`min-w-0 min-h-0 border-r-2 border-ink last:border-r-0 px-1 text-[13px] font-extrabold truncate transition-opacity ${tone} ${
                      picked && picked !== id ? 'opacity-50' : ''
                    }`}
                    style={{ flexGrow: weightOf(bar, s), flexBasis: 0 }}
                  >
                    {seg.unknown ? '?' : fmt(seg.value)}
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
      <Working>{pickedText}</Working>
    </div>
  );
}

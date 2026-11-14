'use client';

import React, { useState } from 'react';
import type { VisualSpec } from '@/lib/visuals/spec';
import { C, range, gcd, fmt, Stat, Working, Stepper, Slider, Toggle } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

function primeFactors(n: number): number[] {
  const out: number[] = [];
  let left = n;
  for (let p = 2; p * p <= left; p++) {
    while (left % p === 0) {
      out.push(p);
      left /= p;
    }
  }
  if (left > 1) out.push(left);
  return out;
}

function isPrime(n: number): boolean {
  return n > 1 && primeFactors(n).length === 1;
}

// ══ Mixed numbers ════════════════════════════════════════════════════════════

export function MixedNumberVisual({ spec }: { spec: Of<'mixedNumber'> }) {
  const [whole, setWhole] = useState(spec.whole);
  const [d, setD] = useState(spec.denominator);
  const [n, setN] = useState(Math.min(spec.numerator, spec.denominator - 1));
  const top = Math.min(n, d - 1);
  const improper = whole * d + top;

  const bar = (filled: number, key: string) => (
    <div key={key} className="flex h-11 rounded-note border-2 border-ink overflow-hidden">
      {range(d).map((i) => (
        <span key={i} className={`flex-1 ${i > 0 ? 'border-l-2 border-ink' : ''} ${i < filled ? 'bg-action' : 'bg-white'}`} />
      ))}
    </div>
  );

  return (
    <div className="space-y-3">
      <div className="space-y-1.5" role="img" aria-label={`${whole} wholes and ${top} out of ${d}`}>
        {range(whole).map((i) => bar(d, `whole${i}`))}
        {top > 0 && bar(top, 'part')}
        {whole === 0 && top === 0 && <p className="text-label text-ink-muted text-center py-3">Nothing yet. Add a whole or a part.</p>}
      </div>
      <Stepper label="wholes" value={whole} min={0} max={5} onChange={setWhole} />
      <Stepper label={`extra parts (out of ${d})`} value={top} min={0} max={d - 1} onChange={setN} />
      <Stepper label="parts in one whole" value={d} min={2} max={12} onChange={setD} />
      <div className="flex gap-2">
        <Stat label="Mixed number" value={`${whole > 0 ? `${whole} ` : ''}${top > 0 || whole === 0 ? `${top}/${d}` : ''}`} />
        <Stat label="Improper fraction" value={`${improper}/${d}`} />
      </div>
      <Working>
        {whole} whole{whole === 1 ? '' : 's'} = {whole} × {d} = {whole * d} parts. With {top} more: {whole * d} + {top} = {improper} parts, so {improper}/{d}.
      </Working>
    </div>
  );
}

// ══ Fraction of a set ════════════════════════════════════════════════════════

export function FractionSetVisual({ spec }: { spec: Of<'fractionSet'> }) {
  const d = spec.denominator;
  const [n, setN] = useState(spec.numerator);
  const each = spec.total / d;
  const item = spec.item ?? 'counters';

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2 justify-center" role="img" aria-label={`${spec.total} ${item} in ${d} equal groups, ${n} groups coloured`}>
        {range(d).map((g) => (
          <button
            key={g}
            type="button"
            onClick={() => setN(g + 1 === n ? g : g + 1)}
            aria-label={`Take ${g + 1} group${g === 0 ? '' : 's'}`}
            className={`min-h-[48px] min-w-[48px] p-2 rounded-tile border-2 grid gap-1 ${g < n ? 'border-ink bg-soft' : 'border-line bg-white'}`}
            style={{ gridTemplateColumns: `repeat(${Math.min(each, 3)}, 12px)` }}
          >
            {range(each).map((i) => (
              <span key={i} className={`w-3 h-3 rounded-full border-2 border-ink ${g < n ? 'bg-action' : 'bg-white'}`} />
            ))}
          </button>
        ))}
      </div>
      <Stepper label={`groups taken (out of ${d})`} value={n} min={0} max={d} onChange={setN} />
      <div className="flex gap-2">
        <Stat label="In each group" value={each} />
        <Stat label={`${n}/${d} of ${spec.total}`} value={n * each} />
      </div>
      <Working>
        {spec.total} {item} shared into {d} equal groups: {spec.total} ÷ {d} = {each} in each. {n} group{n === 1 ? '' : 's'}: {n} × {each} = {n * each}.
      </Working>
    </div>
  );
}

// ══ Factor tree ══════════════════════════════════════════════════════════════

export function FactorTreeVisual({ spec }: { spec: Of<'factorTree'> }) {
  const [num, setNum] = useState(spec.number);
  const primes = primeFactors(num);
  const levels = primes.length - 1;            // number of splits
  const stepX = 34;
  const stepY = 44;
  const width = Math.max(300, 120 + levels * stepX * 2);
  const height = 50 + Math.max(1, levels) * stepY + 20;

  const nodes: React.ReactNode[] = [];
  let x = 70 + levels * stepX * 0.2;
  let y = 28;
  let value = num;
  for (let i = 0; i < levels; i++) {
    const p = primes[i];
    const rest = value / p;
    const lx = x - stepX;
    const rx = x + stepX;
    const ny = y + stepY;
    nodes.push(
      <g key={i}>
        <line x1={x} y1={y + 10} x2={lx} y2={ny - 14} stroke={C.ink} strokeWidth={2} />
        <line x1={x} y1={y + 10} x2={rx} y2={ny - 14} stroke={C.ink} strokeWidth={2} />
        <text x={x} y={y + 5} textAnchor="middle" fontSize={15} fontWeight={800} fill={C.ink}>{value}</text>
        <circle cx={lx} cy={ny} r={14} fill={C.star} stroke={C.ink} strokeWidth={2} />
        <text x={lx} y={ny + 5} textAnchor="middle" fontSize={14} fontWeight={800} fill={C.ink}>{p}</text>
      </g>,
    );
    x = rx;
    y = ny;
    value = rest;
  }

  return (
    <div className="space-y-3">
      <div className="overflow-x-auto">
        <svg viewBox={`0 0 ${width} ${height}`} width={width} height={height} className="mx-auto max-w-none" role="img" aria-label={`Factor tree of ${num}`}>
          {nodes}
          {/* The last number left is prime too. */}
          <circle cx={x} cy={y} r={14} fill={levels === 0 ? C.card : C.star} stroke={C.ink} strokeWidth={2} />
          <text x={x} y={y + 5} textAnchor="middle" fontSize={14} fontWeight={800} fill={C.ink}>{value}</text>
        </svg>
      </div>
      <Slider label="Number" value={num} min={2} max={200} onChange={setNum} />
      <Working>
        {levels === 0
          ? `${num} is a prime number: its only factors are 1 and ${num}.`
          : `${num} = ${primes.join(' × ')}. The circled numbers are its prime factors.`}
      </Working>
    </div>
  );
}

// ══ Venn diagram of factors (HCF and LCM) ════════════════════════════════════

function factorsOf(n: number): number[] {
  const out: number[] = [];
  for (let i = 1; i <= n; i++) if (n % i === 0) out.push(i);
  return out;
}

function VennList({ items, x, y }: { items: number[]; x: number; y: number }) {
  const rows: number[][] = [];
  for (let i = 0; i < items.length; i += 3) rows.push(items.slice(i, i + 3));
  return (
    <>
      {rows.map((row, r) => (
        <text key={r} x={x} y={y + (r - (rows.length - 1) / 2) * 16 + 4} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.ink}>
          {row.join('  ')}
        </text>
      ))}
    </>
  );
}

export function VennVisual({ spec }: { spec: Of<'venn'> }) {
  const [mode, setMode] = useState<'factors' | 'primes'>(spec.mode);
  const a = spec.a;
  const b = spec.b;
  let left: number[] = [];
  let both: number[] = [];
  let right: number[] = [];

  if (mode === 'factors') {
    const fb = factorsOf(b);
    const fa = factorsOf(a);
    left = fa.filter((v) => fb.indexOf(v) === -1);
    both = fa.filter((v) => fb.indexOf(v) !== -1);
    right = fb.filter((v) => fa.indexOf(v) === -1);
  } else {
    // Prime factors with repeats: a shared prime is used once from each number.
    const pb = primeFactors(b);
    const pa = primeFactors(a);
    for (let i = 0; i < pa.length; i++) {
      const at = pb.indexOf(pa[i]);
      if (at !== -1) {
        both.push(pa[i]);
        pb.splice(at, 1);
      } else {
        left.push(pa[i]);
      }
    }
    right = pb;
  }

  const hcf = gcd(a, b);
  const lcm = (a * b) / hcf;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 200" className="w-full h-auto" role="img" aria-label={`Venn diagram for ${a} and ${b}`}>
        <circle cx={112} cy={108} r={84} fill={C.action} fillOpacity={0.16} stroke={C.ink} strokeWidth={2.5} />
        <circle cx={188} cy={108} r={84} fill={C.star} fillOpacity={0.28} stroke={C.ink} strokeWidth={2.5} />
        <text x={70} y={18} textAnchor="middle" fontSize={14} fontWeight={800} fill={C.ink}>{a}</text>
        <text x={230} y={18} textAnchor="middle" fontSize={14} fontWeight={800} fill={C.ink}>{b}</text>
        <VennList items={left} x={66} y={108} />
        <VennList items={both} x={150} y={108} />
        <VennList items={right} x={234} y={108} />
      </svg>
      <Toggle
        options={[{ value: 'factors', label: 'All factors' }, { value: 'primes', label: 'Prime factors' }]}
        value={mode}
        onChange={setMode}
      />
      <div className="flex gap-2">
        <Stat label="HCF" value={hcf} />
        <Stat label="LCM" value={fmt(lcm)} />
      </div>
      <Working>
        {mode === 'factors'
          ? `The middle holds the factors both numbers share. The biggest of them is the HCF: ${hcf}.`
          : `HCF = the middle multiplied together = ${both.length ? both.join(' × ') : '1 (nothing shared)'} = ${hcf}. LCM = everything in the picture multiplied together = ${left.concat(both, right).join(' × ')} = ${fmt(lcm)}.`}
      </Working>
    </div>
  );
}

// ══ Hundred chart ════════════════════════════════════════════════════════════

export function HundredChartVisual({ spec }: { spec: Of<'hundredChart'> }) {
  const [mark, setMark] = useState<'multiples' | 'primes' | 'squares'>(spec.mark);
  const [of, setOf] = useState(spec.of);
  const hit = (v: number): boolean => {
    if (mark === 'multiples') return v % of === 0;
    if (mark === 'primes') return isPrime(v);
    const r = Math.round(Math.sqrt(v));
    return r * r === v;
  };
  let count = 0;
  for (let v = 1; v <= 100; v++) if (hit(v)) count += 1;

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-10 gap-0.5" role="img" aria-label={`Numbers 1 to 100 with ${mark} marked`}>
        {range(100).map((i) => {
          const v = i + 1;
          return (
            <span
              key={v}
              className={`aspect-square flex items-center justify-center rounded-[5px] border text-[11px] font-extrabold ${hit(v) ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink'}`}
            >
              {v}
            </span>
          );
        })}
      </div>
      <Toggle
        options={[{ value: 'multiples', label: 'Multiples' }, { value: 'primes', label: 'Primes' }, { value: 'squares', label: 'Squares' }]}
        value={mark}
        onChange={setMark}
      />
      {mark === 'multiples' && <Stepper label="multiples of" value={of} min={2} max={12} onChange={setOf} />}
      <Working>
        {mark === 'multiples'
          ? `There are ${count} multiples of ${of} up to 100. Look at the pattern they make down the chart.`
          : mark === 'primes'
            ? `There are ${count} prime numbers up to 100. 2 is the only even one.`
            : `There are ${count} square numbers up to 100: 1 × 1, 2 × 2, 3 × 3, … 10 × 10.`}
      </Working>
    </div>
  );
}

// ══ Place-value chart (Indian system) ════════════════════════════════════════

const WHOLE_PLACES = ['Ones', 'Tens', 'Hundreds', 'Thousands', 'Ten thousands', 'Lakhs', 'Ten lakhs', 'Crores', 'Ten crores'];
const WHOLE_SHORT = ['O', 'T', 'H', 'Th', 'TTh', 'L', 'TL', 'C', 'TC'];
const PART_PLACES = ['Tenths', 'Hundredths', 'Thousandths'];
const PART_SHORT = ['t', 'h', 'th'];

export function PlaceChartVisual({ spec }: { spec: Of<'placeChart'> }) {
  // Work in thousandths so the digits are exact.
  const thousandths = Math.round(spec.number * 1000);
  const wholeDigits = String(Math.floor(thousandths / 1000)).split('');
  let partDigits = String(thousandths % 1000 + 1000).slice(1).split('');
  while (partDigits.length > 0 && partDigits[partDigits.length - 1] === '0') partDigits = partDigits.slice(0, -1);

  interface Col { digit: string; name: string; short: string; value: number; group: string }
  const cols: Col[] = [];
  for (let i = 0; i < wholeDigits.length; i++) {
    const place = wholeDigits.length - 1 - i;
    cols.push({
      digit: wholeDigits[i], name: WHOLE_PLACES[place], short: WHOLE_SHORT[place],
      value: Number(wholeDigits[i]) * Math.pow(10, place),
      group: place >= 7 ? 'Crores' : place >= 5 ? 'Lakhs' : place >= 3 ? 'Thousands' : 'Ones',
    });
  }
  for (let i = 0; i < partDigits.length; i++) {
    cols.push({ digit: partDigits[i], name: PART_PLACES[i], short: PART_SHORT[i], value: Number(partDigits[i]) / Math.pow(10, i + 1), group: 'Decimal' });
  }
  const [pick, setPick] = useState(0);
  const chosen = cols[Math.min(pick, cols.length - 1)];
  const shown = `${fmt(Math.floor(thousandths / 1000))}${partDigits.length ? `.${partDigits.join('')}` : ''}`;

  return (
    <div className="space-y-3">
      <p className="font-display text-display text-ink text-center">{shown}</p>
      <div className="flex justify-center overflow-x-auto" role="group" aria-label="Place-value chart">
        {cols.map((c, i) => (
          <React.Fragment key={i}>
            {c.group === 'Decimal' && cols[i - 1] && cols[i - 1].group !== 'Decimal' && (
              <span className="self-end pb-3 px-0.5 font-display text-heading text-ink" aria-hidden="true">.</span>
            )}
            <button
              type="button"
              onClick={() => setPick(i)}
              aria-pressed={chosen === c}
              aria-label={`${c.digit} in the ${c.name.toLowerCase()} place`}
              className={`min-w-[38px] flex-1 max-w-[52px] border-2 -ml-0.5 first:ml-0 flex flex-col items-center ${chosen === c ? 'bg-action border-ink text-white z-10' : `border-line text-ink ${c.group === 'Lakhs' || c.group === 'Ones' ? 'bg-soft' : 'bg-white'}`}`}
            >
              <span className="text-[11px] font-extrabold py-1">{c.short}</span>
              <span className="font-display text-heading pb-2 min-h-[36px]">{c.digit}</span>
            </button>
          </React.Fragment>
        ))}
      </div>
      <p className="text-caption text-ink-muted text-center">Tap a digit. Periods: crores, lakhs, thousands, ones.</p>
      <Working>
        The {chosen.digit} is in the {chosen.name.toLowerCase()} place. Its value is {chosen.group === 'Decimal' ? chosen.value : fmt(chosen.value)}.
      </Working>
    </div>
  );
}

// ══ Square and triangular numbers ════════════════════════════════════════════

export function FigurateVisual({ spec }: { spec: Of<'figurate'> }) {
  const [kind, setKind] = useState<'square' | 'triangular'>(spec.kind);
  const [n, setN] = useState(spec.n);
  const gap = Math.min(24, 200 / n);
  const r = gap * 0.36;
  const dots: React.ReactNode[] = [];
  for (let row = 0; row < n; row++) {
    const inRow = kind === 'square' ? n : row + 1;
    for (let col = 0; col < inRow; col++) {
      // The newest layer: the last row and column of a square, the last row of a triangle.
      const fresh = kind === 'square' ? row === n - 1 || col === n - 1 : row === n - 1;
      const x = kind === 'square' ? 150 - ((n - 1) * gap) / 2 + col * gap : 150 - (row * gap) / 2 + col * gap;
      dots.push(<circle key={`${row}-${col}`} cx={x} cy={20 + row * gap} r={r} fill={fresh ? C.star : C.action} stroke={C.ink} strokeWidth={1.5} />);
    }
  }
  const total = kind === 'square' ? n * n : (n * (n + 1)) / 2;

  return (
    <div className="space-y-3">
      <svg viewBox={`0 0 300 ${40 + (n - 1) * gap}`} className="w-full max-w-[320px] mx-auto h-auto" role="img" aria-label={`${total} dots in a ${kind === 'square' ? 'square' : 'triangle'}`}>
        {dots}
      </svg>
      <Toggle options={[{ value: 'square', label: 'Square numbers' }, { value: 'triangular', label: 'Triangular numbers' }]} value={kind} onChange={setKind} />
      <Stepper label={kind === 'square' ? 'dots along a side' : 'rows'} value={n} min={1} max={10} onChange={setN} />
      <Working>
        {kind === 'square'
          ? `${n} × ${n} = ${total}, so ${total} is a square number and √${total} = ${n}. The gold dots are the newest layer: ${2 * n - 1} of them, the next odd number.`
          : `1 + 2 + … + ${n} = ${n} × ${n + 1} ÷ 2 = ${total}. The gold row is the newest: ${n} more.`}
      </Working>
    </div>
  );
}

// ══ Area model for multiplication ════════════════════════════════════════════

export function AreaModelVisual({ spec }: { spec: Of<'areaModel'> }) {
  const [a, setA] = useState(spec.a);
  const [b, setB] = useState(spec.b);
  const split = (v: number): number[] => (v >= 10 && v % 10 !== 0 ? [v - (v % 10), v % 10] : [v]);
  const across = split(a);
  const down = split(b);
  const colW = across.length === 2 ? [150, 70] : [220];
  const rowH = down.length === 2 ? [100, 50] : [150];
  const fills = [C.action, C.actionSoft, C.hint, C.star];
  const products: number[] = [];
  const cells: React.ReactNode[] = [];
  let y = 30;
  for (let r = 0; r < down.length; r++) {
    let x = 56;
    for (let c = 0; c < across.length; c++) {
      const value = across[c] * down[r];
      products.push(value);
      const idx = r * 2 + c;
      cells.push(
        <g key={`${r}-${c}`}>
          <rect x={x} y={y} width={colW[c]} height={rowH[r]} fill={fills[idx]} fillOpacity={idx === 0 ? 0.3 : 1} stroke={C.ink} strokeWidth={2.5} />
          <text x={x + colW[c] / 2} y={y + rowH[r] / 2 + 5} textAnchor="middle" fontSize={15} fontWeight={800} fill={C.ink}>{fmt(value)}</text>
          {r === 0 && <text x={x + colW[c] / 2} y={22} textAnchor="middle" fontSize={13} fontWeight={800} fill={C.muted}>{across[c]}</text>}
        </g>,
      );
      x += colW[c];
    }
    cells.push(<text key={`row${r}`} x={48} y={y + rowH[r] / 2 + 5} textAnchor="end" fontSize={13} fontWeight={800} fill={C.muted}>{down[r]}</text>);
    y += rowH[r];
  }

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 190" className="w-full h-auto" role="img" aria-label={`${a} times ${b} as a rectangle split into parts`}>{cells}</svg>
      <Slider label="First number" value={a} min={1} max={99} onChange={setA} />
      <Slider label="Second number" value={b} min={1} max={99} onChange={setB} />
      <Working>
        {a} × {b} = {products.length > 1 ? `${products.map((p) => fmt(p)).join(' + ')} = ` : ''}{fmt(a * b)}
      </Working>
    </div>
  );
}

// ══ Ten frames ═══════════════════════════════════════════════════════════════

export function CountersVisual({ spec }: { spec: Of<'counters'> }) {
  const [op, setOp] = useState<'add' | 'subtract'>(spec.op);
  const [a, setA] = useState(spec.a);
  const [b, setB] = useState(spec.b);
  const second = op === 'subtract' ? Math.min(b, a) : b;
  const shown = op === 'add' ? a + second : a;

  const frame = (start: number) => (
    <div key={start} className="grid grid-cols-5 gap-1 p-1.5 rounded-tile border-2 border-ink bg-white">
      {range(10).map((i) => {
        const at = start + i;
        const filled = at < shown;
        const isSecond = op === 'add' ? at >= a && filled : at >= a - second && filled;
        return (
          <span key={i} className="aspect-square rounded-[6px] border-2 border-line flex items-center justify-center">
            {filled && (
              <span className={`w-[72%] h-[72%] rounded-full border-2 border-ink flex items-center justify-center text-[13px] font-extrabold text-ink ${isSecond ? (op === 'add' ? 'bg-star' : 'bg-white') : 'bg-action'}`}>
                {op === 'subtract' && isSecond ? '×' : ''}
              </span>
            )}
          </span>
        );
      })}
    </div>
  );

  const toTen = 10 - a;
  return (
    <div className="space-y-3">
      <div className="space-y-2" role="img" aria-label={op === 'add' ? `${a} plus ${second}` : `${a} take away ${second}`}>
        {frame(0)}
        {shown > 10 && frame(10)}
      </div>
      <Toggle options={[{ value: 'add', label: 'Add' }, { value: 'subtract', label: 'Take away' }]} value={op} onChange={setOp} />
      <Stepper label="first number" value={a} min={0} max={op === 'add' ? 10 : 20} onChange={setA} />
      <Stepper label={op === 'add' ? 'add' : 'take away'} value={second} min={0} max={op === 'add' ? 10 : Math.max(a, 0)} onChange={setB} />
      <Working>
        {op === 'add'
          ? a < 10 && second > toTen && a > 0
            ? `${a} + ${second}: first make ten. ${a} + ${toTen} = 10, then ${second - toTen} more makes ${a + second}.`
            : `${a} + ${second} = ${a + second}`
          : `${a} − ${second} = ${a - second}. The crossed counters are taken away.`}
      </Working>
    </div>
  );
}

// ══ Magic square ═════════════════════════════════════════════════════════════

const MAGIC_LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];

export function MagicSquareVisual({ spec }: { spec: Of<'magicSquare'> }) {
  const [cells, setCells] = useState<number[]>(spec.cells);
  const sums = MAGIC_LINES.map((line) => cells[line[0]] + cells[line[1]] + cells[line[2]]);
  const full = cells.every((v) => v > 0);
  const magic = full && sums.every((s) => s === sums[0]);
  const tag = 'text-[13px] font-extrabold text-ink-muted flex items-center justify-center';

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-4 gap-1.5 max-w-[280px] mx-auto">
        {range(9).map((i) => (
          <React.Fragment key={i}>
            {spec.cells[i] > 0 ? (
              <span className="aspect-square rounded-tile border-2 border-ink bg-soft flex items-center justify-center font-display text-heading text-ink">{cells[i]}</span>
            ) : (
              <input
                type="number"
                inputMode="numeric"
                aria-label={`Row ${Math.floor(i / 3) + 1}, column ${(i % 3) + 1}`}
                value={cells[i] > 0 ? cells[i] : ''}
                onChange={(e) => {
                  const next = cells.slice();
                  next[i] = Math.max(0, Math.min(99, Math.round(Number(e.target.value) || 0)));
                  setCells(next);
                }}
                className="aspect-square w-full rounded-tile border-2 border-action bg-white text-center font-display text-heading text-ink"
              />
            )}
            {i % 3 === 2 && <span className={tag}>= {sums[Math.floor(i / 3)]}</span>}
          </React.Fragment>
        ))}
        {[3, 4, 5].map((k) => <span key={k} className={tag}>= {sums[k]}</span>)}
        <span className={tag}>↘ {sums[6]}</span>
      </div>
      <p className="text-caption text-ink-muted text-center">Diagonals: ↘ {sums[6]} and ↙ {sums[7]}</p>
      <Working>
        {magic
          ? `Every row, column and diagonal adds to ${sums[0]}. It is a magic square!`
          : full
            ? 'The sums are not all equal yet. Find the line that is different.'
            : 'Fill the empty boxes so that every row, column and diagonal adds to the same number.'}
      </Working>
    </div>
  );
}

// ══ Pictograph ═══════════════════════════════════════════════════════════════

export function PictographVisual({ spec }: { spec: Of<'pictograph'> }) {
  const [pick, setPick] = useState(0);
  const each = spec.each;
  const row = spec.rows[Math.min(pick, spec.rows.length - 1)];
  const unit = spec.unit ?? '';
  const symbols = (value: number) => {
    const whole = Math.floor(value / each);
    const part = (value % each) / each;
    return (
      <span className="flex flex-wrap gap-1">
        {range(whole).map((i) => <span key={i} className="w-6 h-6 rounded-full bg-action border-2 border-ink" />)}
        {part > 0 && (
          <span className="w-6 h-6 rounded-full border-2 border-ink overflow-hidden bg-white">
            <span className="block h-full bg-action" style={{ width: `${part * 100}%` }} />
          </span>
        )}
      </span>
    );
  };
  const wholeCount = Math.floor(row.value / each);
  const rest = row.value % each;

  return (
    <div className="space-y-3">
      <div className="space-y-1.5">
        {spec.rows.map((r, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setPick(i)}
            aria-pressed={pick === i}
            aria-label={`${r.label}: ${r.value} ${unit}`}
            className={`w-full min-h-[48px] px-3 py-2 rounded-tile border-2 flex items-center gap-3 text-left ${pick === i ? 'border-ink bg-soft' : 'border-line bg-white hover:border-ink'}`}
          >
            <span className="w-20 flex-shrink-0 text-label text-ink">{r.label}</span>
            {symbols(r.value)}
          </button>
        ))}
      </div>
      <p className="text-label text-ink-muted flex items-center justify-center gap-2">
        <span className="w-5 h-5 rounded-full bg-action border-2 border-ink" aria-hidden="true" /> = {each} {unit}
      </p>
      <Working>
        {row.label}: {wholeCount} full symbol{wholeCount === 1 ? '' : 's'}{rest > 0 ? ' and part of one' : ''} = {wholeCount} × {each}{rest > 0 ? ` + ${rest}` : ''} = {row.value} {unit}
      </Working>
    </div>
  );
}

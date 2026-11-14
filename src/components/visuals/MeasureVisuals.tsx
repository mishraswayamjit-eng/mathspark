'use client';

import React, { useState } from 'react';
import type { VisualSpec } from '@/lib/visuals/spec';
import { C, range, fmt, tidy, Stat, Working, Stepper, Slider, Toggle } from './parts';

type Of<K extends VisualSpec['type']> = Extract<VisualSpec, { type: K }>;

// ══ Clock ════════════════════════════════════════════════════════════════════

function timeInWords(h: number, m: number): string {
  const next = h === 12 ? 1 : h + 1;
  if (m === 0) return `${h} o'clock`;
  if (m === 15) return `quarter past ${h}`;
  if (m === 30) return `half past ${h}`;
  if (m === 45) return `quarter to ${next}`;
  if (m < 30) return `${m} minute${m === 1 ? '' : 's'} past ${h}`;
  return `${60 - m} minute${60 - m === 1 ? '' : 's'} to ${next}`;
}

export function ClockVisual({ spec }: { spec: Of<'clock'> }) {
  const [h, setH] = useState(spec.hour);
  const [m, setM] = useState(spec.minute);
  const cx = 120;
  const cy = 120;
  const hourDeg = (h % 12) * 30 + m * 0.5;
  const minDeg = m * 6;
  const between = Math.abs(hourDeg - minDeg);
  const angle = Math.min(between, 360 - between);
  const tip = (deg: number, len: number) => ({
    x: cx + len * Math.sin((deg * Math.PI) / 180),
    y: cy - len * Math.cos((deg * Math.PI) / 180),
  });
  const hourTip = tip(hourDeg, 52);
  const minTip = tip(minDeg, 82);

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 240 240" className="w-full max-w-[250px] mx-auto h-auto" role="img" aria-label={`Clock showing ${timeInWords(h, m)}`}>
        <circle cx={cx} cy={cy} r={108} fill={C.card} stroke={C.ink} strokeWidth={3} />
        {range(60).map((i) => {
          const a = tip(i * 6, 108);
          const b = tip(i * 6, i % 5 === 0 ? 96 : 102);
          return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={i % 5 === 0 ? C.ink : C.line} strokeWidth={i % 5 === 0 ? 2.5 : 1.5} />;
        })}
        {range(12).map((i) => {
          const p = tip((i + 1) * 30, 80);
          return <text key={i} x={p.x} y={p.y + 5} textAnchor="middle" fontSize={15} fontWeight={800} fill={C.ink}>{i + 1}</text>;
        })}
        <line x1={cx} y1={cy} x2={minTip.x} y2={minTip.y} stroke={C.action} strokeWidth={4} strokeLinecap="round" />
        <line x1={cx} y1={cy} x2={hourTip.x} y2={hourTip.y} stroke={C.ink} strokeWidth={6} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={6} fill={C.star} stroke={C.ink} strokeWidth={2} />
      </svg>
      <Stepper label="hour" value={h} min={1} max={12} onChange={setH} />
      <Slider label="Minutes" value={m} min={0} max={59} onChange={setM} display={`${m} min`} />
      <div className="flex gap-2">
        <Stat label="Time" value={`${h}:${m < 10 ? '0' : ''}${m}`} />
        <Stat label="Between the hands" value={`${tidy(angle)}°`} />
      </div>
      <Working>
        It is {timeInWords(h, m)}. The minute hand turns 6° every minute; the hour hand turns 30° every hour.
      </Working>
    </div>
  );
}

// ══ Calendar ═════════════════════════════════════════════════════════════════

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function isLeap(y: number): boolean {
  return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
}

export function CalendarVisual({ spec }: { spec: Of<'calendar'> }) {
  const [year, setYear] = useState(spec.year);
  const [month, setMonth] = useState(spec.month);
  const [day, setDay] = useState<number | null>(spec.day ?? null);
  const first = new Date(year, month - 1, 1).getDay();
  const count = new Date(year, month, 0).getDate();
  const picked = day !== null && day <= count ? day : null;

  return (
    <div className="space-y-3">
      <div>
        <p className="font-display text-title text-ink text-center mb-2">{MONTHS[month - 1]} {year}</p>
        <div className="grid grid-cols-7 gap-1 text-center">
          {DAYS.map((d) => <span key={d} className="text-caption text-ink-muted">{d.slice(0, 2)}</span>)}
          {range(first).map((i) => <span key={`blank${i}`} />)}
          {range(count).map((i) => {
            const d = i + 1;
            const on = picked === d;
            return (
              <button
                key={d}
                type="button"
                onClick={() => setDay(d)}
                aria-pressed={on}
                className={`h-12 rounded-tile border-2 text-[14px] font-extrabold transition-colors ${on ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink hover:border-ink'}`}
              >
                {d}
              </button>
            );
          })}
        </div>
      </div>
      <Stepper label={`month (${MONTHS[month - 1]})`} value={month} min={1} max={12} onChange={setMonth} />
      <Stepper label="year" value={year} min={1900} max={2100} onChange={setYear} />
      <div className="flex gap-2">
        <Stat label="Days in the month" value={count} />
        <Stat label="Leap year?" value={isLeap(year) ? 'Yes' : 'No'} />
      </div>
      <Working>
        {picked !== null
          ? `${picked} ${MONTHS[month - 1]} ${year} is a ${DAYS[new Date(year, month - 1, picked).getDay()]}.`
          : `${MONTHS[month - 1]} ${year} begins on a ${DAYS[first]}. Tap a date to find its day.`}
        {month === 2 ? ` February has ${count} days because ${year} is ${isLeap(year) ? '' : 'not '}a leap year.` : ''}
      </Working>
    </div>
  );
}

// ══ Money ════════════════════════════════════════════════════════════════════

const DENOMINATIONS = [500, 200, 100, 50, 20, 10, 5, 2, 1];

function fewest(amount: number): number[] {
  const out: number[] = [];
  let left = amount;
  for (let i = 0; i < DENOMINATIONS.length; i++) {
    while (left >= DENOMINATIONS[i]) {
      out.push(DENOMINATIONS[i]);
      left -= DENOMINATIONS[i];
    }
  }
  return out;
}

export function MoneyVisual({ spec }: { spec: Of<'money'> }) {
  const [pile, setPile] = useState<number[]>(() => fewest(spec.amount));
  let total = 0;
  for (let i = 0; i < pile.length; i++) total += pile[i];
  const best = fewest(spec.amount).length;
  const gap = spec.amount - total;

  return (
    <div className="space-y-3">
      <p className="text-label text-ink-muted text-center">Make <span className="font-display text-heading text-ink">₹{fmt(spec.amount)}</span></p>
      <div className="min-h-[96px] bg-soft rounded-card p-3 flex flex-wrap gap-2 content-start" role="group" aria-label="Your notes and coins">
        {pile.length === 0 && <p className="text-label text-ink-muted m-auto">Tap a note or coin below to add it.</p>}
        {pile.map((v, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setPile(pile.filter((_, k) => k !== i))}
            aria-label={`Remove ₹${v}`}
            className={`min-h-[48px] border-2 border-ink font-extrabold text-[14px] text-ink shadow-hard-xs ${v >= 10 ? 'px-3 rounded-tile bg-success-soft' : 'w-12 rounded-full bg-hint'}`}
          >
            ₹{v}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap gap-1.5 justify-center">
        {DENOMINATIONS.map((v) => (
          <button
            key={v}
            type="button"
            disabled={pile.length >= 24}
            onClick={() => setPile(pile.concat([v]))}
            aria-label={`Add ₹${v}`}
            className="min-h-[48px] min-w-[48px] px-2 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[13px] hover:border-ink disabled:opacity-40"
          >
            +₹{v}
          </button>
        ))}
      </div>
      <div className="flex gap-2">
        <Stat label="You have" value={`₹${fmt(total)}`} />
        <Stat label="Notes and coins" value={pile.length} />
      </div>
      <Working>
        {gap === 0
          ? pile.length === best
            ? `Exactly ₹${fmt(spec.amount)}, using the fewest notes and coins possible (${best}).`
            : `Exactly ₹${fmt(spec.amount)}. It can be done with only ${best}. Can you find how?`
          : gap > 0
            ? `₹${fmt(gap)} more to go.`
            : `That is ₹${fmt(-gap)} too much. Tap a note or coin in the pile to take it away.`}
      </Working>
    </div>
  );
}

// ══ Speed, distance and time ═════════════════════════════════════════════════

export function JourneyVisual({ spec }: { spec: Of<'journey'> }) {
  const [t, setT] = useState(spec.hours);
  const [speed, setSpeed] = useState(spec.speed);
  const other = spec.speedB;
  const unit = spec.unit ?? 'km';
  const fastest = Math.max(speed, other ?? 0);
  const full = fastest * spec.hours || 1;
  const x = (d: number) => 20 + (d / full) * 260;
  const d1 = speed * t;
  const d2 = other !== undefined ? other * t : 0;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 130" className="w-full h-auto" role="img" aria-label={`A journey at ${speed} ${unit} per hour for ${tidy(t)} hours`}>
        <line x1={20} y1={70} x2={280} y2={70} stroke={C.ink} strokeWidth={3} strokeLinecap="round" />
        {range(spec.hours + 1).map((i) => (
          <g key={i}>
            <line x1={x(fastest * i)} y1={62} x2={x(fastest * i)} y2={78} stroke={C.ink} strokeWidth={2} />
            <text x={x(fastest * i)} y={96} textAnchor="middle" fontSize={11} fontWeight={800} fill={C.muted}>{fmt(fastest * i)}</text>
          </g>
        ))}
        <text x={150} y={116} textAnchor="middle" fontSize={11} fontWeight={800} fill={C.muted}>distance in {unit}</text>
        <rect x={20} y={64} width={Math.max(0, x(d1) - 20)} height={12} fill={C.action} opacity={0.35} />
        <circle cx={x(d1)} cy={70} r={11} fill={C.action} stroke={C.ink} strokeWidth={2.5} style={{ transition: 'cx 0.15s' }} />
        <text x={x(d1)} y={48} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.action}>{spec.labelA ?? 'A'}: {fmt(d1)}</text>
        {other !== undefined && (
          <>
            <circle cx={x(d2)} cy={70} r={8} fill={C.star} stroke={C.ink} strokeWidth={2.5} style={{ transition: 'cx 0.15s' }} />
            <text x={x(d2)} y={30} textAnchor="middle" fontSize={12} fontWeight={800} fill={C.ink}>{spec.labelB ?? 'B'}: {fmt(d2)}</text>
          </>
        )}
      </svg>
      <Slider label="Time" value={t} min={0} max={spec.hours} step={0.5} onChange={setT} display={`${tidy(t)} h`} />
      <Slider label={`Speed${other !== undefined ? ` of ${spec.labelA ?? 'A'}` : ''}`} value={speed} min={1} max={Math.max(120, spec.speed)} onChange={setSpeed} display={`${speed} ${unit}/h`} />
      <Working>
        Distance = speed × time = {speed} × {tidy(t)} = {fmt(d1)} {unit}
        {other !== undefined ? `. ${spec.labelB ?? 'B'} at ${other} ${unit}/h has gone ${fmt(d2)} ${unit}, so they are ${fmt(Math.abs(d1 - d2))} ${unit} apart.` : ''}
      </Working>
    </div>
  );
}

// ══ Unit ladder ══════════════════════════════════════════════════════════════

const UNIT_SETS: Record<string, Array<{ name: string; size: number }>> = {
  length:   [{ name: 'km', size: 1000 }, { name: 'm', size: 1 }, { name: 'cm', size: 0.01 }, { name: 'mm', size: 0.001 }],
  mass:     [{ name: 'kg', size: 1000 }, { name: 'g', size: 1 }, { name: 'mg', size: 0.001 }],
  capacity: [{ name: 'kl', size: 1000 }, { name: 'l', size: 1 }, { name: 'ml', size: 0.001 }],
};

export function UnitLadderVisual({ spec }: { spec: Of<'unitLadder'> }) {
  const units = UNIT_SETS[spec.quantity];
  const [from, setFrom] = useState(spec.from);
  const [to, setTo] = useState(spec.to);
  const [value, setValue] = useState(spec.value);
  const a = units.filter((u) => u.name === from)[0] ?? units[0];
  const b = units.filter((u) => u.name === to)[0] ?? units[units.length - 1];
  const factor = a.size / b.size;
  const options = units.map((u) => ({ value: u.name, label: u.name }));

  return (
    <div className="space-y-3">
      <div className="flex items-stretch justify-center gap-1" aria-hidden="true">
        {units.map((u, i) => (
          <React.Fragment key={u.name}>
            {i > 0 && (
              <span className="flex flex-col items-center justify-center text-[11px] font-extrabold text-ink-muted px-1">
                <span>× {tidy(units[i - 1].size / u.size)} →</span>
                <span>← ÷ {tidy(units[i - 1].size / u.size)}</span>
              </span>
            )}
            <span className={`min-w-[48px] px-2 py-3 rounded-tile border-2 text-center font-display text-title ${u.name === a.name ? 'bg-action border-ink text-white' : u.name === b.name ? 'bg-star border-ink text-ink' : 'bg-white border-line text-ink'}`}>
              {u.name}
            </span>
          </React.Fragment>
        ))}
      </div>
      <p className="text-caption text-ink-muted text-center">Bigger units on the left, smaller units on the right</p>
      <div>
        <p className="text-caption text-ink-muted mb-1">From</p>
        <Toggle options={options} value={a.name} onChange={setFrom} />
      </div>
      <div>
        <p className="text-caption text-ink-muted mb-1">To</p>
        <Toggle options={options} value={b.name} onChange={setTo} />
      </div>
      <label className="block">
        <span className="text-caption text-ink-muted">Amount in {a.name}</span>
        <input
          type="number"
          inputMode="decimal"
          value={value}
          min={0}
          onChange={(e) => setValue(Math.max(0, Math.min(1000000, Number(e.target.value) || 0)))}
          className="mt-1 w-full min-h-[48px] rounded-control border-2 border-line bg-white px-3 font-extrabold text-ink"
        />
      </label>
      <Working>
        {a.name === b.name
          ? `${tidy(value)} ${a.name} stays ${tidy(value)} ${a.name}.`
          : factor > 1
            ? `${a.name} to ${b.name}: a smaller unit, so multiply. ${tidy(value)} × ${tidy(factor)} = ${tidy(value * factor)} ${b.name}`
            : `${a.name} to ${b.name}: a bigger unit, so divide. ${tidy(value)} ÷ ${tidy(1 / factor)} = ${tidy(value * factor)} ${b.name}`}
      </Working>
    </div>
  );
}

// ══ Profit and loss ══════════════════════════════════════════════════════════

export function ProfitLossVisual({ spec }: { spec: Of<'profitLoss'> }) {
  const [cost, setCost] = useState(spec.cost);
  const [selling, setSelling] = useState(spec.selling);
  const top = Math.max(spec.cost, spec.selling) * 2;
  const step = top > 400 ? 10 : top > 80 ? 5 : 1;
  const diff = selling - cost;
  const percent = cost > 0 ? (Math.abs(diff) / cost) * 100 : 0;
  const word = diff >= 0 ? 'Profit' : 'Loss';
  const bar = (v: number) => `${Math.max(2, (v / top) * 100)}%`;

  return (
    <div className="space-y-3">
      <div className="space-y-2" role="img" aria-label={`Cost price ${cost}, selling price ${selling}`}>
        <div>
          <p className="text-caption text-ink-muted">Cost price ₹{fmt(cost)}</p>
          <div className="h-9 rounded-note border-2 border-ink bg-action" style={{ width: bar(cost), transition: 'width 0.15s' }} />
        </div>
        <div>
          <p className="text-caption text-ink-muted">Selling price ₹{fmt(selling)}</p>
          <div className="flex h-9" style={{ width: bar(Math.max(cost, selling)) }}>
            <div className="h-full rounded-l-note border-2 border-ink bg-action" style={{ width: `${(Math.min(cost, selling) / Math.max(cost, selling, 1)) * 100}%` }} />
            {diff !== 0 && (
              <div className={`h-full flex-1 rounded-r-note border-2 border-l-0 border-ink ${diff > 0 ? 'bg-star' : 'bg-white border-dashed'}`} />
            )}
          </div>
        </div>
      </div>
      <Slider label="Cost price" value={cost} min={step} max={top} step={step} onChange={setCost} display={`₹${fmt(cost)}`} />
      <Slider label="Selling price" value={selling} min={0} max={top} step={step} onChange={setSelling} display={`₹${fmt(selling)}`} />
      <div className="flex gap-2">
        <Stat label={word} value={`₹${fmt(Math.abs(diff))}`} />
        <Stat label={`${word} %`} value={`${tidy(Math.round(percent * 100) / 100)}%`} />
      </div>
      <Working>
        {diff === 0
          ? 'Selling price equals cost price: no profit and no loss.'
          : `${word} = ${diff > 0 ? `${fmt(selling)} − ${fmt(cost)}` : `${fmt(cost)} − ${fmt(selling)}`} = ₹${fmt(Math.abs(diff))}. ${word} % = ${fmt(Math.abs(diff))} ÷ ${fmt(cost)} × 100 = ${tidy(Math.round(percent * 100) / 100)}%, always worked out on the cost price.`}
      </Working>
    </div>
  );
}

// ══ Simple interest ══════════════════════════════════════════════════════════

export function SimpleInterestVisual({ spec }: { spec: Of<'simpleInterest'> }) {
  const [rate, setRate] = useState(spec.rate);
  const [years, setYears] = useState(spec.years);
  const p = spec.principal;
  const perYear = (p * rate) / 100;
  const interest = perYear * years;
  const tallest = p + (p * 20 * 10) / 100;
  const hgt = (v: number) => (v / tallest) * 150;

  return (
    <div className="space-y-3">
      <svg viewBox="0 0 300 190" className="w-full h-auto" role="img" aria-label={`Simple interest on ${p} at ${rate} percent for ${years} years`}>
        <line x1={14} y1={170} x2={290} y2={170} stroke={C.ink} strokeWidth={2} />
        {range(years + 1).map((y) => {
          const w = Math.min(34, 250 / (years + 1) - 6);
          const x = 22 + y * (250 / (years + 1));
          return (
            <g key={y}>
              <rect x={x} y={170 - hgt(p)} width={w} height={hgt(p)} fill={C.action} stroke={C.ink} strokeWidth={2} />
              {y > 0 && <rect x={x} y={170 - hgt(p + perYear * y)} width={w} height={hgt(perYear * y)} fill={C.star} stroke={C.ink} strokeWidth={2} />}
              <text x={x + w / 2} y={184} textAnchor="middle" fontSize={10} fontWeight={800} fill={C.muted}>{y === 0 ? 'start' : `yr ${y}`}</text>
            </g>
          );
        })}
      </svg>
      <Slider label="Rate each year" value={rate} min={1} max={20} onChange={setRate} display={`${rate}%`} />
      <Slider label="Time" value={years} min={1} max={10} onChange={setYears} display={`${years} year${years === 1 ? '' : 's'}`} />
      <div className="flex gap-2">
        <Stat label="Interest" value={`₹${fmt(interest)}`} />
        <Stat label="Amount" value={`₹${fmt(p + interest)}`} />
      </div>
      <Working>
        Each year adds the same ₹{fmt(perYear)}. Interest = P × R × T ÷ 100 = {fmt(p)} × {rate} × {years} ÷ 100 = ₹{fmt(interest)}
      </Working>
    </div>
  );
}

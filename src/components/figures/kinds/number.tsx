'use client';

import type { ReactNode } from 'react';
import type {
  FractionBarsFigure, SetFigure, BarModelFigure, NumberLineFigure, PlaceChartFigure, FactorTreeFigure,
} from '@/lib/figures/types';
import type { KindProps } from './shared';
import { C, Frame, Label, SVG_CLASS, INK_W, HI_W, isOn, text, num, clamp, list, wedgePath, headPoints, estWidth, tidy } from './shared';

// ══ Fraction strips and circles ══════════════════════════════════════════════

export function FractionBarsKind({ spec, className }: KindProps<FractionBarsFigure>) {
  const bars = list(spec.bars);
  if (bars.length === 0) return null;
  const hl = spec.highlight;
  const round = spec.shape === 'circle';
  let anyLabel = false;
  for (let i = 0; i < bars.length; i++) {
    if (bars[i] && text(bars[i].label) !== '') anyLabel = true;
  }

  const body: ReactNode[] = [];
  const said: string[] = [];
  let y = 8;
  for (let i = 0; i < bars.length; i++) {
    const b = bars[i];
    if (!b) continue;
    const parts = clamp(Math.round(num(b.parts, 1)), 1, 24);
    const shaded = clamp(Math.round(num(b.shaded, 0)), 0, parts);
    const label = text(b.label);
    const on = isOn(hl, `b${i}`);
    said.push(`${label ? `${label}: ` : ''}${shaded} of ${parts} equal ${parts === 1 ? 'part' : 'parts'} shaded`);

    if (round) {
      const r = 42;
      const cx = anyLabel ? 62 : 160;
      const cy = y + r + 2;
      const cells: ReactNode[] = [];
      if (parts === 1) {
        cells.push(<circle key="whole" cx={cx} cy={cy} r={r} fill={shaded === 1 ? C.action : C.card} />);
      } else {
        for (let k = 0; k < parts; k++) {
          cells.push(
            <path key={k} d={wedgePath(cx, cy, r, (k * 360) / parts, ((k + 1) * 360) / parts)} fill={k < shaded ? C.action : C.card}
              stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />,
          );
        }
      }
      body.push(
        <g key={i}>
          {cells}
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={on ? C.action : C.ink} strokeWidth={on ? HI_W : INK_W} />
          {label !== '' && <Label x={cx + r + 14} y={cy + 4.5} anchor="start" fill={on ? C.action : C.ink}>{label}</Label>}
        </g>,
      );
      y += 2 * r + 16;
    } else {
      const x0 = 20;
      const bw = 280;
      const bh = 36;
      if (label !== '') {
        body.push(<Label key={`l${i}`} x={x0} y={y + 12} anchor="start" fill={on ? C.action : C.ink}>{label}</Label>);
        y += 20;
      }
      const cells: ReactNode[] = [];
      for (let k = 0; k < parts; k++) {
        cells.push(
          <rect key={k} x={x0 + (k * bw) / parts} y={y} width={bw / parts} height={bh} fill={k < shaded ? C.action : C.card}
            stroke={C.ink} strokeWidth={1.5} />,
        );
      }
      body.push(
        <g key={i}>
          {cells}
          <rect x={x0} y={y} width={bw} height={bh} fill="none" stroke={on ? C.action : C.ink} strokeWidth={on ? HI_W : INK_W} strokeLinejoin="round" />
        </g>,
      );
      y += bh + 14;
    }
  }

  return (
    <Frame label={`${round ? 'Fraction circles' : 'Fraction strips'}: ${said.join('; ')}`} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${y}`} className={SVG_CLASS} aria-hidden="true">
        {body}
      </svg>
    </Frame>
  );
}

// ══ A set of counters ════════════════════════════════════════════════════════

/** How many counters across, so a group looks like a tidy block. */
function countersAcross(k: number): number {
  if (k <= 5) return k;
  for (let d = Math.ceil(Math.sqrt(k)); d <= 10 && d <= k; d++) {
    if (k % d === 0) return d;
  }
  return Math.min(10, Math.ceil(Math.sqrt(k * 1.5)));
}

export function SetKind({ spec, className }: KindProps<SetFigure>) {
  const total = clamp(Math.round(num(spec.total, 0)), 0, 60);
  if (total < 1) return null;
  const hl = spec.highlight;
  const g = Math.round(num(spec.groups, 0));
  const grouped = g >= 1 && g <= total && total % g === 0;
  const groupCount = grouped ? g : 1;
  const k = total / groupCount;
  const shadedGroups = grouped ? clamp(Math.round(num(spec.shadedGroups, 0)), 0, groupCount) : 0;
  const shadedOn = isOn(hl, 'shaded');

  const pitch = 22;
  const across = countersAcross(k);
  const down = Math.ceil(k / across);
  const bw = across * pitch + 10;
  const bh = down * pitch + 10;
  const gap = 8;
  const perRow = Math.min(groupCount, Math.max(1, Math.floor((304 + gap) / (bw + gap))));
  const boxRows = Math.ceil(groupCount / perRow);

  const body: ReactNode[] = [];
  for (let gi = 0; gi < groupCount; gi++) {
    const row = Math.floor(gi / perRow);
    const inRow = row < boxRows - 1 ? perRow : groupCount - perRow * (boxRows - 1);
    const rowW = inRow * (bw + gap) - gap;
    const bx = 160 - rowW / 2 + (gi % perRow) * (bw + gap);
    const by = 8 + row * (bh + gap);
    const shaded = gi < shadedGroups;
    const counters: ReactNode[] = [];
    for (let j = 0; j < k; j++) {
      counters.push(
        <circle key={j} cx={bx + 5 + pitch / 2 + (j % across) * pitch} cy={by + 5 + pitch / 2 + Math.floor(j / across) * pitch} r={8}
          fill={shaded ? C.action : C.card} stroke={C.ink} strokeWidth={2} />,
      );
    }
    body.push(
      <g key={gi}>
        {grouped && (
          <rect x={bx} y={by} width={bw} height={bh} rx={8} fill={C.card}
            stroke={shaded && shadedOn ? C.action : C.ink} strokeWidth={shaded && shadedOn ? 4.5 : 2} />
        )}
        {counters}
      </g>,
    );
  }

  const item = text(spec.item) || 'counters';
  let aria = `${total} ${item}`;
  if (grouped) aria += ` in ${groupCount} equal ${groupCount === 1 ? 'group' : 'groups'}`;
  if (shadedGroups > 0) aria += `, with ${shadedGroups} ${shadedGroups === 1 ? 'group' : 'groups'} shaded`;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${boxRows * (bh + gap) - gap + 16}`} className={SVG_CLASS} aria-hidden="true">
        {body}
      </svg>
    </Frame>
  );
}

// ══ Bar model ════════════════════════════════════════════════════════════════

const TONES: Record<string, string> = { a: C.star, b: C.actionSoft, c: C.successSoft, unknown: C.card };

interface ModelSegment { units: number; label: string; tone: string }
interface ModelBar { label: string; brace: string; segments: ModelSegment[]; total: number }

function bracePath(x0: number, x1: number, yTop: number, yBottom: number): string {
  const mid = (x0 + x1) / 2;
  const c = Math.min(8, (x1 - x0) / 4);
  return `M ${x0} ${yBottom} Q ${x0} ${yTop} ${x0 + c} ${yTop} L ${mid - c} ${yTop} Q ${mid} ${yTop} ${mid} ${yTop - 6} Q ${mid} ${yTop} ${mid + c} ${yTop} L ${x1 - c} ${yTop} Q ${x1} ${yTop} ${x1} ${yBottom}`;
}

export function BarModelKind({ spec, className }: KindProps<BarModelFigure>) {
  const source = list(spec.bars);
  if (source.length === 0) return null;
  const hl = spec.highlight;

  const bars: ModelBar[] = [];
  let maxTotal = 0;
  let maxLabel = 0;
  for (let i = 0; i < source.length; i++) {
    const b = source[i];
    const segments: ModelSegment[] = [];
    let total = 0;
    const raw = b ? list(b.segments) : [];
    for (let k = 0; k < raw.length; k++) {
      const s = raw[k];
      if (!s) continue;
      const units = num(s.units, 1) > 0 ? num(s.units, 1) : 1;
      total += units;
      segments.push({ units, label: text(s.label), tone: typeof s.tone === 'string' && Object.prototype.hasOwnProperty.call(TONES, s.tone) ? s.tone : 'a' });
    }
    const label = b ? text(b.label) : '';
    bars.push({ label, brace: b ? text(b.brace) : '', segments, total });
    maxTotal = Math.max(maxTotal, total);
    maxLabel = Math.max(maxLabel, label.length);
  }
  if (maxTotal <= 0) return null;

  // Short names sit to the left of their bar; longer ones go on a line above it.
  const beside = maxLabel > 0 && maxLabel <= 10;
  const x0 = beside ? 24 + maxLabel * 7.6 : 14;
  const scale = (306 - x0) / maxTotal;
  const h = 38;

  const body: ReactNode[] = [];
  const marks: ReactNode[] = [];
  const said: string[] = [];
  let y = 6;
  for (let i = 0; i < bars.length; i++) {
    const bar = bars[i];
    if (bar.segments.length === 0) continue;
    const barOn = isOn(hl, `b${i}`);
    const x1 = x0 + bar.total * scale;
    if (!beside && bar.label !== '') {
      body.push(<Label key={`n${i}`} x={x0} y={y + 12} anchor="start" fill={barOn ? C.action : C.ink}>{bar.label}</Label>);
      y += 20;
    }
    if (bar.brace !== '') {
      body.push(<Label key={`bl${i}`} x={(x0 + x1) / 2} y={y + 12}>{bar.brace}</Label>);
      body.push(<path key={`bp${i}`} d={bracePath(x0, x1, y + 24, y + 32)} fill="none" stroke={C.ink} strokeWidth={2} strokeLinecap="round" />);
      y += 36;
    }
    if (beside && bar.label !== '') {
      body.push(<Label key={`n${i}`} x={x0 - 9} y={y + h / 2 + 4.5} anchor="end" fill={barOn ? C.action : C.ink}>{bar.label}</Label>);
    }
    const pieces: string[] = [];
    let x = x0;
    for (let k = 0; k < bar.segments.length; k++) {
      const s = bar.segments[k];
      const w = s.units * scale;
      const unknown = s.tone === 'unknown';
      body.push(
        <rect key={`s${i}-${k}`} x={x} y={y} width={w} height={h} fill={TONES[s.tone]} stroke={C.ink} strokeWidth={INK_W}
          strokeDasharray={unknown ? '6 4' : undefined} strokeLinejoin="round" />,
      );
      if (s.label !== '') {
        body.push(
          <Label key={`t${i}-${k}`} x={x + w / 2} y={y + h / 2 + 4.5} size={estWidth(s.label) > w - 6 ? 11 : 13} halo={false}>{s.label}</Label>,
        );
      }
      if (isOn(hl, `b${i}s${k}`)) {
        marks.push(<rect key={`m${i}-${k}`} x={x} y={y} width={w} height={h} fill="none" stroke={C.action} strokeWidth={HI_W} strokeLinejoin="round" />);
      }
      pieces.push(s.label !== '' ? s.label : unknown ? 'an unknown piece' : 'a piece');
      x += w;
    }
    if (barOn) {
      marks.push(<rect key={`m${i}`} x={x0} y={y} width={x1 - x0} height={h} fill="none" stroke={C.action} strokeWidth={HI_W} strokeLinejoin="round" />);
    }
    said.push(`${bar.label !== '' ? bar.label : `Bar ${i + 1}`}: ${pieces.join(', ')}${bar.brace !== '' ? `; the whole bar is ${bar.brace}` : ''}`);
    y += h + 14;
  }

  return (
    <Frame label={`A bar model. ${said.join('. ')}`} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${y}`} className={SVG_CLASS} aria-hidden="true">
        {body}
        {marks}
      </svg>
    </Frame>
  );
}

// ══ Number line ══════════════════════════════════════════════════════════════

export function NumberLineKind({ spec, className }: KindProps<NumberLineFigure>) {
  const hl = spec.highlight;
  const min = num(spec.min, 0);
  const rawMax = num(spec.max, min + 10);
  const max = rawMax > min ? rawMax : min + 1;
  const rawStep = num(spec.step, 1);
  let step = rawStep > 0 ? rawStep : max - min;
  let count = Math.floor((max - min) / step + 1e-6) + 1;
  if (count > 41) {
    count = 41;
    step = (max - min) / 40;
  }
  const X0 = 28;
  const X1 = 292;
  const xOf = (v: number): number => clamp(X0 + ((v - min) / (max - min)) * (X1 - X0), 10, 310);

  const points = list(spec.points);
  const hops = list(spec.hops);
  let anyPointLabel = false;
  for (let i = 0; i < points.length; i++) {
    if (points[i] && text(points[i].label) !== '') anyPointLabel = true;
  }
  const hasHops = hops.length > 0;
  const Y = hasHops ? 64 : anyPointLabel ? 36 : 16;

  // Number as many ticks as fit without the numbers touching.
  const names: string[] = [];
  let longest = 1;
  for (let i = 0; i < count; i++) {
    const name = tidy(min + i * step);
    names.push(name);
    longest = Math.max(longest, name.length);
  }
  const room = Math.max(2, Math.floor(264 / (longest * 7 + 10)) + 1);
  const every = Math.max(1, Math.ceil((count - 1) / (room - 1)));

  const body: ReactNode[] = [];
  for (let i = 0; i < count; i++) {
    const x = xOf(min + i * step);
    body.push(<line key={`t${i}`} x1={x} y1={Y - 7} x2={x} y2={Y + 7} stroke={C.ink} strokeWidth={2} strokeLinecap="round" />);
    const numbered = spec.tickLabels === 'none' ? false
      : spec.tickLabels === 'ends' ? (i === 0 || i === count - 1)
      : i % every === 0;
    if (numbered) {
      body.push(<Label key={`n${i}`} x={x} y={Y + 24} size={12} halo={false}>{names[i]}</Label>);
    }
  }

  const said: string[] = [];
  for (let i = 0; i < hops.length; i++) {
    const hop = hops[i];
    if (!hop || typeof hop.from !== 'number' || typeof hop.to !== 'number' || hop.from === hop.to) continue;
    const on = isOn(hl, `h${i}`);
    const xa = xOf(hop.from);
    const xb = xOf(hop.to);
    const mid = (xa + xb) / 2;
    const label = text(hop.label);
    const colour = on ? C.action : C.ink;
    const bearing = (Math.atan2(xb - mid, -42) * 180) / Math.PI;
    body.push(
      <g key={`h${i}`}>
        <path d={`M ${xa.toFixed(1)} ${Y - 8} Q ${mid.toFixed(1)} ${Y - 50} ${xb.toFixed(1)} ${Y - 8}`} fill="none" stroke={colour}
          strokeWidth={on ? 4 : INK_W} strokeLinecap="round" />
        <polygon points={headPoints({ x: xb, y: Y - 8 }, bearing, on ? 7 : 6)} fill={colour} stroke={colour} strokeWidth={1} strokeLinejoin="round" />
        {label !== '' && <Label x={mid} y={Y - 36} fill={colour}>{label}</Label>}
      </g>,
    );
    said.push(`a hop from ${tidy(hop.from)} to ${tidy(hop.to)}${label !== '' ? ` labelled ${label}` : ''}`);
  }
  for (let i = 0; i < points.length; i++) {
    const p = points[i];
    if (!p || typeof p.at !== 'number' || !isFinite(p.at)) continue;
    const on = isOn(hl, `p${i}`);
    const x = xOf(p.at);
    const label = text(p.label);
    body.push(
      <g key={`p${i}`}>
        <circle cx={x} cy={Y} r={on ? 8.5 : 6} fill={C.action} stroke={C.ink} strokeWidth={2} />
        {label !== '' && <Label x={x} y={hasHops ? Y + 42 : Y - 14} fill={on ? C.action : C.ink}>{label}</Label>}
      </g>,
    );
    said.push(`a point${label !== '' ? ` labelled ${label}` : ''}`);
  }

  let aria = `A number line from ${tidy(min)} to ${tidy(max)}`;
  if (said.length) aria += `, with ${said.join(', ')}`;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${Y + 32 + (hasHops && anyPointLabel ? 18 : 0)}`} className={SVG_CLASS} aria-hidden="true">
        <line x1={12} y1={Y} x2={308} y2={Y} stroke={C.ink} strokeWidth={INK_W} strokeLinecap="round" />
        <polygon points={headPoints({ x: 311, y: Y }, 90, 5)} fill={C.ink} />
        <polygon points={headPoints({ x: 9, y: Y }, 270, 5)} fill={C.ink} />
        {body}
      </svg>
    </Frame>
  );
}

// ══ Indian place-value chart ═════════════════════════════════════════════════

const WHOLE_PLACES = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'lakhs', 'ten lakhs', 'crores', 'ten crores'];
const WHOLE_SHORT = ['O', 'T', 'H', 'Th', 'TTh', 'L', 'TL', 'C', 'TC'];
const PART_PLACES = ['tenths', 'hundredths', 'thousandths'];
const PART_SHORT = ['t', 'h', 'th'];

interface PlaceCell { digit: string; short: string; name: string; index: number }
interface PlaceGroup { period: string; brief: string; cells: PlaceCell[] }

export function PlaceChartKind({ spec, className }: KindProps<PlaceChartFigure>) {
  const raw = text(spec.number);
  const dot = raw.indexOf('.');
  const whole = (dot === -1 ? raw : raw.slice(0, dot)).replace(/[^0-9]/g, '');
  const part = dot === -1 ? '' : raw.slice(dot + 1).replace(/[^0-9]/g, '').slice(0, 3);
  if (whole.length + part.length === 0) return null;
  const hl = spec.highlight;

  const groups: PlaceGroup[] = [];
  const said: string[] = [];
  function add(period: string, brief: string, cell: PlaceCell) {
    const last = groups.length ? groups[groups.length - 1] : undefined;
    if (last && last.period === period) last.cells.push(cell);
    else groups.push({ period, brief, cells: [cell] });
    if (cell.name !== '') said.push(`${cell.digit} in the ${cell.name} place`);
  }
  for (let i = 0; i < whole.length; i++) {
    const place = whole.length - 1 - i;
    const cell: PlaceCell = { digit: whole.charAt(i), short: WHOLE_SHORT[place] || '', name: WHOLE_PLACES[place] || '', index: i };
    if (place >= 7) add('Crores', 'Cr', cell);
    else if (place >= 5) add('Lakhs', 'Lakh', cell);
    else if (place >= 3) add('Thousands', 'Th', cell);
    else add('Ones', 'Ones', cell);
  }
  for (let i = 0; i < part.length; i++) {
    add('Decimals', 'Dec', { digit: part.charAt(i), short: PART_SHORT[i], name: PART_PLACES[i], index: whole.length + i });
  }

  return (
    <Frame label={`A place-value chart for ${raw}: ${said.join(', ')}`} note={spec.note} className={className}>
      <div className="flex justify-center items-stretch w-full max-w-[420px] mx-auto" aria-hidden="true">
        {groups.map((group, gi) => {
          const shade = group.period === 'Lakhs' || group.period === 'Ones';
          return (
            <div key={group.period} className="flex items-stretch min-w-0" style={{ flex: `${group.cells.length} 1 0%`, maxWidth: group.cells.length * 42 + (group.period === 'Decimals' ? 10 : 0) }}>
              {group.period === 'Decimals' && gi > 0 && (
                <span className="self-end pb-1.5 w-[10px] flex-shrink-0 text-center font-display text-[22px] leading-none text-ink">.</span>
              )}
              <div className="flex flex-col flex-1 min-w-0">
                <span className="text-[10px] leading-4 font-extrabold text-ink-muted text-center whitespace-nowrap overflow-hidden">
                  {group.cells.length === 1 ? group.brief : group.period}
                </span>
                <div className="flex">
                  {group.cells.map((cell) => {
                    const on = isOn(hl, `d${cell.index}`);
                    return (
                      <div
                        key={cell.index}
                        className={`flex-1 min-w-0 border-2 -ml-0.5 first:ml-0 flex flex-col items-center ${on ? 'bg-action border-ink text-white relative z-10' : `border-line text-ink ${shade ? 'bg-soft' : 'bg-white'}`}`}
                      >
                        <span className="text-[10px] leading-4 font-extrabold pt-0.5">{cell.short}</span>
                        <span className="font-display text-[20px] leading-7 pb-1">{cell.digit}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Frame>
  );
}

// ══ Factor tree ══════════════════════════════════════════════════════════════

function smallestFactor(n: number): number {
  for (let d = 2; d * d <= n; d++) {
    if (n % d === 0) return d;
  }
  return n;
}

export function FactorTreeKind({ spec, className }: KindProps<FactorTreeFigure>) {
  const n = Math.floor(num(spec.number, 0));
  if (n < 2 || n > 1000000) return null;
  const primesOn = isOn(spec.highlight, 'primes');
  const limit = typeof spec.depth === 'number' && isFinite(spec.depth) ? Math.max(0, Math.floor(spec.depth)) : 99;

  // Each split takes the smallest prime off the left; the rest carries on down the right.
  const splits: Array<{ parent: number; prime: number; rest: number }> = [];
  let cur = n;
  while (splits.length < limit && smallestFactor(cur) !== cur) {
    const prime = smallestFactor(cur);
    splits.push({ parent: cur, prime, rest: cur / prime });
    cur = cur / prime;
  }
  const S = splits.length;
  const lastIsPrime = smallestFactor(cur) === cur;

  const dx = S > 0 ? Math.min(40, 250 / (S + 1)) : 0;
  const dy = 44;
  const rootX = 160 - ((S - 1) * dx) / 2;
  const top = 26;

  const body: ReactNode[] = [];
  function node(key: string, x: number, y: number, value: number, prime: boolean) {
    if (prime) {
      body.push(<circle key={`c${key}`} cx={x} cy={y} r={primesOn ? 16 : 15} fill={primesOn ? C.action : C.star} stroke={C.ink} strokeWidth={2} />);
    }
    body.push(
      <Label key={`v${key}`} x={x} y={y + 5} size={value > 999 ? 12 : 14} fill={prime && primesOn ? C.card : C.ink} halo={!prime}>{value}</Label>,
    );
  }

  const said: string[] = [];
  for (let i = 0; i < S; i++) {
    const x = rootX + i * dx;
    const y = top + i * dy;
    body.push(<line key={`a${i}`} x1={x - 4} y1={y + 11} x2={x - dx + 6} y2={y + dy - 17} stroke={C.ink} strokeWidth={2} strokeLinecap="round" />);
    body.push(<line key={`b${i}`} x1={x + 4} y1={y + 11} x2={x + dx - 6} y2={y + dy - 17} stroke={C.ink} strokeWidth={2} strokeLinecap="round" />);
    said.push(`${splits[i].parent} splits into ${splits[i].prime} and ${splits[i].rest}`);
  }
  for (let i = 0; i < S; i++) {
    node(`s${i}`, rootX + i * dx, top + i * dy, splits[i].parent, false);
    node(`p${i}`, rootX + (i - 1) * dx, top + (i + 1) * dy, splits[i].prime, true);
  }
  node('last', rootX + S * dx, top + S * dy, cur, lastIsPrime);

  const aria = said.length ? `A factor tree for ${n}. ${said.join('. ')}` : `A factor tree starting from ${n}`;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${top + S * dy + 28}`} className={SVG_CLASS} aria-hidden="true">
        {body}
      </svg>
    </Frame>
  );
}

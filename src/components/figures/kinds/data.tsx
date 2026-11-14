'use client';

import type { ReactNode } from 'react';
import type { JourneyFigure, BarChartFigure, TableFigure, VennFigure, BalanceFigure } from '@/lib/figures/types';
import type { KindProps } from './shared';
import { C, Frame, Label, SVG_CLASS, INK_W, HI_W, isOn, text, num, clamp, list, estWidth, tidy } from './shared';

// ══ Journey along a road ═════════════════════════════════════════════════════

export function JourneyKind({ spec, className }: KindProps<JourneyFigure>) {
  const places = list(spec.places);
  const n = places.length;
  if (n < 2) return null;
  const legs = list(spec.legs);
  const hl = spec.highlight;
  const X0 = 34;
  const X1 = 286;
  const Y = 64;
  let longest = 0;
  for (let i = 0; i < n; i++) longest = Math.max(longest, text(places[i]).length);
  const nameSize = n >= 3 && longest > 9 ? 11 : 13;

  const body: ReactNode[] = [];
  const said: string[] = [];
  for (let i = 0; i < n - 1; i++) {
    const xa = X0 + (i * (X1 - X0)) / (n - 1);
    const xb = X0 + ((i + 1) * (X1 - X0)) / (n - 1);
    const on = isOn(hl, `l${i}`);
    const leg = legs[i];
    const topLabel = leg ? text(leg.top) : '';
    const bottomLabel = leg ? text(leg.bottom) : '';
    body.push(<line key={`l${i}`} x1={xa} y1={Y} x2={xb} y2={Y} stroke={on ? C.action : C.ink} strokeWidth={on ? HI_W : INK_W} strokeLinecap="round" />);
    if (topLabel !== '') body.push(<Label key={`t${i}`} x={(xa + xb) / 2} y={Y - 11} fill={on ? C.action : C.ink}>{topLabel}</Label>);
    if (bottomLabel !== '') body.push(<Label key={`b${i}`} x={(xa + xb) / 2} y={Y + 23} fill={on ? C.action : C.ink}>{bottomLabel}</Label>);
    const details: string[] = [];
    if (topLabel !== '') details.push(topLabel);
    if (bottomLabel !== '') details.push(bottomLabel);
    said.push(`${text(places[i])} to ${text(places[i + 1])}${details.length ? `: ${details.join(', ')}` : ''}`);
  }
  for (let i = 0; i < n; i++) {
    const x = X0 + (i * (X1 - X0)) / (n - 1);
    const name = text(places[i]);
    body.push(<circle key={`p${i}`} cx={x} cy={Y} r={7} fill={C.star} stroke={C.ink} strokeWidth={INK_W} />);
    if (name !== '') {
      body.push(
        <Label key={`n${i}`} x={i === 0 ? x - 18 : i === n - 1 ? x + 18 : x} y={24} anchor={i === 0 ? 'start' : i === n - 1 ? 'end' : 'middle'} size={nameSize}>{name}</Label>,
      );
    }
  }

  return (
    <Frame label={`A road. ${said.join('. ')}`} note={spec.note} className={className}>
      <svg viewBox="0 0 320 100" className={SVG_CLASS} aria-hidden="true">
        {body}
      </svg>
    </Frame>
  );
}

// ══ Bar chart and pictograph ═════════════════════════════════════════════════

/** The left part of a counter, for a part-symbol in a pictograph (0 < share < 1). */
function partCounter(cx: number, cy: number, r: number, share: number): string {
  const cos = clamp(1 - 2 * share, -1, 1);
  const x = cx - r * cos;
  const rise = r * Math.sqrt(1 - cos * cos);
  return `M ${x.toFixed(1)} ${(cy - rise).toFixed(1)} A ${r} ${r} 0 ${share > 0.5 ? 1 : 0} 0 ${x.toFixed(1)} ${(cy + rise).toFixed(1)} Z`;
}

interface ChartBar { label: string; value: number; index: number }

export function BarChartKind({ spec, className }: KindProps<BarChartFigure>) {
  const source = list(spec.bars);
  const bars: ChartBar[] = [];
  let top = 0;
  for (let i = 0; i < source.length; i++) {
    const b = source[i];
    if (!b) continue;
    const value = Math.max(0, num(b.value, 0));
    bars.push({ label: text(b.label), value, index: i });
    top = Math.max(top, value);
  }
  const n = bars.length;
  if (n === 0) return null;
  const hl = spec.highlight;
  const unit = text(spec.unit);
  const each = num(spec.each, 0);
  const said: string[] = [];
  for (let i = 0; i < n; i++) said.push(`${bars[i].label}: ${tidy(bars[i].value)}`);

  // ── Pictograph: one row of symbols per bar ──
  if (each > 0) {
    let widest = 0;
    let most = 1;
    for (let i = 0; i < n; i++) {
      widest = Math.max(widest, estWidth(bars[i].label));
      most = Math.max(most, Math.ceil(bars[i].value / each - 1e-9));
    }
    const col = clamp(widest + 12, 34, 124);
    const xs = col + 12;
    const pitch = Math.min(24, (306 - xs) / most);
    const r = Math.max(2, Math.min(9, pitch / 2 - 1.5));
    const rowH = 30;
    const body: ReactNode[] = [];
    for (let i = 0; i < n; i++) {
      const on = isOn(hl, `b${bars[i].index}`);
      const cy = 10 + i * rowH + rowH / 2;
      const count = bars[i].value / each;
      const full = Math.min(80, Math.floor(count + 1e-9));
      const share = count - full;
      body.push(<Label key={`l${i}`} x={col} y={cy + 4.5} anchor="end" fill={on ? C.action : C.ink}>{bars[i].label}</Label>);
      for (let k = 0; k < full; k++) {
        body.push(<circle key={`s${i}-${k}`} cx={xs + pitch / 2 + k * pitch} cy={cy} r={r} fill={on ? C.action : C.star} stroke={C.ink} strokeWidth={1.5} />);
      }
      if (share > 0.02) {
        body.push(
          <path key={`h${i}`} d={partCounter(xs + pitch / 2 + full * pitch, cy, r, share)} fill={on ? C.action : C.star}
            stroke={C.ink} strokeWidth={1.5} strokeLinejoin="round" />,
        );
      }
    }
    const keyY = 10 + n * rowH + 20;
    return (
      <Frame label={`A pictograph. Each symbol stands for ${tidy(each)}${unit ? ` ${unit}` : ''}. ${said.join(', ')}`} note={spec.note} className={className}>
        <svg viewBox={`0 0 320 ${keyY + 16}`} className={SVG_CLASS} aria-hidden="true">
          <line x1={xs - 2} y1={8} x2={xs - 2} y2={12 + n * rowH} stroke={C.ink} strokeWidth={INK_W} strokeLinecap="round" />
          {body}
          <circle cx={xs + 10} cy={keyY} r={9} fill={C.star} stroke={C.ink} strokeWidth={1.5} />
          <Label x={xs + 26} y={keyY + 4.5} anchor="start">= {tidy(each)}{unit ? ` ${unit}` : ''}</Label>
        </svg>
      </Frame>
    );
  }

  // ── Bar chart ──
  const right = 308;
  const topY = 34;
  const base = 184;
  let widest = 0;
  for (let i = 0; i < n; i++) widest = Math.max(widest, estWidth(bars[i].label, 12));
  const tilted = widest > (right - 30) / n - 4;
  const left = tilted ? clamp(widest * 0.77 - (right - 30) / n / 2 + 10, 30, 96) : 30;
  const slot = (right - left) / n;
  const barW = Math.min(46, slot * 0.64);
  const scale = top > 0 ? (base - topY) / top : 0;

  return (
    <Frame label={`A bar chart${unit ? ` in ${unit}` : ''}. ${said.join(', ')}`} note={spec.note} className={className}>
      <svg viewBox={`0 0 320 ${(base + (tilted ? widest * 0.65 + 22 : 28)).toFixed(0)}`} className={SVG_CLASS} aria-hidden="true">
        {unit !== '' && <Label x={8} y={14} anchor="start" size={12} fill={C.muted}>{unit}</Label>}
        {bars.map((bar, i) => {
          const on = isOn(hl, `b${bar.index}`);
          const cx = left + slot * i + slot / 2;
          const h = Math.max(2, bar.value * scale);
          return (
            <g key={i}>
              <rect x={cx - barW / 2} y={base - h} width={barW} height={h} fill={on ? C.action : C.star} stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
              <Label x={cx} y={base - h - 7} fill={on ? C.action : C.ink}>{tidy(bar.value)}</Label>
              {tilted ? (
                <text x={cx + 4} y={base + 14} textAnchor="end" fontSize={12} fontWeight={800} fill={on ? C.action : C.ink} transform={`rotate(-40 ${(cx + 4).toFixed(1)} ${base + 14})`}>
                  {bar.label}
                </text>
              ) : (
                <Label x={cx} y={base + 18} size={12} fill={on ? C.action : C.ink} halo={false}>{bar.label}</Label>
              )}
            </g>
          );
        })}
        <path d={`M ${left} ${topY - 12} L ${left} ${base} L ${right} ${base}`} fill="none" stroke={C.ink} strokeWidth={INK_W} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </Frame>
  );
}

// ══ Table ════════════════════════════════════════════════════════════════════

export function TableKind({ spec, className }: KindProps<TableFigure>) {
  const headers = list(spec.headers);
  const rows = list(spec.rows);
  if (headers.length === 0 && rows.length === 0) return null;
  const hl = spec.highlight;

  const said: string[] = [];
  if (headers.length) said.push(`Headings: ${headers.map((h) => text(h)).join(', ')}`);
  for (let i = 0; i < rows.length; i++) said.push(`Row ${i + 1}: ${list(rows[i]).map((c) => text(c)).join(', ')}`);

  return (
    <Frame label={`A table. ${said.join('. ')}`} note={spec.note} className={className}>
      <table className="w-full max-w-[400px] mx-auto border-collapse text-center" style={{ tableLayout: 'fixed' }} aria-hidden="true">
        {headers.length > 0 && (
          <thead>
            <tr>
              {headers.map((h, i) => (
                <th key={i} className="border-2 border-line bg-soft px-2 py-2 text-[13px] leading-snug font-extrabold text-ink break-words">{text(h)}</th>
              ))}
            </tr>
          </thead>
        )}
        <tbody>
          {rows.map((row, r) => {
            const on = isOn(hl, `r${r}`);
            return (
              <tr key={r}>
                {list(row).map((cell, c) => (
                  <td
                    key={c}
                    className="border-2 border-line px-2 py-2 text-[14px] leading-snug text-ink break-words"
                    style={on ? { backgroundColor: C.actionSoft, color: C.action, fontWeight: 800 } : { backgroundColor: C.card, fontWeight: 700 }}
                  >
                    {text(cell)}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </Frame>
  );
}

// ══ Venn diagram ═════════════════════════════════════════════════════════════

export function VennKind({ spec, className }: KindProps<VennFigure>) {
  const hl = spec.highlight;
  const r = 74;
  const cy = 122;
  const rise = Math.sqrt(r * r - 40 * 40);
  const t = (cy - rise).toFixed(1);
  const b = (cy + rise).toFixed(1);
  const regions = [
    { key: 'left', x: 82, label: text(spec.left), d: `M 160 ${t} A ${r} ${r} 0 1 0 160 ${b} A ${r} ${r} 0 0 1 160 ${t} Z` },
    { key: 'both', x: 160, label: text(spec.both), d: `M 160 ${t} A ${r} ${r} 0 0 1 160 ${b} A ${r} ${r} 0 0 1 160 ${t} Z` },
    { key: 'right', x: 238, label: text(spec.right), d: `M 160 ${t} A ${r} ${r} 0 1 1 160 ${b} A ${r} ${r} 0 0 0 160 ${t} Z` },
  ];
  const leftTitle = text(spec.leftTitle);
  const rightTitle = text(spec.rightTitle);
  const titleSize = Math.max(leftTitle.length, rightTitle.length) > 12 ? 11 : 13;
  const aria = `Two overlapping circles. ${leftTitle || 'Left'} only: ${regions[0].label}. Both: ${regions[1].label}. ${rightTitle || 'Right'} only: ${regions[2].label}`;

  return (
    <Frame label={aria} note={spec.note} className={className}>
      <svg viewBox="0 0 320 210" className={SVG_CLASS} aria-hidden="true">
        {regions.map((region) => (isOn(hl, region.key) ? (
          <path key={region.key} d={region.d} fill={C.actionSoft} />
        ) : null))}
        <circle cx={120} cy={cy} r={r} fill="none" stroke={C.ink} strokeWidth={INK_W} />
        <circle cx={200} cy={cy} r={r} fill="none" stroke={C.ink} strokeWidth={INK_W} />
        {regions.map((region) => (isOn(hl, region.key) ? (
          <path key={region.key} d={region.d} fill="none" stroke={C.action} strokeWidth={4} strokeLinejoin="round" />
        ) : null))}
        {leftTitle !== '' && <Label x={98} y={28} size={titleSize}>{leftTitle}</Label>}
        {rightTitle !== '' && <Label x={222} y={28} size={titleSize}>{rightTitle}</Label>}
        {regions.map((region) => (region.label !== '' ? (
          <Label key={region.key} x={region.x} y={cy + 4.5} size={region.label.length > 8 ? 11 : 13} fill={isOn(hl, region.key) ? C.action : C.ink} halo={false}>
            {region.label}
          </Label>
        ) : null))}
      </svg>
    </Frame>
  );
}

// ══ Balance scale ════════════════════════════════════════════════════════════

export function BalanceKind({ spec, className }: KindProps<BalanceFigure>) {
  const hl = spec.highlight;
  const beamY = 50;
  const panY = 122;
  const pans = [
    { key: 'left', cx: 78, label: text(spec.left) },
    { key: 'right', cx: 242, label: text(spec.right) },
  ];

  return (
    <Frame label={`A balance scale, level. Left pan: ${pans[0].label}. Right pan: ${pans[1].label}`} note={spec.note} className={className}>
      <svg viewBox="0 0 320 196" className={SVG_CLASS} aria-hidden="true">
        <line x1={160} y1={beamY} x2={160} y2={160} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />
        <polygon points="160,146 132,178 188,178" fill={C.ink} stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
        <line x1={78} y1={beamY} x2={242} y2={beamY} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />
        <circle cx={160} cy={beamY} r={6} fill={C.star} stroke={C.ink} strokeWidth={INK_W} />
        {pans.map((pan) => {
          const on = isOn(hl, pan.key);
          const w = clamp(estWidth(pan.label) + 24, 58, 132);
          return (
            <g key={pan.key}>
              <line x1={pan.cx} y1={beamY} x2={pan.cx - 56} y2={panY} stroke={C.ink} strokeWidth={2} />
              <line x1={pan.cx} y1={beamY} x2={pan.cx + 56} y2={panY} stroke={C.ink} strokeWidth={2} />
              <path d={`M ${pan.cx - 62} ${panY} Q ${pan.cx} ${panY + 26} ${pan.cx + 62} ${panY} Z`} fill={C.soft} stroke={C.ink} strokeWidth={INK_W} strokeLinejoin="round" />
              {pan.label !== '' && (
                <g>
                  <rect x={pan.cx - w / 2} y={panY - 37} width={w} height={36} rx={8} fill={on ? C.action : C.star} stroke={C.ink} strokeWidth={INK_W} />
                  <Label x={pan.cx} y={panY - 14.5} size={estWidth(pan.label) > 112 ? 11 : 13} fill={on ? C.card : C.ink} halo={false}>{pan.label}</Label>
                </g>
              )}
            </g>
          );
        })}
      </svg>
    </Frame>
  );
}

'use client';

import type { ReactNode } from 'react';

/** Design-token colours (design/tokens.json) for SVG fills and strokes. */
export const C = {
  ink: '#1d2a4d',
  muted: '#5d6b8c',
  line: '#d3deee',
  soft: '#eef3fb',
  card: '#ffffff',
  action: '#4f46e5',
  actionSoft: '#e0e7ff',
  success: '#12805c',
  successSoft: '#dff6ea',
  star: '#f5a400',
  hint: '#fff1b8',
};

export function range(n: number): number[] {
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(i);
  return out;
}

export function gcd(a: number, b: number): number {
  let x = Math.abs(a);
  let y = Math.abs(b);
  while (y) {
    const t = y;
    y = x % y;
    x = t;
  }
  return x || 1;
}

/** Indian-style digit grouping: 2,34,567. */
export function fmt(n: number): string {
  return n.toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

/** A labelled number in a soft tile. */
export function Stat({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="flex-1 min-w-[92px] bg-soft border-2 border-line rounded-tile px-3 py-2 text-center">
      <p className="text-caption text-ink-muted">{label}</p>
      <p className="font-display text-title text-ink">{value}</p>
    </div>
  );
}

/** The line of maths that the picture shows. */
export function Working({ children }: { children: ReactNode }) {
  return (
    <p className="bg-soft rounded-note border-l-[6px] border-action px-3 py-2 text-label text-ink" aria-live="polite">
      {children}
    </p>
  );
}

const roundBtn =
  'w-12 h-12 flex-shrink-0 rounded-control border-2 border-ink bg-white text-ink text-xl font-extrabold shadow-hard-sm disabled:opacity-40 active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]';

/** − value + control with 48px targets. */
export function Stepper({ label, value, min, max, onChange }: {
  label: string; value: number; min: number; max: number; onChange: (v: number) => void;
}) {
  return (
    <div className="flex items-center gap-2">
      <button type="button" className={roundBtn} disabled={value <= min} onClick={() => onChange(value - 1)} aria-label={`One fewer ${label}`}>
        <span aria-hidden="true">−</span>
      </button>
      <div className="flex-1 text-center">
        <p className="font-display text-title text-ink leading-none">{value}</p>
        <p className="text-caption text-ink-muted mt-0.5">{label}</p>
      </div>
      <button type="button" className={roundBtn} disabled={value >= max} onClick={() => onChange(value + 1)} aria-label={`One more ${label}`}>
        <span aria-hidden="true">+</span>
      </button>
    </div>
  );
}

/** A labelled slider. */
export function Slider({ label, value, min, max, step = 1, onChange, display }: {
  label: string; value: number; min: number; max: number; step?: number;
  onChange: (v: number) => void; display?: string;
}) {
  return (
    <label className="block">
      <span className="flex items-baseline justify-between">
        <span className="text-caption text-ink-muted">{label}</span>
        <span className="text-label text-ink">{display ?? value}</span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-12 accent-action cursor-pointer"
      />
    </label>
  );
}

/** A two-or-more way switch (e.g. Area / Perimeter). */
export function Toggle<T extends string>({ options, value, onChange }: {
  options: Array<{ value: T; label: string }>; value: T; onChange: (v: T) => void;
}) {
  return (
    <div className="flex gap-2" role="group">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          aria-pressed={value === o.value}
          onClick={() => onChange(o.value)}
          className={`flex-1 min-h-[48px] rounded-control border-2 font-extrabold text-[15px] transition-colors ${
            value === o.value ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink hover:border-ink'
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

'use client';

import React from 'react';
import type { PartitionFigure } from '@/lib/handsOn/partition';
import { C } from '@/components/visuals/parts';

/** Text with fractions such as 3/4 set as a stacked fraction. */
export function MathText({ text }: { text: string }) {
  const parts = text.split(/(\d+\/\d+)/);
  return (
    <>
      {parts.map((part, i) => {
        const m = /^(\d+)\/(\d+)$/.exec(part);
        if (!m) return <React.Fragment key={i}>{part}</React.Fragment>;
        return (
          <span key={i} className="inline-flex flex-col items-center align-middle mx-0.5 leading-none text-[0.82em] font-extrabold" role="img" aria-label={`${m[1]} over ${m[2]}`}>
            <span aria-hidden="true" className="px-0.5 pb-px">{m[1]}</span>
            <span aria-hidden="true" className="px-0.5 pt-px border-t-2 border-current">{m[2]}</span>
          </span>
        );
      })}
    </>
  );
}

interface PartitionShapeProps {
  figure: PartitionFigure;
  shaded: boolean[];
  /** Fill for coloured pieces. */
  fill: string;
  /** Given: pieces can be tapped. Omitted: a still picture. */
  onToggle?: (index: number) => void;
  /** Longest side of the drawing in pixels. */
  size?: number;
  label: string;
}

/**
 * A shape cut into pieces. Each piece is a button when the figure is
 * interactive, so it works with touch, mouse and keyboard.
 */
export default function PartitionShape({ figure, shaded, fill, onToggle, size = 240, label }: PartitionShapeProps) {
  const unit = size / Math.max(figure.w, figure.h);
  const pad = 3;
  const width = figure.w * unit + pad * 2;
  const height = figure.h * unit + pad * 2;
  const pts = (piece: number[][]) => piece.map((p) => `${pad + p[0] * unit},${pad + p[1] * unit}`).join(' ');

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      className="max-w-full h-auto select-none hands-on-shape"
      role="group"
      aria-label={label}
    >
      {figure.pieces.map((piece, i) => {
        const on = !!shaded[i];
        const common = {
          points: pts(piece),
          fill: on ? fill : C.card,
          stroke: C.ink,
          strokeWidth: 2.5,
          strokeLinejoin: 'round' as const,
          style: { transition: 'fill 0.15s ease-out' },
        };
        if (!onToggle) return <polygon key={i} {...common} />;
        return (
          <polygon
            key={i}
            {...common}
            className={on ? 'cursor-pointer' : 'cursor-pointer hands-on-piece'}
            role="button"
            tabIndex={0}
            aria-pressed={on}
            aria-label={`Part ${i + 1} of ${figure.pieces.length}`}
            onClick={() => onToggle(i)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onToggle(i);
              }
            }}
          />
        );
      })}
    </svg>
  );
}

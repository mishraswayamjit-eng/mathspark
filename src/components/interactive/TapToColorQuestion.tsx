'use client';

import React, { useState, useCallback } from 'react';
import type { TapToColorData } from '@/types';
import DuoButton from '@/components/DuoButton';

interface Props {
  data: TapToColorData;
  answered: boolean;
  onSubmit: (answer: string, isCorrect: boolean) => void;
}

// ── SVG colors ───────────────────────────────────────────────────────────────
const SELECTED = 'rgba(88, 204, 2, 0.35)';    // duo-green translucent
const CORRECT  = 'rgba(88, 204, 2, 0.5)';
const WRONG    = 'rgba(255, 75, 75, 0.4)';
const UNSHADED = '#F3F4F6';
const STROKE   = '#9CA3AF';

export default function TapToColorQuestion({ data, answered, onSubmit }: Props) {
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [result, setResult] = useState<'correct' | 'wrong' | null>(null);

  const toggle = useCallback((idx: number) => {
    if (answered) return;
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }, [answered]);

  const handleCheck = () => {
    if (answered) return;
    const answer = JSON.stringify([...selected].sort((a, b) => a - b));
    let isCorrect: boolean;
    if (data.correctIndices) {
      const expected = [...data.correctIndices].sort((a, b) => a - b);
      const sorted = [...selected].sort((a, b) => a - b);
      isCorrect = sorted.length === expected.length && sorted.every((v, i) => v === expected[i]);
    } else {
      isCorrect = selected.size === data.correctCount;
    }
    setResult(isCorrect ? 'correct' : 'wrong');
    onSubmit(answer, isCorrect);
  };

  const getFill = (idx: number) => {
    if (result) {
      const isInCorrectSet = data.correctIndices
        ? data.correctIndices.includes(idx)
        : idx < data.correctCount;
      if (selected.has(idx)) {
        return isInCorrectSet ? CORRECT : WRONG;
      }
      // Show missed correct regions
      if (isInCorrectSet && result === 'wrong') return CORRECT;
      return UNSHADED;
    }
    return selected.has(idx) ? SELECTED : UNSHADED;
  };

  // ── Rectangle grid ─────────────────────────────────────────────────────────
  if (data.shape === 'rectangle') {
    const columns = data.columns ?? 4;
    const rows = Math.ceil(data.totalParts / columns);
    const cellW = 240 / columns;
    const cellH = Math.min(50, 160 / rows);
    const w = columns * cellW + 8;
    const h = rows * cellH + 8;

    return (
      <div className="space-y-3">
        {data.label && (
          <p className="text-sm font-semibold text-gray-600 text-center">{data.label}</p>
        )}
        <svg viewBox={`0 0 ${w} ${h}`} className="w-full max-w-[320px] mx-auto" role="img" aria-label="Tap to shade parts">
          {Array.from({ length: data.totalParts }, (_, i) => {
            const col = i % columns;
            const row = Math.floor(i / columns);
            return (
              <rect
                key={i}
                x={4 + col * cellW}
                y={4 + row * cellH}
                width={cellW - 2}
                height={cellH - 2}
                rx={4}
                fill={getFill(i)}
                stroke={selected.has(i) && !result ? '#58CC02' : STROKE}
                strokeWidth={selected.has(i) && !result ? 2 : 1.5}
                className="cursor-pointer"
                onClick={() => toggle(i)}
                role="button"
                aria-label={`Part ${i + 1}${selected.has(i) ? ' (selected)' : ''}`}
              />
            );
          })}
        </svg>
        <p className="text-xs text-gray-500 text-center font-medium">
          {selected.size} / {data.correctCount} parts selected
        </p>
        {!answered && (
          <DuoButton
            variant="green"
            fullWidth
            onClick={handleCheck}
            disabled={selected.size === 0}
          >
            Check Answer
          </DuoButton>
        )}
      </div>
    );
  }

  // ── Circle pie ─────────────────────────────────────────────────────────────
  const cx = 80, cy = 80, r = 65;
  const angleStep = (2 * Math.PI) / data.totalParts;

  function slicePath(i: number) {
    const a1 = i * angleStep - Math.PI / 2;
    const a2 = (i + 1) * angleStep - Math.PI / 2;
    const x1 = cx + r * Math.cos(a1);
    const y1 = cy + r * Math.sin(a1);
    const x2 = cx + r * Math.cos(a2);
    const y2 = cy + r * Math.sin(a2);
    const large = angleStep > Math.PI ? 1 : 0;
    return `M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${large},1 ${x2},${y2} Z`;
  }

  return (
    <div className="space-y-3">
      {data.label && (
        <p className="text-sm font-semibold text-gray-600 text-center">{data.label}</p>
      )}
      <svg viewBox="0 0 160 160" className="w-40 h-40 mx-auto" role="img" aria-label="Tap to shade parts of circle">
        {Array.from({ length: data.totalParts }, (_, i) => (
          <path
            key={i}
            d={slicePath(i)}
            fill={getFill(i)}
            stroke={selected.has(i) && !result ? '#58CC02' : STROKE}
            strokeWidth={selected.has(i) && !result ? 2 : 1}
            className="cursor-pointer"
            onClick={() => toggle(i)}
            role="button"
            aria-label={`Slice ${i + 1}${selected.has(i) ? ' (selected)' : ''}`}
          />
        ))}
      </svg>
      <p className="text-xs text-gray-500 text-center font-medium">
        {selected.size} / {data.correctCount} parts selected
      </p>
      {!answered && (
        <DuoButton
          variant="green"
          fullWidth
          onClick={handleCheck}
          disabled={selected.size === 0}
        >
          Check Answer
        </DuoButton>
      )}
    </div>
  );
}

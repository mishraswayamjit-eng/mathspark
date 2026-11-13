'use client';

import React, { useRef, useState } from 'react';
import type { NumberLineData } from '@/types';
import DuoButton from '@/components/DuoButton';
import { isNumberLineCorrect } from '@/lib/interactiveGrading';

interface Props {
  data: NumberLineData;
  answered: boolean;
  onSubmit: (answer: string, isCorrect: boolean) => void;
}

// SVG geometry (viewBox units)
const VIEW_W  = 320;
const VIEW_H  = 96;
const PAD_X   = 22;
const LINE_Y  = 44;
const TRACK_W = VIEW_W - PAD_X * 2;

// Token colours (design/tokens.json) for SVG fills and strokes
const INK     = '#1d2a4d';
const MUTED   = '#5d6b8c';
const ACTION  = '#4f46e5';
const SUCCESS = '#12805c';
const RETRY   = '#c62f3d';

function decimalsOf(step: number): number {
  const text = String(step);
  const dot = text.indexOf('.');
  return dot === -1 ? 0 : text.length - dot - 1;
}

/**
 * Draggable number line: drag the point (or tap the line, or use the − / +
 * buttons) to a position, then check. The point snaps to every `step`.
 */
export default function NumberLineQuestion({ data, answered, onSubmit }: Props) {
  const stepCount = Math.max(1, Math.round((data.max - data.min) / data.step));
  const decimals  = decimalsOf(data.step);
  const labelEvery = data.labelEvery && data.labelEvery > 0
    ? data.labelEvery
    : Math.max(1, Math.ceil(stepCount / 10));

  // Position is held as a whole number of steps from `min`, so there is no float drift.
  const [pos, setPos] = useState<number>(0);
  const [moved, setMoved] = useState(false);
  const [result, setResult] = useState<boolean | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const draggingRef = useRef(false);

  const locked = answered || result !== null;

  const valueAt = (p: number) => Number((data.min + p * data.step).toFixed(decimals));
  const xAt     = (p: number) => PAD_X + (p / stepCount) * TRACK_W;
  const correctPos = Math.round((data.correctValue - data.min) / data.step);

  function movePointTo(clientX: number) {
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    if (rect.width === 0) return;
    const viewX = ((clientX - rect.left) / rect.width) * VIEW_W;
    const raw   = ((viewX - PAD_X) / TRACK_W) * stepCount;
    const next  = Math.min(stepCount, Math.max(0, Math.round(raw)));
    setPos(next);
    setMoved(true);
  }

  function handlePointerDown(e: React.PointerEvent<SVGSVGElement>) {
    if (locked) return;
    draggingRef.current = true;
    e.currentTarget.setPointerCapture(e.pointerId);
    movePointTo(e.clientX);
  }

  function handlePointerMove(e: React.PointerEvent<SVGSVGElement>) {
    if (locked || !draggingRef.current) return;
    movePointTo(e.clientX);
  }

  function handlePointerUp() {
    draggingRef.current = false;
  }

  function nudge(delta: number) {
    if (locked) return;
    setPos((p) => Math.min(stepCount, Math.max(0, p + delta)));
    setMoved(true);
  }

  function handleCheck() {
    if (locked || !moved) return;
    const value = valueAt(pos);
    const isCorrect = isNumberLineCorrect(data, value);
    setResult(isCorrect);
    onSubmit(JSON.stringify(value), isCorrect);
  }

  const pointColour = result === null ? ACTION : result ? SUCCESS : RETRY;

  const ticks: number[] = [];
  for (let p = 0; p <= stepCount; p++) ticks.push(p);

  return (
    <div className="space-y-3">
      {data.instruction && (
        <p className="text-sm font-bold text-ink-muted text-center">{data.instruction}</p>
      )}

      <div className="ui-card">
        <svg
          ref={svgRef}
          viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
          className="w-full h-auto select-none"
          style={{ touchAction: locked ? 'auto' : 'none', cursor: locked ? 'default' : 'pointer' }}
          role="img"
          aria-label={`Number line from ${data.min} to ${data.max}`}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
        >
          {/* Line */}
          <line x1={PAD_X} y1={LINE_Y} x2={VIEW_W - PAD_X} y2={LINE_Y} stroke={INK} strokeWidth={3} strokeLinecap="round" />

          {/* Ticks and labels */}
          {ticks.map((p) => {
            const major = p % labelEvery === 0 || p === stepCount;
            const x = xAt(p);
            return (
              <g key={p}>
                <line
                  x1={x} y1={LINE_Y - (major ? 9 : 5)}
                  x2={x} y2={LINE_Y + (major ? 9 : 5)}
                  stroke={major ? INK : MUTED}
                  strokeWidth={major ? 2 : 1.5}
                />
                {major && (
                  <text x={x} y={LINE_Y + 28} textAnchor="middle" fontSize={13} fontWeight={800} fill={INK}>
                    {valueAt(p)}
                  </text>
                )}
              </g>
            );
          })}

          {/* Where it should have gone (only after a not-quite answer) */}
          {result === false && (
            <circle cx={xAt(correctPos)} cy={LINE_Y} r={11} fill="#dff6ea" stroke={SUCCESS} strokeWidth={3} />
          )}

          {/* The student's point */}
          <circle cx={xAt(pos)} cy={LINE_Y} r={11} fill={pointColour} stroke={INK} strokeWidth={2.5} />
        </svg>

        {!data.hideValue && (
          <p className="text-center text-label text-ink mt-1" aria-live="polite">
            {moved ? `Your point is at ${valueAt(pos)}` : 'Drag the point along the line'}
          </p>
        )}
      </div>

      {result === false && (
        <div className="bg-success-soft border-2 border-success rounded-note px-3 py-2">
          <p className="text-label text-ink">
            The right spot is <span className="font-extrabold text-success">{valueAt(correctPos)}</span>, shown by the green ring.
          </p>
        </div>
      )}

      {!locked && (
        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={() => nudge(-1)}
            disabled={pos === 0}
            aria-label="Move the point one step left"
            className="w-12 h-12 flex-shrink-0 rounded-control border-2 border-ink bg-white text-ink text-xl font-extrabold shadow-hard-sm disabled:opacity-40 active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]"
          >
            <span aria-hidden="true">◀</span>
          </button>
          <div className="flex-1">
            <DuoButton variant="green" fullWidth onClick={handleCheck} disabled={!moved}>
              Check
            </DuoButton>
          </div>
          <button
            type="button"
            onClick={() => nudge(1)}
            disabled={pos === stepCount}
            aria-label="Move the point one step right"
            className="w-12 h-12 flex-shrink-0 rounded-control border-2 border-ink bg-white text-ink text-xl font-extrabold shadow-hard-sm disabled:opacity-40 active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]"
          >
            <span aria-hidden="true">▶</span>
          </button>
        </div>
      )}
    </div>
  );
}

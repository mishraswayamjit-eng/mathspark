'use client';

import React, { useState, useRef, useCallback } from 'react';
import type { DragToSortData } from '@/types';
import DuoButton from '@/components/DuoButton';

interface Props {
  data: DragToSortData;
  answered: boolean;
  onSubmit: (answer: string, isCorrect: boolean) => void;
}

// ── Colors ───────────────────────────────────────────────────────────────────
const CORRECT_BG = 'bg-green-50 border-duo-green';
const WRONG_BG   = 'bg-red-50 border-duo-red';
const NEUTRAL_BG = 'bg-white border-gray-200';

export default function DragToSortQuestion({ data, answered, onSubmit }: Props) {
  // order[i] = index into data.items
  const [order, setOrder] = useState<number[]>(() =>
    data.items.map((_, i) => i),
  );
  const [result, setResult] = useState<boolean[] | null>(null);
  const [dragIdx, setDragIdx] = useState<number | null>(null);
  const touchStart = useRef<{ idx: number; y: number } | null>(null);
  const [dragOffset, setDragOffset] = useState(0);
  const prefersReducedMotion = typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const swap = useCallback((from: number, to: number) => {
    if (answered || to < 0 || to >= order.length) return;
    setOrder((prev) => {
      const next = [...prev];
      [next[from], next[to]] = [next[to], next[from]];
      return next;
    });
  }, [answered, order.length]);

  const handleCheck = () => {
    if (answered) return;
    const isCorrect = order.every((v, i) => v === data.correctOrder[i]);
    const perItem = order.map((v, i) => v === data.correctOrder[i]);
    setResult(perItem);
    onSubmit(JSON.stringify(order), isCorrect);
  };

  // ── Touch drag handlers ────────────────────────────────────────────────────
  const handleTouchStart = (idx: number, e: React.TouchEvent) => {
    if (answered || prefersReducedMotion) return;
    touchStart.current = { idx, y: e.touches[0].clientY };
    setDragIdx(idx);
    setDragOffset(0);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!touchStart.current || answered) return;
    e.preventDefault();
    const dy = e.touches[0].clientY - touchStart.current.y;
    setDragOffset(dy);
  };

  const handleTouchEnd = () => {
    if (!touchStart.current || answered) return;
    const { idx } = touchStart.current;
    // If dragged more than half a row height, swap
    const threshold = 28;
    if (dragOffset > threshold && idx < order.length - 1) {
      swap(idx, idx + 1);
    } else if (dragOffset < -threshold && idx > 0) {
      swap(idx, idx - 1);
    }
    touchStart.current = null;
    setDragIdx(null);
    setDragOffset(0);
  };

  const getItemBg = (pos: number) => {
    if (!result) return NEUTRAL_BG;
    return result[pos] ? CORRECT_BG : WRONG_BG;
  };

  return (
    <div className="space-y-3">
      {data.instruction && (
        <p className="text-sm font-semibold text-gray-600 text-center">{data.instruction}</p>
      )}

      <div
        className="space-y-2"
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {order.map((itemIdx, pos) => {
          const isDragging = dragIdx === pos;
          return (
            <div
              key={itemIdx}
              className={`flex items-center gap-2 rounded-2xl px-4 py-3 border-2 transition-colors ${getItemBg(pos)} ${
                isDragging ? 'shadow-lg z-10 relative' : ''
              }`}
              style={{
                transform: isDragging ? `translateY(${dragOffset}px)` : undefined,
                transition: isDragging ? 'none' : 'transform 150ms ease',
              }}
              onTouchStart={(e) => handleTouchStart(pos, e)}
            >
              {/* Position number */}
              <span className="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center text-xs font-extrabold text-gray-600 flex-shrink-0">
                {pos + 1}
              </span>

              {/* Item text */}
              <span className="flex-1 text-base font-semibold text-gray-800">
                {data.items[itemIdx]}
              </span>

              {/* Swap buttons (a11y fallback) */}
              {!answered && (
                <div className="flex flex-col gap-0.5 flex-shrink-0">
                  <button
                    onClick={() => swap(pos, pos - 1)}
                    disabled={pos === 0}
                    className="w-7 h-7 rounded-lg bg-gray-100 flex items-center justify-center text-gray-500 disabled:opacity-30 active:bg-gray-200 transition-colors min-h-0"
                    aria-label={`Move ${data.items[itemIdx]} up`}
                  >
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M6 2L2 7h8L6 2z" fill="currentColor" />
                    </svg>
                  </button>
                  <button
                    onClick={() => swap(pos, pos + 1)}
                    disabled={pos === order.length - 1}
                    className="w-7 h-7 rounded-lg bg-gray-100 flex items-center justify-center text-gray-500 disabled:opacity-30 active:bg-gray-200 transition-colors min-h-0"
                    aria-label={`Move ${data.items[itemIdx]} down`}
                  >
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M6 10L2 5h8L6 10z" fill="currentColor" />
                    </svg>
                  </button>
                </div>
              )}

              {/* Result indicator */}
              {result && (
                <span className={`text-lg font-bold flex-shrink-0 ${result[pos] ? 'text-duo-green' : 'text-duo-red'}`}>
                  {result[pos] ? '✓' : '✗'}
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Show correct order on wrong answer */}
      {result && !result.every(Boolean) && (
        <div className="bg-green-50 border border-green-200 rounded-xl px-3 py-2">
          <p className="text-xs font-extrabold text-green-700 mb-1">Correct order:</p>
          <p className="text-sm text-green-800 font-semibold">
            {data.correctOrder.map((idx) => data.items[idx]).join(' → ')}
          </p>
        </div>
      )}

      {!answered && (
        <DuoButton variant="green" fullWidth onClick={handleCheck}>
          Check Order
        </DuoButton>
      )}
    </div>
  );
}

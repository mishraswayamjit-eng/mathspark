'use client';

import React from 'react';
import { HEARTS_MAX, type QuestionResult } from './constants';

/**
 * The hearts left. `compact` (for a crowded header) shows one heart and the
 * number on phones, and the usual row of hearts from 640px up.
 */
export function HeartsBar({ hearts, max = HEARTS_MAX, compact }: { hearts: number; max?: number; compact?: boolean }) {
  const row = (
    <div className={compact ? 'hidden sm:flex items-center gap-0.5' : 'flex items-center gap-0.5'}>
      {Array.from({ length: max }, (_, i) => (
        <span
          key={i}
          className="text-base transition-opacity duration-300"
          style={{ opacity: i < hearts ? 1 : 0.18, filter: i < hearts ? 'none' : 'grayscale(1)' }}
        >
          ❤️
        </span>
      ))}
    </div>
  );
  if (!compact) return row;
  return (
    <div className="flex-shrink-0" role="img" aria-label={`${Math.max(0, hearts)} of ${max} hearts left`}>
      <div className="flex sm:hidden items-center gap-1 text-white font-extrabold text-[15px] leading-none">
        <span className="text-base" aria-hidden="true">❤️</span>
        <span aria-hidden="true">{Math.max(0, hearts)}</span>
      </div>
      {row}
    </div>
  );
}

export const LessonJourney = React.memo(function LessonJourney({
  total,
  currentIdx,
  results,
}: {
  total: number;
  currentIdx: number;
  results: QuestionResult[];
}) {
  return (
    <div className="flex items-center px-4 py-3 gap-0">
      {Array.from({ length: total }, (_, i) => {
        const result    = results[i];
        const isDone    = result !== undefined;
        const isCurrent = i === currentIdx;
        const isCorrect = result?.wasCorrect;

        const circleCls = isDone
          ? isCorrect
            ? 'bg-success-soft border-success text-success'
            : 'bg-retry-soft border-retry text-retry'
          : isCurrent
          ? 'bg-white border-ink text-ink shadow-[2px_2px_0_#1d2a4d]'
          : 'bg-white border-line text-ink-muted';

        const lineCls = i < currentIdx || isDone ? 'bg-action' : 'bg-line';

        return (
          <div key={i} className="flex items-center flex-1 min-w-0">
            {i > 0 && (
              <div className={`h-1 flex-1 rounded-full transition-colors duration-500 ${lineCls}`} />
            )}
            <div
              className={`w-7 h-7 rounded-[9px] border-2 flex items-center justify-center text-xs font-extrabold flex-shrink-0 transition-colors duration-300 ${circleCls}`}
            >
              {isDone ? (isCorrect ? '✓' : '✗') : i + 1}
            </div>
          </div>
        );
      })}
    </div>
  );
});

export const LessonProgressBar = React.memo(function LessonProgressBar({
  total,
  currentIdx,
  results,
  compact,
}: {
  total: number;
  currentIdx: number;
  results: QuestionResult[];
  /** No padding of its own and a slightly thinner bar, to sit inside a strip. */
  compact?: boolean;
}) {
  const pct = total > 0 ? (currentIdx / total) * 100 : 0;

  return (
    <div
      className={compact ? 'w-full' : 'px-4 py-3'}
      role="progressbar"
      aria-label="Session progress"
      aria-valuemin={0}
      aria-valuemax={total}
      aria-valuenow={Math.min(total, currentIdx)}
    >
      <div className={`relative ${compact ? 'h-3' : 'h-3.5'} ui-meter`}>
        {/* Fill */}
        <div
          className="absolute inset-y-0 left-0 bg-action rounded-full transition-[width] duration-700"
          style={{ width: `${pct}%` }}
        />
        {/* Section dots */}
        {Array.from({ length: total - 1 }, (_, i) => {
          const dotPct = ((i + 1) / total) * 100;
          const isDone = results[i] !== undefined;
          return (
            <div
              key={i}
              className={`absolute top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full ${
                isDone ? 'bg-white/70' : 'bg-line'
              }`}
              style={{ left: `${dotPct}%`, marginLeft: '-3px' }}
            />
          );
        })}
      </div>
    </div>
  );
});

export function XpFloat({ amount }: { amount: number }) {
  return (
    <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[70] pointer-events-none">
      <span className="animate-xp-float font-display text-2xl font-bold text-ink bg-star border-2 border-ink rounded-full px-4 py-1 whitespace-nowrap">
        +{amount} XP ⭐
      </span>
    </div>
  );
}

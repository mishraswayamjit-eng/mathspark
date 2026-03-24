'use client';

import React from 'react';
import { HEARTS_MAX, type QuestionResult } from './constants';

export function HeartsBar({ hearts, max = HEARTS_MAX }: { hearts: number; max?: number }) {
  return (
    <div className="flex items-center gap-0.5">
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
            ? 'bg-duo-green border-duo-green-dark text-white'
            : 'bg-duo-red border-duo-red-dark text-white'
          : isCurrent
          ? 'bg-duo-blue border-duo-blue-dark text-white ring-4 ring-blue-100 animate-pulse'
          : 'bg-white border-gray-200 text-gray-500';

        const lineCls = i < currentIdx || isDone ? 'bg-duo-green' : 'bg-gray-200';

        return (
          <div key={i} className="flex items-center flex-1 min-w-0">
            {i > 0 && (
              <div className={`h-1 flex-1 rounded-full transition-colors duration-500 ${lineCls}`} />
            )}
            <div
              className={`w-7 h-7 rounded-full border-2 flex items-center justify-center text-[10px] font-extrabold flex-shrink-0 transition-colors duration-300 ${circleCls}`}
            >
              {isDone ? (isCorrect ? '✓' : '✗') : i + 1}
            </div>
          </div>
        );
      })}
    </div>
  );
});

export function XpFloat({ amount }: { amount: number }) {
  return (
    <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[70] pointer-events-none">
      <span className="animate-xp-float text-2xl font-extrabold text-duo-gold drop-shadow-lg whitespace-nowrap">
        +{amount} XP ⭐
      </span>
    </div>
  );
}

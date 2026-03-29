'use client';

import React, { useState, useEffect, useRef } from 'react';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';

interface XPBreakdown {
  total: number;
  base: number;
  scoreBonus: number;
  firstTimeBonus: number;
  perfectBonus: number;
}

interface LessonCompleteProps {
  score: number;
  total: number;
  xp: XPBreakdown | null;
  isFirstTime: boolean;
  accentColor: string;
  onBackToLevels: () => void;
  onReview: () => void;
}

export default function LessonComplete({
  score,
  total,
  xp,
  isFirstTime,
  accentColor,
  onBackToLevels,
  onReview,
}: LessonCompleteProps) {
  const pct = Math.round((score / total) * 100);
  const passed = pct >= 75;
  const isPerfect = pct === 100;
  const [showConfetti, setShowConfetti] = useState(passed && (isFirstTime || isPerfect));
  const [animatedPct, setAnimatedPct] = useState(0);
  const timerRef = useRef<ReturnType<typeof setTimeout>>();

  // Animate percentage bar
  useEffect(() => {
    timerRef.current = setTimeout(() => setAnimatedPct(pct), 200);
    return () => clearTimeout(timerRef.current);
  }, [pct]);

  return (
    <div className="flex flex-col items-center gap-5 animate-fade-in py-4">
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* Sparky */}
      <div className="animate-sparky-bounce">
        <Sparky
          mood={passed ? 'celebrating' : 'encouraging'}
          size={96}
        />
      </div>

      {/* Message */}
      <div className="text-center">
        <h2 className="text-xl font-extrabold text-gray-800 mb-1">
          {isPerfect ? 'Perfect Score!' : passed ? 'Great Job!' : 'Keep Practicing!'}
        </h2>
        <p className="text-sm text-gray-500 font-semibold">
          {passed
            ? 'You can move on to the next level!'
            : 'Review the lessons and try again.'}
        </p>
      </div>

      {/* Score display */}
      <div className="w-full max-w-xs">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-bold text-gray-600">Score</span>
          <span className="text-sm font-extrabold" style={{ color: accentColor }}>
            {score}/{total} ({pct}%)
          </span>
        </div>
        <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-1000 ease-out"
            style={{
              width: `${animatedPct}%`,
              backgroundColor: passed ? '#58CC02' : '#FF9600',
            }}
          />
        </div>
        {pct < 75 && (
          <p className="text-xs text-gray-400 font-semibold mt-1 text-center">
            75% needed to pass
          </p>
        )}
      </div>

      {/* XP breakdown */}
      {xp && xp.total > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl px-5 py-4 w-full max-w-xs">
          <p className="text-sm font-extrabold text-amber-800 mb-2 text-center">
            <span aria-hidden="true">⭐ </span>+{xp.total} XP earned!
          </p>
          <div className="space-y-1">
            <div className="flex justify-between text-xs text-amber-700">
              <span>Completion</span>
              <span className="font-bold">+{xp.base}</span>
            </div>
            {xp.scoreBonus > 0 && (
              <div className="flex justify-between text-xs text-amber-700">
                <span>Score bonus</span>
                <span className="font-bold">+{xp.scoreBonus}</span>
              </div>
            )}
            {xp.firstTimeBonus > 0 && (
              <div className="flex justify-between text-xs text-amber-700">
                <span>First time!</span>
                <span className="font-bold">+{xp.firstTimeBonus}</span>
              </div>
            )}
            {xp.perfectBonus > 0 && (
              <div className="flex justify-between text-xs text-amber-700">
                <span>Perfect score!</span>
                <span className="font-bold">+{xp.perfectBonus}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-3 w-full max-w-xs">
        <button
          onClick={onReview}
          className="flex-1 py-3 rounded-2xl text-sm font-extrabold border-2 border-gray-200 text-gray-600 active:scale-95 transition-transform"
        >
          Review Lessons
        </button>
        <button
          onClick={onBackToLevels}
          className="flex-1 py-3 rounded-2xl text-sm font-extrabold text-white active:scale-95 transition-transform"
          style={{ backgroundColor: accentColor }}
        >
          Back to Levels
        </button>
      </div>
    </div>
  );
}

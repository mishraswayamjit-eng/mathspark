'use client';

import React, { useState, useCallback } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import type { LessonStep } from '@/types/lesson';

interface LessonStepperProps {
  steps: LessonStep[];
  onDone: () => void;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

export default function LessonStepper({ steps, onDone }: LessonStepperProps) {
  const [current, setCurrent] = useState(0);
  const step = steps[current];
  const isLast = current === steps.length - 1;

  const next = useCallback(() => {
    if (isLast) {
      onDone();
    } else {
      setCurrent((c) => c + 1);
    }
  }, [isLast, onDone]);

  const back = useCallback(() => {
    setCurrent((c) => Math.max(0, c - 1));
  }, []);

  return (
    <div className="animate-fade-in">
      {/* Step counter dots */}
      <div className="flex items-center justify-center gap-1.5 mb-4">
        {steps.map((_, i) => (
          <div
            key={i}
            className={`h-2 rounded-full transition-all duration-300 ${
              i === current
                ? 'w-6 bg-duo-blue'
                : i < current
                ? 'w-2 bg-duo-green'
                : 'w-2 bg-gray-200'
            }`}
          />
        ))}
      </div>

      {/* Step label */}
      <p className="text-xs font-bold text-gray-400 text-center mb-3">
        Step {current + 1} of {steps.length}
      </p>

      {/* Step content */}
      <div key={current} className="animate-fade-in">
        <p className="text-sm font-semibold text-gray-800 leading-relaxed mb-3">
          {step.text}
        </p>

        {/* Notation box */}
        {step.notation && (
          <div className="bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-3 mb-3 text-center">
            {hasLatex(step.notation) ? (
              <KatexRenderer latex={step.notation} displayMode className="text-base" />
            ) : (
              <p className="text-base font-bold text-indigo-800 font-mono">
                {step.notation}
              </p>
            )}
          </div>
        )}

        {/* Tip callout (shown on last step if present) */}
        {step.tip && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl px-4 py-3 mt-3">
            <p className="text-xs font-bold text-yellow-800">
              <span aria-hidden="true">💡 </span>
              {step.tip}
            </p>
          </div>
        )}
      </div>

      {/* Navigation buttons */}
      <div className="flex gap-3 mt-6">
        {current > 0 && (
          <button
            onClick={back}
            className="flex-1 py-3 rounded-2xl text-sm font-extrabold border-2 border-gray-200 text-gray-600 active:scale-95 transition-transform"
          >
            Back
          </button>
        )}
        <button
          onClick={next}
          className="flex-1 py-3 rounded-2xl text-sm font-extrabold text-white bg-duo-blue active:scale-95 transition-transform"
        >
          {isLast ? 'Continue' : 'Next'}
        </button>
      </div>
    </div>
  );
}

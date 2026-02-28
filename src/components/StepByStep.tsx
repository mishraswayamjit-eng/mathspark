'use client';

import { useState } from 'react';
import KatexRenderer from './KatexRenderer';
import type { StepItem } from '@/types';

interface StepByStepProps {
  steps: StepItem[];
  /** Called when student clicks "Got it! Next Question →" after reading the solution. */
  onGotIt?: () => void;
  /** If provided, shows a "Practice Similar Question" button alongside Got it. */
  onPracticeSimilar?: () => void;
}

export default function StepByStep({ steps, onGotIt, onPracticeSimilar }: StepByStepProps) {
  const [open, setOpen] = useState(false);

  if (!steps || steps.length === 0) return null;

  return (
    <div className="rounded-2xl border border-green-100 overflow-hidden shadow-sm">
      {/* Toggle button */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-[#1CB0F6] hover:bg-[#22bfff] text-white font-extrabold text-sm transition-colors"
      >
        <span>✨ See the full solution</span>
        <span className="text-base">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="bg-white">
          {steps.map((step, i) => (
            <div
              key={step.step ?? i}
              className={`px-4 py-3 flex gap-3 ${i < steps.length - 1 ? 'border-b border-green-50' : ''}`}
            >
              {/* Step number circle */}
              <div className="w-6 h-6 rounded-full bg-[#1CB0F6] text-white flex items-center justify-center text-xs font-extrabold flex-shrink-0 mt-0.5">
                {step.step ?? i + 1}
              </div>

              <div className="flex-1">
                <p className="text-gray-700 text-sm leading-relaxed font-medium">{step.text}</p>
                {/* LaTeX expression for this step (highlighted green — shows what changed) */}
                {step.latex && (
                  <div className="mt-2 p-3 bg-green-50 border-l-4 border-[#58CC02] rounded-r-xl overflow-x-auto">
                    <KatexRenderer latex={step.latex} displayMode />
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Action buttons */}
          {(onGotIt || onPracticeSimilar) && (
            <div className="px-4 py-4 bg-gray-50 border-t border-green-50 space-y-2">
              {onPracticeSimilar && (
                <button
                  onClick={onPracticeSimilar}
                  className="w-full min-h-[52px] bg-[#1CB0F6] hover:bg-[#22bfff] active:bg-[#0a98dc] text-white font-extrabold text-sm rounded-2xl py-3 transition-colors flex items-center justify-center gap-2 shadow-sm"
                >
                  🔁 Practice Similar Question
                </button>
              )}
              {onGotIt && (
                <button
                  onClick={onGotIt}
                  className="w-full min-h-[52px] bg-[#58CC02] hover:bg-[#5bd800] active:bg-[#46a302] text-white font-extrabold text-base rounded-2xl py-3 transition-colors flex items-center justify-center gap-2 shadow-sm"
                >
                  Got it! Next Question →
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

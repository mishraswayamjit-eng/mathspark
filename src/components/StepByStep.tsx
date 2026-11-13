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
    <div className="rounded-2xl border-2 border-ink overflow-hidden bg-white">
      {/* Toggle button */}
      <button
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="w-full flex items-center justify-between px-4 py-2 bg-ink text-white font-display font-semibold text-lg"
      >
        <span><span aria-hidden="true">📖</span> Solved solution</span>
        <span
          className="text-base transition-transform duration-300"
          style={{ transform: open ? 'rotate(180deg)' : 'rotate(0deg)' }}
        >
          ▼
        </span>
      </button>

      {open && (
        <div className="bg-white">
          {steps.map((step, i) => (
            <div
              key={step.step ?? i}
              className={`px-4 py-3 flex gap-3 opacity-0 animate-fade-in ${
                i < steps.length - 1 ? 'border-b-2 border-soft' : ''
              }`}
              style={{ animationDelay: `${i * 120}ms`, animationFillMode: 'forwards' }}
            >
              {/* Step number circle */}
              <div className="w-7 h-7 rounded-full bg-soft text-ink flex items-center justify-center text-xs font-extrabold flex-shrink-0 mt-0.5">
                {step.step ?? i + 1}
              </div>

              <div className="flex-1 min-w-0">
                <p className="text-ink text-[15px] leading-relaxed font-semibold [overflow-wrap:anywhere]">{step.text}</p>
                {/* LaTeX expression for this step (highlighted green — shows what changed) */}
                {step.latex && (
                  <div className="mt-2 p-3 bg-success-soft border-l-[6px] border-success rounded-[10px] overflow-x-auto">
                    <KatexRenderer latex={step.latex} displayMode />
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Action buttons */}
          {(onGotIt || onPracticeSimilar) && (
            <div
              className="px-4 py-4 bg-soft border-t-2 border-line space-y-2 opacity-0 animate-fade-in"
              style={{ animationDelay: `${steps.length * 120}ms`, animationFillMode: 'forwards' }}
            >
              {onPracticeSimilar && (
                <button
                  onClick={onPracticeSimilar}
                  className="ui-btn w-full text-sm"
                >
                  🔁 Practice Similar Question
                </button>
              )}
              {onGotIt && (
                <button
                  onClick={onGotIt}
                  className="ui-btn ui-btn-primary w-full"
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

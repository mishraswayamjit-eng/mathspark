'use client';

import { useState } from 'react';
import KatexRenderer from './KatexRenderer';
import type { StepItem } from '@/types';

interface StepByStepProps {
  steps: StepItem[];
}

export default function StepByStep({ steps }: StepByStepProps) {
  const [open, setOpen] = useState(false);

  if (!steps || steps.length === 0) return null;

  return (
    <div className="rounded-spark border border-spark-indigo/20 overflow-hidden bg-surface-card shadow-soft">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3.5 bg-spark-indigo-soft text-spark-indigo font-body font-bold text-sm"
        aria-expanded={open}
        aria-controls="step-by-step-panel"
      >
        <span>📖 See step-by-step solution</span>
        <span className="text-base transition-transform duration-200" style={{ transform: open ? 'rotate(180deg)' : 'none' }}>▾</span>
      </button>

      {open && (
        <div id="step-by-step-panel" className="divide-y divide-spark-indigo/10">
          {steps.map((step, i) => (
            <div key={step.step ?? i} className="px-4 py-3.5">
              <p className="text-xs font-body font-bold text-spark-indigo uppercase tracking-wide mb-1">
                Step {step.step ?? i + 1}
              </p>
              <p className="font-body text-ink text-sm leading-relaxed">{step.text}</p>
              {step.latex && (
                <div className="mt-2 p-3 bg-spark-green-soft rounded-xl overflow-x-auto">
                  <KatexRenderer latex={step.latex} displayMode />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

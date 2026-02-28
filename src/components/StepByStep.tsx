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
    <div className="rounded-2xl border border-blue-200 overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-blue-50 text-blue-700 font-semibold text-sm"
      >
        <span>📖 See step-by-step solution</span>
        <span className="text-lg">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="divide-y divide-blue-100 bg-white">
          {steps.map((step, i) => (
            <div key={step.step ?? i} className="px-4 py-3">
              <p className="text-xs font-bold text-blue-500 uppercase tracking-wide mb-1">
                Step {step.step ?? i + 1}
              </p>
              <p className="text-gray-700 text-sm leading-relaxed">{step.text}</p>
              {step.latex && (
                <div className="mt-2 p-2 bg-green-50 rounded-lg overflow-x-auto">
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

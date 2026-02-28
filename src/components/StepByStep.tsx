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
    <div className="rounded-2xl border border-blue-100 overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-[#1CB0F6] text-white font-extrabold text-sm rounded-xl"
      >
        <span>📖 See step-by-step solution</span>
        <span className="text-lg">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="divide-y divide-blue-50 bg-white">
          {steps.map((step, i) => (
            <div key={step.step ?? i} className="px-4 py-3 flex gap-3">
              {/* Numbered circle */}
              <div className="w-6 h-6 rounded-full bg-[#1CB0F6] text-white flex items-center justify-center text-xs font-extrabold flex-shrink-0 mt-0.5">
                {step.step ?? i + 1}
              </div>
              <div className="flex-1">
                <p className="text-gray-700 text-sm leading-relaxed font-medium">{step.text}</p>
                {step.latex && (
                  <div className="mt-2 p-3 bg-green-50 border-l-4 border-[#58CC02] rounded-r-xl overflow-x-auto">
                    <KatexRenderer latex={step.latex} displayMode />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

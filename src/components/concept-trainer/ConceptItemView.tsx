'use client';

import { useState } from 'react';
import type { ConceptItem, ConceptModule } from '@/types/conceptTrainer';
import ConceptVisualView from './ConceptVisual';

interface Props {
  module: ConceptModule;
  item: ConceptItem;
  index: number;      // 1-based position within the module
  total: number;
  onBack: () => void;
  onNext: (() => void) | null;
}

/**
 * The three-thinking-steps flow for a single concept item. Steps unlock
 * progressively: you must choose the correct option for a step before the next
 * one reveals. Every option shows its diagnostic feedback (naming the
 * misconception) — a wrong pick is a teaching moment, not a dead end.
 */
export default function ConceptItemView({ module, item, index, total, onBack, onNext }: Props) {
  // picked[i] = the letter the student has selected for step i (or undefined)
  const [picked, setPicked] = useState<Record<number, string>>({});
  const [hintOpen, setHintOpen] = useState<Record<number, boolean>>({});

  const isStepDone = (i: number): boolean => {
    const letter = picked[i];
    if (!letter) return false;
    const choice = item.steps[i].choices.find((c) => c.letter === letter);
    return !!choice?.isCorrect;
  };

  // A step is visible once all earlier steps are answered correctly.
  const revealedCount = (() => {
    let n = 1;
    for (let i = 0; i < item.steps.length; i++) {
      if (isStepDone(i)) n = i + 2;
      else break;
    }
    return Math.min(n, item.steps.length);
  })();

  const allDone = item.steps.every((_, i) => isStepDone(i));

  return (
    <div className="max-w-lg mx-auto px-4 pt-4 pb-28 animate-fade-in">
      {/* Breadcrumb / back */}
      <button
        onClick={onBack}
        className="text-duo-blue text-sm font-bold mb-3 min-h-[36px] flex items-center gap-1"
      >
        &larr; {module.title}
      </button>

      <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wide">
        Item {index} of {total}
      </p>
      <h2 className="text-lg font-extrabold text-gray-800 mb-2">{item.title}</h2>

      {/* Story */}
      <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm mb-4">
        <p className="text-[15px] leading-relaxed text-gray-800 font-medium">{item.story}</p>
      </div>

      {/* Steps */}
      {item.steps.map((step, i) => {
        if (i >= revealedCount) return null;
        const chosen = picked[i];
        const done = isStepDone(i);
        return (
          <div key={i} className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <span
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold text-white ${
                  done ? 'bg-duo-green' : 'bg-duo-blue'
                }`}
              >
                {done ? '✓' : i + 1}
              </span>
              <p className="font-bold text-gray-800 text-sm">{step.prompt}</p>
            </div>

            <div className="space-y-2">
              {step.choices.map((c) => {
                const isChosen = chosen === c.letter;
                const showState = isChosen;
                let cls = 'border-gray-200 bg-white';
                if (showState && c.isCorrect) cls = 'border-duo-green bg-green-50';
                else if (showState && !c.isCorrect) cls = 'border-duo-orange bg-orange-50';
                // Lock further changes once the step is correctly answered.
                const locked = done;
                return (
                  <button
                    key={c.letter}
                    disabled={locked}
                    onClick={() => setPicked((p) => ({ ...p, [i]: c.letter }))}
                    className={`w-full text-left rounded-xl border-2 px-3 py-2.5 transition-colors min-h-[48px] ${cls} ${
                      locked ? 'cursor-default' : 'active:scale-[0.99]'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <span className="font-extrabold text-gray-400 text-sm">{c.letter}</span>
                      <span className="text-sm text-gray-800 font-medium">{c.text}</span>
                    </div>
                    {showState && (
                      <p
                        className={`text-xs mt-1.5 pl-5 font-medium leading-snug ${
                          c.isCorrect ? 'text-duo-green' : 'text-duo-orange'
                        }`}
                      >
                        {c.isCorrect ? '✓ ' : '↻ '}
                        {c.feedback}
                      </p>
                    )}
                  </button>
                );
              })}
            </div>

            {/* Per-step hint */}
            {!done && (
              <div className="mt-2">
                <button
                  onClick={() => setHintOpen((h) => ({ ...h, [i]: !h[i] }))}
                  className="text-duo-blue text-xs font-bold min-h-[32px]"
                >
                  {hintOpen[i] ? 'Hide hint' : 'Need a hint? 💡'}
                </button>
                {hintOpen[i] && (
                  <p className="text-xs text-gray-600 bg-blue-50 border border-blue-100 rounded-lg px-3 py-2 mt-1 leading-snug">
                    {step.hint}
                  </p>
                )}
              </div>
            )}
          </div>
        );
      })}

      {/* Solution / visual / explain — revealed once all steps are correct */}
      {allDone && (
        <div className="animate-slide-up">
          {item.visual && (
            <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm mb-4">
              <p className="text-[11px] font-extrabold text-gray-400 uppercase tracking-wide mb-2">
                Picture it
              </p>
              <ConceptVisualView visual={item.visual} />
            </div>
          )}

          <div className="bg-green-50 rounded-2xl p-4 border border-green-200 mb-4">
            <p className="text-sm font-extrabold text-duo-green mb-2">Worked solution</p>
            <ol className="space-y-1.5">
              {item.solution.map((s, i) => (
                <li key={i} className="text-sm text-gray-800 font-medium leading-snug flex gap-2">
                  <span className="text-duo-green font-bold">{i + 1}.</span>
                  <span>{s.text}</span>
                </li>
              ))}
            </ol>
            <p className="text-base font-extrabold text-gray-900 mt-3">
              Answer: {item.answer}{item.unit ? ` ${item.unit}` : ''}
            </p>
            {item.check && (
              <p className="text-xs text-gray-600 mt-2 font-medium">✓ Check: {item.check}</p>
            )}
          </div>

          {item.explain && (
            <div className="bg-purple-50 rounded-2xl p-4 border border-purple-200 mb-4">
              <p className="text-xs font-extrabold text-purple-700 mb-1">Why it works</p>
              <p className="text-sm text-purple-900 font-medium leading-snug">{item.explain}</p>
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={onBack}
              className="flex-1 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl py-3 min-h-[48px] active:scale-[0.98] transition-transform"
            >
              Back to list
            </button>
            {onNext && (
              <button
                onClick={onNext}
                className="flex-1 bg-duo-green text-white font-extrabold rounded-xl py-3 min-h-[48px] active:scale-[0.98] transition-transform"
              >
                Next item →
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

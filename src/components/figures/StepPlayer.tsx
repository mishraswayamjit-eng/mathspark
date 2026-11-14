'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import FigureView from './FigureView';
import KatexRenderer from '@/components/KatexRenderer';
import ReadAloudButton from '@/components/ReadAloudButton';
import { stepToSpeech, toSpeech } from '@/lib/speech/mathToSpeech';
import type { FigureSpec } from '@/lib/figures/types';
import type { Question } from '@/types';

/**
 * Walks through a solution one step at a time, with the figure for each step
 * above its text.
 *
 * Where the steps come from:
 *   - the question's own `stepByStep`, each paired by position with
 *     `visual.stepFigures`; or
 *   - `visual.steps` (a solution computed offline) when the question has no
 *     steps of its own.
 * Everything shown is pre-verified content. Nothing is worked out here.
 */

interface PlayerStep {
  text: string;
  latex?: string;
  figure: FigureSpec | null;
  /** What the read-aloud button says for this step. */
  speech: string;
}

function buildSteps(question: Question): PlayerStep[] {
  const out: PlayerStep[] = [];
  const own = Array.isArray(question.stepByStep) ? question.stepByStep : [];
  const visual = question.visual;
  // Authored narration for the steps, when there is one line for every step shown.
  const shownCount = own.length > 0 ? own.length : (visual && visual.steps ? visual.steps.length : 0);
  const spoken = question.speech && question.speech.steps.length === shownCount ? question.speech.steps : [];
  const said = (i: number): string => (typeof spoken[i] === 'string' ? spoken[i].trim() : '');

  if (own.length === 0) {
    const computed = visual && visual.steps ? visual.steps : [];
    for (let i = 0; i < computed.length; i++) {
      const text = typeof computed[i].text === 'string' ? computed[i].text : '';
      out.push({ text, figure: computed[i].figure || null, speech: said(i) || toSpeech(text) });
    }
    return out;
  }

  const figures = visual && visual.stepFigures ? visual.stepFigures : [];
  for (let i = 0; i < own.length; i++) {
    const step = own[i];
    const text = typeof step.text === 'string' ? step.text : '';
    const latex = typeof step.latex === 'string' && step.latex ? step.latex : undefined;
    out.push({
      text,
      latex,
      figure: i < figures.length ? figures[i] || null : null,
      speech: said(i) || stepToSpeech({ step: i + 1, text, latex }),
    });
  }
  return out;
}

/** True when the question has a solution to walk through, from either source. */
export function hasSolutionSteps(question: Question): boolean {
  if (Array.isArray(question.stepByStep) && question.stepByStep.length > 0) return true;
  return !!(question.visual && question.visual.steps && question.visual.steps.length > 0);
}

/** Two steps often share a picture; this tells when it really changed. */
function figureKey(figure: FigureSpec | null): string {
  return figure ? JSON.stringify(figure) : '';
}

/** Matches `fade-in` in globals.css. */
const FADE_MS = 250;

interface StepPlayerProps {
  question: Question;
  /** Extra classes for the outer element. */
  className?: string;
}

export default function StepPlayer({ question, className }: StepPlayerProps) {
  const steps = useMemo(() => buildSteps(question), [question]);
  const [index, setIndex] = useState(0);
  // The picture being faded out while the next one fades in.
  const [leaving, setLeaving] = useState<FigureSpec | null>(null);
  const leaveTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // A different question: back to its first step.
  useEffect(() => {
    setIndex(0);
    setLeaving(null);
  }, [question.id]);

  useEffect(() => () => {
    if (leaveTimer.current) clearTimeout(leaveTimer.current);
  }, []);

  if (steps.length === 0) {
    return (
      <div className={`rounded-control border-2 border-line bg-soft px-4 py-5 text-center ${className ?? ''}`}>
        <p className="text-[16px] font-bold text-ink leading-relaxed">
          <span aria-hidden="true">🌟</span> There are no written steps for this one yet.
        </p>
        <p className="text-[15px] font-semibold text-ink-muted leading-relaxed mt-1">
          Ask Sparky if you would like it explained.
        </p>
      </div>
    );
  }

  const current = Math.min(index, steps.length - 1);
  const step = steps[current];
  const isLast = current === steps.length - 1;

  function go(next: number) {
    if (next < 0 || next >= steps.length || next === current) return;
    const from = steps[current].figure;
    const to = steps[next].figure;
    if (leaveTimer.current) clearTimeout(leaveTimer.current);
    if (from && to && figureKey(from) !== figureKey(to)) {
      setLeaving(from);
      leaveTimer.current = setTimeout(() => setLeaving(null), FADE_MS);
    } else {
      setLeaving(null);
    }
    setIndex(next);
  }

  return (
    <div className={`space-y-3 ${className ?? ''}`}>
      {/* Where we are */}
      <div className="flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-[15px] font-extrabold text-ink">
            Step {current + 1} of {steps.length}
          </p>
          <div className="flex items-center gap-1.5 mt-1.5" aria-hidden="true">
            {steps.map((_, i) => (
              <span
                key={i}
                className={`h-2.5 rounded-full border-2 transition-all duration-200 ${
                  i === current
                    ? 'w-6 bg-action border-ink'
                    : i < current
                    ? 'w-2.5 bg-ink border-ink'
                    : 'w-2.5 bg-white border-line'
                }`}
              />
            ))}
          </div>
        </div>
        <ReadAloudButton text={step.speech} label={`step ${current + 1}`} />
      </div>

      {/* The picture for this step, cross-faded when it changes */}
      {step.figure && (
        <div className="relative">
          <div key={figureKey(step.figure)} className="animate-fade-in">
            <FigureView spec={step.figure} />
          </div>
          {leaving && (
            <div
              className="absolute inset-0 pointer-events-none"
              style={{ animation: `fade-in ${FADE_MS}ms ease-out reverse forwards` }}
              aria-hidden="true"
            >
              <FigureView spec={leaving} />
            </div>
          )}
        </div>
      )}

      {/* The step itself */}
      <div aria-live="polite">
        <div key={current} className="animate-fade-in">
          {step.text && (
            <p className="text-[19px] font-bold text-ink leading-relaxed [overflow-wrap:anywhere]">
              {step.text.indexOf('\\') !== -1 ? (
                <KatexRenderer latex={step.text} displayMode={false} />
              ) : (
                step.text
              )}
            </p>
          )}
          {step.latex && (
            <div className="mt-2 p-3 bg-success-soft border-l-[6px] border-success rounded-[10px] overflow-x-auto">
              <KatexRenderer latex={step.latex} displayMode />
            </div>
          )}
        </div>
      </div>

      {/* Back and Next */}
      <div className="flex items-center gap-3 pt-1">
        <button
          type="button"
          onClick={() => go(current - 1)}
          disabled={current === 0}
          className="ui-btn flex-1"
        >
          <span aria-hidden="true">←</span> Back
        </button>
        {isLast ? (
          <button
            type="button"
            onClick={() => go(0)}
            disabled={steps.length === 1}
            className="ui-btn flex-1"
          >
            <span aria-hidden="true">↺</span> Start again
          </button>
        ) : (
          <button
            type="button"
            onClick={() => go(current + 1)}
            className="ui-btn ui-btn-primary flex-1"
          >
            Next <span aria-hidden="true">→</span>
          </button>
        )}
      </div>
    </div>
  );
}

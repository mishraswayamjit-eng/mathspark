'use client';

import { useEffect, useState } from 'react';
import FigureView from './FigureView';
import StepPlayer from './StepPlayer';
import ScratchPad from './ScratchPad';
import type { Question } from '@/types';

/**
 * The second pane beside (or under) a question.
 *
 *   before answering   the question's figure when it has one, otherwise a
 *                      working space; hints (practice only) and a pencil pad
 *   after answering    the solution, one step at a time (practice and review)
 *
 * A test never shows hints or steps, whatever the stage. A review goes
 * straight to the steps.
 */

export interface WorkPaneProps {
  question: Question;
  stage: 'answering' | 'answered';
  mode: 'practice' | 'test' | 'review';
  /**
   * How many hints are showing (0 to 3). Pass this together with
   * `onHintLevelUp` when the screen keeps its own count (practice does, since
   * it records hint use). Leave both out and the pane keeps count itself.
   */
  hintLevel?: number;
  onHintLevelUp?: (next: number) => void;
  /** Extra classes for the outer element. */
  className?: string;
}

export default function WorkPane({ question, stage, mode, hintLevel, onHintLevelUp, className }: WorkPaneProps) {
  const figure = question.visual && question.visual.figure ? question.visual.figure : null;
  const hasFigure = figure !== null;

  const [localLevel, setLocalLevel] = useState(0);
  // The pad is the main thing when there is no figure, and tucked away when there is one.
  const [padOpen, setPadOpen] = useState(!hasFigure);

  // A new question: hints hidden again, pad back to its starting state.
  useEffect(() => {
    setLocalLevel(0);
    setPadOpen(!hasFigure);
  }, [question.id, hasFigure]);

  const showSteps = mode === 'review' || (mode === 'practice' && stage === 'answered');

  if (showSteps) {
    return (
      <section className={`space-y-4 ${className ?? ''}`} aria-label="Step by step solution">
        <h2 className="font-display text-title text-ink">
          <span aria-hidden="true">📖</span> Step by step
        </h2>
        <StepPlayer question={question} />
      </section>
    );
  }

  const level = hintLevel !== undefined ? hintLevel : localLevel;
  const levelUp = onHintLevelUp || setLocalLevel;
  const showHints = mode === 'practice' && !!question.hint1;

  return (
    <section className={`space-y-4 ${className ?? ''}`} aria-label={hasFigure ? 'Picture for this question' : 'Working space'}>
      <h2 className="font-display text-title text-ink">
        {hasFigure ? (
          <><span aria-hidden="true">🔎</span> Look at the picture</>
        ) : (
          <><span aria-hidden="true">✏️</span> Working space</>
        )}
      </h2>

      {figure && <FigureView spec={figure} />}

      {/* Hints: one at a time, only when asked for */}
      {showHints && level === 0 && (
        <button type="button" onClick={() => levelUp(1)} className="ui-btn w-full">
          <span aria-hidden="true">💡</span> Show a hint
        </button>
      )}
      {showHints && level > 0 && (
        // Only the first, strategy hint is offered before answering. The later
        // hints work the question through, so they wait until after an answer.
        <p role="note" className="bg-hint rounded-control border-2 border-line px-4 py-3 text-[15px] leading-relaxed font-semibold text-ink">
          <span aria-hidden="true">💡 </span>{question.hint1}
        </p>
      )}

      {/* Pencil pad */}
      <div>
        <button
          type="button"
          onClick={() => setPadOpen(!padOpen)}
          aria-expanded={padOpen}
          className="w-full min-h-[48px] px-4 rounded-control border-2 border-line bg-soft text-ink font-extrabold text-[15px] flex items-center justify-between gap-2 hover:border-ink transition-colors"
        >
          <span><span aria-hidden="true">✏️</span> Pencil pad</span>
          <span aria-hidden="true">{padOpen ? '▲' : '▼'}</span>
        </button>
        {/* Kept mounted while closed so the working is still there when it opens again. */}
        <div className={padOpen ? 'mt-2' : 'hidden'}>
          <ScratchPad resetKey={question.id} />
        </div>
      </div>
    </section>
  );
}

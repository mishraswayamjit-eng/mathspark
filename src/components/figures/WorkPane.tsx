'use client';

import { useEffect, useRef, useState } from 'react';
import FigureView from './FigureView';
import StepPlayer from './StepPlayer';
import ScratchPad from './ScratchPad';
import TeachPlayer from '@/components/teach/TeachPlayer';
import { useTeachAvailable } from '@/components/teach/player/useTeachAvailable';
import type { Question } from '@/types';

/**
 * The second pane beside (or under) a question.
 *
 *   before answering   the question's figure when it has one, otherwise a
 *                      working space; hints (practice only) and a pencil pad
 *   after answering    the solution (practice and review)
 *
 * In practice, a question that has a lesson offers "Explain it to me": the
 * teacher talks it through on a board, in this pane. After answering it is the
 * main thing here, with "Read the steps" as the quieter choice. Before
 * answering it sits at the bottom of the working space behind a clear line
 * that it shows the whole solution, and taking it counts as the strongest
 * hint. The lesson only ever starts when the child asks for it.
 *
 * A test never shows hints, steps or lessons, whatever the stage. A review
 * goes straight to the steps.
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
  /**
   * Called when the child takes "Explain it to me" before answering. The lesson
   * shows the whole solution, so the screen should count it as the strongest
   * hint. Left out, the pane raises the hint level to 3 through `onHintLevelUp`
   * (or its own count).
   */
  onLessonBeforeAnswer?: () => void;
  /** Told when a lesson opens (true) and when it closes (false), so the screen can keep quiet meanwhile. */
  onLessonChange?: (open: boolean) => void;
  /** False while the pane is covered or put away: an open lesson is closed, so it never plays unseen. Default true. */
  active?: boolean;
  /** Extra classes for the outer element. */
  className?: string;
}

/** What the pane is showing of the solution: the choice, the lesson, or the written steps. */
type SolutionView = 'choice' | 'lesson' | 'steps';

export default function WorkPane({
  question, stage, mode, hintLevel, onHintLevelUp, onLessonBeforeAnswer, onLessonChange, active, className,
}: WorkPaneProps) {
  const figure = question.visual && question.visual.figure ? question.visual.figure : null;
  const hasFigure = figure !== null;

  const [localLevel, setLocalLevel] = useState(0);
  // The pad is the main thing when there is no figure, and tucked away when there is one.
  const [padOpen, setPadOpen] = useState(!hasFigure);

  // "Explain it to me" is for practice only. One light call says whether this question has a lesson.
  const teach = useTeachAvailable(mode === 'practice' ? question.id : null);
  const [view, setView] = useState<SolutionView>('choice');
  // Before answering: the child has tapped "Explain it to me" and is being told it shows the whole solution.
  const [confirming, setConfirming] = useState(false);

  // A new question: hints hidden again, pad back to its starting state, no lesson playing.
  useEffect(() => {
    setLocalLevel(0);
    setPadOpen(!hasFigure);
    setView('choice');
    setConfirming(false);
  }, [question.id, hasFigure]);

  // Covered or put away: stop the lesson.
  const isActive = active !== false;
  useEffect(() => {
    if (!isActive) setView((v) => (v === 'lesson' ? 'choice' : v));
  }, [isActive]);

  const lessonOpen = mode === 'practice' && view === 'lesson';

  // Tell the screen while a lesson is open (and when this pane goes away with one open).
  const lessonChangeRef = useRef(onLessonChange);
  lessonChangeRef.current = onLessonChange;
  useEffect(() => {
    if (!lessonOpen) return;
    if (lessonChangeRef.current) lessonChangeRef.current(true);
    return () => {
      if (lessonChangeRef.current) lessonChangeRef.current(false);
    };
  }, [lessonOpen]);

  const showSteps = mode === 'review' || (mode === 'practice' && stage === 'answered');

  const level = hintLevel !== undefined ? hintLevel : localLevel;
  const levelUp = onHintLevelUp || setLocalLevel;
  const showHints = mode === 'practice' && !!question.hint1;

  function startLessonBeforeAnswer() {
    // The lesson shows the whole solution: it counts as the strongest hint.
    if (onLessonBeforeAnswer) onLessonBeforeAnswer();
    else levelUp(3);
    setConfirming(false);
    setView('lesson');
  }

  // The lesson keeps its place in the tree across answering, so it carries on
  // playing if the child answers while it is open.
  const lesson = lessonOpen ? (
    <TeachPlayer
      questionId={question.id}
      onClose={() => setView('choice')}
      closeLabel="Back to the question"
      fallback={<StepPlayer question={question} />}
    />
  ) : null;

  if (showSteps) {
    const offerLesson = mode === 'practice' && teach === 'yes';
    const checking = mode === 'practice' && teach === 'checking';
    return (
      <section className={`space-y-4 ${className ?? ''}`} aria-label={lessonOpen ? 'Explain it to me' : 'Step by step solution'}>
        {lesson}
        {!lessonOpen && offerLesson && view === 'choice' && (
          <>
            <h2 className="font-display text-title text-ink">
              <span aria-hidden="true">🎓</span> How was it solved?
            </h2>
            <button
              type="button"
              onClick={() => setView('lesson')}
              className="ui-btn ui-btn-primary w-full min-h-[60px] text-[18px]"
            >
              <span aria-hidden="true">🎓</span> Explain it to me
            </button>
            <p className="text-[15px] font-semibold text-ink-muted leading-relaxed">
              Sparky talks you through it on the board, one move at a time.
            </p>
            <button
              type="button"
              onClick={() => setView('steps')}
              className="w-full min-h-[48px] px-4 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[15px] hover:border-ink transition-colors"
            >
              <span aria-hidden="true">📖</span> Read the steps
            </button>
          </>
        )}
        {!lessonOpen && checking && (
          <div className="h-[60px] rounded-control border-2 border-line bg-soft animate-pulse" role="status" aria-label="Getting this ready" />
        )}
        {!lessonOpen && !checking && (!offerLesson || view === 'steps') && (
          <>
            <h2 className="font-display text-title text-ink">
              <span aria-hidden="true">📖</span> Step by step
            </h2>
            <StepPlayer question={question} />
            {offerLesson && (
              <button
                type="button"
                onClick={() => setView('lesson')}
                className="w-full min-h-[48px] px-4 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[15px] hover:border-ink transition-colors"
              >
                <span aria-hidden="true">🎓</span> Explain it to me
              </button>
            )}
          </>
        )}
      </section>
    );
  }

  const offerLessonFirst = mode === 'practice' && teach === 'yes';

  return (
    <section className={`space-y-4 ${className ?? ''}`} aria-label={lessonOpen ? 'Explain it to me' : hasFigure ? 'Picture for this question' : 'Working space'}>
      {lesson}
      {/* Hidden, not removed, while a lesson plays: the pencil-pad working is kept. */}
      <div className={lessonOpen ? 'hidden' : 'space-y-4'}>
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
          {/* The live coach looks at the pad in practice, before answering (this
              branch is never reached in practice once answered). Never in a
              test, and not while a lesson is playing over the pad. */}
          <ScratchPad
            resetKey={question.id}
            coachFor={mode === 'practice' && !lessonOpen ? { questionId: question.id } : undefined}
          />
        </div>
      </div>

      {/* Explain it to me, before answering: offered quietly, and only after a clear
          line that it shows the whole solution. */}
      {offerLessonFirst && !confirming && (
        <button
          type="button"
          onClick={() => setConfirming(true)}
          className="w-full min-h-[48px] px-4 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[15px] hover:border-ink transition-colors"
        >
          <span aria-hidden="true">🎓</span> Explain it to me
        </button>
      )}
      {offerLessonFirst && confirming && (
        <div className="rounded-control border-2 border-ink bg-hint px-4 py-3 space-y-3" role="group" aria-label="Explain it to me">
          <p className="text-[15px] font-bold text-ink leading-relaxed">
            <span aria-hidden="true">🎓</span> This shows the whole solution, from start to finish. It is fine to
            watch it, or you can have a go yourself first.
          </p>
          <div className="flex flex-col sm:flex-row gap-2">
            <button type="button" onClick={startLessonBeforeAnswer} className="ui-btn ui-btn-primary flex-1">
              Yes, explain it
            </button>
            <button type="button" onClick={() => setConfirming(false)} className="ui-btn flex-1">
              I&apos;ll try first
            </button>
          </div>
        </div>
      )}
      </div>
    </section>
  );
}

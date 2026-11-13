'use client';

import { useEffect, useRef, useState } from 'react';
import KatexRenderer from './KatexRenderer';
import type { Question, AnswerKey, StepItem } from '@/types';

// ── Types ─────────────────────────────────────────────────────────────────────

interface AnimatedWalkthroughProps {
  question:      Question;
  studentAnswer: AnswerKey | null;
  onClose:       () => void;
  onSimilar?:    () => void;  // "Practice This Concept Again"
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const OPTION_KEYS: AnswerKey[] = ['A', 'B', 'C', 'D'];

function optionText(q: Question, key: AnswerKey): string {
  return q[`option${OPTION_KEYS.indexOf(key) + 1}` as keyof Question] as string;
}

/** Tokenize text into words for staggered animation. */
function tokenize(text: string): string[] {
  return text.split(/\s+/).filter(Boolean);
}

// ── Simple view (0–1 steps) ───────────────────────────────────────────────────

function SimpleView({
  question, studentAnswer, onClose, onSimilar,
}: { question: Question; studentAnswer: AnswerKey | null; onClose: () => void; onSimilar?: () => void }) {
  const correctText = optionText(question, question.correctAnswer);
  const wasWrong    = studentAnswer && studentAnswer !== question.correctAnswer;
  const misconKey   = studentAnswer ? `misconception${studentAnswer}` as keyof Question : null;
  const misconText  = misconKey ? question[misconKey] as string : '';

  return (
    <div className="fixed inset-0 z-[100] flex flex-col justify-end">
      <div className="absolute inset-0 bg-ink/60" onClick={onClose} />
      <div
        className="relative bg-white rounded-t-card border-2 border-b-0 border-ink max-w-lg mx-auto w-full px-5 pt-5 pb-8"
        style={{ animation: 'walkthrough-slide-up 0.4s ease-out' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <p className="font-display text-title text-ink">Solution</p>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg"
          >
            ✕
          </button>
        </div>

        {/* Question (dimmed) */}
        <p className="text-sm text-ink-muted font-semibold mb-4 leading-snug">{question.questionText}</p>

        {/* Correct answer */}
        <div
          className="bg-success-soft border-2 border-success rounded-card px-4 py-3 mb-3"
          style={{ animation: 'answer-celebrate 0.6s ease-out' }}
        >
          <p className="text-caption text-ink mb-1">✅ Correct answer</p>
          <p className="font-extrabold text-ink">{question.correctAnswer}: {correctText}</p>
        </div>

        {/* Wrong: student's answer + misconception */}
        {wasWrong && studentAnswer && (
          <div className="bg-retry-soft border-2 border-retry rounded-card px-4 py-3 mb-3">
            <p className="text-xs font-bold text-retry mb-1">You chose {studentAnswer}: {optionText(question, studentAnswer)}</p>
            {misconText && <p className="text-xs font-semibold text-ink">💡 {misconText}</p>}
          </div>
        )}

        {onSimilar && (
          <button
            onClick={() => { onClose(); onSimilar(); }}
            className="w-full min-h-[52px] rounded-control border-2 border-ink shadow-hard-sm bg-action hover:bg-action-dark text-white font-extrabold text-sm mt-2 flex items-center justify-center gap-2"
          >
            🔄 Practice This Concept Again
          </button>
        )}
        <button
          onClick={onClose}
          className={`w-full min-h-[48px] rounded-control border-2 border-ink shadow-hard-sm font-extrabold text-base mt-2 ${
            onSimilar ? 'bg-white text-ink' : 'bg-action text-white'
          }`}
        >
          Got it! ✓
        </button>
      </div>
    </div>
  );
}

// ── Step slide ────────────────────────────────────────────────────────────────

function StepSlide({
  step, stepIndex, totalSteps, question, isFirst, isLast,
  studentAnswer,
}: {
  step: StepItem; stepIndex: number; totalSteps: number;
  question: Question; isFirst: boolean; isLast: boolean;
  studentAnswer: AnswerKey | null;
}) {
  const tokens       = tokenize(step.text);
  const correctText  = optionText(question, question.correctAnswer);
  const wasWrong     = studentAnswer && studentAnswer !== question.correctAnswer;
  const misconKey    = studentAnswer ? `misconception${studentAnswer}` as keyof Question : null;
  const misconText   = misconKey ? question[misconKey] as string : '';
  // Delay after which the LaTeX block fades in (after all word tokens have appeared)
  const latexDelayMs = Math.min(tokens.length * 150 + 100, 1000);

  return (
    <div
      className="px-5"
      style={{ animation: 'step-crossfade 0.4s ease-out' }}
    >
      {/* Step 1: show dimmed question text */}
      {isFirst && (
        <p className="text-sm text-ink-muted font-semibold mb-3 leading-snug" style={{ opacity: 0.65 }}>
          📋 {question.questionText}
        </p>
      )}

      {/* Step label */}
      <p className="text-caption text-ink-muted mb-2">
        Step {stepIndex + 1} of {totalSteps}
      </p>

      {/* Step text — word-by-word stagger */}
      <div className="text-question text-ink leading-relaxed mb-3 min-h-[56px]">
        {tokens.map((word, i) => (
          <span
            key={i}
            className="inline-block mr-[0.3em]"
            style={{
              opacity: 0,
              animation: 'token-build 0.25s ease forwards',
              animationDelay: `${i * 150}ms`,
            }}
          >
            {word}
          </span>
        ))}
      </div>

      {/* LaTeX block — appears after text tokens */}
      {step.latex ? (
        <div
          className="p-3 bg-success-soft border-l-[6px] border-success rounded-r-note overflow-x-auto"
          style={{
            opacity: 0,
            animation: 'token-build 0.35s ease forwards',
            animationDelay: `${latexDelayMs}ms`,
          }}
        >
          <KatexRenderer latex={step.latex} displayMode />
        </div>
      ) : null}

      {/* Final step: answer celebration */}
      {isLast && (
        <div
          className="mt-4 bg-success-soft border-2 border-success rounded-card px-4 py-3"
          style={{ animation: 'answer-celebrate 0.6s ease-out 0.3s both' }}
        >
          <p className="text-caption text-ink mb-1">✅ The answer is</p>
          <p className="font-extrabold text-ink text-base">{question.correctAnswer}: {correctText}</p>

          {wasWrong && studentAnswer && (
            <div className="mt-2 pt-2 border-t-2 border-success/30">
              <p className="text-xs text-retry font-bold">
                You chose {studentAnswer}: {optionText(question, studentAnswer)}
              </p>
              {misconText && (
                <p className="text-xs font-semibold text-ink mt-1">💡 {misconText}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function AnimatedWalkthrough({
  question, studentAnswer, onClose, onSimilar,
}: AnimatedWalkthroughProps) {
  const steps = question.stepByStep ?? [];

  if (steps.length <= 1) {
    return (
      <SimpleView
        question={question}
        studentAnswer={studentAnswer}
        onClose={onClose}
        onSimilar={onSimilar}
      />
    );
  }

  return (
    <WalkthroughPlayer
      question={question}
      studentAnswer={studentAnswer}
      steps={steps}
      onClose={onClose}
      onSimilar={onSimilar}
    />
  );
}

// ── Walkthrough Player (multi-step) ──────────────────────────────────────────

function WalkthroughPlayer({
  question, studentAnswer, steps, onClose, onSimilar,
}: AnimatedWalkthroughProps & { steps: StepItem[] }) {
  const totalSteps = steps.length;

  const [stepIndex, setStepIndex] = useState(0);
  const [stepKey,   setStepKey]   = useState(0);  // increment to re-trigger animation
  const [isPaused,  setIsPaused]  = useState(false);

  const touchStartX = useRef<number | null>(null);

  const isFirst  = stepIndex === 0;
  const isLast   = stepIndex >= totalSteps - 1;

  // ── Auto-advance ────────────────────────────────────────────────────────────
  useEffect(() => {
    if (isPaused || isLast) return;
    const timer = setTimeout(() => {
      setStepIndex((prev) => Math.min(prev + 1, totalSteps - 1));
      setStepKey((k) => k + 1);
    }, 3200);
    return () => clearTimeout(timer);
  }, [stepIndex, isPaused, isLast, totalSteps]);

  // ── Navigation ──────────────────────────────────────────────────────────────
  function goNext() {
    if (isLast) return;
    setStepIndex((s) => s + 1);
    setStepKey((k) => k + 1);
  }

  function goPrev() {
    if (isFirst) return;
    setStepIndex((s) => s - 1);
    setStepKey((k) => k + 1);
  }

  // ── Touch swipe ─────────────────────────────────────────────────────────────
  function handleTouchStart(e: React.TouchEvent) {
    touchStartX.current = e.touches[0].clientX;
  }

  function handleTouchEnd(e: React.TouchEvent) {
    if (touchStartX.current === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX.current;
    touchStartX.current = null;
    if (dx < -50) goNext();
    else if (dx > 50) goPrev();
  }

  const pct = Math.round(((stepIndex + 1) / totalSteps) * 100);

  return (
    <div className="fixed inset-0 z-[100] flex flex-col justify-end">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-ink/60" onClick={onClose} />

      {/* Card */}
      <div
        className="relative bg-white rounded-t-card border-2 border-b-0 border-ink max-w-lg mx-auto w-full overflow-hidden"
        style={{ animation: 'walkthrough-slide-up 0.4s ease-out', maxHeight: '92vh' }}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        {/* ── Header ── */}
        <div className="flex items-center justify-between px-5 pt-5 pb-2">
          <div>
            <p className="text-xs font-extrabold text-ink-muted">🎬 Watch Solution</p>
            <p className="text-sm font-bold text-ink mt-0.5">{question.subTopic}</p>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg hover:border-ink transition-colors"
            aria-label="Close walkthrough"
          >
            ✕
          </button>
        </div>

        {/* ── Progress bar ── */}
        <div className="mx-5 mb-4 h-3 ui-meter">
          <div
            className="h-full bg-action rounded-full transition-[width] duration-500 ease-out"
            style={{ width: `${pct}%` }}
          />
        </div>

        {/* ── Step content (scrollable) ── */}
        <div className="overflow-y-auto" style={{ maxHeight: 'calc(92vh - 200px)' }}>
          <div key={stepKey} className="pb-4">
            <StepSlide
              step={steps[stepIndex]}
              stepIndex={stepIndex}
              totalSteps={totalSteps}
              question={question}
              isFirst={isFirst}
              isLast={isLast}
              studentAnswer={studentAnswer}
            />
          </div>
        </div>

        {/* ── Controls ── */}
        <div className="border-t-2 border-line px-5 pt-3 pb-4 bg-white space-y-2">
          {/* "Practice Again" — prominent on last step if onSimilar provided */}
          {isLast && onSimilar && (
            <button
              onClick={() => { onClose(); onSimilar(); }}
              className="w-full min-h-[52px] rounded-control border-2 border-ink shadow-hard-sm bg-action hover:bg-action-dark text-white font-extrabold text-sm flex items-center justify-center gap-2 transition-colors"
            >
              🔄 Practice This Concept Again
            </button>
          )}

          {/* Nav row */}
          <div className="flex items-center gap-3">
            <button
              onClick={goPrev}
              disabled={isFirst}
              className="min-h-[48px] px-4 rounded-control border-2 border-line bg-white font-bold text-ink disabled:opacity-30 flex items-center gap-1 hover:border-ink transition-colors"
            >
              ◀ Back
            </button>
            <button
              onClick={() => setIsPaused((p) => !p)}
              className="min-h-[48px] px-4 rounded-control border-2 border-line bg-white font-bold text-ink flex items-center gap-1 hover:border-ink transition-colors"
            >
              {isPaused ? '▶ Play' : '⏸ Pause'}
            </button>
            {isLast ? (
              <button
                onClick={onClose}
                className={`flex-1 min-h-[48px] rounded-control border-2 border-ink shadow-hard-sm font-extrabold text-base flex items-center justify-center gap-1 transition-colors ${
                  onSimilar
                    ? 'bg-white text-ink hover:bg-soft'
                    : 'bg-action hover:bg-action-dark text-white'
                }`}
              >
                Got it! ✓
              </button>
            ) : (
              <button
                onClick={goNext}
                className="flex-1 min-h-[48px] rounded-control border-2 border-ink shadow-hard-sm bg-action hover:bg-action-dark text-white font-extrabold text-base flex items-center justify-center gap-1 transition-colors"
              >
                Next ▶
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

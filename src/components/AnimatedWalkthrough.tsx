'use client';

import { useEffect, useRef, useState } from 'react';
import KatexRenderer from './KatexRenderer';
import type { Question, AnswerKey, StepItem } from '@/types';

// ── Types ─────────────────────────────────────────────────────────────────────

interface AnimatedWalkthroughProps {
  question:      Question;
  studentAnswer: AnswerKey | null;
  onClose:       () => void;
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
  question, studentAnswer, onClose,
}: { question: Question; studentAnswer: AnswerKey | null; onClose: () => void }) {
  const correctText = optionText(question, question.correctAnswer);
  const wasWrong    = studentAnswer && studentAnswer !== question.correctAnswer;
  const misconKey   = studentAnswer ? `misconception${studentAnswer}` as keyof Question : null;
  const misconText  = misconKey ? question[misconKey] as string : '';

  return (
    <div className="fixed inset-0 z-[100] flex flex-col justify-end">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div
        className="relative bg-white rounded-t-3xl max-w-lg mx-auto w-full px-5 pt-5 pb-8"
        style={{ animation: 'walkthrough-slide-up 0.4s ease-out' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <p className="font-extrabold text-gray-700 text-base">Solution</p>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 font-bold text-lg"
          >
            ✕
          </button>
        </div>

        {/* Question (dimmed) */}
        <p className="text-sm text-gray-400 font-medium mb-4 leading-snug">{question.questionText}</p>

        {/* Correct answer */}
        <div
          className="bg-green-50 border border-green-200 rounded-2xl px-4 py-3 mb-3"
          style={{ animation: 'answer-celebrate 0.6s ease-out' }}
        >
          <p className="text-xs font-extrabold text-green-600 uppercase tracking-wide mb-1">✅ Correct answer</p>
          <p className="font-extrabold text-gray-800">{question.correctAnswer}: {correctText}</p>
        </div>

        {/* Wrong: student's answer + misconception */}
        {wasWrong && studentAnswer && (
          <div className="bg-red-50 border border-red-100 rounded-2xl px-4 py-3 mb-3">
            <p className="text-xs font-semibold text-red-400 mb-1">You chose {studentAnswer}: {optionText(question, studentAnswer)}</p>
            {misconText && <p className="text-xs text-gray-500">💡 {misconText}</p>}
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full min-h-[52px] rounded-2xl bg-[#58CC02] text-white font-extrabold text-base mt-2"
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
        <p className="text-sm text-gray-400 font-medium mb-3 leading-snug" style={{ opacity: 0.65 }}>
          📋 {question.questionText}
        </p>
      )}

      {/* Step label */}
      <p className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-2">
        Step {stepIndex + 1} of {totalSteps}
      </p>

      {/* Step text — word-by-word stagger */}
      <div className="text-[18px] font-bold text-gray-800 leading-relaxed mb-3 min-h-[56px]">
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
          className="p-3 bg-green-50 border-l-4 border-[#58CC02] rounded-r-2xl overflow-x-auto"
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
          className="mt-4 bg-green-50 border border-green-200 rounded-2xl px-4 py-3"
          style={{ animation: 'answer-celebrate 0.6s ease-out 0.3s both' }}
        >
          <p className="text-xs font-extrabold text-green-600 uppercase tracking-wide mb-1">✅ The answer is</p>
          <p className="font-extrabold text-gray-800 text-base">{question.correctAnswer}: {correctText}</p>

          {wasWrong && studentAnswer && (
            <div className="mt-2 pt-2 border-t border-green-100">
              <p className="text-xs text-red-400 font-semibold">
                You chose {studentAnswer}: {optionText(question, studentAnswer)}
              </p>
              {misconText && (
                <p className="text-xs text-gray-500 mt-1">💡 {misconText}</p>
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
  question, studentAnswer, onClose,
}: AnimatedWalkthroughProps) {
  const steps = question.stepByStep ?? [];

  // Simple view when no multi-step solution exists
  if (steps.length <= 1) {
    return (
      <SimpleView
        question={question}
        studentAnswer={studentAnswer}
        onClose={onClose}
      />
    );
  }

  return (
    <WalkthroughPlayer
      question={question}
      studentAnswer={studentAnswer}
      steps={steps}
      onClose={onClose}
    />
  );
}

// ── Walkthrough Player (multi-step) ──────────────────────────────────────────

function WalkthroughPlayer({
  question, studentAnswer, steps, onClose,
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
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />

      {/* Card */}
      <div
        className="relative bg-white rounded-t-3xl max-w-lg mx-auto w-full overflow-hidden"
        style={{ animation: 'walkthrough-slide-up 0.4s ease-out', maxHeight: '92vh' }}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        {/* ── Header ── */}
        <div className="flex items-center justify-between px-5 pt-5 pb-2">
          <div>
            <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest">🎬 Watch Solution</p>
            <p className="text-sm font-bold text-gray-700 mt-0.5">{question.subTopic}</p>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 font-bold text-lg hover:bg-gray-200 transition-colors"
            aria-label="Close walkthrough"
          >
            ✕
          </button>
        </div>

        {/* ── Progress bar ── */}
        <div className="mx-5 mb-4 h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-[#58CC02] to-[#89E219] rounded-full transition-all duration-500 ease-out"
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
        <div className="border-t border-gray-100 px-5 py-4 flex items-center gap-3 bg-white">
          {/* Back */}
          <button
            onClick={goPrev}
            disabled={isFirst}
            className="min-h-[48px] px-4 rounded-2xl border-2 border-gray-200 font-bold text-gray-500 disabled:opacity-30 flex items-center gap-1 hover:bg-gray-50 transition-colors"
          >
            ◀ Back
          </button>

          {/* Pause / Play */}
          <button
            onClick={() => setIsPaused((p) => !p)}
            className="min-h-[48px] px-4 rounded-2xl bg-gray-100 font-bold text-gray-600 flex items-center gap-1 hover:bg-gray-200 transition-colors"
          >
            {isPaused ? '▶ Play' : '⏸ Pause'}
          </button>

          {/* Next or Got it */}
          {isLast ? (
            <button
              onClick={onClose}
              className="flex-1 min-h-[48px] rounded-2xl bg-[#58CC02] hover:bg-[#5bd800] active:bg-[#46a302] text-white font-extrabold text-base flex items-center justify-center gap-1 shadow-sm transition-colors"
            >
              Got it! ✓
            </button>
          ) : (
            <button
              onClick={goNext}
              className="flex-1 min-h-[48px] rounded-2xl bg-[#1CB0F6] hover:bg-[#22bfff] active:bg-[#0a98dc] text-white font-extrabold text-base flex items-center justify-center gap-1 shadow-sm transition-colors"
            >
              Next ▶
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

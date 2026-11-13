'use client';

import React, { lazy, Suspense } from 'react';
import KatexRenderer from './KatexRenderer';
import QuestionDiagram from './diagrams/QuestionDiagram';
import type { AnswerKey, Difficulty, Question } from '@/types';

// Lazy-load interactive components (only loaded when needed)
const TapToColorQuestion = lazy(() => import('./interactive/TapToColorQuestion'));
const DragToSortQuestion = lazy(() => import('./interactive/DragToSortQuestion'));
const ChartTapQuestion = lazy(() => import('./interactive/ChartTapQuestion'));

// ── Message banks ─────────────────────────────────────────────────────────────

const CORRECT_MESSAGES = [
  'Great job! ⭐',
  'You got it! 🎯',
  'Excellent thinking! 🧠',
  'Well done! 🌟',
  'Awesome! 🎉',
];

const WRONG_MESSAGES = [
  "Not quite — let's think about this together!",
  "Almost! Here's a hint.",
  "Good try! Let's look at it another way.",
];

export function randomCorrect() {
  return CORRECT_MESSAGES[Math.floor(Math.random() * CORRECT_MESSAGES.length)];
}
export function randomWrong() {
  return WRONG_MESSAGES[Math.floor(Math.random() * WRONG_MESSAGES.length)];
}

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Returns true if a string contains LaTeX markup (backslash commands). */
function hasLatex(text: string): boolean {
  return text.includes('\\');
}

/** Color tokens for each difficulty level. */
function difficultyColors(d: Difficulty) {
  if (d === 'Easy') return { dot: 'bg-success', label: 'text-success', bg: 'bg-success-soft border-success/30' };
  if (d === 'Hard') return { dot: 'bg-retry', label: 'text-retry', bg: 'bg-retry-soft border-retry/30' };
  return { dot: 'bg-star', label: 'text-hint-ink', bg: 'bg-hint border-hint-ink/30' }; // Medium
}

// ── Component ─────────────────────────────────────────────────────────────────

export const LABELS: AnswerKey[] = ['A', 'B', 'C', 'D'];

interface QuestionCardProps {
  question: Question;
  answered: boolean;
  selected: AnswerKey | null;
  onAnswer: (key: AnswerKey, isCorrect: boolean) => void;
  onInteractiveAnswer?: (answer: string, isCorrect: boolean) => void;
}

const QuestionCard = React.memo(function QuestionCard({
  question,
  answered,
  selected,
  onAnswer,
  onInteractiveAnswer,
}: QuestionCardProps) {
  const options: Array<{ key: AnswerKey; text: string }> = [
    { key: 'A', text: question.option1 },
    { key: 'B', text: question.option2 },
    { key: 'C', text: question.option3 },
    { key: 'D', text: question.option4 },
  ];

  const diff = difficultyColors(question.difficulty);

  // ── Style builders ──────────────────────────────────────────────────────────

  function badgeCls(key: AnswerKey): string {
    const base =
      'w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-[15px] font-extrabold transition-colors duration-200';
    if (!answered) return `${base} bg-soft text-ink`;
    if (key === question.correctAnswer)
      return `${base} bg-success text-white animate-pop-in`;
    if (key === selected) return `${base} bg-retry text-white`;
    return `${base} bg-soft text-ink-muted`;
  }

  function cardCls(key: AnswerKey): string {
    const base =
      'w-full text-left rounded-[14px] px-3.5 py-3 min-h-[52px] border-2 flex items-center gap-3 transition-colors duration-200';
    if (!answered)
      return `${base} bg-white border-line text-ink hover:border-ink cursor-pointer`;
    if (key === question.correctAnswer)
      return `${base} bg-success-soft border-success text-success`;
    if (key === selected)
      return `${base} bg-retry-soft border-retry text-retry`;
    return `${base} bg-white border-line text-ink opacity-40`;
  }

  return (
    <div className="space-y-4">
      {/* ── Question card ─────────────────────────────────────────────── */}
      <div className="ui-card ui-card-pop animate-card-pop">

        {/* SubTopic + Difficulty tags at TOP */}
        <div className="flex items-center gap-2 mb-3 flex-wrap">
          <div className={`flex items-center gap-1.5 px-2.5 py-0.5 rounded-full border-2 ${diff.bg}`}>
            <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${diff.dot}`} />
            <span className={`text-[13px] font-extrabold ${diff.label}`}>
              {question.difficulty}
            </span>
          </div>
          <span className="ui-chip max-w-[220px]">
            <span className="truncate">{question.subTopic}</span>
          </span>
        </div>

        {/* Question text (min 18px) — render KaTeX if LaTeX markers detected */}
        <div className="text-[19px] font-bold text-ink leading-normal [overflow-wrap:anywhere]">
          {hasLatex(question.questionText) ? (
            <KatexRenderer latex={question.questionText} displayMode={false} />
          ) : (
            question.questionText
          )}
        </div>

        {/* LaTeX expression below text (if present) */}
        {question.questionLatex && (
          <div className="mt-3 overflow-x-auto p-3 bg-soft rounded-[10px] border-l-[6px] border-action">
            <KatexRenderer latex={question.questionLatex} displayMode className="block" />
          </div>
        )}

        {/* Diagram (if this question has an associated figure) */}
        <QuestionDiagram questionId={question.id} />
      </div>

      {/* ── Interactive question or MCQ options ──────────────────────── */}
      {question.interactionType && question.interactionData ? (
        <Suspense fallback={<div className="h-40 bg-gray-50 rounded-2xl animate-pulse" />}>
          {question.interactionType === 'tapToColor' && (
            <TapToColorQuestion
              data={question.interactionData as import('@/types').TapToColorData}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                // Map to MCQ callback for compatibility
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
          {question.interactionType === 'dragToSort' && (
            <DragToSortQuestion
              data={question.interactionData as import('@/types').DragToSortData}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
          {question.interactionType === 'chartTap' && (
            <ChartTapQuestion
              data={question.interactionData as import('@/types').ChartTapData}
              questionId={question.id}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
        </Suspense>
      ) : (
      <div className="grid gap-2.5">
        {options.map(({ key, text }) => (
          <button
            key={key}
            disabled={answered}
            onClick={() => onAnswer(key, key === question.correctAnswer)}
            className={cardCls(key)}
          >
            {/* Letter badge */}
            <span className={badgeCls(key)}>
              {answered && key === question.correctAnswer ? '✓' : key}
            </span>

            {/* Option text — KaTeX if LaTeX markers detected */}
            <span className="flex-1 text-left text-[17px] font-bold leading-snug">
              {hasLatex(text) ? (
                <KatexRenderer latex={text} displayMode={false} />
              ) : (
                text
              )}
            </span>

            {/* Wrong-answer indicator */}
            {answered && key === selected && key !== question.correctAnswer && (
              <span className="ml-auto text-retry font-bold text-xl flex-shrink-0" aria-hidden="true">✗</span>
            )}
          </button>
        ))}
      </div>
      )}
    </div>
  );
});

export default QuestionCard;

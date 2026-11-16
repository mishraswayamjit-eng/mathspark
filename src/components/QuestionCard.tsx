'use client';

import React, { lazy, Suspense } from 'react';
import KatexRenderer from './KatexRenderer';
import QuestionDiagram from './diagrams/QuestionDiagram';
import ReadAloudButton from './ReadAloudButton';
import { questionToSpeech } from '@/lib/speech/mathToSpeech';
import { narrationAudioSrc } from '@/hooks/useReadAloud';
import { tidyQuestionText, questionTextSize, topicChipLabel, type QuestionTextSize } from '@/lib/questionDisplay';
import type { AnswerKey, Difficulty, Question } from '@/types';

// Lazy-load interactive components (only loaded when needed)
const TapToColorQuestion = lazy(() => import('./interactive/TapToColorQuestion'));
const DragToSortQuestion = lazy(() => import('./interactive/DragToSortQuestion'));
const ChartTapQuestion = lazy(() => import('./interactive/ChartTapQuestion'));
const TileBuildQuestion = lazy(() => import('./interactive/TileBuildQuestion'));
const NumberLineQuestion = lazy(() => import('./interactive/NumberLineQuestion'));

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

/**
 * How many of the three level dots are filled. Difficulty is shown in ink, not
 * in green or red: those two colours only ever mean "correct" and "not quite".
 */
function difficultyLevel(d: Difficulty): number {
  if (d === 'Easy') return 1;
  if (d === 'Hard') return 3;
  return 2; // Medium
}

const LEVEL_DOTS = [1, 2, 3];

/**
 * Question text scales with how much there is to read: a one-liner is set
 * large, a long word problem a step smaller with more room between lines.
 */
const QUESTION_TEXT_CLS: Record<QuestionTextSize, string> = {
  short: 'text-[22px] leading-[1.35]',
  medium: 'text-[19px] leading-normal',
  long: 'text-[17px] leading-[1.6]',
};

/** Options this short (numbers, one or two words) sit two to a row on wider screens. */
const COMPACT_OPTION_MAX = 12;

// ── Component ─────────────────────────────────────────────────────────────────

export const LABELS: AnswerKey[] = ['A', 'B', 'C', 'D'];

interface QuestionCardProps {
  question: Question;
  answered: boolean;
  selected: AnswerKey | null;
  onAnswer: (key: AnswerKey, isCorrect: boolean) => void;
  onInteractiveAnswer?: (answer: string, isCorrect: boolean) => void;
  /** Shown between the question and the options, e.g. the question's figure. */
  figureSlot?: React.ReactNode;
}

const QuestionCard = React.memo(function QuestionCard({
  question,
  answered,
  selected,
  onAnswer,
  onInteractiveAnswer,
  figureSlot,
}: QuestionCardProps) {
  const options: Array<{ key: AnswerKey; text: string }> = [
    { key: 'A', text: question.option1 },
    { key: 'B', text: question.option2 },
    { key: 'C', text: question.option3 },
    { key: 'D', text: question.option4 },
  ];

  const level = difficultyLevel(question.difficulty);
  const topicLabel = topicChipLabel(question.subTopic);
  // Display only: the stored text, the spoken text and the grading are untouched.
  const shownText = tidyQuestionText(question.questionText || '');
  const textCls = QUESTION_TEXT_CLS[questionTextSize(shownText)];
  let compactOptions = true;
  for (let i = 0; i < options.length; i++) {
    const t = options[i].text;
    if (typeof t !== 'string' || t.length > COMPACT_OPTION_MAX || hasLatex(t)) compactOptions = false;
  }

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

        {/* Topic first, then difficulty; the read-aloud button at the right */}
        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center gap-2 flex-wrap flex-1 min-w-0">
            {topicLabel && (
              <span className="ui-chip min-w-0 max-w-full" title={question.subTopic}>
                <span className="truncate">{topicLabel}</span>
              </span>
            )}
            <span className="ui-chip bg-white flex-shrink-0">
              <span className="flex items-center gap-0.5" aria-hidden="true">
                {LEVEL_DOTS.map((n) => (
                  <span key={n} className={`w-1.5 h-1.5 rounded-full ${n <= level ? 'bg-ink' : 'bg-line'}`} />
                ))}
              </span>
              {question.difficulty}
            </span>
          </div>
          <ReadAloudButton
            text={questionToSpeech(question)}
            audioSrc={narrationAudioSrc(question.id, 'question')}
            label="the question"
          />
        </div>

        {/* Question text (17px at the smallest). KaTeX when LaTeX markers are found;
            otherwise the wording, tidied for display. */}
        <div className={`font-bold text-ink [overflow-wrap:anywhere] ${textCls}`}>
          {hasLatex(question.questionText) ? (
            <KatexRenderer latex={question.questionText} displayMode={false} />
          ) : (
            shownText
          )}
        </div>

        {/* LaTeX expression below text (if present) */}
        {question.questionLatex && (
          <div className="mt-3 overflow-x-auto p-3 bg-soft rounded-[10px] border-l-[6px] border-action">
            <KatexRenderer latex={question.questionLatex} displayMode className="block" />
          </div>
        )}

        {/* Diagram (if this question has an associated figure) */}
        {/* The older diagram set is used only where the question has no figure of its own. */}
        {!(question.visual && question.visual.figure) && <QuestionDiagram questionId={question.id} />}
      </div>

      {/* ── Optional slot between the question and the options ───────── */}
      {figureSlot}

      {/* ── Interactive question or MCQ options ──────────────────────── */}
      {question.interactionType && question.interactionData ? (
        <Suspense fallback={<div className="h-40 bg-gray-50 rounded-2xl animate-pulse" />}>
          {question.interactionType === 'tapToColor' && (
            <TapToColorQuestion
              key={question.id}
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
              key={question.id}
              data={question.interactionData as import('@/types').DragToSortData}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
          {question.interactionType === 'tileBuild' && (
            <TileBuildQuestion
              key={question.id}
              data={question.interactionData as import('@/types').TileBuildData}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
          {question.interactionType === 'numberLine' && (
            <NumberLineQuestion
              key={question.id}
              data={question.interactionData as import('@/types').NumberLineData}
              answered={answered}
              onSubmit={(answer, isCorrect) => {
                if (onInteractiveAnswer) onInteractiveAnswer(answer, isCorrect);
                onAnswer(isCorrect ? question.correctAnswer : ('A' === question.correctAnswer ? 'B' : 'A'), isCorrect);
              }}
            />
          )}
          {question.interactionType === 'chartTap' && (
            <ChartTapQuestion
              key={question.id}
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
      <div className={`grid gap-2.5 ${compactOptions ? 'sm:grid-cols-2' : ''}`}>
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

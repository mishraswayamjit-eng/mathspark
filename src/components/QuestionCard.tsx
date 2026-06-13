'use client';

import { motion, useReducedMotion } from 'framer-motion';
import KatexRenderer from './KatexRenderer';
import { humaniseSubTopic } from '@/lib/utils';
import type { AnswerKey, Question } from '@/types';

function OptionText({ text }: { text: string }) {
  const hasMath = /[\$\\^_]|\/\d|\d\//.test(text);
  if (hasMath) {
    return <KatexRenderer latex={text} />;
  }
  return <span>{text}</span>;
}

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

interface QuestionCardProps {
  question: Question;
  answered: boolean;
  selected: AnswerKey | null;
  onAnswer: (key: AnswerKey, isCorrect: boolean) => void;
}

export default function QuestionCard({
  question,
  answered,
  selected,
  onAnswer,
}: QuestionCardProps) {
  const reduce = useReducedMotion();

  const options: Array<{ key: AnswerKey; text: string }> = [
    { key: 'A', text: question.option1 },
    { key: 'B', text: question.option2 },
    { key: 'C', text: question.option3 },
    { key: 'D', text: question.option4 },
  ];

  // Visual state per option (no pure red — "not quite" uses warm amber).
  function optionClasses(key: AnswerKey): string {
    const base =
      'group w-full text-left rounded-2xl px-4 py-4 min-h-[64px] border-2 flex items-center gap-3.5 transition-all duration-200 ' +
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-spark-indigo focus-visible:ring-offset-2 focus-visible:ring-offset-surface-cream';

    if (!answered) {
      return `${base} bg-surface-card border-transparent shadow-soft hover:border-spark-indigo hover:-translate-y-0.5 hover:shadow-soft-lg cursor-pointer`;
    }
    if (key === question.correctAnswer) {
      return `${base} bg-spark-green-soft border-spark-green shadow-soft`;
    }
    if (key === selected) {
      return `${base} bg-spark-amber-soft border-spark-amber shadow-soft`;
    }
    return `${base} bg-surface-card border-transparent opacity-45`;
  }

  function chipClasses(key: AnswerKey): string {
    const base =
      'w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-bold font-body transition-colors';
    if (answered && key === question.correctAnswer) return `${base} bg-spark-green text-white`;
    if (answered && key === selected)               return `${base} bg-spark-amber text-white`;
    return `${base} bg-surface-muted text-ink-muted group-hover:bg-spark-indigo-soft group-hover:text-spark-indigo`;
  }

  return (
    <div className="space-y-5">
      {/* Question prompt */}
      <div className="bg-surface-card rounded-spark p-5 sm:p-6 shadow-soft">
        <p
          id="question-text"
          className="font-display text-xl sm:text-2xl font-semibold text-ink leading-snug"
        >
          {question.questionText}
        </p>
        {question.questionLatex && (
          <div className="mt-4 overflow-x-auto text-lg">
            <KatexRenderer latex={question.questionLatex} displayMode className="block" />
          </div>
        )}
        <p className="mt-3 text-xs font-body font-semibold text-ink-faint uppercase tracking-wide">
          {humaniseSubTopic(question.subTopic)} · {question.difficulty}
        </p>
      </div>

      {/* Options */}
      <div className="space-y-3" role="group" aria-labelledby="question-text">
        {options.map(({ key, text }) => {
          const isCorrect = answered && key === question.correctAnswer;
          const isWrongPick = answered && key === selected && key !== question.correctAnswer;
          return (
            <motion.button
              key={key}
              disabled={answered}
              onClick={() => onAnswer(key, key === question.correctAnswer)}
              className={optionClasses(key)}
              aria-label={`Option ${key}: ${text}`}
              aria-pressed={selected === key}
              whileTap={!answered && !reduce ? { scale: 0.98 } : undefined}
              animate={
                reduce
                  ? {}
                  : isCorrect
                  ? { scale: [1, 1.04, 1] }
                  : isWrongPick
                  ? { x: [0, -4, 4, -3, 3, 0] }
                  : {}
              }
              transition={{ duration: 0.4, ease: 'easeInOut' }}
            >
              <span className={chipClasses(key)}>{key}</span>
              <span className="font-body text-base text-ink flex-1">
                <OptionText text={text} />
              </span>
              {isCorrect && <span className="ml-auto text-spark-green font-bold text-lg">✓</span>}
              {isWrongPick && <span className="ml-auto text-spark-amber font-bold text-lg">!</span>}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}

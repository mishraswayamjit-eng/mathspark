'use client';

import KatexRenderer from './KatexRenderer';
import type { AnswerKey, Difficulty, Question } from '@/types';

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
  if (d === 'Easy') return { dot: 'bg-duo-green', label: 'text-duo-green-dark', bg: 'bg-green-50' };
  if (d === 'Hard') return { dot: 'bg-duo-red', label: 'text-duo-red-dark', bg: 'bg-red-50' };
  return { dot: 'bg-duo-orange', label: 'text-duo-orange-dark', bg: 'bg-amber-50' }; // Medium
}

// ── Component ─────────────────────────────────────────────────────────────────

export const LABELS: AnswerKey[] = ['A', 'B', 'C', 'D'];

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
      'w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-extrabold transition-colors duration-200';
    if (!answered) return `${base} bg-gray-100 text-gray-600`;
    if (key === question.correctAnswer)
      return `${base} bg-duo-green text-white animate-pop-in`;
    if (key === selected) return `${base} bg-duo-red text-white`;
    return `${base} bg-gray-100 text-gray-400`;
  }

  function cardCls(key: AnswerKey): string {
    const base =
      'w-full text-left rounded-2xl px-4 py-4 min-h-[56px] border-2 flex items-center gap-3 transition-colors duration-200 shadow-sm';
    if (!answered)
      return `${base} bg-white border-gray-200 hover:border-duo-blue hover:bg-blue-50 hover:shadow-md cursor-pointer`;
    if (key === question.correctAnswer)
      return `${base} bg-green-50 border-duo-green shadow-md`;
    if (key === selected)
      return `${base} bg-red-50 border-duo-red`;
    return `${base} bg-white border-gray-100 opacity-40`;
  }

  return (
    <div className="space-y-4">
      {/* ── Question card ─────────────────────────────────────────────── */}
      <div className="bg-white rounded-2xl p-5 shadow-md border border-gray-100">

        {/* SubTopic + Difficulty tags at TOP */}
        <div className="flex items-center gap-2 mb-3 flex-wrap">
          <div className={`flex items-center gap-1.5 px-2.5 py-0.5 rounded-full ${diff.bg}`}>
            <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${diff.dot}`} />
            <span className={`text-[11px] font-extrabold uppercase tracking-wide ${diff.label}`}>
              {question.difficulty}
            </span>
          </div>
          <span className="text-[11px] font-semibold text-gray-400 truncate max-w-[200px]">
            {question.subTopic}
          </span>
        </div>

        {/* Question text (min 18px) — render KaTeX if LaTeX markers detected */}
        <div className="text-[18px] font-bold text-gray-800 leading-relaxed">
          {hasLatex(question.questionText) ? (
            <KatexRenderer latex={question.questionText} displayMode={false} />
          ) : (
            question.questionText
          )}
        </div>

        {/* LaTeX expression below text (if present) */}
        {question.questionLatex && (
          <div className="mt-3 overflow-x-auto p-3 bg-gray-50 rounded-xl border border-gray-100">
            <KatexRenderer latex={question.questionLatex} displayMode className="block" />
          </div>
        )}
      </div>

      {/* ── Answer options ────────────────────────────────────────────── */}
      <div className="space-y-3">
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
            <span className="flex-1 text-left text-gray-800 text-base font-semibold leading-snug">
              {hasLatex(text) ? (
                <KatexRenderer latex={text} displayMode={false} />
              ) : (
                text
              )}
            </span>

            {/* Wrong-answer indicator */}
            {answered && key === selected && key !== question.correctAnswer && (
              <span className="ml-auto text-duo-red font-bold text-xl flex-shrink-0">✗</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

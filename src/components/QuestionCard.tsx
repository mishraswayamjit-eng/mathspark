'use client';

import KatexRenderer from './KatexRenderer';
import type { AnswerKey, Question } from '@/types';

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

const LABELS: AnswerKey[] = ['A', 'B', 'C', 'D'];

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

  function optionStyle(key: AnswerKey): string {
    const base = 'w-full text-left rounded-2xl px-4 py-4 min-h-[56px] transition-all duration-200 border-2 flex items-center gap-3';
    if (!answered) return `${base} bg-white border-gray-200 hover:border-blue-400 hover:bg-blue-50 cursor-pointer`;
    if (key === question.correctAnswer) return `${base} bg-green-50 border-green-500`;
    if (key === selected) return `${base} bg-red-50 border-red-400`;
    return `${base} bg-white border-gray-100 opacity-50`;
  }

  return (
    <div className="space-y-4">
      {/* Question text */}
      <div className="bg-white rounded-2xl p-5 shadow-sm">
        <p className="text-lg font-medium text-gray-800 leading-relaxed">
          {question.questionText}
        </p>
        {question.questionLatex && (
          <div className="mt-3 overflow-x-auto">
            <KatexRenderer latex={question.questionLatex} displayMode className="block" />
          </div>
        )}
        <p className="mt-2 text-xs text-gray-400 uppercase tracking-wide">
          {question.subTopic} · {question.difficulty}
        </p>
      </div>

      {/* Options */}
      <div className="space-y-3">
        {options.map(({ key, text }) => (
          <button
            key={key}
            disabled={answered}
            onClick={() => onAnswer(key, key === question.correctAnswer)}
            className={optionStyle(key)}
          >
            <span
              className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-bold ${
                answered && key === question.correctAnswer
                  ? 'bg-green-500 text-white'
                  : answered && key === selected
                  ? 'bg-red-400 text-white'
                  : 'bg-gray-100 text-gray-600'
              }`}
            >
              {key}
            </span>
            <span className="text-gray-800 text-base">{text}</span>
            {answered && key === question.correctAnswer && (
              <span className="ml-auto text-green-600 font-bold">✓</span>
            )}
            {answered && key === selected && key !== question.correctAnswer && (
              <span className="ml-auto text-red-500 font-bold">✗</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import type { QuizQuestion } from '@/types/lesson';

interface LessonQuizProps {
  questions: QuizQuestion[];
  accentColor: string;
  onComplete: (score: number, total: number) => void;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

function normalize(s: string): string {
  return s.trim().toLowerCase().replace(/\s+/g, ' ');
}

export default function LessonQuiz({ questions, accentColor, onComplete }: LessonQuizProps) {
  const [qIndex, setQIndex] = useState(0);
  const [input, setInput] = useState('');
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState<'correct' | 'wrong' | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  const q = questions[qIndex];
  const isLast = qIndex === questions.length - 1;

  // Focus input on new question
  useEffect(() => {
    inputRef.current?.focus();
  }, [qIndex]);

  const check = useCallback(() => {
    if (!input.trim()) return;

    const isCorrect = normalize(input) === normalize(q.answer);

    if (isCorrect) {
      setScore((s) => s + 1);
      setStreak((s) => s + 1);
      setFeedback('correct');
    } else {
      setStreak(0);
      setFeedback('wrong');
    }

    // Move to next after a short delay
    setTimeout(() => {
      setFeedback(null);
      setInput('');
      setShowHint(false);
      if (isLast) {
        const finalScore = isCorrect ? score + 1 : score;
        onCompleteRef.current(finalScore, questions.length);
      } else {
        setQIndex((i) => i + 1);
      }
    }, 1200);
  }, [input, q.answer, isLast, score, questions.length]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Enter' && !feedback) {
        check();
      }
    },
    [check, feedback],
  );

  return (
    <div className="animate-fade-in">
      {/* Header: score + streak + progress */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-sm font-extrabold text-gray-700">
            <span aria-hidden="true">⭐ </span>{score}/{questions.length}
          </span>
          {streak >= 2 && (
            <span className="text-sm font-extrabold text-orange-500 animate-pop-in">
              <span aria-hidden="true">🔥 </span>{streak} streak!
            </span>
          )}
        </div>
        <p className="text-xs font-bold text-gray-400">
          Q{qIndex + 1} of {questions.length}
        </p>
      </div>

      {/* Progress bar */}
      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden mb-5">
        <div
          className="h-full rounded-full transition-[width] duration-500"
          style={{
            width: `${((qIndex + 1) / questions.length) * 100}%`,
            backgroundColor: accentColor,
          }}
        />
      </div>

      <div key={qIndex} className="animate-fade-in">
        {/* Story box for word problems */}
        {q.story && (
          <div className="bg-purple-50 border border-purple-200 rounded-xl px-4 py-3 mb-4">
            <p className="text-xs font-bold text-purple-600 mb-1">
              <span aria-hidden="true">📖 </span>Story
            </p>
            <p className="text-sm text-purple-800 leading-relaxed">{q.story}</p>
          </div>
        )}

        {/* Question */}
        <div className="bg-white border border-gray-200 rounded-2xl px-4 py-5 mb-4 text-center shadow-sm">
          {hasLatex(q.question) ? (
            <KatexRenderer latex={q.question} displayMode className="text-lg" />
          ) : (
            <p className="text-lg font-bold text-gray-800">{q.question}</p>
          )}
        </div>

        {/* Input */}
        <div className="relative mb-4">
          <input
            ref={inputRef}
            type="text"
            inputMode="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!!feedback}
            placeholder="Your answer..."
            aria-label="Your answer"
            className={`w-full px-4 py-3.5 rounded-2xl text-center text-lg font-bold border-2 outline-none transition-colors ${
              feedback === 'correct'
                ? 'border-green-400 bg-green-50 text-green-800'
                : feedback === 'wrong'
                ? 'border-red-400 bg-red-50 text-red-800 animate-[shake_0.3s_ease-in-out]'
                : 'border-gray-200 bg-white text-gray-800 focus:border-duo-blue'
            }`}
          />
        </div>

        {/* Feedback message */}
        {feedback === 'correct' && (
          <div className="text-center mb-4 animate-pop-in">
            <p className="text-sm font-extrabold text-green-600">
              <span aria-hidden="true">✅ </span>Correct!
            </p>
          </div>
        )}
        {feedback === 'wrong' && (
          <div className="text-center mb-4 animate-pop-in">
            <p className="text-sm font-extrabold text-red-600">
              <span aria-hidden="true">❌ </span>The answer is {q.answer}
            </p>
          </div>
        )}

        {/* Check button */}
        {!feedback && (
          <button
            onClick={check}
            disabled={!input.trim()}
            className="w-full py-3.5 rounded-2xl text-sm font-extrabold text-white active:scale-95 transition-transform disabled:opacity-40"
            style={{ backgroundColor: accentColor }}
          >
            Check
          </button>
        )}

        {/* Hint toggle */}
        {!feedback && (
          <button
            onClick={() => setShowHint((h) => !h)}
            className="w-full mt-3 py-2 text-xs font-bold text-gray-500 hover:text-gray-700 transition-colors"
          >
            {showHint ? 'Hide hint' : 'Need a hint?'}
          </button>
        )}

        {showHint && !feedback && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 mt-2 animate-fade-in">
            <p className="text-xs font-semibold text-amber-800">
              <span aria-hidden="true">💡 </span>{q.hint}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

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
          <span className="text-sm font-extrabold text-ink">
            <span aria-hidden="true">⭐ </span>{score}/{questions.length}
          </span>
          {streak >= 2 && (
            <span className="text-sm font-extrabold text-ink animate-pop-in">
              <span aria-hidden="true">🔥 </span>{streak} streak!
            </span>
          )}
        </div>
        <p className="text-xs font-bold text-ink-muted">
          Q{qIndex + 1} of {questions.length}
        </p>
      </div>

      {/* Progress bar */}
      <div className="w-full h-2 bg-soft rounded-full overflow-hidden mb-5">
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
          <div className="bg-soft border-2 border-line rounded-control px-4 py-3 mb-4">
            <p className="text-xs font-bold text-ink-muted mb-1">
              <span aria-hidden="true">📖 </span>Story
            </p>
            <p className="text-sm text-ink leading-relaxed">{q.story}</p>
          </div>
        )}

        {/* Question */}
        <div className="bg-white border-2 border-line rounded-card px-4 py-5 mb-4 text-center">
          {hasLatex(q.question) ? (
            <KatexRenderer latex={q.question} displayMode className="text-lg" />
          ) : (
            <p className="text-lg font-bold text-ink">{q.question}</p>
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
            className={`w-full px-4 py-3.5 rounded-control text-center text-lg font-bold border-2 outline-none transition-colors ${
              feedback === 'correct'
                ? 'border-success bg-success-soft text-success'
                : feedback === 'wrong'
                ? 'border-retry bg-retry-soft text-retry animate-[shake_0.3s_ease-in-out]'
                : 'border-line bg-white text-ink focus:border-action'
            }`}
          />
        </div>

        {/* Feedback message */}
        {feedback === 'correct' && (
          <div className="text-center mb-4 animate-pop-in">
            <p className="text-sm font-extrabold text-success">
              <span aria-hidden="true">✅ </span>Correct!
            </p>
          </div>
        )}
        {feedback === 'wrong' && (
          <div className="text-center mb-4 animate-pop-in">
            <p className="text-sm font-extrabold text-retry">
              <span aria-hidden="true">❌ </span>The answer is {q.answer}
            </p>
          </div>
        )}

        {/* Check button */}
        {!feedback && (
          <button
            onClick={check}
            disabled={!input.trim()}
            className="w-full py-3.5 rounded-control text-sm font-extrabold text-white border-2 border-ink shadow-hard-sm active:scale-95 transition-transform disabled:opacity-40"
            style={{ backgroundColor: accentColor }}
          >
            Check
          </button>
        )}

        {/* Hint toggle */}
        {!feedback && (
          <button
            onClick={() => setShowHint((h) => !h)}
            className="w-full mt-3 py-2 text-xs font-bold text-action hover:text-action-dark transition-colors"
          >
            {showHint ? 'Hide hint' : 'Need a hint?'}
          </button>
        )}

        {showHint && !feedback && (
          <div className="bg-hint border-2 border-dashed border-hint-ink rounded-control px-4 py-3 mt-2 animate-fade-in">
            <p className="text-[13px] font-bold text-hint-ink">
              <span aria-hidden="true">💡 </span>{q.hint}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

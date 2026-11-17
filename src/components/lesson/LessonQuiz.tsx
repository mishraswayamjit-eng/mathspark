'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import type { QuizQuestion } from '@/types/lesson';
import { answerFormatHint, isQuizAnswerRight } from './quizAnswer';

interface LessonQuizProps {
  questions: QuizQuestion[];
  accentColor: string;
  onComplete: (score: number, total: number) => void;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

// What Sparky says first after a miss, before showing the answer.
const MISS_LINES = [
  "Not quite — let's look at it together.",
  'Good try! Here is how it comes out.',
  'Almost! Have a look at this one.',
];

export default function LessonQuiz({ questions, onComplete }: LessonQuizProps) {
  const [qIndex, setQIndex] = useState(0);
  const [input, setInput] = useState('');
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState<'correct' | 'miss' | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const continueRef = useRef<HTMLButtonElement>(null);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  // The running score, for the moment the quiz ends (state may not have caught up yet).
  const scoreRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const q = questions[qIndex];
  const isLast = qIndex === questions.length - 1;
  const formatHint = answerFormatHint(q.answer);

  // Focus input on new question
  useEffect(() => {
    inputRef.current?.focus();
  }, [qIndex]);

  // After a miss the child reads the answer and taps to go on: put the button under their finger.
  useEffect(() => {
    if (feedback === 'miss') continueRef.current?.focus();
  }, [feedback]);

  // Leaving the quiz: nothing fires afterwards.
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  /** On to the next question, or the end of the quiz. */
  const advance = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    setFeedback(null);
    setInput('');
    setShowHint(false);
    if (isLast) {
      onCompleteRef.current(scoreRef.current, questions.length);
    } else {
      setQIndex((i) => i + 1);
    }
  }, [isLast, questions.length]);

  const check = useCallback(() => {
    if (!input.trim() || feedback) return;

    if (isQuizAnswerRight(input, q.answer)) {
      scoreRef.current += 1;
      setScore(scoreRef.current);
      setStreak((s) => s + 1);
      setFeedback('correct');
      // A right answer moves on by itself after a moment.
      timerRef.current = setTimeout(advance, 1200);
    } else {
      setStreak(0);
      // A miss stays up until the child has read the answer and taps to go on.
      setFeedback('miss');
    }
  }, [input, feedback, q.answer, advance]);

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
        <p className="text-sm font-bold text-ink-muted">
          Q{qIndex + 1} of {questions.length}
        </p>
      </div>

      {/* Progress bar */}
      <div className="w-full h-2.5 ui-meter mb-5">
        <div
          className="h-full rounded-full bg-action transition-[width] duration-500"
          style={{
            width: `${((qIndex + 1) / questions.length) * 100}%`,
          }}
        />
      </div>

      <div key={qIndex} className="animate-fade-in">
        {/* Story box for word problems */}
        {q.story && (
          <div className="bg-soft border-2 border-line rounded-control px-4 py-3 mb-4">
            <p className="text-sm font-bold text-ink-muted mb-1">
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
            aria-describedby={formatHint ? 'quiz-format-hint' : undefined}
            className={`w-full px-4 py-3.5 rounded-control text-center text-lg font-bold border-2 outline-none transition-colors ${
              feedback === 'correct'
                ? 'border-success bg-success-soft text-success'
                : feedback === 'miss'
                ? 'border-retry bg-retry-soft text-ink'
                : 'border-line bg-white text-ink focus:border-action'
            }`}
          />
          {/* How to write the answer, when it carries a unit. The numbers are left blank. */}
          {formatHint && !feedback && (
            <p id="quiz-format-hint" className="text-sm font-semibold text-ink-muted text-center mt-2">
              Write it like this: {formatHint}
            </p>
          )}
        </div>

        {/* Feedback message */}
        <div aria-live="polite">
          {feedback === 'correct' && (
            <div className="text-center mb-4 animate-pop-in">
              <p className="text-sm font-extrabold text-success">
                <span aria-hidden="true">✅ </span>Great job!
              </p>
            </div>
          )}
          {feedback === 'miss' && (
            <div className="bg-hint border-2 border-line rounded-control px-4 py-3 mb-4 text-center animate-fade-in">
              <p className="text-sm font-bold text-ink">
                {MISS_LINES[qIndex % MISS_LINES.length]}
              </p>
              <p className="text-base font-extrabold text-ink mt-1">
                The answer is {q.answer}
              </p>
            </div>
          )}
        </div>

        {/* After a miss: the child goes on when they have read the answer */}
        {feedback === 'miss' && (
          <button
            ref={continueRef}
            type="button"
            onClick={advance}
            className="w-full ui-btn ui-btn-primary text-sm min-h-[48px]"
          >
            {isLast ? 'Finish' : 'Next question'}
          </button>
        )}

        {/* Check button */}
        {!feedback && (
          <button
            type="button"
            onClick={check}
            disabled={!input.trim()}
            className="w-full ui-btn ui-btn-primary text-sm min-h-[48px]"
          >
            Check
          </button>
        )}

        {/* Hint toggle */}
        {!feedback && (
          <button
            type="button"
            onClick={() => setShowHint((h) => !h)}
            className="w-full mt-3 min-h-[48px] text-sm font-bold text-action hover:text-action-dark transition-colors"
          >
            {showHint ? 'Hide hint' : 'Need a hint?'}
          </button>
        )}

        {showHint && !feedback && (
          <div role="note" className="bg-hint border-2 border-dashed border-hint-ink rounded-control px-4 py-3 mt-2 animate-fade-in">
            <p className="text-sm font-bold text-hint-ink">
              <span aria-hidden="true">💡 </span>{q.hint}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

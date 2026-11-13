'use client';

import { useEffect, useRef } from 'react';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

/** How ready the child feels for this topic, before the first question. */
export type Confidence = 'low' | 'medium' | 'high';

interface LessonIntroProps {
  topicName: string;
  topicEmoji: string;
  questionCount: number;
  onStart: () => void;
  /**
   * When provided, the intro asks "Could you solve these?" and waits for an
   * answer instead of auto-starting. The answer only nudges the difficulty of
   * the first few questions; it is never graded.
   */
  onConfidence?: (confidence: Confidence) => void;
}

const CONFIDENCE_CHOICES: Array<{ value: Confidence; label: string; emoji: string }> = [
  { value: 'low',    label: 'Not yet', emoji: '🌱' },
  { value: 'medium', label: 'Maybe',   emoji: '🤔' },
  { value: 'high',   label: 'Yes!',    emoji: '💪' },
];

export default function LessonIntro({ topicName, topicEmoji, questionCount, onStart, onConfidence }: LessonIntroProps) {
  const onStartRef = useRef(onStart);
  onStartRef.current = onStart;
  const asksConfidence = Boolean(onConfidence);

  // Auto-start after 3s if user doesn't tap (not while a confidence question is waiting)
  useEffect(() => {
    if (asksConfidence) return;
    const t = setTimeout(() => onStartRef.current(), 3000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-6 gap-5 text-center animate-fade-in">
      <div className="animate-sparky-bounce">
        <Sparky mood="happy" size={80} />
      </div>

      <div className="animate-pop-in text-5xl" aria-hidden="true">
        {topicEmoji}
      </div>

      <h1 className="text-2xl font-extrabold text-gray-800">
        {topicName}
      </h1>

      <p className="text-sm text-gray-500 font-semibold">
        {questionCount} questions · Earn up to {questionCount * 20} XP
      </p>

      {onConfidence ? (
        <div className="w-full max-w-xs mt-2 space-y-3">
          <p className="text-title text-ink">Could you solve these right now?</p>
          <div className="grid grid-cols-3 gap-2.5">
            {CONFIDENCE_CHOICES.map((c) => (
              <button
                key={c.value}
                type="button"
                onClick={() => { onConfidence(c.value); onStart(); }}
                className="min-h-[72px] rounded-control border-2 border-ink bg-white text-ink shadow-hard-sm flex flex-col items-center justify-center gap-1 font-extrabold text-[15px] active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[transform,box-shadow]"
              >
                <span className="text-2xl leading-none" aria-hidden="true">{c.emoji}</span>
                {c.label}
              </button>
            ))}
          </div>
          <p className="text-[13px] font-semibold text-ink-muted">
            Any answer is fine. It just helps Sparky pick your first questions.
          </p>
        </div>
      ) : (
        <div className="w-full max-w-xs mt-2">
          <DuoButton variant="green" fullWidth onClick={onStart}>
            Start
          </DuoButton>
        </div>
      )}
    </div>
  );
}

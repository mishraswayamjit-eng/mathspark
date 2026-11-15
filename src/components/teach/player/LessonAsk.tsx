'use client';

import type { BeatAsk } from '@/lib/teach/types';

/**
 * The child's turn in a lesson.
 *
 *   choose  the choices as large buttons. Once one is tapped they stay up while
 *           the teacher replies, with the right one marked. It is never asked twice.
 *   think   one button, "I've got an idea".
 * Either way the child can say "Show me" instead and the lesson carries on.
 */

interface LessonAskProps {
  ask: BeatAsk;
  /** True while the teacher is replying to the choice: the buttons no longer do anything. */
  answered: boolean;
  /** The choice the child tapped, if any. */
  picked: number | null;
  onChoose: (choice: number) => void;
  onReady: () => void;
  onShowMe: () => void;
}

export default function LessonAsk({ ask, answered, picked, onChoose, onReady, onShowMe }: LessonAskProps) {
  if (ask.kind === 'think') {
    if (answered) return null;
    return (
      <div className="space-y-2">
        <button type="button" onClick={onReady} className="ui-btn ui-btn-primary w-full min-h-[56px] text-[17px]">
          <span aria-hidden="true">💡</span> I&apos;ve got an idea
        </button>
        <button
          type="button"
          onClick={onShowMe}
          className="w-full min-h-[48px] text-[15px] font-extrabold text-ink-muted underline underline-offset-4"
        >
          Show me
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-2" role="group" aria-label="Your turn: choose one">
      {ask.choices.map((choice, i) => {
        const isRight = i === ask.answer;
        const isPicked = picked === i;
        let look = '';
        if (answered) {
          if (isRight) look = 'bg-success-soft border-success';
          else if (isPicked) look = 'bg-soft border-line shadow-none';
          else look = 'opacity-50 shadow-none';
        }
        return (
          <button
            key={i}
            type="button"
            onClick={answered ? undefined : () => onChoose(i)}
            aria-disabled={answered}
            className={`ui-btn w-full min-h-[56px] text-[17px] text-left justify-between ${look}`}
          >
            <span className="[overflow-wrap:anywhere]">{choice}</span>
            {answered && isRight && <span aria-hidden="true">✓</span>}
          </button>
        );
      })}
      {!answered && (
        <button
          type="button"
          onClick={onShowMe}
          className="w-full min-h-[48px] text-[15px] font-extrabold text-ink-muted underline underline-offset-4"
        >
          Show me
        </button>
      )}
    </div>
  );
}

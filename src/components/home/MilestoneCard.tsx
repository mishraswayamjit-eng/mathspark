'use client';

import { useEffect, useLayoutEffect, useState } from 'react';
import Sparky from '@/components/Sparky';

// Shown on the day a streak milestone is reached. The child can put it away;
// that choice is remembered for the day in localStorage. Like the plan ticks,
// the page's inline restore script hides it before first paint on a full load
// and the layout effect below covers in-app navigation.

const useIsoLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;

function milestoneKey(): string {
  return `mathspark_milestone_${new Date().toDateString()}`;
}

export default function MilestoneCard({
  emoji,
  title,
  description,
  streak,
}: {
  emoji: string;
  title: string;
  description: string;
  streak: number;
}) {
  const [dismissed, setDismissed] = useState(false);

  useIsoLayoutEffect(() => {
    try {
      if (localStorage.getItem(milestoneKey()) === 'true') setDismissed(true);
    } catch {
      // Storage blocked: keep showing the card.
    }
  }, []);

  function dismiss() {
    setDismissed(true);
    try {
      localStorage.setItem(milestoneKey(), 'true');
    } catch {
      // Storage blocked: hidden for this visit only.
    }
  }

  return (
    <div
      className="ui-card border-l-[10px] border-l-star"
      data-milestone
      hidden={dismissed}
      suppressHydrationWarning
    >
      <div className="flex items-center gap-3">
        <div className="shrink-0">
          <Sparky mood="celebrating" size={52} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-display text-xl font-semibold text-ink">
            <span aria-hidden="true">{emoji} </span>{title}
          </p>
          <p className="text-sm text-ink-muted font-medium">
            <span aria-hidden="true">🔥 </span>{`${streak} day streak · ${description}`}
          </p>
        </div>
        <button
          type="button"
          onClick={dismiss}
          aria-label="Hide this message"
          className="shrink-0 min-h-[48px] min-w-[48px] flex items-center justify-center text-ink-muted hover:text-ink text-xl leading-none"
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>
    </div>
  );
}

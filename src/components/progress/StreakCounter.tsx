'use client';

import { useEffect, useState } from 'react';
import { loadStreak, getStreakMilestone, type StreakData } from '@/lib/streak';

interface StreakCounterProps {
  /** Override streak data (from parent state). Otherwise loads from localStorage. */
  streak?: StreakData;
  /** Compact mode for inline display (no milestone text). */
  compact?: boolean;
}

export default function StreakCounter({ streak: externalStreak, compact }: StreakCounterProps) {
  const [data, setData] = useState<StreakData | null>(null);

  useEffect(() => {
    if (externalStreak) {
      setData(externalStreak);
    } else {
      setData(loadStreak());
    }
  }, [externalStreak]);

  if (!data) return null;

  const milestone = getStreakMilestone(data.currentStreak);

  if (compact) {
    return (
      <div className="flex items-center gap-1.5">
        <span className="text-lg animate-pulse">🔥</span>
        <span className="text-sm font-extrabold text-ink">
          {data.currentStreak}
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3 bg-white rounded-card px-4 py-3 border-2 border-star">
      {/* Fire emoji */}
      <div className="text-3xl animate-bounce" style={{ animationDuration: '2s' }}>
        🔥
      </div>

      {/* Streak info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-1.5">
          <span className="text-2xl font-extrabold text-ink">
            {data.currentStreak}
          </span>
          <span className="text-sm font-bold text-ink-muted">day streak</span>
        </div>

        {milestone && (
          <p className="text-xs font-bold text-ink-muted mt-0.5 truncate">
            {milestone}
          </p>
        )}
      </div>

      {/* Freeze indicator */}
      {data.freezesRemaining > 0 && (
        <div className="flex items-center gap-1 bg-soft rounded-full px-2.5 py-1 border-2 border-line">
          <span className="text-sm">❄️</span>
          <span className="text-xs font-bold text-ink">{data.freezesRemaining}</span>
        </div>
      )}
    </div>
  );
}

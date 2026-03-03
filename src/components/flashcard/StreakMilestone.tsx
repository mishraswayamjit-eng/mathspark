'use client';

import { useEffect, useState } from 'react';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import type { StreakMilestone as StreakMilestoneType } from '@/lib/flashcardXP';

// ── Streak Milestone Celebration ─────────────────────────────────────────────
// Full-screen overlay when a student hits a streak milestone (3/7/14/21/30 days).
// Auto-dismisses after 5s or on tap.

interface StreakMilestoneCelebrationProps {
  milestone: StreakMilestoneType;
  streak: number;
  onDismiss: () => void;
}

export function StreakMilestoneCelebration({
  milestone,
  streak,
  onDismiss,
}: StreakMilestoneCelebrationProps) {
  // Auto-dismiss after 5s
  useEffect(() => {
    const t = setTimeout(onDismiss, 5000);
    return () => clearTimeout(t);
  }, [onDismiss]);

  return (
    <div
      className="fixed inset-0 z-[70] bg-[#0F172A]/95 backdrop-blur-sm flex flex-col items-center justify-center px-6 animate-fade-in"
      onClick={onDismiss}
    >
      <Confetti />

      <div className="animate-sparky-dance">
        <Sparky mood="celebrating" size={90} />
      </div>

      {/* Milestone badge */}
      <div className="mt-4 mb-2 animate-pop-in">
        <span className="text-6xl">{milestone.emoji}</span>
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mb-1 animate-pop-in">
        {milestone.title}
      </h1>

      <p className="text-sm text-[#94A3B8] mb-4 text-center max-w-xs">
        {milestone.description}
      </p>

      {/* Streak count */}
      <div className="flex items-center gap-2 bg-[#1E293B] rounded-full px-4 py-2 mb-3">
        <span className="text-lg">🔥</span>
        <span className="text-lg font-black text-[#FBBF24] tabular-nums">{streak}</span>
        <span className="text-xs text-[#64748B]">day streak</span>
      </div>

      {/* XP bonus */}
      {milestone.xpBonus > 0 && (
        <div className="animate-xp-float">
          <span className="text-sm font-black text-[#34D399]">
            +{milestone.xpBonus} XP Bonus!
          </span>
        </div>
      )}

      <p className="text-xs text-[#475569] mt-6">Tap anywhere to continue</p>
    </div>
  );
}

// ── XP Popup (inline, small) ─────────────────────────────────────────────────
// Shows "+N XP" floating from where it's placed.

interface XPPopupProps {
  xp: number;
  triggerKey: number; // change this to re-trigger animation
}

export function XPPopup({ xp, triggerKey }: XPPopupProps) {
  if (xp <= 0) return null;

  return (
    <span
      key={triggerKey}
      className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-black text-[#34D399] animate-xp-float whitespace-nowrap pointer-events-none"
    >
      +{xp} XP
    </span>
  );
}

// ── Streak Progress Bar (for deck page) ──────────────────────────────────────
// Shows progress toward next milestone.

interface StreakProgressProps {
  streak: number;
  nextMilestone: StreakMilestoneType | null;
  progress: number; // 0-1
}

export function StreakProgress({ streak, nextMilestone, progress }: StreakProgressProps) {
  if (streak === 0) return null;

  return (
    <div className="flex items-center gap-3 bg-[#1E293B]/60 rounded-xl px-3 py-2">
      <div className="flex items-center gap-1.5 flex-shrink-0">
        <span className="text-sm">🔥</span>
        <span className="text-sm font-black text-[#FBBF24] tabular-nums">{streak}</span>
      </div>

      {nextMilestone ? (
        <div className="flex-1">
          <div className="flex items-center justify-between mb-0.5">
            <span className="text-[10px] text-[#64748B]">
              Next: {nextMilestone.emoji} {nextMilestone.title.replace('!', '')}
            </span>
            <span className="text-[10px] text-[#64748B] tabular-nums">
              {streak}/{nextMilestone.days}
            </span>
          </div>
          <div className="h-1 bg-white/5 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#FBBF24] rounded-full transition-all duration-500"
              style={{ width: `${progress * 100}%` }}
            />
          </div>
        </div>
      ) : (
        <span className="text-[10px] text-[#34D399] font-bold">
          👑 All milestones achieved!
        </span>
      )}
    </div>
  );
}

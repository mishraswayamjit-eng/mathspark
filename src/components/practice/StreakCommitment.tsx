'use client';

import { useState } from 'react';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

const GOALS = [
  { days: 3, emoji: '🌱', label: 'Getting started', color: 'border-action' },
  { days: 7, emoji: '🔥', label: 'Building momentum', color: 'border-action' },
  { days: 14, emoji: '🏆', label: 'Going strong', color: 'border-action' },
] as const;

interface StreakCommitmentProps {
  onDone: () => void;
}

export default function StreakCommitment({ onDone }: StreakCommitmentProps) {
  const [selected, setSelected] = useState(7);

  const handleConfirm = () => {
    localStorage.setItem('mathspark_streakGoal', String(selected));
    localStorage.setItem('mathspark_streakGoalSet', 'true');
    onDone();
  };

  return (
    <div className="fixed inset-0 z-[80] bg-paper flex flex-col items-center justify-center px-6 animate-fade-in">
      <div className="animate-sparky-bounce">
        <Sparky mood="happy" size={100} />
      </div>

      <h1 className="text-display text-ink mt-4 mb-1 text-center">
        Build a study habit!
      </h1>
      <p className="text-sm text-ink-muted font-semibold mb-6 text-center">
        How many days in a row can you practice?
      </p>

      <div className="w-full max-w-xs space-y-3">
        {GOALS.map((g) => (
          <button
            key={g.days}
            onClick={() => setSelected(g.days)}
            className={`w-full rounded-control border-2 px-4 py-4 flex items-center gap-3 transition-colors ${
              selected === g.days
                ? `${g.color} bg-soft`
                : 'border-line bg-white'
            }`}
          >
            <span className="text-2xl" aria-hidden="true">{g.emoji}</span>
            <div className="text-left">
              <p className="text-base font-extrabold text-ink">{g.days} days</p>
              <p className="text-xs text-ink-muted font-semibold">{g.label}</p>
            </div>
            {selected === g.days && (
              <span className="ml-auto text-action text-lg font-extrabold">✓</span>
            )}
          </button>
        ))}
      </div>

      <div className="w-full max-w-xs mt-6 space-y-3">
        <DuoButton variant="green" fullWidth onClick={handleConfirm}>
          Set my goal
        </DuoButton>
        <button
          onClick={() => {
            localStorage.setItem('mathspark_streakGoalSet', 'true');
            onDone();
          }}
          className="w-full text-sm text-ink-muted font-bold min-h-[44px]"
        >
          Skip for now
        </button>
      </div>
    </div>
  );
}

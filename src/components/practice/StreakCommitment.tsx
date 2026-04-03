'use client';

import { useState } from 'react';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

const GOALS = [
  { days: 3, emoji: '🌱', label: 'Getting started', color: 'border-duo-green' },
  { days: 7, emoji: '🔥', label: 'Building momentum', color: 'border-duo-orange' },
  { days: 14, emoji: '🏆', label: 'Going strong', color: 'border-duo-gold' },
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
    <div className="fixed inset-0 z-[80] bg-white flex flex-col items-center justify-center px-6 animate-fade-in">
      <div className="animate-sparky-bounce">
        <Sparky mood="happy" size={100} />
      </div>

      <h1 className="text-2xl font-extrabold text-gray-800 mt-4 mb-1 text-center">
        Build a study habit!
      </h1>
      <p className="text-sm text-gray-500 font-medium mb-6 text-center">
        How many days in a row can you practice?
      </p>

      <div className="w-full max-w-xs space-y-3">
        {GOALS.map((g) => (
          <button
            key={g.days}
            onClick={() => setSelected(g.days)}
            className={`w-full rounded-2xl border-2 px-4 py-4 flex items-center gap-3 transition-colors ${
              selected === g.days
                ? `${g.color} bg-gray-50`
                : 'border-gray-200 bg-white'
            }`}
          >
            <span className="text-2xl" aria-hidden="true">{g.emoji}</span>
            <div className="text-left">
              <p className="text-base font-extrabold text-gray-800">{g.days} days</p>
              <p className="text-xs text-gray-500 font-medium">{g.label}</p>
            </div>
            {selected === g.days && (
              <span className="ml-auto text-duo-green text-lg">✓</span>
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
          className="w-full text-sm text-gray-400 font-semibold min-h-[44px]"
        >
          Skip for now
        </button>
      </div>
    </div>
  );
}

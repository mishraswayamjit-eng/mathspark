'use client';

import DuoButton from '@/components/DuoButton';

export default function LeaderboardError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white gap-4 p-8 text-center">
      <p className="text-5xl">😕</p>
      <h2 className="font-extrabold text-gray-800 text-lg">League temporarily unavailable</h2>
      <p className="text-gray-400 text-sm font-medium">
        {error.message ?? 'Something went wrong loading the leaderboard.'}
      </p>
      <DuoButton variant="blue" onClick={reset}>Try Again</DuoButton>
    </div>
  );
}

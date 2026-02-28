'use client';

import { useEffect } from 'react';

export default function ChaptersError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => console.error(error), [error]);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-8 text-center">
      <div className="text-6xl mb-4">🧮</div>
      <h2 className="text-xl font-extrabold text-gray-800 mb-2">
        Oops! Sparky tripped over a number!
      </h2>
      <p className="text-gray-400 text-sm mb-6">Something went wrong. Let&apos;s try again!</p>
      <button
        onClick={reset}
        className="bg-[#58CC02] text-white font-extrabold rounded-2xl px-8 py-3"
      >
        Try Again
      </button>
    </div>
  );
}

'use client';

import { useEffect } from 'react';

export default function PageError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => console.error(error), [error]);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-8 text-center">
      <div className="text-6xl mb-4" aria-hidden="true">&#x1F464;</div>
      <h2 className="text-xl font-extrabold text-gray-800 mb-2">
        Profile page hit a snag!
      </h2>
      <p className="text-gray-500 text-sm mb-6">Something went wrong. Let&apos;s try again!</p>
      <button
        onClick={reset}
        className="bg-duo-green text-white font-extrabold rounded-2xl px-8 py-3"
      >
        Try Again
      </button>
    </div>
  );
}

'use client';

import { useEffect } from 'react';
import { logError } from '@/lib/logger';

export default function PageError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => logError('[chat] error boundary', error), [error]);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-paper p-8 text-center">
      <div className="text-6xl mb-4" aria-hidden="true">&#x1F4AC;</div>
      <h2 className="text-xl font-extrabold text-ink mb-2">
        The chat ran into trouble!
      </h2>
      <p className="text-ink-muted text-sm mb-6">Oops! Sparky tripped over a number. Let&apos;s try again!</p>
      <button
        onClick={reset}
        className="bg-action text-white font-extrabold rounded-control border-2 border-ink shadow-hard-sm px-8 py-3"
      >
        Try Again
      </button>
    </div>
  );
}

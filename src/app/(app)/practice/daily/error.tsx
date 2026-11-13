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
  useEffect(() => logError('[practice/daily] error boundary', error), [error]);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-paper p-8 text-center">
      <div className="text-6xl mb-4" aria-hidden="true">&#x1F3AF;</div>
      <h2 className="text-heading text-ink mb-2">
        Daily practice hit a snag!
      </h2>
      <p className="text-ink-muted text-sm mb-6">Something went wrong. Let&apos;s try again!</p>
      <button
        onClick={reset}
        className="ui-btn ui-btn-primary px-8"
      >
        Try Again
      </button>
    </div>
  );
}

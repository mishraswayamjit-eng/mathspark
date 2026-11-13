'use client';

import { useEffect } from 'react';
import { logError } from '@/lib/logger';
import DuoButton from '@/components/DuoButton';

export default function TestError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    logError('[/test error boundary]', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 text-center gap-6">
      <span className="text-6xl">😕</span>
      <div className="space-y-2">
        <h2 className="text-heading text-ink">Oops! Sparky tripped over a number</h2>
        <p className="text-ink-muted font-medium text-sm">
          We couldn&apos;t load your test. Don&apos;t worry — your progress is saved!
        </p>
      </div>
      <div className="w-full max-w-xs space-y-3">
        <DuoButton variant="blue" fullWidth onClick={reset}>
          Try again
        </DuoButton>
        <a href="/test" className="block text-action text-sm font-semibold text-center py-2">
          Back to tests
        </a>
      </div>
    </div>
  );
}

'use client';

import { useEffect } from 'react';
import DuoButton from '@/components/DuoButton';

export default function TestError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('[/test error boundary]', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6 text-center gap-6">
      <span className="text-6xl">😕</span>
      <div className="space-y-2">
        <h2 className="text-xl font-extrabold text-gray-800">Something went wrong</h2>
        <p className="text-gray-500 font-medium text-sm">
          We couldn&apos;t load your test. Don&apos;t worry — your progress is saved!
        </p>
      </div>
      <div className="w-full max-w-xs space-y-3">
        <DuoButton variant="blue" fullWidth onClick={reset}>
          Try again
        </DuoButton>
        <a href="/test" className="block text-gray-400 text-sm font-semibold text-center py-2">
          Back to tests
        </a>
      </div>
    </div>
  );
}

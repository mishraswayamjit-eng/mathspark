'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6 text-center">
      <div className="text-6xl mb-4">🤔</div>
      <h2 className="text-2xl font-bold text-gray-800 mb-2">
        Oops! Something went a bit wobbly
      </h2>
      <p className="text-gray-500 mb-6 text-base">
        Don't worry — your progress is saved. Let's try again!
      </p>
      <button
        onClick={reset}
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-2xl text-base min-h-[48px] transition-colors"
      >
        Try again 🚀
      </button>
      <a
        href="/chapters"
        className="mt-3 text-blue-500 underline text-sm"
      >
        Go back to chapters
      </a>
    </div>
  );
}

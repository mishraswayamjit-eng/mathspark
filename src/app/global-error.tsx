'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6 text-center font-sans">
        <div className="text-6xl mb-4">😅</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Something went wrong
        </h2>
        <p className="text-gray-500 mb-6">
          MathSpark hit a bump. Your progress is safe!
        </p>
        <button
          onClick={reset}
          className="bg-blue-500 text-white font-semibold px-6 py-3 rounded-2xl min-h-[48px]"
        >
          Try again 🚀
        </button>
      </body>
    </html>
  );
}

import Link from 'next/link';

// The one loading skeleton for a worked example. Used by loading.tsx and by
// page.tsx while the example loads, so both show the same placeholder.
export default function ExampleSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/learn/examples" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1 min-w-0">
          <h1 className="text-white text-title">Loading...</h1>
          <div className="h-4" />
        </div>
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
        <div className="bg-white rounded-card p-6 border-2 border-line animate-pulse h-40" />
        <div className="bg-white rounded-card p-6 border-2 border-line animate-pulse h-60" />
      </div>
    </div>
  );
}

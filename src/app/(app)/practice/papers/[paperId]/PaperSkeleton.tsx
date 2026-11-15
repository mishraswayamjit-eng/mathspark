import Sparky from '@/components/Sparky';

// The one loader for an exam paper. Used by loading.tsx and by page.tsx while
// the paper loads, so both show the same thing.
export default function PaperSkeleton() {
  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 gap-4">
      <Sparky mood="thinking" size={64} />
      <p className="text-sm font-bold text-ink-muted animate-pulse">Loading exam paper...</p>
    </div>
  );
}

import Sparky from '@/components/Sparky';

// Mirrors the session page's own first loader (page.tsx, phase === 'loading'),
// so the child sees one loader instead of the /practice topic grid followed by
// this one. Keep the two in step if either changes.
export default function PracticeSessionLoading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-paper gap-4 px-6">
      <div className="animate-sparky-bounce">
        <Sparky mood="thinking" size={100} />
      </div>
      <p className="text-ink-muted font-semibold">Loading your lesson…</p>
    </div>
  );
}

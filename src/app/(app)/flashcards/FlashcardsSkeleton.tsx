// The one loading skeleton for /flashcards.
// - FlashcardsBodySkeleton is what page.tsx shows under its (real) header while
//   the decks load. It reserves the stats strip, so nothing jumps when data lands.
// - The default export adds a header bar of the same height and is what
//   loading.tsx shows while the route itself loads.

export function FlashcardsBodySkeleton() {
  return (
    <>
      {/* Stats strip: totals card + "new cards today" row */}
      <div className="space-y-3">
        <div className="h-[72px] bg-card border-2 border-line rounded-card animate-pulse" />
        <div className="h-10 bg-card border-2 border-line rounded-control animate-pulse" />
      </div>
      {/* Quick Start decks */}
      <div className="space-y-2">
        <div className="h-7 w-28 mx-1 bg-line rounded animate-pulse" />
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-20 bg-card border-2 border-line rounded-card animate-pulse" />
        ))}
      </div>
      {/* Game modes */}
      <div className="space-y-2">
        <div className="h-7 w-32 mx-1 bg-line rounded animate-pulse" />
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-[76px] bg-card border-2 border-line rounded-card animate-pulse" />
        ))}
      </div>
    </>
  );
}

export default function FlashcardsSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="sticky top-0 z-30 bg-ink px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto h-12">
          <div className="h-4 w-14 rounded bg-white/20 animate-pulse" />
          <div className="h-6 w-36 rounded bg-white/20 animate-pulse" />
          <div className="w-12" />
        </div>
      </div>
      <div className="max-w-md mx-auto px-4 pt-4 space-y-6">
        <FlashcardsBodySkeleton />
      </div>
    </div>
  );
}

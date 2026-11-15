// The one loading skeleton for /leaderboard.
// - LeagueListLoading is the loader page.tsx shows inside the list panel while
//   this week's league loads.
// - The default export is the whole page in its loading state (header bar,
//   status card, tab bar, list panel) and is what loading.tsx shows, so the
//   route loader and the page's own loader look the same.

export function LeagueListLoading() {
  return (
    <div className="py-20 flex flex-col items-center gap-3">
      <div className="w-10 h-10 rounded-full border-4 border-action border-t-transparent animate-spin" />
      <p className="text-gray-500 font-semibold text-sm">Loading your league…</p>
    </div>
  );
}

export default function LeaderboardSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header bar */}
      <div className="bg-ink pt-10 pb-4 px-4">
        <div className="h-7 w-32 rounded bg-white/20 animate-pulse" />
        <div className="h-5 w-64 max-w-full rounded bg-white/20 animate-pulse mt-0.5" />
      </div>
      {/* Status card */}
      <div className="mt-4 mb-4">
        <div className="mx-4 rounded-card bg-soft animate-pulse h-28" />
      </div>
      {/* Tab bar */}
      <div className="flex mx-4 gap-1 bg-soft border-2 border-line rounded-control p-1 mb-2">
        <div className="flex-1 h-8 rounded-note bg-line animate-pulse" />
        <div className="flex-1 h-8" />
        <div className="flex-1 h-8" />
      </div>
      {/* List panel */}
      <div className="bg-white rounded-t-card border-t-2 border-line overflow-hidden">
        <LeagueListLoading />
      </div>
    </div>
  );
}

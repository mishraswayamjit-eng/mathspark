// The one Home skeleton. Used by home/loading.tsx and by anything else that has
// to wait on the Home screen, so the child only ever sees a single placeholder.
// It mirrors the real layout block for block (dark header, stats row, hero,
// plan, topics) so nothing jumps when the content arrives.
// No hooks: works as a server or a client component.

export default function HomeSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24" aria-busy="true" aria-label="Loading your home screen">
      {/* Header (same height as the real one: 48px avatar + 8px padding each side) */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-2 flex items-center gap-3">
        <div className="flex-1 min-w-0 space-y-2">
          <div className="h-5 bg-white/20 rounded w-44 animate-pulse" />
          <div className="h-3 bg-white/20 rounded w-24 animate-pulse" />
        </div>
        <div className="w-12 h-12 rounded-full bg-white/20 shrink-0 animate-pulse" />
      </div>

      <div className="px-4 pt-4 space-y-4">
        {/* Narration line + stat pills */}
        <div className="space-y-2.5 animate-pulse">
          <div className="h-4 bg-soft rounded w-40" />
          <div className="flex gap-2">
            <div className="h-9 bg-soft rounded-tile w-16" />
            <div className="h-9 bg-soft rounded-tile w-20" />
            <div className="h-9 bg-soft rounded-tile w-24" />
          </div>
        </div>

        {/* Hero card */}
        <div className="bg-card rounded-card border-2 border-line h-[84px] animate-pulse" />

        {/* Plan card */}
        <div className="bg-card rounded-card p-4 border-2 border-line animate-pulse">
          <div className="h-4 bg-soft rounded w-28 mb-3" />
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-3 py-3 min-h-[56px] border-b-2 border-line last:border-b-0">
              <div className="w-6 h-6 rounded-full bg-soft shrink-0" />
              <div className="w-6 h-6 rounded bg-soft shrink-0" />
              <div className="flex-1 space-y-1.5">
                <div className="h-3.5 bg-soft rounded w-3/4" />
                <div className="h-2.5 bg-soft rounded w-1/2" />
              </div>
              <div className="h-5 bg-soft rounded-full w-10 shrink-0" />
            </div>
          ))}
        </div>

        {/* Topics card */}
        <div className="bg-card rounded-card p-4 border-2 border-line animate-pulse">
          <div className="h-4 bg-soft rounded w-24 mb-4" />
          {[0, 1, 2].map((i) => (
            <div key={i} className="flex items-center gap-3 py-1.5">
              <div className="w-6 h-6 rounded bg-soft shrink-0" />
              <div className="w-28 h-3 bg-soft rounded shrink-0" />
              <div className="flex-1 h-2 bg-soft rounded-full" />
              <div className="w-9 h-3 bg-soft rounded shrink-0" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

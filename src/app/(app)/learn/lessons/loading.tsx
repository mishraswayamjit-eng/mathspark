export default function LessonsLoading() {
  return (
    <div className="min-h-screen bg-paper pb-24 animate-pulse">
      {/* Same bar as the page header (sticky, 60px tall) */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4">
        <div className="h-7 bg-white/20 rounded w-40" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro box skeleton */}
        <div className="bg-white rounded-card p-4 border-2 border-line h-[66px] mb-5" />
        {/* Grid skeleton */}
        <div className="grid grid-cols-2 gap-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-card p-4 border-2 border-line h-44" />
          ))}
        </div>
      </div>
    </div>
  );
}

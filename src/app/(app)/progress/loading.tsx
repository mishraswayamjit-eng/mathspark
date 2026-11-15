export default function ProgressLoading() {
  return (
    // Same markup as the loading state inside progress/page.tsx, so the route
    // loader and the page's own loader are one skeleton. Keep the two in step.
    <div className="min-h-screen bg-paper pb-24">
      <div className="bg-ink px-4 py-4 flex items-center gap-3">
        <div className="h-5 bg-white/20 rounded w-24 animate-pulse" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
        {[0, 1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-28" />
        ))}
      </div>
    </div>
  );
}

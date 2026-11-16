export default function TestLoading() {
  return (
    // Mirrors test/page.tsx: dark header bar, then the three test cards.
    <div className="min-h-screen bg-paper pb-28">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <div className="min-h-[48px] min-w-[48px]" />
        <div>
          <div className="h-6 w-20 bg-white/20 rounded mb-1" />
          <div className="h-3 w-52 bg-white/20 rounded" />
        </div>
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4 animate-pulse">
        <div className="bg-white border-2 border-line rounded-card h-[168px]" />
        <div className="bg-white border-2 border-line rounded-card h-[168px]" />
        <div className="bg-white border-2 border-line rounded-card h-[260px]" />
      </div>
    </div>
  );
}

export default function TestLoading() {
  return (
    // Mirrors test/page.tsx: no dark bar, back link + title row, four paper
    // options, the rules card and the start button.
    <div className="min-h-screen bg-paper flex flex-col pb-28 animate-pulse">
      <div className="px-4 pt-8 pb-4">
        <div className="h-12 mb-4 flex items-center">
          <div className="h-4 w-14 bg-line rounded" />
        </div>
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-line rounded-full shrink-0" />
          <div>
            <div className="h-8 w-48 bg-line rounded mb-1" />
            <div className="h-4 w-56 bg-line rounded" />
          </div>
        </div>
      </div>
      <div className="px-4">
        <div className="h-4 w-28 bg-line rounded mb-2" />
        <div className="space-y-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-white rounded-control border-2 border-line h-[76px]" />
          ))}
        </div>
      </div>
      <div className="px-4 mt-3">
        <div className="bg-white border-2 border-line rounded-card h-[92px]" />
      </div>
      <div className="px-4 mt-4">
        <div className="h-12 bg-line rounded-control" />
      </div>
    </div>
  );
}

export default function ChaptersLoading() {
  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
      <div className="bg-duo-dark px-4 py-4 flex items-center gap-3">
        <div className="h-5 bg-white/20 rounded w-24" />
        <div className="ml-auto flex gap-3">
          <div className="h-5 bg-white/20 rounded w-12" />
          <div className="h-5 bg-white/20 rounded w-12" />
        </div>
      </div>
      <div className="max-w-lg mx-auto px-4 pt-4">
        {/* Grade tabs */}
        <div className="flex gap-2 mb-4 overflow-hidden">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-9 bg-gray-200 rounded-full w-16 shrink-0" />
          ))}
        </div>
        {/* Topic cards */}
        <div className="space-y-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 h-24 flex items-center gap-3">
              <div className="w-12 h-12 bg-gray-200 rounded-xl shrink-0" />
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                <div className="h-2 bg-gray-100 rounded-full w-full" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

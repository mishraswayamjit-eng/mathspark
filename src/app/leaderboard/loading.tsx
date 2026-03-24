export default function LeaderboardLoading() {
  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
      <div className="bg-duo-dark px-4 py-4">
        <div className="h-6 bg-white/20 rounded w-24" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-4">
        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          <div className="h-9 bg-gray-200 rounded-full w-28" />
          <div className="h-9 bg-gray-100 rounded-full w-28" />
        </div>
        {/* Tier badge */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 mb-4 h-20" />
        {/* Member rows */}
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="flex items-center gap-3 py-3 border-b border-gray-50">
            <div className="w-6 h-4 bg-gray-200 rounded" />
            <div className="w-10 h-10 bg-gray-200 rounded-full" />
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-28 mb-1" />
              <div className="h-3 bg-gray-100 rounded w-16" />
            </div>
            <div className="h-4 bg-gray-200 rounded w-12" />
          </div>
        ))}
      </div>
    </div>
  );
}

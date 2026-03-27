export default function HomeLoading() {
  return (
    <div className="px-4 pt-6 pb-24 animate-pulse">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 bg-gray-200 rounded-full" />
        <div>
          <div className="h-5 bg-gray-200 rounded w-32 mb-1" />
          <div className="h-3 bg-gray-100 rounded w-20" />
        </div>
      </div>
      {/* Stats cards */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-2xl p-4 h-20" />
        ))}
      </div>
      {/* Continue section */}
      <div className="h-5 bg-gray-200 rounded w-40 mb-3" />
      <div className="bg-gray-100 rounded-2xl h-24 mb-6" />
      {/* Quick actions */}
      <div className="grid grid-cols-2 gap-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-2xl h-20" />
        ))}
      </div>
    </div>
  );
}

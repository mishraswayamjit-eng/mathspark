export default function ProgressLoading() {
  return (
    <div className="px-4 pt-6 pb-24 animate-pulse">
      <div className="h-7 bg-gray-200 rounded-lg w-36 mb-6" />
      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-2xl p-4 text-center h-20">
            <div className="h-6 bg-gray-200 rounded w-12 mx-auto mb-2" />
            <div className="h-3 bg-gray-200 rounded w-16 mx-auto" />
          </div>
        ))}
      </div>
      {/* Chart placeholder */}
      <div className="bg-gray-100 rounded-2xl h-48 mb-6" />
      {/* Topic list */}
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-xl p-4 h-16" />
        ))}
      </div>
    </div>
  );
}

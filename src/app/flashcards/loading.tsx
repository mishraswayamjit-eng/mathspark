export default function FlashcardsLoading() {
  return (
    <div className="px-4 pt-6 pb-24 animate-pulse">
      <div className="h-7 bg-gray-200 rounded-lg w-40 mb-2" />
      <div className="h-4 bg-gray-100 rounded w-64 mb-6" />
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-2xl p-4 h-20 flex items-center gap-4">
            <div className="w-12 h-12 bg-gray-200 rounded-xl shrink-0" />
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

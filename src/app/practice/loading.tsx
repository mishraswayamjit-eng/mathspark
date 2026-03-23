export default function PracticeLoading() {
  return (
    <div className="px-4 pt-6 pb-24 animate-pulse">
      <div className="h-7 bg-gray-200 rounded-lg w-48 mb-6" />
      <div className="grid grid-cols-2 gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-2xl p-4 h-28">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-3" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        ))}
      </div>
    </div>
  );
}

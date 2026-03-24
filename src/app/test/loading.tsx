export default function TestLoading() {
  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
      <div className="bg-duo-dark px-4 py-4">
        <div className="h-6 bg-white/20 rounded w-32" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-6 space-y-4">
        {/* Test type cards */}
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl p-5 border border-gray-100 h-28" />
        ))}
        {/* History section */}
        <div className="h-5 bg-gray-200 rounded w-32 mt-6" />
        {Array.from({ length: 2 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 h-20" />
        ))}
      </div>
    </div>
  );
}

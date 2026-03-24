export default function LearnLoading() {
  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
      <div className="bg-duo-dark px-4 py-4">
        <div className="h-6 bg-white/20 rounded w-28" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-6 space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl p-5 border border-gray-100 h-24" />
        ))}
      </div>
    </div>
  );
}

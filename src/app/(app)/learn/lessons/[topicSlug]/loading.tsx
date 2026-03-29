export default function TopicLoading() {
  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
      <div className="bg-duo-dark px-4 py-4">
        <div className="h-6 bg-white/20 rounded w-32" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-6 space-y-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 h-24" />
        ))}
      </div>
    </div>
  );
}

export default function Loading() {
  return (
    <div className="min-h-screen bg-white p-4 space-y-4 animate-pulse">
      <div className="h-6 bg-gray-100 rounded-xl w-1/3" />
      <div className="h-40 bg-gray-100 rounded-2xl" />
      <div className="space-y-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-16 bg-gray-100 rounded-2xl" />
        ))}
      </div>
    </div>
  );
}

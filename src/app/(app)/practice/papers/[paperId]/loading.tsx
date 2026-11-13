export default function Loading() {
  return (
    <div className="min-h-screen bg-paper p-4 space-y-4 animate-pulse">
      <div className="h-6 bg-line rounded-tile w-1/3" />
      <div className="h-40 bg-white border-2 border-line rounded-card" />
      <div className="space-y-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-16 bg-white border-2 border-line rounded-control" />
        ))}
      </div>
    </div>
  );
}

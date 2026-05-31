'use client';

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-3" />
      <div className="h-3 bg-gray-200 rounded w-1/2 mb-6" />
      <div className="space-y-3">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-14 bg-gray-200 rounded-xl" />
        ))}
      </div>
    </div>
  );
}

export function SkeletonStatRow() {
  return (
    <div className="grid grid-cols-3 gap-3 animate-pulse">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="h-8 bg-gray-200 rounded mb-2" />
          <div className="h-3 bg-gray-200 rounded w-2/3" />
        </div>
      ))}
    </div>
  );
}

export function SkeletonGrid({ count = 16 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 gap-3 animate-pulse">
      {[...Array(count)].map((_, i) => (
        <div key={i} className="bg-white rounded-2xl p-4 shadow-sm h-28 border border-gray-100" />
      ))}
    </div>
  );
}

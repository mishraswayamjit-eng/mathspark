'use client';

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
      <div className="h-4 skeleton-shimmer rounded w-3/4 mb-3" />
      <div className="h-3 skeleton-shimmer rounded w-1/2 mb-6" />
      <div className="space-y-3">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-14 skeleton-shimmer rounded-2xl" />
        ))}
      </div>
    </div>
  );
}

export function SkeletonStatRow() {
  return (
    <div className="grid grid-cols-3 gap-3">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="bg-white rounded-2xl p-4 shadow-sm">
          <div className="h-8 skeleton-shimmer rounded mb-2" />
          <div className="h-3 skeleton-shimmer rounded w-2/3" />
        </div>
      ))}
    </div>
  );
}

export function SkeletonGrid({ count = 16 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {[...Array(count)].map((_, i) => (
        <div key={i} className="bg-white rounded-2xl p-4 border-2 border-gray-100 flex flex-col gap-2 h-36">
          <div className="h-3 skeleton-shimmer rounded w-1/3" />
          <div className="h-4 skeleton-shimmer rounded w-3/4" />
          <div className="h-5 skeleton-shimmer rounded-full w-1/2" />
          <div className="mt-auto h-1.5 skeleton-shimmer rounded-full w-full" />
        </div>
      ))}
    </div>
  );
}

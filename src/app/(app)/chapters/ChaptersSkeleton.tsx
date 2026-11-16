import React from 'react';

// The one loading skeleton for /chapters. Used by both loading.tsx (while the
// route loads) and page.tsx (while its data loads), so the child sees a single
// placeholder that keeps the page's real layout: dark top bar, greeting, grade
// tabs, coverage bar, the mock test card, the list heading and the topic rows.
export default function ChaptersSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Top bar */}
      <div className="sticky top-0 z-50 h-14 bg-ink flex items-center justify-between px-4">
        <div className="h-5 w-24 rounded-full bg-white/20 animate-pulse" />
        <div className="flex gap-2">
          {[1, 2, 3, 4].map((n) => (
            <div key={n} className="h-6 w-12 rounded-full bg-white/20 animate-pulse" />
          ))}
        </div>
      </div>
      {/* Greeting */}
      <div className="px-4 pt-5 pb-2">
        <div className="h-7 w-64 max-w-full rounded-xl bg-gray-200 animate-pulse mb-1" />
        <div className="h-7 w-40 rounded-xl bg-gray-200 animate-pulse mb-1" />
        <div className="h-4 w-36 rounded-xl bg-gray-200 animate-pulse" />
      </div>
      {/* Grade tabs */}
      <div className="flex gap-2 px-4 pb-3 overflow-hidden">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className="flex-shrink-0 h-9 w-16 rounded-full bg-gray-200 animate-pulse" />
        ))}
      </div>
      {/* Syllabus coverage bar */}
      <div className="px-4 pb-3">
        <div className="flex items-center justify-between mb-1.5">
          <div className="h-4 w-28 rounded bg-gray-200 animate-pulse" />
          <div className="h-4 w-32 rounded bg-gray-200 animate-pulse" />
        </div>
        <div className="h-2 bg-soft rounded-full" />
      </div>
      {/* Mock test entry card */}
      <div className="px-4 pt-1">
        <div className="h-[68px] mb-3 bg-white border-2 border-line rounded-card animate-pulse" />
      </div>
      {/* Topic list: group heading, then one card per topic */}
      <div className="px-4 pt-1">
        <div className="h-[25px] w-36 mb-3 rounded-full bg-gray-200 animate-pulse" />
        <div className="space-y-3">
          {Array.from({ length: 6 }, (_, i) => (
            <div key={i} className="h-[76px] bg-white border-2 border-line rounded-card animate-pulse" />
          ))}
        </div>
      </div>
    </div>
  );
}

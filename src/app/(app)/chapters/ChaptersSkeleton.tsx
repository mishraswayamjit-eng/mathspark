import React from 'react';

// The one loading skeleton for /chapters. Used by both loading.tsx (while the
// route loads) and page.tsx (while its data loads), so the child sees a single
// placeholder that keeps the page's real layout: dark top bar, greeting, the
// lessons banner, grade tabs, coverage bar, two entry cards and the skill path.
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
      {/* Concept lessons banner */}
      <div className="mx-4 mb-3 h-16 bg-white border-2 border-line rounded-card animate-pulse" />
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
      {/* Flashcards + mock test entry cards */}
      <div className="px-4 pt-1">
        <div className="h-[68px] mb-3 bg-white border-2 border-line rounded-card animate-pulse" />
        <div className="h-[68px] mb-3 bg-white border-2 border-line rounded-card animate-pulse" />
      </div>
      {/* Skill path */}
      <div className="px-4 space-y-2">
        {Array.from({ length: 6 }, (_, i) => (
          <React.Fragment key={i}>
            {i > 0 && <div className="flex justify-center"><div className="w-1 h-8 bg-gray-200 rounded-full" /></div>}
            <div className={`flex items-center gap-3 px-3 py-3 ${i % 2 === 1 ? 'flex-row-reverse' : ''}`}>
              <div className="w-14 h-14 rounded-full bg-gray-200 animate-pulse flex-shrink-0" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-32 rounded-xl bg-gray-200 animate-pulse" />
                <div className="h-3 w-20 rounded-xl bg-gray-200 animate-pulse" />
              </div>
            </div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

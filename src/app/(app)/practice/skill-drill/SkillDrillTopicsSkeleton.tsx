import Link from 'next/link';

// The one loading skeleton for /practice/skill-drill. Used by loading.tsx and
// by page.tsx while the topics load, so both show the same placeholder. It
// keeps the page's real layout: sticky header (title + one line under it),
// intro box, level legend, then the topic cards.
export default function SkillDrillTopicsSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/practice" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Skill Drills</h1>
          <div className="h-4" />
        </div>
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro box */}
        <div className="bg-soft rounded-card border-2 border-line mb-5 h-[66px] animate-pulse" />
        {/* Level legend */}
        <div className="flex gap-1.5 mb-5 pb-1 overflow-hidden">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="h-7 w-20 bg-white rounded-full border-2 border-line shrink-0 animate-pulse" />
          ))}
        </div>
        {/* Topic cards */}
        <div className="space-y-3">
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-24" />
          ))}
        </div>
      </div>
    </div>
  );
}

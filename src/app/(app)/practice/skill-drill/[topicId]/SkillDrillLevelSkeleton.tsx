import Link from 'next/link';

// The one loading skeleton for a skill-drill level (the list of sessions).
// Used by loading.tsx and by [levelId]/page.tsx while the sessions load, so
// both show the same placeholder. The bar is as tall as the real header
// (title line + level line).
export default function SkillDrillLevelSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/practice/skill-drill" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title leading-8">Loading...</h1>
          <div className="h-4 mt-0.5" />
        </div>
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Level tabs */}
        <div className="flex gap-1.5 mb-5 pb-1 overflow-hidden">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-10 w-24 rounded-full bg-white border-2 border-line animate-pulse shrink-0" />
          ))}
        </div>
        <div className="space-y-3">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-20" />
          ))}
        </div>
      </div>
    </div>
  );
}

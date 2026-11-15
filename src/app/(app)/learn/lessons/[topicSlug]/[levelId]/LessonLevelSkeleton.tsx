// The one loading skeleton for a lesson level. Used by loading.tsx and by
// page.tsx while the level loads, so both show the same placeholder.
export default function LessonLevelSkeleton() {
  return (
    <div className="min-h-screen bg-paper pb-24 animate-pulse">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4">
        <div className="h-7 bg-white/20 rounded w-32" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
        <div className="bg-white rounded-card p-5 border-2 border-line h-64" />
        <div className="bg-white rounded-card p-5 border-2 border-line h-16" />
      </div>
    </div>
  );
}

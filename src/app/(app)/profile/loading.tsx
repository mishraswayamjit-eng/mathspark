// Mirrors the loading skeleton inside profile/page.tsx (the variant it shows
// before the child's name is known): dark identity header with the avatar
// circle, then four card placeholders. Keep the two in step.
export default function ProfileLoading() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="bg-ink pt-10 pb-6 px-4">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-full border-4 border-white bg-white/20 shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="space-y-2">
              <div className="h-6 bg-white/20 rounded-xl w-36 animate-pulse" />
              <div className="h-4 bg-white/10 rounded-xl w-48 animate-pulse" />
            </div>
          </div>
        </div>
      </div>
      {[0, 1, 2, 3].map((i) => (
        <div key={i} className="bg-white mt-2 px-4 py-6 border-y-2 border-line">
          <div className="h-3 bg-gray-100 rounded w-24 mb-4 animate-pulse" />
          <div className="h-12 bg-gray-100 rounded-control animate-pulse" />
        </div>
      ))}
    </div>
  );
}

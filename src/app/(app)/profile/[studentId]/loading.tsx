// Same skeleton as the loading state inside profile/[studentId]/page.tsx, so a
// public profile does not show the "my profile" skeleton first. Keep the two in step.
export default function PublicProfileLoading() {
  return (
    <div className="min-h-screen bg-paper animate-pulse">
      <div className="bg-ink pt-10 pb-8 px-4">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-full bg-white/20" />
          <div className="flex-1 space-y-2">
            <div className="h-6 bg-white/20 rounded-xl w-32" />
            <div className="h-4 bg-white/10 rounded-xl w-24" />
          </div>
        </div>
      </div>
      <div className="m-4 grid grid-cols-2 gap-3">
        {[0, 1, 2, 3].map((i) => <div key={i} className="h-24 bg-gray-200 rounded-card" />)}
      </div>
    </div>
  );
}

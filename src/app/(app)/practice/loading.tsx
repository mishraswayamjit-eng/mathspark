// Shown while a route under /practice loads. It has the same outline as the
// Practise page (header bar, the 88px personal card, five rows), so that page
// arrives without anything moving. It carries no words or links, because the
// routes beneath /practice that have no loading file of their own show it too.
export default function PracticeLoading() {
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="bg-ink px-4 py-4 h-20 flex items-center">
        <div className="h-5 bg-white/20 rounded w-28 animate-pulse" />
      </div>
      <div className="max-w-lg mx-auto px-4 pt-5">
        <div className="h-[88px] mb-6 bg-white rounded-card border-2 border-line animate-pulse" />
        <div className="space-y-3">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="h-[76px] bg-white rounded-card border-2 border-line animate-pulse" />
          ))}
        </div>
      </div>
    </div>
  );
}

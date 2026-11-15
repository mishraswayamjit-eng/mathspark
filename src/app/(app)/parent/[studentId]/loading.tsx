export default function Loading() {
  return (
    // Same loader as the one inside parent/[studentId]/page.tsx, so the two
    // do not show one after the other. Keep the two in step.
    <div className="flex items-center justify-center min-h-screen bg-paper">
      <div className="text-center">
        <div className="text-5xl mb-4 animate-bounce">🌟</div>
        <p className="text-ink-muted font-bold">Loading progress report…</p>
      </div>
    </div>
  );
}

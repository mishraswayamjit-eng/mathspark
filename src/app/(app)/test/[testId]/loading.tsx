// Same loader as the one inside test/[testId]/page.tsx, so the child does not
// see the /test menu skeleton first. Keep the two in step.
export default function TestSessionLoading() {
  return (
    <div className="min-h-screen bg-paper flex items-center justify-center">
      <div className="text-center space-y-3">
        <div className="w-12 h-12 border-4 border-line border-t-action rounded-full animate-spin mx-auto" />
        <p className="text-ink-muted font-semibold">Loading your test…</p>
      </div>
    </div>
  );
}

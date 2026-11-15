// Same loader as the one inside test/history/page.tsx. Keep the two in step.
export default function TestHistoryLoading() {
  return (
    <div className="min-h-screen bg-paper flex items-center justify-center">
      <div className="w-10 h-10 border-4 border-line border-t-action rounded-full animate-spin" />
    </div>
  );
}

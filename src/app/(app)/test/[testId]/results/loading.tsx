// Same loader as the one inside test/[testId]/results/page.tsx. Keep the two in step.
export default function TestResultsLoading() {
  return (
    <div className="min-h-screen bg-paper flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-line border-t-action rounded-full animate-spin" />
    </div>
  );
}

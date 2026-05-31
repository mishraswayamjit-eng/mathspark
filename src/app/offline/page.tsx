export default function OfflinePage() {
  return (
    <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-center p-6 text-center">
      <div className="text-8xl mb-6">📚</div>
      <h1 className="text-3xl font-bold text-gray-800 mb-3">No internet? No problem!</h1>
      <p className="text-gray-500 text-base mb-6 max-w-xs">
        It looks like you're offline. Come back when you have a connection and keep learning!
      </p>
      <p className="text-4xl">🌟</p>
    </div>
  );
}

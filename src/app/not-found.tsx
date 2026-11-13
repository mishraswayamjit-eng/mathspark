import Link from 'next/link';
import Sparky from '@/components/Sparky';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
      <Sparky size={80} mood="thinking" className="mb-6" />
      <h1 className="text-2xl font-extrabold text-ink mb-2">Page not found</h1>
      <p className="text-gray-500 text-sm mb-8">
        Sparky looked everywhere but couldn&apos;t find this page.
      </p>
      <Link
        href="/home"
        className="bg-action text-white font-extrabold py-3 px-8 rounded-control border-2 border-ink shadow-hard-sm hover:bg-action-dark transition-colors"
      >
        Go Home
      </Link>
    </div>
  );
}

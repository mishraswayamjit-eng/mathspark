'use client';

import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

function DevGate({ children }: { children: React.ReactNode }) {
  const params = useSearchParams();
  const key = params.get('key');

  if (process.env.NODE_ENV === 'production' && key !== 'mathspark2026') {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <p className="text-gray-500 font-bold">Access denied</p>
      </div>
    );
  }

  return <>{children}</>;
}

export default function DevLayout({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={null}>
      <DevGate>{children}</DevGate>
    </Suspense>
  );
}

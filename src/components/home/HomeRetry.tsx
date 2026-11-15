'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

/** Shown in place of the Home content when its data could not be loaded. */
export default function HomeRetry() {
  const router = useRouter();
  const [trying, setTrying] = useState(false);

  function retry() {
    setTrying(true);
    // Ask the server for the page again; this component is replaced if it works.
    router.refresh();
    window.setTimeout(() => setTrying(false), 4000);
  }

  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-4 px-6 pb-24 text-center">
      <p className="text-ink font-extrabold text-lg">Oops! Sparky tripped over a number</p>
      <p className="text-ink-muted text-sm">We could not load your home screen. Check your connection.</p>
      <div className="flex items-center gap-3">
        <button type="button" onClick={retry} disabled={trying} className="ui-btn ui-btn-primary">
          {trying ? 'Trying…' : 'Retry'}
        </button>
        <Link href="/student/login" className="text-action font-extrabold text-sm px-4 min-h-[48px] flex items-center">
          Log in again
        </Link>
      </div>
    </div>
  );
}

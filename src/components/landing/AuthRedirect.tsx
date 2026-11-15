'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { PARENT_SESSION_FLAG } from '@/lib/student/types';

// Sends signed-in visitors on from the marketing page:
//  - a parent (NextAuth session) → /parent/dashboard
//  - a child (id in localStorage) → /home
// A parent wins when both are present, as before. The NextAuth check is a
// network round trip, so a child is not made to wait for it: unless this
// device is known to hold a parent session (PARENT_SESSION_FLAG, kept up to
// date here and by the app shell's StudentProvider), the child leaves at once.
export default function AuthRedirect() {
  const router = useRouter();
  const { status } = useSession();

  useEffect(() => {
    let childId: string | null = null;
    let parentKnown = false;
    try {
      childId = localStorage.getItem('mathspark_student_id');
      parentKnown = localStorage.getItem(PARENT_SESSION_FLAG) === '1';
    } catch { /* storage unavailable: fall through to the session check */ }

    if (status === 'authenticated') {
      try { localStorage.setItem(PARENT_SESSION_FLAG, '1'); } catch { /* ignore */ }
      router.replace('/parent/dashboard');
      return;
    }

    if (status === 'unauthenticated') {
      try { localStorage.removeItem(PARENT_SESSION_FLAG); } catch { /* ignore */ }
      if (childId) router.replace('/home');
      return;
    }

    // Still checking for a parent session. Only wait if one is expected.
    if (childId && !parentKnown) router.replace('/home');
  }, [status, router]);

  return null;
}

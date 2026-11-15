'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import HomeSkeleton from '@/components/home/HomeSkeleton';

/**
 * Rendered by the Home page when there is no child session on the server.
 * The server cannot see localStorage, so this picks where to go:
 *  - this device has signed in as a child before (an id is stored) → /student/login
 *    (the session ran out; they only need their PIN again)
 *  - otherwise → /start (a brand-new visitor)
 * Neither page sends anyone back to /home on its own (only a successful sign-in
 * does), so this can never loop.
 */
export default function HomeSignedOut() {
  const router = useRouter();

  useEffect(() => {
    let hasChildId = false;
    try {
      hasChildId = !!localStorage.getItem('mathspark_student_id');
    } catch {
      // Storage blocked: treat as a new visitor.
    }
    router.replace(hasChildId ? '/student/login' : '/start');
  }, [router]);

  return <HomeSkeleton />;
}

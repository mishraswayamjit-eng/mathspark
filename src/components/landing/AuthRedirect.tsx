'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';

export default function AuthRedirect() {
  const router = useRouter();
  const { status } = useSession();

  useEffect(() => {
    if (status === 'loading') return;
    if (status === 'authenticated') { router.replace('/parent/dashboard'); return; }
    const id = localStorage.getItem('mathspark_student_id');
    if (id) router.replace('/home');
  }, [status, router]);

  return null;
}

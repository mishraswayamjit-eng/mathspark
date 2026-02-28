'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    router.replace(id ? '/chapters' : '/start');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <span className="text-5xl animate-bounce">⭐</span>
    </div>
  );
}

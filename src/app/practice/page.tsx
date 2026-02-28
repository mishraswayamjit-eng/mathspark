'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

// /practice without a topicId → smart redirect to weakest topic
export default function PracticePage() {
  const router = useRouter();

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    fetch(`/api/dashboard?studentId=${studentId}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.weakestTopicId) {
          router.replace(`/practice/${data.weakestTopicId}`);
        } else {
          router.replace('/chapters');
        }
      })
      .catch(() => router.replace('/chapters'));
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <span className="text-5xl animate-bounce">🎯</span>
    </div>
  );
}

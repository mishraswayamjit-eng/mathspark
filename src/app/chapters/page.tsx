'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ChapterGrid from '@/components/ChapterGrid';
import type { Topic, Progress, TopicWithProgress } from '@/types';

export default function ChaptersPage() {
  const router = useRouter();
  const [topics,   setTopics]   = useState<TopicWithProgress[]>([]);
  const [name,     setName]     = useState('');
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }
    setName(localStorage.getItem('mathspark_student_name') ?? 'there');

    async function load() {
      const [topicsRes, progressRes] = await Promise.all([
        fetch('/api/topics'),
        fetch(`/api/progress?studentId=${studentId}`),
      ]);

      const topicsData:   Topic[]    = await topicsRes.json();
      const progressData: Progress[] = await progressRes.json();

      const merged: TopicWithProgress[] = topicsData.map((t) => {
        const p = progressData.find((x) => x.topicId === t.id);
        return {
          ...t,
          mastery:   p?.mastery   ?? 'NotStarted',
          attempted: p?.attempted ?? 0,
          correct:   p?.correct   ?? 0,
        };
      });

      setTopics(merged);
      setLoading(false);
    }

    load().catch(console.error);
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-5xl animate-bounce">📚</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-8">
      {/* Header */}
      <div className="px-4 pt-8 pb-4">
        <h1 className="text-2xl font-bold text-gray-800">Hi {name}! 👋</h1>
        <p className="text-gray-500 mt-1">Choose a topic to practice:</p>
      </div>

      <ChapterGrid topics={topics} />
    </div>
  );
}

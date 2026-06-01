'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import ChapterGrid from '@/components/ChapterGrid';
import { SkeletonGrid } from '@/components/Skeleton';
import type { Topic, Progress, TopicWithProgress } from '@/types';
import { getUnmetPrerequisiteIds } from '@/lib/prerequisites';

export default function ChaptersPage() {
  const router = useRouter();
  const [topics,   setTopics]   = useState<TopicWithProgress[]>([]);
  const [name,     setName]     = useState('');
  const [loading,  setLoading]  = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [practicedToday, setPracticedToday] = useState<boolean>(true);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }
    setName(localStorage.getItem('mathspark_student_name') ?? 'there');

    const lastPractice = localStorage.getItem('mathspark_last_practice');
    const today = new Date().toISOString().slice(0, 10);
    setPracticedToday(lastPractice === today);

    async function load() {
      try {
        const [topicsRes, progressRes] = await Promise.all([
          fetch('/api/topics'),
          fetch(`/api/progress?studentId=${studentId}`),
        ]);

        if (!topicsRes.ok || !progressRes.ok) {
          setLoadError(true);
          setLoading(false);
          return;
        }

        const topicsData:   Topic[]    = await topicsRes.json();
        const progressData: Progress[] = await progressRes.json();

        if (!Array.isArray(topicsData)) {
          setLoadError(true);
          setLoading(false);
          return;
        }

        const merged: TopicWithProgress[] = topicsData.map((t) => {
          const p = Array.isArray(progressData)
            ? progressData.find((x) => x.topicId === t.id)
            : undefined;
          return {
            ...t,
            mastery:   p?.mastery   ?? 'NotStarted',
            attempted: p?.attempted ?? 0,
            correct:   p?.correct   ?? 0,
          };
        });

        setTopics(merged);
        setLoading(false);
      } catch (err) {
        console.error('[chapters load]', err);
        setLoadError(true);
        setLoading(false);
      }
    }

    load();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router, retryCount]);

  // Build a mastery lookup: topicId → mastery level
  const masteryMap = useMemo<Record<string, string>>(() => {
    const map: Record<string, string> = {};
    topics.forEach((t) => { map[t.id] = t.mastery; });
    return map;
  }, [topics]);

  // Build a topic name lookup: topicId → topic name
  const topicNameMap = useMemo<Record<string, string>>(() => {
    const map: Record<string, string> = {};
    topics.forEach((t) => { map[t.id] = t.name; });
    return map;
  }, [topics]);

  // Compute soft prerequisite hints for each topic
  const prerequisiteHints = useMemo<Record<string, string>>(() => {
    const hints: Record<string, string> = {};
    topics.forEach((t) => {
      const unmet = getUnmetPrerequisiteIds(t.id, masteryMap);
      if (unmet.length > 0) {
        hints[t.id] = topicNameMap[unmet[0]] ?? unmet[0];
      }
    });
    return hints;
  }, [topics, masteryMap, topicNameMap]);

  if (loadError) {
    return (
      <motion.div
        className="min-h-screen flex flex-col items-center justify-center px-6 gap-4 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.25 }}
      >
        <div className="text-5xl" aria-hidden="true">😅</div>
        <h2 className="text-xl font-bold text-gray-800">Oops, couldn&apos;t load your topics!</h2>
        <p className="text-gray-500 text-sm">Check your internet connection and try again.</p>
        <button
          onClick={() => { setLoadError(false); setLoading(true); setRetryCount((n) => n + 1); }}
          className="bg-blue-500 text-white font-bold py-3 px-6 rounded-2xl text-base"
        >
          Try again
        </button>
      </motion.div>
    );
  }

  if (loading) {
    return (
      <motion.div
        className="min-h-screen pb-8"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="px-4 pt-8 pb-4">
          <h1 className="text-2xl font-bold text-gray-800">Hi {name}! 👋</h1>
          <p className="text-gray-500 mt-1">Choose a topic to practice:</p>
        </div>
        <div className="px-4">
          <SkeletonGrid count={16} />
        </div>
      </motion.div>
    );
  }

  const attemptedMap: Record<string, number> = {};
  topics.forEach((p: { id: string; attempted: number }) => {
    attemptedMap[p.id] = p.attempted;
  });

  return (
    <motion.div
      className="min-h-screen pb-8"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
    >
      {/* Header */}
      <div className="px-4 pt-8 pb-4">
        <h1 className="text-2xl font-bold text-gray-800">Hi {name}! 👋</h1>
        <p className="text-gray-500 mt-1">Choose a topic to practice:</p>
      </div>

      {/* Streak reminder banner */}
      {!practicedToday && (
        <div className="mx-4 mt-4 bg-amber-50 border border-amber-200 rounded-2xl px-4 py-3 flex items-center gap-3">
          <span className="text-2xl">🔥</span>
          <div className="flex-1">
            <p className="text-sm font-semibold text-amber-800">Don&apos;t lose your streak!</p>
            <p className="text-xs text-amber-600">Practice any topic today to keep going.</p>
          </div>
          <button
            onClick={() => setPracticedToday(true)}
            className="text-amber-400 hover:text-amber-600 text-lg leading-none"
            aria-label="Dismiss reminder"
          >
            ×
          </button>
        </div>
      )}

      <ChapterGrid topics={topics} prerequisiteHints={prerequisiteHints} attemptedMap={attemptedMap} />
    </motion.div>
  );
}

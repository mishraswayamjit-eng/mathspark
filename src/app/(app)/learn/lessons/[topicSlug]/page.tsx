'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import LevelMap from '@/components/lesson/LevelMap';
import type { LessonTopic } from '@/types/lesson';

interface ProgressRow {
  topicSlug: string;
  levelId: number;
  quizScore: number;
}

export default function TopicPage({
  params,
}: {
  params: { topicSlug: string };
}) {
  const router = useRouter();
  const { topicSlug } = params;
  const [topic, setTopic] = useState<LessonTopic | null>(null);
  const [progress, setProgress] = useState<ProgressRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch(`/api/lessons/${topicSlug}`).then((r) => {
        if (!r.ok) throw new Error('Not found');
        return r.json();
      }),
      fetch('/api/lessons/progress')
        .then((r) => (r.ok ? r.json() : { progress: [] }))
        .catch((err) => { console.error('[lessons/topic] fetch progress', err); return { progress: [] }; }),
    ])
      .then(([topicData, progressData]) => {
        setTopic(topicData);
        setProgress(progressData.progress ?? []);
      })
      .catch((err) => { console.error('[lessons/topic] fetch topic data', err); setError(true); })
      .finally(() => setLoading(false));
  }, [topicSlug]);

  const levelProgress = useMemo(() => {
    return progress
      .filter((p) => p.topicSlug === topicSlug)
      .map((p) => ({ levelId: p.levelId, quizScore: p.quizScore }));
  }, [progress, topicSlug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
        <div className="bg-duo-dark px-4 py-4">
          <div className="h-6 bg-white/20 rounded w-32" />
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 h-24" />
          ))}
        </div>
      </div>
    );
  }

  if (error || !topic) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4 pb-24">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-gray-500">Topic not found</p>
        <button
          onClick={() => router.push('/learn/lessons')}
          className="bg-duo-green text-white font-extrabold px-6 py-2.5 rounded-2xl text-sm active:scale-95 transition-transform"
        >
          Back to Lessons
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link
          href="/learn/lessons"
          className="text-white/60 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <span className="text-xl" aria-hidden="true">{topic.emoji}</span>
        <h1 className="text-white font-extrabold text-lg">{topic.topic}</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        {/* Topic description */}
        <div
          className="rounded-2xl px-4 py-3 mb-5 border"
          style={{
            backgroundColor: topic.color + '10',
            borderColor: topic.color + '30',
          }}
        >
          <p className="text-sm font-semibold" style={{ color: topic.color }}>
            {topic.description}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Grades {topic.gradeRange[0]}–{topic.gradeRange[1]} &middot; 5 levels
          </p>
        </div>

        {/* Level map */}
        <LevelMap
          topicSlug={topicSlug}
          levels={topic.levels}
          progress={levelProgress}
        />
      </div>
    </div>
  );
}

'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import TopicGrid from '@/components/lesson/TopicGrid';
import { LESSON_TOPICS } from '@/data/lessonTopics';

interface ProgressRow {
  topicSlug: string;
  levelId: number;
  quizScore: number;
}

export default function LessonsPage() {
  const [progress, setProgress] = useState<ProgressRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/lessons/progress')
      .then((r) => {
        if (!r.ok) return { progress: [] };
        return r.json();
      })
      .then((d) => setProgress(d.progress ?? []))
      .catch(() => setProgress([]))
      .finally(() => setLoading(false));
  }, []);

  const topicProgress = useMemo(() => {
    const map = new Map<string, Set<number>>();
    for (const row of progress) {
      if (row.quizScore >= 75) {
        if (!map.has(row.topicSlug)) map.set(row.topicSlug, new Set());
        map.get(row.topicSlug)!.add(row.levelId);
      }
    }
    return LESSON_TOPICS.map((t) => ({
      topicSlug: t.id,
      completed: map.get(t.id)?.size ?? 0,
      total: 5,
    }));
  }, [progress]);

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link
          href="/chapters"
          className="text-white/60 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <h1 className="text-white font-extrabold text-lg">Concept Lessons</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        {/* Intro box */}
        <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl px-4 py-3 border border-purple-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-purple-800">
              Learn new concepts step by step!
            </p>
            <p className="text-xs text-purple-600 mt-0.5">
              Each topic has 5 levels with lessons and quizzes.
            </p>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="grid grid-cols-2 gap-3 animate-pulse">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 h-44" />
            ))}
          </div>
        )}

        {/* Topic grid */}
        {!loading && (
          <TopicGrid topics={LESSON_TOPICS} progress={topicProgress} />
        )}
      </div>
    </div>
  );
}

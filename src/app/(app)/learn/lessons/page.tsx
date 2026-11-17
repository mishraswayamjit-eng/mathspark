'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import TopicGrid from '@/components/lesson/TopicGrid';
import { LESSON_TOPICS } from '@/data/lessonTopics';
import { gradeInRange } from '@/lib/sharedUtils';
import { logError } from '@/lib/logger';
import { useStudentGrade } from '@/components/lesson/useStudentGrade';

interface ProgressRow {
  topicSlug: string;
  levelId: number;
  quizScore: number;
}

export default function LessonsPage() {
  const [progress, setProgress] = useState<ProgressRow[]>([]);
  const [loading, setLoading] = useState(true);
  // The child's grade from the app shell (null for a moment when it is not known yet).
  const grade = useStudentGrade();

  useEffect(() => {
    fetch('/api/lessons/progress')
      .then((r) => {
        if (!r.ok) return { progress: [] };
        return r.json();
      })
      .then((d) => setProgress(d.progress ?? []))
      .catch((err) => { logError('[lessons] fetch progress', err); setProgress([]); })
      .finally(() => setLoading(false));
  }, []);

  const visibleTopics = useMemo(
    () => (grade === null ? [] : LESSON_TOPICS.filter((t) => gradeInRange(t.gradeRange, grade))),
    [grade],
  );

  const topicProgress = useMemo(() => {
    const map = new Map<string, Set<number>>();
    for (const row of progress) {
      if (row.quizScore >= 75) {
        if (!map.has(row.topicSlug)) map.set(row.topicSlug, new Set());
        map.get(row.topicSlug)!.add(row.levelId);
      }
    }
    return visibleTopics.map((t) => ({
      topicSlug: t.id,
      completed: map.get(t.id)?.size ?? 0,
      total: 5,
    }));
  }, [progress, visibleTopics]);

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href="/learn"
          className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
          aria-label="Back"
        >
          &larr;
        </Link>
        <h1 className="text-white text-title">Concept Lessons</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro box */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">
              Learn new concepts step by step!
            </p>
            <p className="text-sm text-ink-muted mt-0.5">
              Each topic has 5 levels with lessons and quizzes.
            </p>
          </div>
        </div>

        {/* Loading */}
        {(loading || grade === null) && (
          <div className="grid grid-cols-2 gap-3 animate-pulse">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line h-44" />
            ))}
          </div>
        )}

        {/* Topic grid */}
        {!loading && grade !== null && (
          <TopicGrid topics={visibleTopics} progress={topicProgress} />
        )}
      </div>
    </div>
  );
}

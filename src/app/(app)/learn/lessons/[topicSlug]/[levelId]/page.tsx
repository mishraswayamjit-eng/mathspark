'use client';

import React, { useEffect, useState, useCallback, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import LessonViewer from '@/components/lesson/LessonViewer';
import LessonQuiz from '@/components/lesson/LessonQuiz';
import LessonComplete from '@/components/lesson/LessonComplete';
import type { LessonLevel } from '@/types/lesson';

type Phase = 'lessons' | 'quiz' | 'complete';

interface XPBreakdown {
  total: number;
  base: number;
  scoreBonus: number;
  firstTimeBonus: number;
  perfectBonus: number;
}

export default function LessonSessionPage({
  params,
}: {
  params: { topicSlug: string; levelId: string };
}) {
  const router = useRouter();
  const { topicSlug, levelId: levelIdStr } = params;
  const levelId = parseInt(levelIdStr, 10);

  const [level, setLevel] = useState<LessonLevel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [phase, setPhase] = useState<Phase>('lessons');
  const [quizScore, setQuizScore] = useState(0);
  const [quizTotal, setQuizTotal] = useState(0);
  const [xp, setXP] = useState<XPBreakdown | null>(null);
  const [isFirstTime, setIsFirstTime] = useState(true);
  const [accentColor, setAccentColor] = useState('#8B5CF6');
  const startTimeRef = useRef(Date.now());

  useEffect(() => {
    fetch(`/api/lessons/${topicSlug}`)
      .then((r) => {
        if (!r.ok) throw new Error('Not found');
        return r.json();
      })
      .then((data) => {
        const lvl = data.levels?.find((l: LessonLevel) => l.id === levelId);
        if (!lvl) throw new Error('Level not found');
        setLevel(lvl);
        setAccentColor(lvl.color || data.color || '#8B5CF6');
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [topicSlug, levelId]);

  const handleLessonsDone = useCallback(() => {
    setPhase('quiz');
  }, []);

  const handleQuizComplete = useCallback(
    (score: number, total: number) => {
      setQuizScore(score);
      setQuizTotal(total);
      setPhase('complete');

      const pct = Math.round((score / total) * 100);
      const durationSec = Math.round((Date.now() - startTimeRef.current) / 1000);

      // POST progress
      fetch('/api/lessons/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topicSlug,
          levelId,
          quizScore: pct,
          durationSec,
        }),
      })
        .then((r) => {
          if (!r.ok) return null;
          return r.json();
        })
        .then((data) => {
          if (data?.xp) {
            setXP(data.xp);
            setIsFirstTime(data.xp.firstTimeBonus > 0);
          }
        })
        .catch(() => {
          // Silently fail — score is still shown
          console.error('Failed to save lesson progress');
        });
    },
    [topicSlug, levelId],
  );

  const handleBackToLevels = useCallback(() => {
    router.push(`/learn/lessons/${topicSlug}`);
  }, [router, topicSlug]);

  const handleReview = useCallback(() => {
    setPhase('lessons');
    startTimeRef.current = Date.now();
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement) return;
      if (e.key === ' ' && phase === 'lessons') {
        e.preventDefault();
        // Space triggers the "next" button if visible
        const nextBtn = document.querySelector<HTMLButtonElement>(
          'button:last-of-type',
        );
        nextBtn?.click();
      }
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [phase]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24 animate-pulse">
        <div className="bg-duo-dark px-4 py-4">
          <div className="h-6 bg-white/20 rounded w-32" />
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-4">
          <div className="bg-white rounded-2xl p-5 border border-gray-100 h-64" />
          <div className="bg-white rounded-2xl p-5 border border-gray-100 h-16" />
        </div>
      </div>
    );
  }

  if (error || !level) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4 pb-24">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-gray-500">Level not found</p>
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
          href={`/learn/lessons/${topicSlug}`}
          className="text-white/60 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <span className="text-lg" aria-hidden="true">{level.emoji}</span>
        <h1 className="text-white font-extrabold text-lg truncate">{level.label}</h1>
        {phase !== 'complete' && (
          <span className="ml-auto text-xs font-bold text-white/40 capitalize">
            {phase === 'lessons' ? 'Learning' : 'Quiz'}
          </span>
        )}
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {phase === 'lessons' && (
          <LessonViewer
            lessons={level.lessons}
            accentColor={accentColor}
            onDone={handleLessonsDone}
          />
        )}

        {phase === 'quiz' && (
          <LessonQuiz
            questions={level.quiz}
            accentColor={accentColor}
            onComplete={handleQuizComplete}
          />
        )}

        {phase === 'complete' && (
          <LessonComplete
            score={quizScore}
            total={quizTotal}
            xp={xp}
            isFirstTime={isFirstTime}
            accentColor={accentColor}
            onBackToLevels={handleBackToLevels}
            onReview={handleReview}
          />
        )}
      </div>
    </div>
  );
}

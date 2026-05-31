'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import ProgressBar from '@/components/ProgressBar';
import { SkeletonStatRow, SkeletonGrid } from '@/components/Skeleton';
import type { DashboardData } from '@/types';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

function masteryColor(m: string) {
  if (m === 'Mastered')   return 'bg-green-500';
  if (m === 'Practicing') return 'bg-amber-400';
  return 'bg-gray-200';
}

function masteryDot(m: string) {
  if (m === 'Mastered')   return 'bg-green-500';
  if (m === 'Practicing') return 'bg-amber-400';
  return 'bg-gray-200';
}

export default function DashboardPage() {
  const router = useRouter();
  const [data,         setData]         = useState<DashboardData | null>(null);
  const [loading,      setLoading]      = useState(true);
  const [showConfirm,  setShowConfirm]  = useState(false);
  const [resetting,    setResetting]    = useState(false);
  const [resetError,   setResetError]   = useState<string | null>(null);
  const [newlyMastered, setNewlyMastered] = useState<string | null>(null); // topic name

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    fetch(`/api/dashboard?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d) => {
        setData(d);

        // Check for newly mastered topics
        const snapshotKey = 'mathspark_mastery_snapshot';
        try {
          const raw = localStorage.getItem(snapshotKey);
          const prev: Record<string, string> = raw ? JSON.parse(raw) : {};

          const freshlyMastered = d.topics.find(
            (t: { id: string; mastery: string; name: string }) =>
              t.mastery === 'Mastered' && prev[t.id] !== 'Mastered'
          );

          if (freshlyMastered) {
            setNewlyMastered(freshlyMastered.name);
          }

          // Update snapshot
          const next: Record<string, string> = {};
          d.topics.forEach((t: { id: string; mastery: string }) => { next[t.id] = t.mastery; });
          localStorage.setItem(snapshotKey, JSON.stringify(next));
        } catch { /* ignore */ }

        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [router]);

  async function handleReset() {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    setResetting(true);
    setResetError(null);

    try {
      const res = await fetch('/api/progress/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentId }),
      });

      if (!res.ok) throw new Error('Reset failed');

      localStorage.removeItem('mathspark_student_id');
      localStorage.removeItem('mathspark_student_name');
      router.replace('/start');
    } catch {
      setResetError('Oops! Something went wrong. Please try again.');
      setResetting(false);
      setShowConfirm(false);
    }
  }

  if (loading) {
    return (
      <motion.div
        className="min-h-screen pb-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        <div className="px-4 pt-8 pb-4">
          <div className="h-7 bg-gray-200 rounded w-40 mb-1 animate-pulse" />
          <div className="h-4 bg-gray-100 rounded w-32 animate-pulse" />
        </div>
        <div className="px-4 mb-6">
          <SkeletonStatRow />
        </div>
        <div className="px-4">
          <SkeletonGrid count={16} />
        </div>
      </motion.div>
    );
  }

  if (!data) {
    return (
      <motion.div
        className="flex items-center justify-center min-h-screen text-gray-400"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        Could not load dashboard. Please try again.
      </motion.div>
    );
  }

  const { student, stats, topics, weeklyData, weakestTopicId } = data;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  return (
    <motion.div
      className="min-h-screen pb-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="px-4 pt-8 pb-4">
        <h1 className="text-2xl font-bold text-gray-800">Hi {student.name}! 🌟</h1>
        <p className="text-gray-400 text-sm">Here&#39;s how you&#39;re doing</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3 px-4 mb-6">
        {[
          { label: 'Solved',    value: stats.totalSolved,    emoji: '✅' },
          { label: 'Mastered',  value: stats.topicsMastered, emoji: '⭐' },
          { label: 'Day streak',value: stats.streakDays,     emoji: '🔥' },
        ].map(({ label, value, emoji }) => (
          <div key={label} className="bg-white rounded-2xl p-3 text-center shadow-sm border border-gray-100">
            <div className="text-2xl">{emoji}</div>
            <div className="text-xl font-bold text-gray-800">{value}</div>
            <div className="text-xs text-gray-400">{label}</div>
          </div>
        ))}
      </div>

      {/* Share progress with parent */}
      <div className="px-4 mb-4 text-center">
        <button
          onClick={() => {
            const url = `${window.location.origin}/share/${localStorage.getItem('mathspark_student_id')}`;
            navigator.clipboard.writeText(url).then(() => {
              alert('Share link copied! Send it to your parent. 📤');
            });
          }}
          className="text-sm text-blue-500 underline underline-offset-2 hover:text-blue-600 transition-colors"
        >
          Share progress with parent <span aria-hidden="true">📤</span>
        </button>
      </div>

      {/* Continue learning */}
      {weakestTopicId && (
        <div className="px-4 mb-6">
          <Link
            href={`/practice/${weakestTopicId}`}
            className="block bg-blue-500 hover:bg-blue-600 text-white rounded-2xl px-4 py-4 transition-colors"
          >
            <p className="text-xs font-semibold uppercase tracking-wide opacity-75">Continue learning</p>
            <p className="text-base font-bold mt-0.5">
              {topics.find((t) => t.id === weakestTopicId)?.name ?? weakestTopicId} →
            </p>
          </Link>
        </div>
      )}

      {/* Weekly bar chart */}
      <div className="px-4 mb-6">
        <h2 className="text-sm font-bold text-gray-600 uppercase tracking-wide mb-3">This week</h2>
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-end gap-1.5 h-24">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full bg-blue-400 rounded-t-sm transition-all"
                  style={{
                    height: `${(count / maxBar) * 72}px`,
                    minHeight: count > 0 ? '4px' : '0',
                  }}
                />
                <span className="text-xs text-gray-400">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-400 text-center mt-2">Correct answers per day</p>
        </div>
      </div>

      {/* Topic grid */}
      <div className="px-4">
        <h2 className="text-sm font-bold text-gray-600 uppercase tracking-wide mb-3">All topics</h2>
        <div className="grid grid-cols-2 gap-2">
          {[...topics]
            .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
            .map((t) => {
              const pct = t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
              return (
                <Link
                  key={t.id}
                  href={`/practice/${t.id}`}
                  className="bg-white rounded-xl border border-gray-100 p-3 flex items-center gap-2 hover:shadow-sm transition-shadow"
                >
                  <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${masteryDot(t.mastery)}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-gray-700 truncate">{t.name}</p>
                    <ProgressBar value={pct} color={masteryColor(t.mastery)} height="h-1 mt-1" />
                  </div>
                </Link>
              );
            })}
        </div>
      </div>

      {/* Achievements */}
      {data.achievements && (
        <div className="px-4 mt-6">
          <h2 className="text-sm font-bold text-gray-600 uppercase tracking-wide mb-3">
            Badges {data.achievements.filter((a) => a.earned).length}/{data.achievements.length}
          </h2>
          <div className="grid grid-cols-3 gap-2">
            {data.achievements.map((badge) => (
              <div
                key={badge.id}
                className={`bg-white rounded-xl border p-3 text-center transition-opacity ${
                  badge.earned
                    ? 'border-amber-200 opacity-100'
                    : 'border-gray-100 opacity-30 grayscale'
                }`}
              >
                <div className="text-2xl mb-1">{badge.emoji}</div>
                <p className="text-xs font-bold text-gray-700 leading-tight">{badge.title}</p>
                <p className="text-xs text-gray-400 leading-tight mt-0.5">{badge.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Reset progress */}
      <div className="px-4 mt-8 pb-4 text-center">
        {resetError && (
          <p className="text-red-400 text-sm mb-2">{resetError}</p>
        )}
        <button
          onClick={() => { setShowConfirm(true); setResetError(null); }}
          className="text-sm text-gray-400 underline underline-offset-2 hover:text-gray-500 transition-colors min-h-[48px] px-4"
        >
          Reset my progress
        </button>
      </div>

      {/* Confirmation dialog */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-6">
          <div className="bg-white rounded-2xl p-6 shadow-xl max-w-sm w-full">
            <p className="text-lg font-bold text-gray-800 mb-2">Start fresh? 🔄</p>
            <p className="text-gray-500 text-sm mb-6">
              This will wipe out all your stars and start fresh. Are you sure?
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowConfirm(false)}
                disabled={resetting}
                className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl py-3 transition-colors min-h-[48px]"
              >
                No, keep going!
              </button>
              <button
                onClick={handleReset}
                disabled={resetting}
                className="flex-1 bg-red-100 hover:bg-red-200 text-red-600 font-semibold rounded-xl py-3 transition-colors min-h-[48px]"
              >
                {resetting ? 'Resetting...' : 'Yes, reset'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Mastery celebration modal */}
      {newlyMastered && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-6">
          <div className="bg-white rounded-3xl p-8 shadow-2xl max-w-sm w-full text-center">
            <div className="text-7xl mb-4">🏆</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Topic Mastered!</h2>
            <p className="text-gray-500 mb-2">
              You&apos;ve mastered
            </p>
            <p className="text-lg font-bold text-blue-600 mb-6">{newlyMastered}</p>
            <p className="text-3xl mb-6">⭐ ⭐ ⭐</p>
            <button
              onClick={() => setNewlyMastered(null)}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors min-h-[48px]"
            >
              Keep going! 🚀
            </button>
          </div>
        </div>
      )}
    </motion.div>
  );
}

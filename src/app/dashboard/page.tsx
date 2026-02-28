'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ProgressBar from '@/components/ProgressBar';
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
  const [data,    setData]    = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    fetch(`/api/dashboard?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-5xl animate-bounce">📊</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-400">
        Could not load dashboard. Please try again.
      </div>
    );
  }

  const { student, stats, topics, weeklyData, weakestTopicId } = data;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  return (
    <div className="min-h-screen pb-8">
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
    </div>
  );
}

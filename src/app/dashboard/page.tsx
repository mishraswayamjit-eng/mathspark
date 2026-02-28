'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ProgressBar from '@/components/ProgressBar';
import DuoButton from '@/components/DuoButton';
import Sparky from '@/components/Sparky';
import type { DashboardData } from '@/types';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

function masteryColor(m: string) {
  if (m === 'Mastered')   return 'bg-[#58CC02]';
  if (m === 'Practicing') return 'bg-[#FF9600]';
  return 'bg-gray-200';
}

function masteryBorder(m: string) {
  if (m === 'Mastered')   return 'border-l-4 border-[#58CC02]';
  if (m === 'Practicing') return 'border-l-4 border-[#FF9600]';
  return 'border-l-4 border-gray-200';
}

export default function DashboardPage() {
  const router = useRouter();
  const [data,        setData]        = useState<DashboardData | null>(null);
  const [loading,     setLoading]     = useState(true);
  const [studentName, setStudentName] = useState('');

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }
    setStudentName(localStorage.getItem('mathspark_student_name') ?? '');

    fetch(`/api/dashboard?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-white animate-pulse">
        {/* Header skeleton */}
        <div className="bg-[#131F24] px-4 pt-8 pb-5 h-24" />
        {/* Stats row skeleton */}
        <div className="grid grid-cols-3 gap-3 px-4 -mt-3 mb-6">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-24 bg-gray-100 rounded-2xl" />
          ))}
        </div>
        {/* Button skeleton */}
        <div className="px-4 mb-6">
          <div className="h-12 bg-gray-100 rounded-2xl" />
        </div>
        {/* Chart skeleton */}
        <div className="px-4 mb-6">
          <div className="h-4 w-24 bg-gray-100 rounded mb-3" />
          <div className="h-36 bg-gray-100 rounded-2xl" />
        </div>
        {/* Topic rows skeleton */}
        <div className="px-4">
          <div className="h-4 w-24 bg-gray-100 rounded mb-3" />
          <div className="grid grid-cols-2 gap-2">
            {[0, 1, 2, 3, 4].map((i) => (
              <div key={i} className="h-12 bg-gray-100 rounded-xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen text-gray-400 bg-white">
        Could not load dashboard. Please try again.
      </div>
    );
  }

  const { student, stats, topics, weeklyData, weakestTopicId } = data;
  const displayName = studentName || student.name;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  return (
    <div className="min-h-screen bg-white pb-8 animate-fade-in">
      {/* Dark header */}
      <div className="bg-[#131F24] px-4 pt-8 pb-5 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Hi {displayName}! 🌟</h1>
          <p className="text-white/60 text-sm font-medium">Here&#39;s how you&#39;re doing</p>
        </div>
        <Sparky mood="happy" size={56} />
      </div>

      {/* Stats row — colored cards */}
      <div className="grid grid-cols-3 gap-3 px-4 -mt-3 mb-6">
        {[
          { label: 'Solved',    value: stats.totalSolved,    emoji: '✅', bg: 'bg-[#58CC02]' },
          { label: 'Mastered',  value: stats.topicsMastered, emoji: '⭐', bg: 'bg-[#1CB0F6]' },
          { label: 'Day Streak',value: stats.streakDays,     emoji: '🔥', bg: 'bg-[#FF9600]' },
        ].map(({ label, value, emoji, bg }) => (
          <div key={label} className={`${bg} rounded-2xl p-3 text-center shadow-md`}>
            <div className="text-2xl">{emoji}</div>
            <div className="text-2xl font-extrabold text-white">{value}</div>
            <div className="text-xs text-white/80 font-bold">{label}</div>
          </div>
        ))}
      </div>

      {/* Continue learning */}
      {weakestTopicId && (
        <div className="px-4 mb-6">
          <DuoButton
            variant="blue"
            fullWidth
            onClick={() => router.push(`/practice/${weakestTopicId}`)}
          >
            Continue learning →
          </DuoButton>
        </div>
      )}

      {/* Weekly bar chart */}
      <div className="px-4 mb-6">
        <h2 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-3">This week</h2>
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-end gap-1.5 h-24">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full bg-[#58CC02] rounded-t-sm transition-all"
                  style={{
                    height: `${(count / maxBar) * 72}px`,
                    minHeight: count > 0 ? '4px' : '0',
                  }}
                />
                <span className="text-xs text-gray-400 font-semibold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-400 text-center mt-2 font-medium">Correct answers per day</p>
        </div>
      </div>

      {/* Topic grid */}
      <div className="px-4">
        <h2 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-3">All topics</h2>
        <div className="grid grid-cols-2 gap-2">
          {[...topics]
            .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
            .map((t) => {
              const pct = t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
              return (
                <Link
                  key={t.id}
                  href={`/practice/${t.id}`}
                  className={`bg-white rounded-xl ${masteryBorder(t.mastery)} p-3 flex items-center gap-2 hover:shadow-sm transition-shadow shadow-sm`}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-gray-700 truncate">{t.name}</p>
                    <ProgressBar value={pct} color={masteryColor(t.mastery)} height="h-1.5 mt-1" />
                  </div>
                </Link>
              );
            })}
        </div>
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import DuoButton from '@/components/DuoButton';
import Sparky from '@/components/Sparky';
import type { DashboardData } from '@/types';

// ── Topic metadata ─────────────────────────────────────────────────────────────

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06':    '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11':    '📊', 'ch12':    '📏', 'ch13':    '🔤', 'ch14':    '⚖️',
  'ch15':    '🧩', 'ch16':    '🔢', 'ch17':    '🕐', 'ch18':    '📐',
  'ch19':    '🔺', 'ch20':    '⬜', 'ch21':    '⭕', 'dh':      '📈',
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function timeAgo(isoDate: string): string {
  const ms      = Date.now() - new Date(isoDate).getTime();
  const minutes = Math.floor(ms / 60_000);
  if (minutes < 60)  return `${minutes}m ago`;
  const hours = Math.floor(ms / 3_600_000);
  if (hours < 24)    return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
  const days  = Math.floor(ms / 86_400_000);
  return `${days} day${days !== 1 ? 's' : ''} ago`;
}

function masteryDot(m: string) {
  if (m === 'Mastered')   return 'bg-[#58CC02]';
  if (m === 'Practicing') return 'bg-[#FF9600]';
  return 'bg-gray-300';
}

// ── Loading skeleton ──────────────────────────────────────────────────────────

function Skeleton() {
  return (
    <div className="min-h-screen bg-white animate-pulse">
      <div className="bg-[#131F24] h-24 px-4" />
      <div className="grid grid-cols-3 gap-3 px-4 -mt-3 mb-6">
        {[0,1,2].map((i) => <div key={i} className="h-24 bg-gray-100 rounded-2xl" />)}
      </div>
      <div className="px-4 mb-5"><div className="h-12 bg-gray-100 rounded-2xl" /></div>
      <div className="px-4 mb-5">
        <div className="h-4 w-24 bg-gray-100 rounded mb-3" />
        <div className="h-36 bg-gray-100 rounded-2xl" />
      </div>
      <div className="px-4 mb-5">
        <div className="h-4 w-24 bg-gray-100 rounded mb-3" />
        <div className="grid grid-cols-2 gap-2">
          {Array.from({length:8}, (_,i) => <div key={i} className="h-10 bg-gray-100 rounded-xl" />)}
        </div>
      </div>
      <div className="px-4">
        <div className="h-4 w-32 bg-gray-100 rounded mb-3" />
        {[0,1,2,3,4].map((i) => <div key={i} className="h-14 bg-gray-100 rounded-xl mb-2" />)}
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

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

  if (loading) return <Skeleton />;
  if (!data)   return (
    <div className="flex items-center justify-center min-h-screen text-gray-400 bg-white">
      Could not load dashboard. Please try again.
    </div>
  );

  const { student, stats, topics, weeklyData, weakestTopicId, weakestTopicName, recentActivity } = data;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  const sortedTopics = [...topics].sort(
    (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
  );

  return (
    <div className="min-h-screen bg-white pb-24 animate-fade-in">

      {/* ── Header ──────────────────────────────────────────────────────── */}
      <div className="bg-[#131F24] px-4 pt-8 pb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white">
            Hi {student.name}! Here&#39;s your progress 🌟
          </h1>
          <p className="text-white/60 text-sm font-medium mt-0.5">Keep up the great work!</p>
        </div>
        <Sparky mood="happy" size={56} />
      </div>

      {/* ── Stat cards ──────────────────────────────────────────────────── */}
      <div className="grid grid-cols-3 gap-3 px-4 -mt-3 mb-6">
        {([
          { emoji: '🎯', value: stats.totalSolved,    label: 'Questions\nSolved',   bg: 'bg-[#58CC02]' },
          { emoji: '🔥', value: stats.streakDays,     label: 'Day\nStreak',         bg: 'bg-[#FF9600]' },
          { emoji: '⭐', value: stats.topicsMastered, label: 'Topics\nMastered',    bg: 'bg-[#1CB0F6]' },
        ] as const).map(({ emoji, value, label, bg }) => (
          <div key={label} className={`${bg} rounded-2xl p-3 text-center shadow-md`}>
            <div className="text-2xl leading-none mb-1">{emoji}</div>
            <div className="text-2xl font-extrabold text-white leading-none">{value}</div>
            <div className="text-[10px] text-white/80 font-bold mt-1 whitespace-pre-line leading-tight">
              {label}
            </div>
          </div>
        ))}
      </div>

      {/* ── Continue Learning ────────────────────────────────────────────── */}
      {weakestTopicId && (
        <div className="px-4 mb-6">
          <DuoButton
            variant="blue"
            fullWidth
            onClick={() => router.push(`/practice/${weakestTopicId}`)}
          >
            Keep going with {weakestTopicName ?? 'your topic'} →
          </DuoButton>
        </div>
      )}

      {/* ── Weekly activity chart ────────────────────────────────────────── */}
      <div className="px-4 mb-6">
        <h2 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-3">
          This week
        </h2>
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-end gap-1.5 h-28">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                {/* Count label */}
                <span className="text-[10px] text-gray-400 font-semibold min-h-[14px]">
                  {count > 0 ? count : ''}
                </span>
                {/* Bar with gray background + green fill */}
                <div className="w-full relative bg-gray-100 rounded-sm" style={{ height: 72 }}>
                  <div
                    className="absolute bottom-0 left-0 right-0 bg-[#58CC02] rounded-sm transition-all duration-500"
                    style={{
                      height: count > 0 ? `${Math.max(4, Math.round((count / maxBar) * 72))}px` : '0px',
                    }}
                  />
                </div>
                {/* Day label */}
                <span className="text-[10px] text-gray-400 font-semibold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-gray-400 text-center mt-2 font-medium">
            Questions attempted per day
          </p>
        </div>
      </div>

      {/* ── Topic mastery overview ───────────────────────────────────────── */}
      <div className="px-4 mb-6">
        <h2 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-3">
          All topics
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {sortedTopics.map((t) => {
            const pct = t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
            return (
              <button
                key={t.id}
                onClick={() => router.push(`/practice/${t.id}`)}
                className="flex items-center gap-2 bg-white rounded-xl px-3 py-2.5 shadow-sm border border-gray-100 hover:border-[#1CB0F6] text-left transition-colors active:scale-[0.97]"
              >
                <span className="text-lg leading-none flex-shrink-0">
                  {TOPIC_EMOJI[t.id] ?? '📚'}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-[11px] font-bold text-gray-700 truncate leading-tight">
                    {t.name}
                  </p>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${masteryDot(t.mastery)}`} />
                    <span className="text-[10px] text-gray-400 font-semibold">
                      {t.attempted > 0 ? `${pct}%` : '—'}
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Recent activity ──────────────────────────────────────────────── */}
      {recentActivity.length > 0 && (
        <div className="px-4 mb-6">
          <h2 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-3">
            Recent activity
          </h2>
          <div className="space-y-2">
            {recentActivity.map((session, i) => {
              const pct = session.attempted > 0
                ? Math.round((session.correct / session.attempted) * 100)
                : 0;
              const perfEmoji = pct >= 80 ? '🎯' : pct >= 60 ? '🟡' : '💪';
              return (
                <button
                  key={`${session.topicId}-${i}`}
                  onClick={() => router.push(`/practice/${session.topicId}`)}
                  className="w-full text-left bg-white rounded-xl px-4 py-3 shadow-sm border border-gray-100 hover:border-[#1CB0F6] transition-colors active:scale-[0.98]"
                >
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="text-base leading-none flex-shrink-0">
                        {TOPIC_EMOJI[session.topicId] ?? '📚'}
                      </span>
                      <div className="min-w-0">
                        <p className="text-xs font-extrabold text-gray-800 truncate">
                          {session.topicName}
                        </p>
                        <p className="text-[11px] text-gray-400 font-semibold">
                          {session.correct}/{session.attempted} ({pct}%) {perfEmoji}
                        </p>
                      </div>
                    </div>
                    <span className="text-[10px] text-gray-400 font-semibold flex-shrink-0">
                      {timeAgo(session.createdAt)}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
}

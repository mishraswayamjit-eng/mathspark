'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import type { DashboardData } from '@/types';

// ─── Constants ─────────────────────────────────────────────────────────────────

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

const TOPIC_SHORT: Record<string, string> = {
  'ch01-05': 'Numbers',      'ch06': 'Factors',       'ch07-08': 'Fractions',
  'ch09-10': 'Operations',   'ch11': 'Decimals',       'ch12': 'Measurement',
  'ch13': 'Algebra',         'ch14': 'Equations',      'ch15': 'Puzzles',
  'ch16': 'Sequences',       'ch17': 'Time',           'ch18': 'Angles',
  'ch19': 'Triangles',       'ch20': 'Quadrilaterals', 'ch21': 'Circle',
  'dh': 'Data Handling',
};

const ENCOURAGEMENTS = [
  "Excellent work! Keep it up! 🌟",
  "I'm so proud of how hard you're working! 💪",
  "You're doing amazing — every question makes you smarter! 🧠",
  "Math is your superpower! Keep shining! ✨",
  "I believe in you! You've got this! 🎉",
  "Practice makes perfect — and you're getting there! 🚀",
  "You're getting better every single day! 📈",
  "Nothing can stop a kid who loves learning! 🏆",
];

function masteryColor(m: string) {
  if (m === 'Mastered')   return { bg: '#f4fbef', border: '#58CC02', text: '#2d6a04' };
  if (m === 'Practicing') return { bg: '#fff8ee', border: '#FF9600', text: '#7a4600' };
  return { bg: '#f8f8f8', border: '#e0e0e0', text: '#888' };
}

function masteryLabel(m: string) {
  if (m === 'Mastered')   return '✓ Mastered';
  if (m === 'Practicing') return '◑ In Progress';
  return '○ Not started';
}

// ─── Page ──────────────────────────────────────────────────────────────────────

export default function ParentDashboardPage() {
  const params = useParams<{ studentId: string }>();
  const studentId = params?.studentId ?? '';

  const [data,    setData]    = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied,  setCopied]  = useState(false);

  useEffect(() => {
    if (!studentId) return;
    fetch(`/api/dashboard?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d: DashboardData) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [studentId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="text-5xl mb-4 animate-bounce">🌟</div>
          <p className="text-gray-500 font-bold">Loading progress report…</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-8 text-center">
        <div className="text-5xl mb-4">😕</div>
        <h2 className="text-xl font-extrabold text-gray-700 mb-2">Report not found</h2>
        <p className="text-gray-400 text-sm">This link may have expired or the student ID is invalid.</p>
      </div>
    );
  }

  const { student, stats, topics, weeklyData } = data;
  const accuracy = stats.totalSolved > 0
    ? Math.round((stats.totalSolved / Math.max(topics.reduce((s, t) => s + t.attempted, 0), 1)) * 100)
    : 0;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  const sortedTopics = [...topics].sort(
    (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
  );
  const attemptedTopics = sortedTopics.filter((t) => t.attempted > 0);
  const strongest = [...attemptedTopics].sort(
    (a, b) => (b.correct / (b.attempted || 1)) - (a.correct / (a.attempted || 1)),
  )[0];
  const weakest = attemptedTopics
    .filter((t) => t.mastery !== 'Mastered')
    .sort((a, b) => (a.correct / (a.attempted || 1)) - (b.correct / (b.attempted || 1)))[0];

  const pageUrl = typeof window !== 'undefined' ? window.location.href : '';

  return (
    <div className="min-h-screen bg-gray-50 pb-12">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div style={{ background: 'linear-gradient(135deg,#58CC02,#46a302)' }} className="px-6 pt-10 pb-8">
        <div className="max-w-lg mx-auto">
          <p className="text-green-100 text-sm font-semibold mb-1">MathSpark Progress Report</p>
          <h1 className="text-white text-3xl font-extrabold mb-1">{student.name}</h1>
          <p className="text-green-100 text-sm font-medium">Grade {student.grade} · Math Explorer</p>

          {/* Quick stats */}
          <div className="grid grid-cols-3 gap-3 mt-6">
            {[
              { emoji: '✅', value: `${stats.totalSolved}`, label: 'Solved' },
              { emoji: '🔥', value: `${stats.streakDays}d`, label: 'Streak' },
              { emoji: '⭐', value: `${stats.topicsMastered}/16`, label: 'Mastered' },
            ].map(({ emoji, value, label }) => (
              <div key={label} className="bg-white/20 rounded-2xl p-3 text-center">
                <div className="text-xl mb-0.5">{emoji}</div>
                <div className="text-white font-extrabold text-xl leading-none">{value}</div>
                <div className="text-green-100 text-[11px] font-semibold mt-1">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4">

        {/* ── Accuracy highlight ────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-4 flex items-center gap-4">
          <div className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-extrabold border-4 flex-shrink-0"
            style={{
              borderColor: accuracy >= 70 ? '#58CC02' : accuracy >= 50 ? '#FF9600' : '#FF4B4B',
              color:       accuracy >= 70 ? '#46a302' : accuracy >= 50 ? '#cc7800' : '#cc3333',
            }}>
            {accuracy}%
          </div>
          <div>
            <p className="font-extrabold text-gray-800 text-base">Overall Accuracy</p>
            <p className="text-gray-400 text-sm font-medium">
              {accuracy >= 80 ? 'Excellent — top of the class! 🏆' :
               accuracy >= 60 ? 'Good work — improving every day! 📈' :
               'Keep practicing — it gets easier! 💪'}
            </p>
          </div>
        </div>

        {/* ── Weekly chart ──────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-4">This Week's Activity</h2>
          <div className="flex items-end gap-1.5 h-20 mb-1">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm transition-all"
                  style={{
                    background: count > 0 ? 'linear-gradient(to top,#46a302,#58CC02)' : 'transparent',
                    height: `${(count / maxBar) * 64}px`,
                    minHeight: count > 0 ? '4px' : '0',
                  }}
                />
                <span className="text-[10px] text-gray-400 font-semibold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-gray-400 text-center font-medium">Correct answers per day</p>
        </div>

        {/* ── Strongest & Weakest ───────────────────────────────────────── */}
        {(strongest || weakest) && (
          <div className="grid grid-cols-2 gap-3 mt-3">
            {strongest && (
              <div className="bg-green-50 border border-green-200 rounded-2xl p-4">
                <p className="text-[10px] text-green-700 font-extrabold uppercase tracking-wide">💪 Best at</p>
                <p className="text-sm font-extrabold text-gray-800 mt-1">{TOPIC_SHORT[strongest.id] ?? strongest.name}</p>
                <p className="text-xs text-green-600 font-bold mt-0.5">
                  {strongest.attempted > 0 ? Math.round(strongest.correct / strongest.attempted * 100) : 0}% accurate
                </p>
              </div>
            )}
            {weakest && (
              <div className="bg-orange-50 border border-orange-200 rounded-2xl p-4">
                <p className="text-[10px] text-orange-700 font-extrabold uppercase tracking-wide">📈 Focus on</p>
                <p className="text-sm font-extrabold text-gray-800 mt-1">{TOPIC_SHORT[weakest.id] ?? weakest.name}</p>
                <p className="text-xs text-orange-600 font-bold mt-0.5">
                  {weakest.attempted > 0 ? Math.round(weakest.correct / weakest.attempted * 100) : 0}% accurate
                </p>
              </div>
            )}
          </div>
        )}

        {/* ── All topics ────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-4">All 16 Topics</h2>
          <div className="space-y-2">
            {sortedTopics.map((t) => {
              const pct = t.attempted > 0 ? Math.round(t.correct / t.attempted * 100) : 0;
              const { bg, border, text } = masteryColor(t.mastery);
              return (
                <div
                  key={t.id}
                  className="flex items-center gap-3 rounded-xl px-3 py-2.5"
                  style={{ backgroundColor: bg, border: `1px solid ${border}` }}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-gray-700 truncate">
                      {TOPIC_SHORT[t.id] ?? t.name}
                    </p>
                  </div>
                  {t.attempted > 0 && (
                    <span className="text-xs font-extrabold flex-shrink-0" style={{ color: text }}>
                      {pct}%
                    </span>
                  )}
                  <span className="text-[10px] font-bold flex-shrink-0 ml-1" style={{ color: text }}>
                    {masteryLabel(t.mastery)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Encouragement messages ────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-4">
            Send Encouragement to {student.name}
          </h2>
          <p className="text-gray-400 text-sm mb-3 font-medium">
            Copy a message and share it with your child!
          </p>
          <div className="space-y-2">
            {ENCOURAGEMENTS.map((msg, i) => (
              <button
                key={i}
                style={{ minHeight: 0 }}
                onClick={() => {
                  navigator.clipboard.writeText(msg).then(() => {
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  });
                }}
                className="w-full text-left bg-gray-50 hover:bg-green-50 border border-gray-200 hover:border-green-300 rounded-xl px-4 py-3 text-sm text-gray-700 font-medium transition-colors"
              >
                {msg}
              </button>
            ))}
          </div>
          {copied && (
            <p className="text-center text-sm font-bold text-[#58CC02] mt-3 animate-pop-in">
              ✓ Copied to clipboard!
            </p>
          )}
        </div>

        {/* ── Share this page ───────────────────────────────────────────── */}
        <div className="mt-4 text-center">
          <button
            style={{ minHeight: 0 }}
            onClick={() => {
              navigator.clipboard.writeText(pageUrl);
              setCopied(true);
              setTimeout(() => setCopied(false), 2000);
            }}
            className="text-sm font-bold text-gray-400 hover:text-gray-600 transition-colors"
          >
            🔗 Copy page link
          </button>
        </div>

        {/* ── Footer ───────────────────────────────────────────────────── */}
        <div className="mt-8 text-center">
          <p className="text-xs text-gray-300 font-medium">
            MathSpark · Grade 4 Math · India
          </p>
          <p className="text-xs text-gray-300 font-medium mt-1">
            This is a read-only progress view for parents.
          </p>
        </div>

      </div>
    </div>
  );
}

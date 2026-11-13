'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import type { DashboardData } from '@/types';
import { TOPIC_ORDER } from '@/lib/sharedUtils';
import { logError } from '@/lib/logger';

// ─── Constants ─────────────────────────────────────────────────────────────────

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
  if (m === 'Mastered')   return { bg: '#dff6ea', border: '#12805c', text: '#1d2a4d' };
  if (m === 'Practicing') return { bg: '#fff1b8', border: '#5a4300', text: '#5a4300' };
  return { bg: '#eef3fb', border: '#d3deee', text: '#5d6b8c' };
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
    fetch(`/api/parent/report/${studentId}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: DashboardData) => { setData(d); setLoading(false); })
      .catch((err) => { logError('[parent/report] fetch report', err); setLoading(false); });
  }, [studentId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-paper">
        <div className="text-center">
          <div className="text-5xl mb-4 animate-bounce">🌟</div>
          <p className="text-ink-muted font-bold">Loading progress report…</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-paper p-8 text-center">
        <div className="text-5xl mb-4">😕</div>
        <h2 className="text-xl font-extrabold text-ink mb-2">Report not found</h2>
        <p className="text-gray-500 text-sm">This link may have expired or the student ID is invalid.</p>
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
    <div className="min-h-screen bg-paper pb-12">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div style={{ background: '#1d2a4d' }} className="px-6 pt-10 pb-8">
        <div className="max-w-lg mx-auto">
          <p className="text-white/70 text-sm font-semibold mb-1">MathSpark Progress Report</p>
          <h1 className="text-white text-3xl font-extrabold mb-1">{student.name}</h1>
          <p className="text-white/70 text-sm font-medium">Grade {student.grade} · Math Explorer</p>

          {/* Quick stats */}
          <div className="grid grid-cols-3 gap-3 mt-6">
            {[
              { emoji: '✅', value: `${stats.totalSolved}`, label: 'Solved' },
              { emoji: '🔥', value: `${stats.streakDays}d`, label: 'Streak' },
              { emoji: '⭐', value: `${stats.topicsMastered}/16`, label: 'Mastered' },
            ].map(({ emoji, value, label }) => (
              <div key={label} className="bg-white/10 border-2 border-white/30 rounded-tile p-3 text-center">
                <div className="text-xl mb-0.5">{emoji}</div>
                <div className="text-white font-extrabold text-xl leading-none">{value}</div>
                <div className="text-white/70 text-xs font-semibold mt-1">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4">

        {/* ── Accuracy highlight ────────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-4 flex items-center gap-4">
          <div className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-extrabold border-4 flex-shrink-0"
            style={{
              borderColor: accuracy >= 70 ? '#12805c' : accuracy >= 50 ? '#f5a400' : '#c62f3d',
              color:       accuracy >= 70 ? '#12805c' : accuracy >= 50 ? '#5a4300' : '#c62f3d',
            }}>
            {accuracy}%
          </div>
          <div>
            <p className="font-extrabold text-ink text-base">Overall Accuracy</p>
            <p className="text-gray-500 text-sm font-medium">
              {accuracy >= 80 ? 'Excellent — top of the class! 🏆' :
               accuracy >= 60 ? 'Good work — improving every day! 📈' :
               'Keep practicing — it gets easier! 💪'}
            </p>
          </div>
        </div>

        {/* ── Weekly chart ──────────────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-4">This Week's Activity</h2>
          <div className="flex items-end gap-1.5 h-20 mb-1">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm transition-[height]"
                  style={{
                    background: count > 0 ? '#4f46e5' : 'transparent',
                    height: `${(count / maxBar) * 64}px`,
                    minHeight: count > 0 ? '4px' : '0',
                  }}
                />
                <span className="text-xs text-ink-muted font-semibold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 text-center font-medium">Correct answers per day</p>
        </div>

        {/* ── Strongest & Weakest ───────────────────────────────────────── */}
        {(strongest || weakest) && (
          <div className="grid grid-cols-2 gap-3 mt-3">
            {strongest && (
              <div className="bg-success-soft border-2 border-success rounded-card p-4">
                <p className="text-xs text-ink font-extrabold">💪 Best at</p>
                <p className="text-sm font-extrabold text-ink mt-1">{TOPIC_SHORT[strongest.id] ?? strongest.name}</p>
                <p className="text-[15px] text-success font-bold mt-0.5">
                  {strongest.attempted > 0 ? Math.round(strongest.correct / strongest.attempted * 100) : 0}% accurate
                </p>
              </div>
            )}
            {weakest && (
              <div className="bg-hint border-2 border-hint-ink rounded-card p-4">
                <p className="text-xs text-hint-ink font-extrabold">📈 Focus on</p>
                <p className="text-sm font-extrabold text-ink mt-1">{TOPIC_SHORT[weakest.id] ?? weakest.name}</p>
                <p className="text-[15px] text-hint-ink font-bold mt-0.5">
                  {weakest.attempted > 0 ? Math.round(weakest.correct / weakest.attempted * 100) : 0}% accurate
                </p>
              </div>
            )}
          </div>
        )}

        {/* ── All topics ────────────────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-4">All 16 Topics</h2>
          <div className="space-y-2">
            {sortedTopics.map((t) => {
              const pct = t.attempted > 0 ? Math.round(t.correct / t.attempted * 100) : 0;
              const { bg, border, text } = masteryColor(t.mastery);
              return (
                <div
                  key={t.id}
                  className="flex items-center gap-3 rounded-control px-3 py-2.5"
                  style={{ backgroundColor: bg, border: `1px solid ${border}` }}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-ink truncate">
                      {TOPIC_SHORT[t.id] ?? t.name}
                    </p>
                  </div>
                  {t.attempted > 0 && (
                    <span className="text-xs font-extrabold flex-shrink-0" style={{ color: text }}>
                      {pct}%
                    </span>
                  )}
                  <span className="text-xs font-bold flex-shrink-0 ml-1" style={{ color: text }}>
                    {masteryLabel(t.mastery)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Encouragement messages ────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-4">
            Send Encouragement to {student.name}
          </h2>
          <p className="text-gray-500 text-sm mb-3 font-medium">
            Copy a message and share it with your child!
          </p>
          <div className="space-y-2">
            {ENCOURAGEMENTS.map((msg, i) => (
              <button
                key={i}
                onClick={() => {
                  navigator.clipboard.writeText(msg).then(() => {
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  });
                }}
                className="w-full text-left bg-white hover:bg-soft border-2 border-line hover:border-ink rounded-control px-4 py-3 text-sm text-ink font-medium transition-colors min-h-[48px]"
              >
                {msg}
              </button>
            ))}
          </div>
          {copied && (
            <p className="text-center text-[15px] font-bold text-success mt-3 animate-pop-in">
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
            className="text-sm font-bold text-ink-muted hover:text-ink transition-colors"
          >
            🔗 Copy page link
          </button>
        </div>

        {/* ── Footer ───────────────────────────────────────────────────── */}
        <div className="mt-8 text-center">
          <p className="text-xs text-ink-muted font-medium">
            MathSpark · Grade 4 Math · India
          </p>
          <p className="text-xs text-ink-muted font-medium mt-1">
            This is a read-only progress view for parents.
          </p>
        </div>

      </div>
    </div>
  );
}

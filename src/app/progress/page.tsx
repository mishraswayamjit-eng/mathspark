'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import type { DashboardData } from '@/types';

// ── Mastery helpers ───────────────────────────────────────────────────────────

interface TopicEntry {
  id: string;
  name: string;
  attempted: number;
  correct: number;
  mastery: string;
}

function accuracyPct(t: TopicEntry) {
  return t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
}

function masteryLevel(pct: number) {
  if (pct >= 90) return { label: 'Mastered', color: '#4CAF50', emoji: '✅', bg: '#F0FDF4' };
  if (pct >= 75) return { label: 'Strong',   color: '#8BC34A', emoji: '💪', bg: '#F7FEE7' };
  if (pct >= 50) return { label: 'Developing',color: '#FFC107', emoji: '🔄', bg: '#FFFBEB' };
  return                 { label: 'Needs Practice', color: '#FF5722', emoji: '🎯', bg: '#FEF2F2' };
}

function readinessLabel(score: number) {
  if (score >= 90) return { text: 'Exam Ready! Keep polishing.', emoji: '🏆' };
  if (score >= 75) return { text: 'Almost there. Focus on weak spots.', emoji: '💪' };
  if (score >= 60) return { text: 'Good foundation. Need more practice.', emoji: '🔄' };
  if (score >= 40) return { text: 'Building up. Consistency is key.', emoji: '🎯' };
  return { text: 'Early stages. Daily practice will make a big difference.', emoji: '🌱' };
}

// ── Mistake pattern type ──────────────────────────────────────────────────────

interface MistakePattern {
  id: string;
  name: string;
  emoji: string;
  category: string;
  description: string;
  howToFix: string;
  frequency: string;
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ProgressPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [mistakes, setMistakes] = useState<MistakePattern[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    Promise.all([
      fetch(`/api/dashboard?studentId=${studentId}`).then((r) => r.json()),
      fetch('/api/mistake-patterns').then((r) => r.json()).catch(() => ({ patterns: [] })),
    ])
      .then(([dashData, mistakeData]) => {
        setData(dashData);
        setMistakes(mistakeData.patterns ?? []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        <div className="bg-duo-dark px-4 py-4 flex items-center gap-3">
          <div className="h-5 bg-white/20 rounded w-24 animate-pulse" />
        </div>
        <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-28" />
          ))}
        </div>
      </div>
    );
  }

  const { student, stats, topics, weeklyData } = data;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  // Compute accuracy & readiness
  const totalAttempted = topics.reduce((s, t) => s + t.attempted, 0);
  const totalCorrect = topics.reduce((s, t) => s + t.correct, 0);
  const overallAccuracy = totalAttempted > 0 ? Math.round((totalCorrect / totalAttempted) * 100) : 0;

  const attemptedTopics = topics.filter((t) => t.attempted > 0);
  const practiceConsistency = Math.min(100, Math.round((stats.streakDays / 7) * 100));
  const readinessScore = attemptedTopics.length > 0
    ? Math.round(overallAccuracy * 0.6 + practiceConsistency * 0.25 + Math.min(100, (attemptedTopics.length / topics.length) * 100) * 0.15)
    : 0;
  const readiness = readinessLabel(readinessScore);

  // Strengths & weaknesses
  const strengths = attemptedTopics
    .filter((t) => t.attempted >= 5 && accuracyPct(t) >= 80)
    .sort((a, b) => accuracyPct(b) - accuracyPct(a));

  const weakAreas = attemptedTopics
    .filter((t) => t.attempted >= 3 && accuracyPct(t) < 60)
    .sort((a, b) => accuracyPct(a) - accuracyPct(b));

  // Top 3 mistake patterns (most relevant — "Very High" frequency first)
  const freqOrder: Record<string, number> = { 'Very High': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
  const topMistakes = [...mistakes]
    .sort((a, b) => (freqOrder[a.frequency] ?? 4) - (freqOrder[b.frequency] ?? 4))
    .slice(0, 3);

  // Recommendations
  const recommendations: { emoji: string; text: string; link: string }[] = [];
  if (topMistakes.length > 0) {
    recommendations.push({
      emoji: '🔍',
      text: `Learn about the "${topMistakes[0].name}" mistake pattern — it's very common!`,
      link: '/learn/mistakes',
    });
  }
  if (weakAreas.length > 0) {
    recommendations.push({
      emoji: '🎯',
      text: `Practice ${weakAreas[0].name} — you're at ${accuracyPct(weakAreas[0])}%. A few drills will help!`,
      link: `/practice/${weakAreas[0].id}`,
    });
  }
  if (strengths.length > 0) {
    recommendations.push({
      emoji: '⭐',
      text: `Keep ${strengths[0].name} sharp with a quick review this week!`,
      link: `/practice/${strengths[0].id}`,
    });
  }
  if (recommendations.length < 3) {
    recommendations.push({
      emoji: '📝',
      text: 'Try a practice paper to test your exam readiness!',
      link: '/practice/papers',
    });
  }

  // Readiness ring
  const ringR = 46;
  const ringCircumference = 2 * Math.PI * ringR;
  const ringOffset = ringCircumference * (1 - readinessScore / 100);
  const ringColor = readinessScore >= 75 ? '#4CAF50' : readinessScore >= 50 ? '#FFC107' : '#FF5722';

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/home" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">My Progress</h1>
          <p className="text-white/50 text-xs font-medium">{student.name} &middot; Grade {student.grade}</p>
        </div>
        <Link href={`/progress/report`} className="text-xs font-bold text-white/60 bg-white/10 rounded-full px-3 py-1.5 hover:bg-white/20 transition-colors">
          Parent Report
        </Link>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── AT A GLANCE ──────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-3">At a Glance</h2>
          <div className="grid grid-cols-4 gap-2">
            {[
              { value: stats.totalSolved, label: 'Solved', emoji: '✅', color: '#58CC02' },
              { value: `${overallAccuracy}%`, label: 'Accuracy', emoji: '🎯', color: overallAccuracy >= 70 ? '#58CC02' : '#FF9600' },
              { value: `${stats.streakDays}d`, label: 'Streak', emoji: '🔥', color: '#FF9600' },
              { value: `${stats.topicsMastered}`, label: 'Mastered', emoji: '⭐', color: '#1CB0F6' },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <span className="text-lg">{s.emoji}</span>
                <p className="text-lg font-extrabold" style={{ color: s.color }}>{s.value}</p>
                <p className="text-[9px] font-bold text-gray-400 uppercase">{s.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* ── EXAM READINESS ───────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4">
          <svg width="100" height="100" viewBox="0 0 100 100" className="shrink-0">
            <circle cx="50" cy="50" r={ringR} stroke="#E5E7EB" strokeWidth="8" fill="none" />
            <circle
              cx="50" cy="50" r={ringR}
              stroke={ringColor}
              strokeWidth="8"
              fill="none"
              strokeDasharray={ringCircumference}
              strokeDashoffset={ringOffset}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
              style={{ transition: 'stroke-dashoffset 1s ease' }}
            />
            <text x="50" y="46" textAnchor="middle" fontSize="20" fontWeight="800" fill={ringColor}>{readinessScore}</text>
            <text x="50" y="60" textAnchor="middle" fontSize="8" fill="#9CA3AF">/ 100</text>
          </svg>
          <div>
            <p className="text-sm font-extrabold text-gray-800">Exam Readiness</p>
            <p className="text-xs text-gray-500 font-medium mt-0.5">
              {readiness.emoji} {readiness.text}
            </p>
          </div>
        </div>

        {/* ── WEEKLY ACTIVITY ──────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-3">This Week</h2>
          <div className="flex items-end gap-1.5 h-24">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <span className="text-[9px] text-gray-400 font-semibold min-h-[12px]">
                  {count > 0 ? count : ''}
                </span>
                <div className="w-full relative bg-gray-100 rounded-sm" style={{ height: 56 }}>
                  <div
                    className="absolute bottom-0 left-0 right-0 rounded-sm transition-[height] duration-500"
                    style={{
                      height: count > 0 ? `${Math.max(4, Math.round((count / maxBar) * 56))}px` : '0px',
                      background: 'linear-gradient(to top, #46a302, #58CC02)',
                    }}
                  />
                </div>
                <span className="text-[9px] text-gray-400 font-bold">{date}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ── STRENGTHS ────────────────────────────────────────────── */}
        {strengths.length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <h2 className="text-[10px] font-extrabold text-green-600 uppercase tracking-wide mb-3">
              💪 Strengths — What You&apos;re Great At
            </h2>
            <div className="space-y-2">
              {strengths.slice(0, 4).map((t) => {
                const pct = accuracyPct(t);
                return (
                  <div key={t.id} className="flex items-center gap-3 bg-green-50 rounded-xl px-3 py-2.5 border border-green-100">
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-extrabold text-gray-800 truncate">{t.name}</p>
                      <p className="text-[10px] text-green-600 font-bold">{t.correct}/{t.attempted} correct</p>
                    </div>
                    <span className="text-sm font-extrabold text-green-600 shrink-0">{pct}%</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── AREAS TO STRENGTHEN ──────────────────────────────────── */}
        {weakAreas.length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <h2 className="text-[10px] font-extrabold text-orange-600 uppercase tracking-wide mb-3">
              🎯 Areas to Strengthen
            </h2>
            <div className="space-y-2">
              {weakAreas.slice(0, 4).map((t) => {
                const pct = accuracyPct(t);
                return (
                  <Link
                    key={t.id}
                    href={`/practice/${t.id}`}
                    className="flex items-center gap-3 bg-orange-50 rounded-xl px-3 py-2.5 border border-orange-100 active:bg-orange-100 transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-extrabold text-gray-800 truncate">{t.name}</p>
                      <p className="text-[10px] text-orange-600 font-bold">{pct}% — keep practicing!</p>
                    </div>
                    <span className="text-xs font-extrabold text-orange-500 shrink-0">Practice →</span>
                  </Link>
                );
              })}
            </div>
          </div>
        )}

        {/* ── TOP 3 MISTAKE PATTERNS ───────────────────────────────── */}
        {topMistakes.length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-[10px] font-extrabold text-red-500 uppercase tracking-wide">
                🔍 Mistakes to Watch For
              </h2>
              <Link href="/learn/mistakes" className="text-[10px] font-bold text-blue-500">See all →</Link>
            </div>
            <div className="space-y-2.5">
              {topMistakes.map((m) => (
                <div key={m.id} className="bg-red-50 rounded-xl p-3 border border-red-100">
                  <div className="flex items-start gap-2">
                    <span className="text-lg shrink-0">{m.emoji}</span>
                    <div className="flex-1">
                      <p className="text-xs font-extrabold text-gray-800">{m.name}</p>
                      <p className="text-[11px] text-gray-500 font-medium mt-0.5 line-clamp-2">{m.description}</p>
                      <p className="text-[10px] text-green-700 font-bold mt-1">Fix: {m.howToFix.slice(0, 80)}…</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── TOPIC MASTERY HEATMAP ────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-3">
            🗺️ Topic Mastery Map
          </h2>
          {/* Legend */}
          <div className="flex gap-2 mb-3 flex-wrap">
            {[
              { label: 'Mastered', color: '#4CAF50' },
              { label: 'Strong', color: '#8BC34A' },
              { label: 'Developing', color: '#FFC107' },
              { label: 'Needs Work', color: '#FF5722' },
              { label: 'Not Started', color: '#E5E7EB' },
            ].map((l) => (
              <div key={l.label} className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: l.color }} />
                <span className="text-[9px] font-bold text-gray-500">{l.label}</span>
              </div>
            ))}
          </div>
          {/* Heatmap grid */}
          <div className="grid grid-cols-4 gap-1.5">
            {topics.map((t) => {
              const pct = accuracyPct(t);
              const level = t.attempted === 0
                ? { color: '#E5E7EB', label: 'Not started', emoji: '—', bg: '#F9FAFB' }
                : masteryLevel(pct);
              return (
                <Link
                  key={t.id}
                  href={`/practice/${t.id}`}
                  className="rounded-xl p-2 text-center transition-transform active:scale-95"
                  style={{ backgroundColor: level.bg, border: `1.5px solid ${level.color}` }}
                >
                  <span className="text-sm">{level.emoji}</span>
                  <p className="text-[8px] font-bold text-gray-700 leading-tight mt-0.5 line-clamp-2">
                    {t.name.length > 16 ? t.name.slice(0, 14) + '…' : t.name}
                  </p>
                  {t.attempted > 0 && (
                    <p className="text-[9px] font-extrabold mt-0.5" style={{ color: level.color }}>{pct}%</p>
                  )}
                </Link>
              );
            })}
          </div>
        </div>

        {/* ── RECOMMENDATIONS ──────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-3">
            📋 What to Do This Week
          </h2>
          <div className="space-y-2">
            {recommendations.slice(0, 3).map((rec, i) => (
              <Link
                key={i}
                href={rec.link}
                className="flex items-center gap-3 bg-blue-50 rounded-xl px-3 py-3 border border-blue-100 active:bg-blue-100 transition-colors"
              >
                <span className="text-lg shrink-0">{rec.emoji}</span>
                <p className="text-xs font-medium text-gray-700 flex-1">{rec.text}</p>
                <span className="text-xs text-blue-500 font-bold shrink-0">Go →</span>
              </Link>
            ))}
          </div>
        </div>

        {/* ── SPARKY ENCOURAGEMENT ─────────────────────────────────── */}
        <div className="bg-purple-50 rounded-2xl p-4 border border-purple-200 flex items-start gap-3">
          <Sparky mood="celebrating" size={40} />
          <div>
            <p className="text-sm font-bold text-purple-800">
              {overallAccuracy >= 80
                ? "You're doing incredible! Keep pushing for the top!"
                : overallAccuracy >= 50
                ? "Great progress! Every practice session makes you stronger!"
                : "Every expert was once a beginner. Keep going!"}
            </p>
            <p className="text-xs text-purple-600 mt-0.5">
              {stats.totalSolved > 0
                ? `You've solved ${stats.totalSolved} questions so far. That's awesome!`
                : 'Start practicing to track your progress!'}
            </p>
          </div>
        </div>

        {/* ── SHARE WITH PARENT ────────────────────────────────────── */}
        <Link
          href="/progress/report"
          className="block bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-4 border border-green-200 shadow-sm text-center hover:shadow-md transition-shadow"
        >
          <span className="text-2xl">📊</span>
          <p className="text-sm font-extrabold text-green-800 mt-1">Generate Parent Report</p>
          <p className="text-xs text-green-600 font-medium">Share your progress with your parents!</p>
        </Link>
      </div>
    </div>
  );
}

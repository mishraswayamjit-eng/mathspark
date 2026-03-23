'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import type { DashboardData } from '@/types';

// ── Helpers ───────────────────────────────────────────────────────────────────

function accuracyPct(t: { attempted: number; correct: number }) {
  return t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
}

function masteryColor(pct: number) {
  if (pct >= 90) return { bg: '#F0FDF4', border: '#4CAF50', text: '#2D6A04', label: 'Mastered ✅' };
  if (pct >= 75) return { bg: '#F7FEE7', border: '#8BC34A', text: '#3F6212', label: 'Strong 💪' };
  if (pct >= 50) return { bg: '#FFFBEB', border: '#FFC107', text: '#78350F', label: 'Developing 🔄' };
  return                 { bg: '#FEF2F2', border: '#FF5722', text: '#7F1D1D', label: 'Needs Practice 🎯' };
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ParentReportPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [studentId, setStudentId] = useState('');

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);

    fetch(`/api/dashboard?studentId=${id}`)
      .then((r) => r.json())
      .then((d: DashboardData) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [router]);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="text-5xl mb-4 animate-bounce">📊</div>
          <p className="text-gray-500 font-bold">Generating report…</p>
        </div>
      </div>
    );
  }

  const { student, stats, topics, weeklyData } = data;
  const totalAttempted = topics.reduce((s, t) => s + t.attempted, 0);
  const totalCorrect = topics.reduce((s, t) => s + t.correct, 0);
  const overallAccuracy = totalAttempted > 0 ? Math.round((totalCorrect / totalAttempted) * 100) : 0;
  const maxBar = Math.max(...weeklyData.map((d) => d.count), 1);

  const attemptedTopics = topics.filter((t) => t.attempted > 0);
  const strengths = attemptedTopics
    .filter((t) => t.attempted >= 5 && accuracyPct(t) >= 80)
    .sort((a, b) => accuracyPct(b) - accuracyPct(a));
  const weakAreas = attemptedTopics
    .filter((t) => t.attempted >= 3 && accuracyPct(t) < 60)
    .sort((a, b) => accuracyPct(a) - accuracyPct(b));

  // Readiness
  const practiceConsistency = Math.min(100, Math.round((stats.streakDays / 7) * 100));
  const readinessScore = attemptedTopics.length > 0
    ? Math.round(overallAccuracy * 0.6 + practiceConsistency * 0.25 + Math.min(100, (attemptedTopics.length / topics.length) * 100) * 0.15)
    : 0;

  const readinessLabel = readinessScore >= 90 ? '🏆 Exam Ready!'
    : readinessScore >= 75 ? '💪 Almost There'
    : readinessScore >= 60 ? '🔄 Good Foundation'
    : readinessScore >= 40 ? '🎯 Building Up'
    : '🌱 Getting Started';

  // Share link
  const shareUrl = typeof window !== 'undefined' ? `${window.location.origin}/parent/${studentId}` : '';

  const today = new Date();
  const dateStr = today.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });

  return (
    <div className="min-h-screen bg-gray-50 pb-12 animate-fade-in" id="parent-report">

      {/* ── Header ──────────────────────────────────────────────── */}
      <div style={{ background: 'linear-gradient(135deg, #58CC02, #46a302)' }} className="px-6 pt-8 pb-6">
        <div className="max-w-lg mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <Sparky mood="happy" size={44} />
            <div>
              <p className="text-green-100 text-xs font-semibold">MathSpark Progress Report</p>
              <p className="text-green-100 text-[10px] font-medium">{dateStr}</p>
            </div>
          </div>
          <h1 className="text-white text-2xl font-extrabold">{student.name}&apos;s Report</h1>
          <p className="text-green-100 text-sm font-medium">Grade {student.grade}</p>

          {/* Quick stats */}
          <div className="grid grid-cols-4 gap-2 mt-5">
            {[
              { value: stats.totalSolved, label: 'Solved', emoji: '✅' },
              { value: `${overallAccuracy}%`, label: 'Accuracy', emoji: '🎯' },
              { value: `${stats.streakDays}d`, label: 'Streak', emoji: '🔥' },
              { value: `${stats.topicsMastered}`, label: 'Mastered', emoji: '⭐' },
            ].map((s) => (
              <div key={s.label} className="bg-white/20 rounded-xl p-2.5 text-center">
                <span className="text-lg">{s.emoji}</span>
                <p className="text-white font-extrabold text-lg leading-none mt-0.5">{s.value}</p>
                <p className="text-green-100 text-[9px] font-bold mt-0.5">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4">

        {/* ── Exam Readiness ───────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-4 flex items-center gap-4">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-xl font-extrabold border-4 shrink-0"
            style={{
              borderColor: readinessScore >= 75 ? '#4CAF50' : readinessScore >= 50 ? '#FFC107' : '#FF5722',
              color: readinessScore >= 75 ? '#2D6A04' : readinessScore >= 50 ? '#78350F' : '#7F1D1D',
            }}
          >
            {readinessScore}
          </div>
          <div>
            <p className="font-extrabold text-gray-800 text-sm">Exam Readiness Score</p>
            <p className="text-xs text-gray-500 font-medium mt-0.5">{readinessLabel}</p>
          </div>
        </div>

        {/* ── Strengths ────────────────────────────────────────────── */}
        {strengths.length > 0 && (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
            <h2 className="text-[11px] font-extrabold text-green-600 uppercase tracking-widest mb-3">
              💪 What {student.name} is Great At
            </h2>
            <div className="space-y-2">
              {strengths.slice(0, 4).map((t) => (
                <div key={t.id} className="bg-green-50 rounded-xl px-3 py-2.5 border border-green-100 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-gray-800">{t.name}</p>
                    <p className="text-[10px] text-green-600 font-medium">{t.correct}/{t.attempted} correct — brilliant!</p>
                  </div>
                  <span className="text-sm font-extrabold text-green-600">{accuracyPct(t)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Areas to Strengthen ──────────────────────────────────── */}
        {weakAreas.length > 0 && (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
            <h2 className="text-[11px] font-extrabold text-orange-600 uppercase tracking-widest mb-3">
              🎯 Areas to Strengthen
            </h2>
            <p className="text-xs text-gray-400 font-medium mb-2">
              These topics just need a bit more practice — totally fixable!
            </p>
            <div className="space-y-2">
              {weakAreas.slice(0, 4).map((t) => (
                <div key={t.id} className="bg-orange-50 rounded-xl px-3 py-2.5 border border-orange-100 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-gray-800">{t.name}</p>
                    <p className="text-[10px] text-orange-600 font-medium">{accuracyPct(t)}% — more practice will help</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Weekly Activity ──────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">This Week&apos;s Activity</h2>
          <div className="flex items-end gap-1.5 h-16 mb-1">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm transition-[height]"
                  style={{
                    background: count > 0 ? 'linear-gradient(to top,#46a302,#58CC02)' : 'transparent',
                    height: `${Math.max(count > 0 ? 4 : 0, Math.round((count / maxBar) * 48))}px`,
                  }}
                />
                <span className="text-[9px] text-gray-400 font-bold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-gray-400 text-center font-medium">Questions practiced per day</p>
        </div>

        {/* ── Topic Mastery Map ─────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">
            🗺️ Topic Mastery Map
          </h2>
          <div className="space-y-1.5">
            {topics.map((t) => {
              const pct = accuracyPct(t);
              const level = t.attempted === 0
                ? { bg: '#F9FAFB', border: '#E5E7EB', text: '#9CA3AF', label: 'Not started' }
                : masteryColor(pct);
              return (
                <div
                  key={t.id}
                  className="flex items-center gap-3 rounded-xl px-3 py-2"
                  style={{ backgroundColor: level.bg, border: `1px solid ${level.border}` }}
                >
                  <p className="text-xs font-bold text-gray-700 flex-1 truncate">{t.name}</p>
                  {t.attempted > 0 && (
                    <span className="text-xs font-extrabold shrink-0" style={{ color: level.text }}>{pct}%</span>
                  )}
                  <span className="text-[9px] font-bold shrink-0" style={{ color: level.text }}>{level.label}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Recommendations ──────────────────────────────────────── */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-3">
          <h2 className="text-[11px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">
            📋 What to Do This Week
          </h2>
          <div className="space-y-2.5">
            {weakAreas.length > 0 && (
              <div className="flex items-start gap-2">
                <span className="text-sm shrink-0 mt-0.5">1️⃣</span>
                <p className="text-xs text-gray-700 font-medium">
                  Spend 10 minutes on <strong>{weakAreas[0].name}</strong> — {student.name} is at {accuracyPct(weakAreas[0])}%.
                  A few focused practice sessions will make a big difference!
                </p>
              </div>
            )}
            {strengths.length > 0 && (
              <div className="flex items-start gap-2">
                <span className="text-sm shrink-0 mt-0.5">2️⃣</span>
                <p className="text-xs text-gray-700 font-medium">
                  Keep <strong>{strengths[0].name}</strong> sharp with a quick 5-minute review this week!
                </p>
              </div>
            )}
            <div className="flex items-start gap-2">
              <span className="text-sm shrink-0 mt-0.5">3️⃣</span>
              <p className="text-xs text-gray-700 font-medium">
                Try a practice paper to test overall exam readiness. Even 15 minutes helps!
              </p>
            </div>
          </div>
        </div>

        {/* ── Sparky's Message ─────────────────────────────────────── */}
        <div className="bg-purple-50 rounded-2xl p-4 mt-3 border border-purple-200 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-purple-800">
              {overallAccuracy >= 80
                ? `${student.name} is doing amazing! Top-level performance!`
                : overallAccuracy >= 50
                ? `${student.name} is making great progress! Consistent practice is the key.`
                : `${student.name} is on the right track! Every question makes them stronger.`}
            </p>
            <p className="text-xs text-purple-600 mt-0.5 italic">
              — Sparky, your math buddy
            </p>
          </div>
        </div>

        {/* ── Share ────────────────────────────────────────────────── */}
        <div className="mt-5 space-y-3">
          <button
            onClick={() => {
              navigator.clipboard.writeText(shareUrl);
              setCopied(true);
              setTimeout(() => setCopied(false), 2000);
            }}
            className="w-full bg-duo-green text-white font-extrabold text-sm py-3 rounded-2xl shadow-md hover:bg-duo-green-dark transition-colors active:scale-[0.98]"
          >
            {copied ? '✓ Link Copied!' : '🔗 Copy Shareable Link for Parents'}
          </button>

          <button
            onClick={() => router.back()}
            className="w-full text-gray-400 font-bold text-sm py-2"
          >
            ← Back to Progress
          </button>
        </div>

        {/* ── Footer ───────────────────────────────────────────────── */}
        <div className="mt-6 text-center pb-4">
          <p className="text-[10px] text-gray-300 font-medium">
            MathSpark · Generated {dateStr} · For parents of {student.name}
          </p>
        </div>
      </div>
    </div>
  );
}

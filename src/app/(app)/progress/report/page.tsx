'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import type { DashboardData } from '@/types';
import { logError } from '@/lib/logger';

// ── Helpers ───────────────────────────────────────────────────────────────────

function accuracyPct(t: { attempted: number; correct: number }) {
  return t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
}

function masteryColor(pct: number) {
  if (pct >= 90) return { bg: '#dff6ea', border: '#12805c', text: '#1d2a4d', label: 'Mastered ✅' };
  if (pct >= 75) return { bg: '#dff3f8', border: '#0e7490', text: '#0e7490', label: 'Strong 💪' };
  if (pct >= 50) return { bg: '#fff1b8', border: '#5a4300', text: '#5a4300', label: 'Developing 🔄' };
  return                 { bg: '#fde8ea', border: '#c62f3d', text: '#c62f3d', label: 'Needs Practice 🎯' };
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

    fetch('/api/dashboard')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: DashboardData) => { setData(d); setLoading(false); })
      .catch((err) => { logError('[progress/report] fetch dashboard', err); setLoading(false); });
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-paper">
        <div className="text-center">
          <div className="text-5xl mb-4 animate-bounce">📊</div>
          <p className="text-ink-muted font-bold">Generating report…</p>
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
    <div className="min-h-screen bg-paper pb-12 animate-fade-in" id="parent-report">

      {/* ── Header ──────────────────────────────────────────────── */}
      <div style={{ background: 'linear-gradient(135deg, #1d2a4d, #1d2a4d)' }} className="px-6 pt-8 pb-6">
        <div className="max-w-lg mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <Sparky mood="happy" size={44} />
            <div>
              <p className="text-white/70 text-xs font-semibold">MathSpark Progress Report</p>
              <p className="text-white/70 text-xs font-medium">{dateStr}</p>
            </div>
          </div>
          <h1 className="text-white text-heading">{student.name}&apos;s Report</h1>
          <p className="text-white/70 text-sm font-medium">Grade {student.grade}</p>

          {/* Quick stats */}
          <div className="grid grid-cols-4 gap-2 mt-5">
            {[
              { value: stats.totalSolved, label: 'Solved', emoji: '✅' },
              { value: `${overallAccuracy}%`, label: 'Accuracy', emoji: '🎯' },
              { value: `${stats.streakDays}d`, label: 'Streak', emoji: '🔥' },
              { value: `${stats.topicsMastered}`, label: 'Mastered', emoji: '⭐' },
            ].map((s) => (
              <div key={s.label} className="bg-white/10 rounded-tile p-2.5 text-center">
                <span className="text-lg">{s.emoji}</span>
                <p className="text-white font-extrabold text-lg leading-none mt-0.5">{s.value}</p>
                <p className="text-white/70 text-xs font-bold mt-0.5">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4">

        {/* ── Exam Readiness ───────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-4 flex items-center gap-4">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-xl font-extrabold border-4 shrink-0"
            style={{
              borderColor: readinessScore >= 75 ? '#12805c' : readinessScore >= 50 ? '#f5a400' : '#c62f3d',
              color: readinessScore >= 75 ? '#12805c' : readinessScore >= 50 ? '#5a4300' : '#c62f3d',
            }}
          >
            {readinessScore}
          </div>
          <div>
            <p className="font-extrabold text-ink text-sm">Exam Readiness Score</p>
            <p className="text-xs text-ink-muted font-medium mt-0.5">{readinessLabel}</p>
          </div>
        </div>

        {/* ── Strengths ────────────────────────────────────────────── */}
        {strengths.length > 0 && (
          <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
            <h2 className="text-title text-ink mb-3">
              💪 What {student.name} is Great At
            </h2>
            <div className="space-y-2">
              {strengths.slice(0, 4).map((t) => (
                <div key={t.id} className="bg-success-soft rounded-control px-3 py-2.5 border-2 border-success flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-ink">{t.name}</p>
                    <p className="text-xs text-ink-muted font-medium">{t.correct}/{t.attempted} correct — brilliant!</p>
                  </div>
                  <span className="text-label font-extrabold text-success">{accuracyPct(t)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Areas to Strengthen ──────────────────────────────────── */}
        {weakAreas.length > 0 && (
          <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
            <h2 className="text-title text-ink mb-3">
              🎯 Areas to Strengthen
            </h2>
            <p className="text-xs text-ink-muted font-medium mb-2">
              These topics just need a bit more practice — totally fixable!
            </p>
            <div className="space-y-2">
              {weakAreas.slice(0, 4).map((t) => (
                <div key={t.id} className="bg-hint rounded-control px-3 py-2.5 border-2 border-hint-ink flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-ink">{t.name}</p>
                    <p className="text-xs text-hint-ink font-medium">{accuracyPct(t)}% — more practice will help</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Weekly Activity ──────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-3">This Week&apos;s Activity</h2>
          <div className="flex items-end gap-1.5 h-16 mb-1">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm transition-[height]"
                  style={{
                    background: count > 0 ? 'linear-gradient(to top,#4f46e5,#4f46e5)' : 'transparent',
                    height: `${Math.max(count > 0 ? 4 : 0, Math.round((count / maxBar) * 48))}px`,
                  }}
                />
                <span className="text-xs text-ink-muted font-bold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-ink-muted text-center font-medium">Questions practiced per day</p>
        </div>

        {/* ── Topic Mastery Map ─────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-3">
            🗺️ Topic Mastery Map
          </h2>
          <div className="space-y-1.5">
            {topics.map((t) => {
              const pct = accuracyPct(t);
              const level = t.attempted === 0
                ? { bg: '#ffffff', border: '#d3deee', text: '#5d6b8c', label: 'Not started' }
                : masteryColor(pct);
              return (
                <div
                  key={t.id}
                  className="flex items-center gap-3 rounded-control px-3 py-2"
                  style={{ backgroundColor: level.bg, border: `1px solid ${level.border}` }}
                >
                  <p className="text-xs font-bold text-ink flex-1 truncate">{t.name}</p>
                  {t.attempted > 0 && (
                    <span className="text-xs font-extrabold shrink-0" style={{ color: level.text }}>{pct}%</span>
                  )}
                  <span className="text-xs font-bold shrink-0" style={{ color: level.text }}>{level.label}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Recommendations ──────────────────────────────────────── */}
        <div className="bg-white rounded-card border-2 border-line p-5 mt-3">
          <h2 className="text-title text-ink mb-3">
            📋 What to Do This Week
          </h2>
          <div className="space-y-2.5">
            {weakAreas.length > 0 && (
              <div className="flex items-start gap-2">
                <span className="text-sm shrink-0 mt-0.5">1️⃣</span>
                <p className="text-xs text-ink font-medium">
                  Spend 10 minutes on <strong>{weakAreas[0].name}</strong> — {student.name} is at {accuracyPct(weakAreas[0])}%.
                  A few focused practice sessions will make a big difference!
                </p>
              </div>
            )}
            {strengths.length > 0 && (
              <div className="flex items-start gap-2">
                <span className="text-sm shrink-0 mt-0.5">2️⃣</span>
                <p className="text-xs text-ink font-medium">
                  Keep <strong>{strengths[0].name}</strong> sharp with a quick 5-minute review this week!
                </p>
              </div>
            )}
            <div className="flex items-start gap-2">
              <span className="text-sm shrink-0 mt-0.5">3️⃣</span>
              <p className="text-xs text-ink font-medium">
                Try a practice paper to test overall exam readiness. Even 15 minutes helps!
              </p>
            </div>
          </div>
        </div>

        {/* ── Sparky's Message ─────────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 mt-3 border-2 border-line flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">
              {overallAccuracy >= 80
                ? `${student.name} is doing amazing! Top-level performance!`
                : overallAccuracy >= 50
                ? `${student.name} is making great progress! Consistent practice is the key.`
                : `${student.name} is on the right track! Every question makes them stronger.`}
            </p>
            <p className="text-xs text-ink-muted mt-0.5 italic">
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
            className="w-full bg-action text-white border-2 border-ink shadow-hard-sm font-extrabold text-sm py-3 rounded-control hover:bg-action-dark transition-colors active:scale-[0.98]"
          >
            {copied ? '✓ Link Copied!' : '🔗 Copy Shareable Link for Parents'}
          </button>

          <button
            onClick={() => window.history.length > 1 ? router.back() : router.push('/progress')}
            className="w-full text-action font-bold text-sm py-2"
          >
            ← Back to Progress
          </button>
        </div>

        {/* ── Footer ───────────────────────────────────────────────── */}
        <div className="mt-6 text-center pb-4">
          <p className="text-xs text-ink-muted font-medium">
            MathSpark · Generated {dateStr} · For parents of {student.name}
          </p>
        </div>
      </div>
    </div>
  );
}

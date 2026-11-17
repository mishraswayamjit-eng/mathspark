'use client';

import { useEffect, useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import AvatarLink from '@/components/shell/AvatarLink';
import type { DashboardData } from '@/types';
import { logError } from '@/lib/logger';

// ── Mastery helpers ───────────────────────────────────────────────────────────

/**
 * One topic as GET /api/dashboard reports it for a keyed grade (Grade 5 and
 * the other grades whose topics share one database topic): a topic-tree node
 * with the Brain Engine's stored numbers.
 */
interface NodeTopic {
  id: string;
  name: string;
  emoji: string;
  href: string;
  extra: boolean;
  attempted: number;
  correct: number;
  accuracy: number;
  mastery: number;
  status: string;
}

/** The dashboard response, with the per-topic rows keyed grades also get. */
type ProgressData = DashboardData & {
  nodeTopics?: NodeTopic[] | null;
  nodeTopicsMastered?: number | null;
};

/** One topic on this page, whichever source it came from. */
interface TopicEntry {
  id: string;
  name: string;
  attempted: number;
  correct: number;
  /** Practice link that opens exactly this topic. */
  href: string;
}

/** Sign-in is gone: forget this device's child and ask them to log in again. */
function clearChildFromDevice(): void {
  try {
    Object.keys(localStorage)
      .filter((k) => k.indexOf('mathspark_') === 0)
      .forEach((k) => localStorage.removeItem(k));
  } catch {
    // Storage blocked: nothing to forget.
  }
}

function accuracyPct(t: { attempted: number; correct: number }) {
  return t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
}

function masteryLevel(pct: number) {
  if (pct >= 90) return { label: 'Mastered', color: '#12805c', emoji: '✅', bg: '#dff6ea' };
  if (pct >= 75) return { label: 'Strong',   color: '#0e7490', emoji: '💪', bg: '#dff3f8' };
  if (pct >= 50) return { label: 'Developing',color: '#5a4300', emoji: '🔄', bg: '#fff1b8' };
  return                 { label: 'Needs Practice', color: '#c62f3d', emoji: '🎯', bg: '#fde8ea' };
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
  const [data, setData] = useState<ProgressData | null>(null);
  const [mistakes, setMistakes] = useState<MistakePattern[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    // The sign-in has run out (or the account is gone). That is not a connection
    // problem: send the child to log in again, and keep the loading screen up
    // meanwhile instead of telling them to check their connection.
    let signedOut = false;

    Promise.all([
      fetch('/api/dashboard').then((r) => {
        if (r.status === 401 || r.status === 404) {
          signedOut = true;
          throw new Error('Signed out');
        }
        if (!r.ok) throw new Error('Dashboard fetch failed');
        return r.json();
      }),
      fetch('/api/mistake-patterns').then((r) => r.ok ? r.json() : { patterns: [] }).catch((err) => { logError('[progress] fetch mistake-patterns', err); return { patterns: [] }; }),
    ])
      .then(([dashData, mistakeData]) => {
        setData(dashData);
        setMistakes(mistakeData.patterns ?? []);
        setLoading(false);
      })
      .catch((err) => {
        if (signedOut) {
          clearChildFromDevice();
          router.replace('/student/login');
          return;
        }
        logError('[fetch]', err);
        setFetchError(true);
        setLoading(false);
      });
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const topics = data?.topics ?? [];
  const streakDays = data?.stats?.streakDays ?? 0;

  // The topics this page lists. A keyed grade (Grade 5 …) keeps all its
  // questions under ONE database topic, so `topics` is a single row for the
  // whole grade; its real topics come as `nodeTopics`, each with its own link.
  const nodeTopics = data?.nodeTopics;
  const hasNodeTopics = Array.isArray(nodeTopics) && nodeTopics.length > 0;
  const topicRows: TopicEntry[] = useMemo(() => {
    if (Array.isArray(nodeTopics) && nodeTopics.length > 0) {
      return nodeTopics.map((t) => ({
        id: t.id,
        name: t.name,
        attempted: t.attempted,
        correct: t.correct,
        href: t.href,
      }));
    }
    return topics.map((t) => ({
      id: t.id,
      name: t.name,
      attempted: t.attempted,
      correct: t.correct,
      href: `/practice/${t.id}`,
    }));
  }, [nodeTopics, topics]);

  const maxBar = useMemo(
    () => Math.max(...(data?.weeklyData ?? []).map((d) => d.count), 1),
    [data?.weeklyData],
  );

  // Compute accuracy & readiness
  const { totalAttempted, totalCorrect, overallAccuracy } = useMemo(() => {
    const attempted = topics.reduce((s, t) => s + t.attempted, 0);
    const correct = topics.reduce((s, t) => s + t.correct, 0);
    const accuracy = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;
    return { totalAttempted: attempted, totalCorrect: correct, overallAccuracy: accuracy };
  }, [topics]);

  const attemptedTopics = useMemo(
    () => topicRows.filter((t) => t.attempted > 0),
    [topicRows],
  );

  // Coverage: how many of the grade's topics the child has started.
  const practiceConsistency = Math.min(100, Math.round((streakDays / 7) * 100));
  const readinessScore = attemptedTopics.length > 0 && topicRows.length > 0
    ? Math.round(overallAccuracy * 0.6 + practiceConsistency * 0.25 + Math.min(100, (attemptedTopics.length / topicRows.length) * 100) * 0.15)
    : 0;
  const readiness = readinessLabel(readinessScore);

  // Strengths & weaknesses
  const strengths = useMemo(
    () => attemptedTopics
      .filter((t) => t.attempted >= 5 && accuracyPct(t) >= 80)
      .sort((a, b) => accuracyPct(b) - accuracyPct(a)),
    [attemptedTopics],
  );

  const weakAreas = useMemo(
    () => attemptedTopics
      .filter((t) => t.attempted >= 3 && accuracyPct(t) < 60)
      .sort((a, b) => accuracyPct(a) - accuracyPct(b)),
    [attemptedTopics],
  );

  // Top 3 mistake patterns (most relevant — "Very High" frequency first)
  const topMistakes = useMemo(() => {
    const freqOrder: Record<string, number> = { 'Very High': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
    return [...mistakes]
      .sort((a, b) => (freqOrder[a.frequency] ?? 4) - (freqOrder[b.frequency] ?? 4))
      .slice(0, 3);
  }, [mistakes]);

  // Recommendations
  const recommendations = useMemo(() => {
    const recs: { emoji: string; text: string; link: string }[] = [];
    if (topMistakes.length > 0) {
      recs.push({
        emoji: '🔍',
        text: `Learn about the "${topMistakes[0].name}" mistake pattern — it's very common!`,
        link: '/learn/mistakes',
      });
    }
    if (weakAreas.length > 0) {
      recs.push({
        emoji: '🎯',
        text: `Practice ${weakAreas[0].name} — you're at ${accuracyPct(weakAreas[0])}%. A few drills will help!`,
        link: weakAreas[0].href,
      });
    }
    if (strengths.length > 0) {
      recs.push({
        emoji: '⭐',
        text: `Keep ${strengths[0].name} sharp with a quick review this week!`,
        link: strengths[0].href,
      });
    }
    if (recs.length < 3) {
      recs.push({
        emoji: '📝',
        text: 'Try a practice paper to test your exam readiness!',
        link: '/practice/papers',
      });
    }
    return recs;
  }, [topMistakes, weakAreas, strengths]);

  // Readiness ring
  const ringR = 46;
  const ringCircumference = 2 * Math.PI * ringR;
  const ringOffset = ringCircumference * (1 - readinessScore / 100);
  const ringColor = readinessScore >= 75 ? '#12805c' : readinessScore >= 50 ? '#f5a400' : '#c62f3d';

  if (!loading && (fetchError || !data)) {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-4 pb-24">
        <p className="text-ink font-extrabold text-lg">Oops! Sparky tripped over a number</p>
        <p className="text-ink-muted text-sm">Could not load progress data. Check your connection.</p>
        <button onClick={() => window.location.reload()} className="bg-action text-white border-2 border-ink shadow-hard-sm font-extrabold px-6 py-2.5 rounded-control text-sm active:scale-95 transition-transform">
          Retry
        </button>
      </div>
    );
  }

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-paper pb-24">
        <div className="bg-ink px-4 py-4 flex items-center gap-3">
          <div className="h-5 bg-white/20 rounded w-24 animate-pulse" />
        </div>
        <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-28" />
          ))}
        </div>
      </div>
    );
  }

  const { student, stats, weeklyData } = data;
  // Topics mastered. For a keyed grade the Progress table has one row for the
  // whole grade, so the count comes from the per-topic rows instead.
  const masteredCount = hasNodeTopics && typeof data.nodeTopicsMastered === 'number'
    ? data.nodeTopicsMastered
    : stats.topicsMastered;

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-white text-title">My Progress</h1>
          <p className="text-white/70 text-[13px] font-semibold truncate">{student.name} &middot; Grade {student.grade}</p>
        </div>
        <AvatarLink />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── MY PROGRESS | LEAGUE ─────────────────────────────────── */}
        <nav aria-label="Progress sections" className="flex gap-1 bg-soft border-2 border-line rounded-control p-1">
          <span
            aria-current="page"
            className="flex-1 min-h-[48px] flex items-center justify-center rounded-note bg-white border-2 border-ink text-label font-extrabold text-ink"
          >
            My progress
          </span>
          <Link
            href="/leaderboard"
            className="flex-1 min-h-[48px] flex items-center justify-center rounded-note border-2 border-transparent text-label font-extrabold text-ink-muted hover:text-ink transition-colors"
          >
            <span aria-hidden="true">🏆&nbsp;</span>League
          </Link>
        </nav>

        {/* ── AT A GLANCE ──────────────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line">
          <h2 className="text-title text-ink mb-3">At a Glance</h2>
          <div className="grid grid-cols-4 gap-2">
            {[
              { value: stats.totalSolved, label: 'Solved', emoji: '✅', color: '#12805c' },
              { value: `${overallAccuracy}%`, label: 'Accuracy', emoji: '🎯', color: overallAccuracy >= 70 ? '#12805c' : '#5a4300' },
              { value: `${stats.streakDays}d`, label: 'Streak', emoji: '🔥', color: '#1d2a4d' },
              { value: `${masteredCount}`, label: 'Mastered', emoji: '⭐', color: '#12805c' },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <span className="text-lg" aria-hidden="true">{s.emoji}</span>
                <p className="text-lg font-extrabold" style={{ color: s.color }}>{s.value}</p>
                <p className="text-xs font-bold text-ink-muted">{s.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* ── EXAM READINESS ───────────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line flex items-center gap-4">
          <svg width="100" height="100" viewBox="0 0 100 100" className="shrink-0">
            <circle cx="50" cy="50" r={ringR} stroke="#d3deee" strokeWidth="8" fill="none" />
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
            <text x="50" y="60" textAnchor="middle" fontSize="8" fill="#5d6b8c">/ 100</text>
          </svg>
          <div>
            <p className="text-sm font-extrabold text-ink">Exam Readiness</p>
            <p className="text-xs text-ink-muted font-medium mt-0.5">
              <span aria-hidden="true">{readiness.emoji} </span>{readiness.text}
            </p>
          </div>
        </div>

        {/* ── WEEKLY ACTIVITY ──────────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line">
          <h2 className="text-title text-ink mb-3">This Week</h2>
          <div className="flex items-end gap-1.5 h-24">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <span className="text-xs text-ink-muted font-semibold min-h-[12px]">
                  {count > 0 ? count : ''}
                </span>
                <div className="w-full relative bg-soft rounded-sm h-[56px]">
                  <div
                    className="absolute bottom-0 left-0 right-0 rounded-sm transition-[height] duration-500 bg-action"
                    style={{
                      height: count > 0 ? `${Math.max(4, Math.round((count / maxBar) * 56))}px` : '0px',
                    }}
                  />
                </div>
                <span className="text-xs text-ink-muted font-bold">{date}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ── STRENGTHS ────────────────────────────────────────────── */}
        {strengths.length > 0 && (
          <div className="bg-white rounded-card p-4 border-2 border-line">
            <h2 className="text-title text-ink mb-3">
              <span aria-hidden="true">💪 </span>Strengths — What You&apos;re Great At
            </h2>
            <div className="space-y-2">
              {strengths.slice(0, 4).map((t) => {
                const pct = accuracyPct(t);
                return (
                  <div key={t.id} className="flex items-center gap-3 bg-success-soft rounded-control px-3 py-2.5 border-2 border-success">
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-extrabold text-ink truncate">{t.name}</p>
                      <p className="text-xs text-ink-muted font-bold">{t.correct}/{t.attempted} correct</p>
                    </div>
                    <span className="text-label font-extrabold text-success shrink-0">{pct}%</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── AREAS TO STRENGTHEN ──────────────────────────────────── */}
        {weakAreas.length > 0 && (
          <div className="bg-white rounded-card p-4 border-2 border-line">
            <h2 className="text-title text-ink mb-3">
              <span aria-hidden="true">🎯 </span>Areas to Strengthen
            </h2>
            <div className="space-y-2">
              {weakAreas.slice(0, 4).map((t) => {
                const pct = accuracyPct(t);
                return (
                  <Link
                    key={t.id}
                    href={t.href}
                    className="flex items-center gap-3 bg-hint rounded-control px-3 py-2.5 border-2 border-hint-ink active:bg-white transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-extrabold text-ink truncate">{t.name}</p>
                      <p className="text-xs text-hint-ink font-bold">{pct}% — keep practicing!</p>
                    </div>
                    <span className="text-xs font-extrabold text-action shrink-0">Practice →</span>
                  </Link>
                );
              })}
            </div>
          </div>
        )}

        {/* ── TOP 3 MISTAKE PATTERNS ───────────────────────────────── */}
        {topMistakes.length > 0 && (
          <div className="bg-white rounded-card p-4 border-2 border-line">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-title text-ink">
                <span aria-hidden="true">🔍 </span>Mistakes to Watch For
              </h2>
              <Link href="/learn/mistakes" className="text-xs font-bold text-action">See all →</Link>
            </div>
            <div className="space-y-2.5">
              {topMistakes.map((m) => (
                <div key={m.id} className="bg-soft rounded-control p-3 border-2 border-line">
                  <div className="flex items-start gap-2">
                    <span className="text-lg shrink-0" aria-hidden="true">{m.emoji}</span>
                    <div className="flex-1">
                      <p className="text-xs font-extrabold text-ink">{m.name}</p>
                      <p className="text-xs text-ink-muted font-medium mt-0.5 line-clamp-2">{m.description}</p>
                      <p className="text-xs text-ink font-bold mt-1">Fix: {m.howToFix.slice(0, 80)}…</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── TOPIC MASTERY HEATMAP ────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line">
          <h2 className="text-title text-ink mb-3">
            <span aria-hidden="true">🗺️ </span>Topic Mastery Map
          </h2>
          {/* Legend */}
          <div className="flex gap-2 mb-3 flex-wrap">
            {[
              { label: 'Mastered', color: '#12805c' },
              { label: 'Strong', color: '#0e7490' },
              { label: 'Developing', color: '#5a4300' },
              { label: 'Keep practising', color: '#c62f3d' },
              { label: 'Not Started', color: '#d3deee' },
            ].map((l) => (
              <div key={l.label} className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: l.color }} />
                <span className="text-xs font-bold text-ink-muted">{l.label}</span>
              </div>
            ))}
          </div>
          {/* Heatmap grid */}
          <div className="grid grid-cols-4 gap-1.5">
            {topicRows.map((t) => {
              const pct = accuracyPct(t);
              const level = t.attempted === 0
                ? { color: '#d3deee', label: 'Not started', emoji: '—', bg: '#ffffff' }
                : masteryLevel(pct);
              return (
                <Link
                  key={t.id}
                  href={t.href}
                  className="rounded-tile p-2 text-center transition-transform active:scale-95"
                  style={{ backgroundColor: level.bg, border: `1.5px solid ${level.color}` }}
                >
                  <span className="text-sm" aria-hidden="true">{level.emoji}</span>
                  <span className="sr-only">{level.label}: </span>
                  <p className="text-xs font-bold text-ink leading-tight mt-0.5 line-clamp-2 break-words">
                    {t.name.length > 16 ? t.name.slice(0, 14) + '…' : t.name}
                  </p>
                  {t.attempted > 0 && (
                    <p className="text-xs font-extrabold mt-0.5" style={{ color: level.color }}>{pct}%</p>
                  )}
                </Link>
              );
            })}
          </div>
        </div>

        {/* ── RECOMMENDATIONS ──────────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line">
          <h2 className="text-title text-ink mb-3">
            <span aria-hidden="true">📋 </span>What to Do This Week
          </h2>
          <div className="space-y-2">
            {recommendations.slice(0, 3).map((rec, i) => (
              <Link
                key={i}
                href={rec.link}
                className="flex items-center gap-3 bg-soft rounded-control px-3 py-3 border-2 border-line active:border-ink transition-colors"
              >
                <span className="text-lg shrink-0" aria-hidden="true">{rec.emoji}</span>
                <p className="text-xs font-medium text-ink flex-1">{rec.text}</p>
                <span className="text-xs text-action font-bold shrink-0">Go →</span>
              </Link>
            ))}
          </div>
        </div>

        {/* ── SPARKY ENCOURAGEMENT ─────────────────────────────────── */}
        <div className="bg-white rounded-card p-4 border-2 border-line flex items-start gap-3">
          <Sparky mood="celebrating" size={40} />
          <div>
            <p className="text-sm font-bold text-ink">
              {overallAccuracy >= 80
                ? "You're doing incredible! Keep pushing for the top!"
                : overallAccuracy >= 50
                ? "Great progress! Every practice session makes you stronger!"
                : "Every expert was once a beginner. Keep going!"}
            </p>
            <p className="text-xs text-ink-muted mt-0.5">
              {stats.totalSolved > 0
                ? `You've solved ${stats.totalSolved} questions so far. That's awesome!`
                : 'Start practicing to track your progress!'}
            </p>
          </div>
        </div>

        {/* ── SHARE WITH PARENT ────────────────────────────────────── */}
        <Link
          href="/progress/report"
          className="block bg-white rounded-control p-4 border-2 border-ink shadow-hard-sm text-center hover:bg-soft transition-colors"
        >
          <span className="text-2xl" aria-hidden="true">📨</span>
          <p className="text-label font-extrabold text-ink mt-1">Share with parent</p>
          <p className="text-[13px] text-ink-muted font-semibold">Make a report your parents can read, and send them the link.</p>
        </Link>
      </div>
    </div>
  );
}

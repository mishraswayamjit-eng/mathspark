'use client';

import { useState, useEffect } from 'react';
import { logError } from '@/lib/logger';
import { useRouter } from 'next/navigation';
import DuoButton from '@/components/DuoButton';
import Sparky from '@/components/Sparky';
import type { TestType, PYQYear } from '@/types';
import { MONETIZATION_ENABLED } from '@/lib/monetization';

// ── Synthetic test options ─────────────────────────────────────────────────────

const TEST_OPTIONS: Array<{
  type: TestType;
  label: string;
  emoji: string;
  questions: number;
  time: string;
  desc: string;
  color: string;
  border: string;
}> = [
  {
    type: 'quick',
    label: 'Quick Test',
    emoji: '⚡',
    questions: 15,
    time: '20 min',
    desc: 'Fast check-in across key topics',
    color: 'bg-soft',
    border: 'border-action',
  },
  {
    type: 'half',
    label: 'Half Paper',
    emoji: '📄',
    questions: 30,
    time: '40 min',
    desc: 'Mid-term style practice paper',
    color: 'bg-soft',
    border: 'border-action',
  },
  {
    type: 'ipm',
    label: 'IPM Blueprint',
    emoji: '🎯',
    questions: 40,
    time: '60 min',
    desc: 'Matches real IPM topic & difficulty distribution',
    color: 'bg-soft',
    border: 'border-action',
  },
  {
    type: 'full',
    label: 'Full Paper',
    emoji: '🏆',
    questions: 50,
    time: '60 min',
    desc: 'Extended paper — full grade question pool',
    color: 'bg-soft',
    border: 'border-action',
  },
];

// ── Previous year paper cards ──────────────────────────────────────────────────

const PYQ_YEARS: Array<{
  year: PYQYear;
  label: string;
  subtitle: string;
  color: string;
}> = [
  { year: 2019, label: 'IPM 2019',  subtitle: '40 Qs · 60 min · Most Recent', color: 'bg-white' },
  { year: 2018, label: 'IPM 2018',  subtitle: '40 Qs · 60 min',               color: 'bg-white' },
  { year: 2017, label: 'IPM 2017',  subtitle: '40 Qs · 60 min',               color: 'bg-white' },
  { year: 2016, label: 'IPM 2016',  subtitle: '40 Qs · 60 min · First Year',  color: 'bg-white' },
];

// ── Component ──────────────────────────────────────────────────────────────────

export default function TestConfigPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<TestType>('ipm');
  const [loading,           setLoading]           = useState(false);
  const [pyqLoading,        setPyqLoading]        = useState<PYQYear | null>(null);
  const [megaLoading,       setMegaLoading]       = useState(false);
  const [error,             setError]             = useState('');
  const [studentId,         setStudentId]         = useState<string | null>(null);
  const [studentGrade,      setStudentGrade]      = useState<number>(4);
  const [subscriptionTier,  setSubscriptionTier]  = useState<number>(0);
  const [trialActive,       setTrialActive]       = useState(false);

  useEffect(() => {
    const id    = localStorage.getItem('mathspark_student_id');
    const grade = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);
    setStudentGrade(isNaN(grade) ? 4 : grade);

    // Check trial status from localStorage (fast, synchronous)
    const trialExpires = localStorage.getItem('mathspark_trial_expires');
    if (trialExpires) {
      setTrialActive(new Date(trialExpires) > new Date());
    }

    // Fetch subscription tier + authoritative trial from home API
    fetch('/api/home')
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data?.student?.subscriptionTier != null) {
          setSubscriptionTier(data.student.subscriptionTier);
        }
        if (data?.student?.trialExpiresAt) {
          setTrialActive(new Date(data.student.trialExpiresAt) > new Date());
        }
      })
      .catch((err) => logError('[fetch]', err));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const IS_MEGA_ACCESSIBLE = !MONETIZATION_ENABLED || subscriptionTier >= 2 || trialActive;

  // Start a synthetic test (quick / half / ipm / full)
  async function handleStart() {
    if (!studentId) return;
    setLoading(true);
    setError('');
    try {
      // For non-Grade-4 students, scope quick/half/full to their grade pool
      // IPM generator handles grade-aware topic selection server-side
      const topicIds = studentGrade !== 4 && selected !== 'ipm'
        ? [`grade${studentGrade}`]
        : undefined;

      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ type: selected, topicIds }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        if (res.status === 401) throw new Error('Session expired — please log in again.');
        if (res.status === 429) throw new Error('Too many tests created. Wait a minute and try again.');
        throw new Error(body?.error || 'Failed to create test. Please try again.');
      }
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again!');
      setLoading(false);
    }
  }

  // Start a previous-year paper
  async function handlePYQ(year: PYQYear) {
    if (!studentId) return;
    setPyqLoading(year);
    setError('');
    try {
      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ type: 'pyq', year }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        if (res.status === 401) throw new Error('Session expired — please log in again.');
        if (res.status === 429) throw new Error('Too many tests created. Wait a minute and try again.');
        throw new Error(body?.error || 'Failed to create test. Please try again.');
      }
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again!');
      setPyqLoading(null);
    }
  }

  // Start a Mega Final test
  async function handleMega() {
    if (!studentId) return;
    setMegaLoading(true);
    setError('');
    try {
      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ type: 'mega', topicIds: [`grade${studentGrade}`] }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        if (res.status === 401) throw new Error('Session expired — please log in again.');
        if (res.status === 429) throw new Error('Too many tests created. Wait a minute and try again.');
        throw new Error(body?.error || 'Failed to create test. Please try again.');
      }
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again!');
      setMegaLoading(false);
    }
  }

  const opt = TEST_OPTIONS.find((o) => o.type === selected)!;

  return (
    <div className="min-h-screen bg-paper flex flex-col pb-28 animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-8 pb-4">
        <button
          onClick={() => window.history.length > 1 ? router.back() : router.push('/practice')}
          className="text-ink-muted text-sm font-semibold mb-4 flex items-center gap-1 hover:text-ink transition-colors"
        >
          ← Back
        </button>
        <div className="flex items-center gap-3 mb-2">
          <div className="animate-sparky-bounce">
            <Sparky mood="thinking" size={48} />
          </div>
          <div>
            <h1 className="text-display text-ink">IPM Mock Test</h1>
            <p className="text-ink-muted text-sm font-medium">No hints · Timed · Full simulation</p>
          </div>
        </div>
      </div>

      {/* ── Section: Synthetic tests ────────────────────────────────────────── */}
      <div className="px-4">
        <p className="text-caption text-ink-muted mb-2">
          Synthetic Papers
        </p>
        <div className="space-y-2">
          {TEST_OPTIONS.map((o) => {
            const isSelected = selected === o.type;
            return (
              <button
                key={o.type}
                onClick={() => setSelected(o.type)}
                className={`w-full text-left rounded-control p-4 border-2 transition-[colors,border-color,box-shadow,transform] duration-150 ${
                  isSelected
                    ? `${o.color} ${o.border} active:scale-[0.97]`
                    : 'bg-white border-line hover:border-ink active:scale-[0.97]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{o.emoji}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className={`font-extrabold text-sm ${isSelected ? 'text-ink' : 'text-ink'}`}>
                        {o.label}
                      </span>
                      <div className="flex items-center gap-1.5">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          isSelected ? 'bg-white text-ink' : 'bg-soft text-ink-muted'
                        }`}>{o.questions} Qs</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          isSelected ? 'bg-white text-ink' : 'bg-soft text-ink-muted'
                        }`}>{o.time}</span>
                      </div>
                    </div>
                    <p className={`text-xs mt-0.5 font-medium ${isSelected ? 'text-ink-muted' : 'text-ink-muted'}`}>
                      {o.desc}
                    </p>
                  </div>
                  {isSelected && <span className="text-action text-base ml-1">✓</span>}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Rules callout */}
      <div className="px-4 mt-3">
        <div className="bg-white border-2 border-line rounded-card p-3 space-y-1">
          <p className="text-ink font-extrabold text-xs">📋 Exam Rules</p>
          <ul className="text-ink-muted text-xs font-medium space-y-0.5">
            <li>• No hints or feedback during the test</li>
            <li>• Jump between questions freely · Flag for review</li>
            <li>• Full analytics shown after submission</li>
          </ul>
        </div>
      </div>

      {error && <p className="text-retry text-sm text-center font-semibold px-4 mt-2">{error}</p>}

      {/* Start CTA */}
      <div className="px-4 mt-4">
        <DuoButton variant="green" fullWidth loading={loading} onClick={handleStart}>
          Start {opt.label} {opt.emoji}
        </DuoButton>
      </div>

      {/* ── Section: Previous Year Papers ──────────────────────────────────── */}
      <div className="px-4 mt-6">
        <div className="flex items-center gap-2 mb-3">
          <p className="text-caption text-ink-muted">
            Previous Year Papers
          </p>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {PYQ_YEARS.map(({ year, label, subtitle, color }) => (
            <button
              key={year}
              onClick={() => handlePYQ(year)}
              disabled={pyqLoading !== null}
              className={`relative ${color} border-2 border-ink shadow-hard-sm rounded-control p-4 text-left transition-[opacity,transform] duration-150 min-h-[100px] flex flex-col justify-between active:scale-[0.97] disabled:opacity-60`}
            >
              <div>
                <p className="text-ink font-extrabold text-base leading-tight">{label}</p>
                <p className="text-ink-muted text-xs font-semibold mt-1">{subtitle}</p>
              </div>
              <div className="flex items-center justify-between mt-3">
                <span className="text-ink-muted text-xs font-bold">Shuffled order</span>
                {pyqLoading === year ? (
                  <span className="inline-block w-4 h-4 border-2 border-line border-t-action rounded-full animate-spin" />
                ) : (
                  <span className="text-action text-sm">→</span>
                )}
              </div>
            </button>
          ))}
        </div>
        <p className="text-ink-muted text-xs text-center mt-2 font-medium">
          Actual questions from 2016–2019 IPM papers
        </p>
      </div>

      {/* ── Section: Mega Final ─────────────────────────────────────────────── */}
      <div className="px-4 mt-6">
        <div className="flex items-center gap-2 mb-3">
          <p className="text-caption text-ink-muted">
            Mega Final Experience
          </p>
        </div>

        {/* Timed Mega Final card */}
        <div className="relative mb-3">
          <div className={`bg-white border-2 ${IS_MEGA_ACCESSIBLE ? 'border-ink shadow-hard-lg' : 'border-line'} rounded-card p-4 space-y-3`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="text-2xl">🏆</span>
                <div>
                  <p className="text-ink font-extrabold text-sm leading-tight">THE ULTIMATE CHALLENGE</p>
                  <p className="text-ink-muted text-xs">Full Mega Mock · 15 Qs · 45 min</p>
                </div>
              </div>
              <span className="text-xs font-bold px-2 py-1 rounded-full bg-soft text-ink border-2 border-line shrink-0">
                PRO
              </span>
            </div>
            <div className="space-y-1">
              <p className="text-ink-muted text-xs">✦ Grade {studentGrade}-specific · Hard difficulty only</p>
              <p className="text-ink-muted text-xs">✦ No repeats · No hints · Full simulation</p>
              <p className="text-ink-muted text-xs">✦ Detailed performance report after</p>
            </div>
            <DuoButton variant="green" fullWidth loading={megaLoading} onClick={handleMega}>
              Begin Mega Final 🚀
            </DuoButton>
          </div>

          {/* Frosted overlay for non-subscribers */}
          {!IS_MEGA_ACCESSIBLE && (
            <div
              className="absolute inset-0 rounded-card flex flex-col items-center justify-center"
              style={{ backdropFilter: 'blur(6px)', background: 'rgba(13,26,32,0.75)' }}
            >
              <span className="text-3xl mb-2">🔒</span>
              <p className="text-white font-extrabold text-sm mb-1">Pro Feature</p>
              <p className="text-white/70 text-xs mb-3 text-center px-8">Start your free trial to unlock the Ultimate Challenge</p>
              <button
                onClick={() => router.push('/pricing')}
                className="bg-star border-2 border-ink shadow-hard-sm text-ink font-extrabold px-5 py-2 rounded-control text-xs active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs transition-[colors,border-color,transform]"
              >
                Unlock with Pro Trial →
              </button>
            </div>
          )}
        </div>

        {/* Untimed Challenge card */}
        <div className="relative">
          <div className={`bg-white border-2 ${IS_MEGA_ACCESSIBLE ? 'border-line' : 'border-line'} rounded-card p-4`}>
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="text-ink font-extrabold text-sm">MEGA CHALLENGE MODE</p>
                <p className="text-ink-muted text-xs">Untimed · Random hard questions</p>
              </div>
              <span className="text-xs font-bold px-2 py-1 rounded-full bg-soft text-ink border-2 border-line shrink-0">
                PRO
              </span>
            </div>
            <DuoButton variant="blue" fullWidth loading={false} onClick={handleMega}>
              Start Challenge ⚡
            </DuoButton>
          </div>

          {!IS_MEGA_ACCESSIBLE && (
            <div
              className="absolute inset-0 rounded-card"
              style={{ backdropFilter: 'blur(4px)', background: 'rgba(13,26,32,0.6)' }}
            />
          )}
        </div>
      </div>

      {/* View history link */}
      <div className="px-4 mt-4">
        <button
          onClick={() => router.push('/test/history')}
          className="w-full text-action text-sm font-semibold text-center py-2 hover:text-action-dark transition-colors"
        >
          View past tests →
        </button>
      </div>
    </div>
  );
}

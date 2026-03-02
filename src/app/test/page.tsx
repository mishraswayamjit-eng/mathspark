'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DuoButton from '@/components/DuoButton';
import Sparky from '@/components/Sparky';
import type { TestType, PYQYear } from '@/types';

// ── Synthetic test options ─────────────────────────────────────────────────────

const TEST_OPTIONS: Array<{
  type: TestType;
  label: string;
  emoji: string;
  questions: number;
  time: string;
  desc: string;
  descGradePool: string; // shown for non-Grade-4 students
  color: string;
  border: string;
  grade4Only?: boolean;
}> = [
  {
    type: 'quick',
    label: 'Quick Test',
    emoji: '⚡',
    questions: 15,
    time: '20 min',
    desc: 'Fast check-in across key topics',
    descGradePool: 'Fast check-in from your grade\'s IPM practice pool',
    color: 'bg-blue-50',
    border: 'border-[#1CB0F6]',
  },
  {
    type: 'half',
    label: 'Half Paper',
    emoji: '📄',
    questions: 30,
    time: '40 min',
    desc: 'Mid-term style practice paper',
    descGradePool: 'Mid-term style paper from your grade\'s question pool',
    color: 'bg-amber-50',
    border: 'border-[#FF9600]',
  },
  {
    type: 'ipm',
    label: 'IPM Blueprint',
    emoji: '🎯',
    questions: 40,
    time: '60 min',
    desc: 'Matches real IPM topic & difficulty distribution',
    descGradePool: 'Matches real IPM topic & difficulty distribution',
    color: 'bg-purple-50',
    border: 'border-purple-400',
    grade4Only: true,
  },
  {
    type: 'full',
    label: 'Full Paper',
    emoji: '🏆',
    questions: 50,
    time: '60 min',
    desc: 'Extended paper — all 16 topics, max challenge',
    descGradePool: 'Extended paper — full grade IPM question pool',
    color: 'bg-green-50',
    border: 'border-[#58CC02]',
  },
];

// ── Previous year paper cards ──────────────────────────────────────────────────

const PYQ_YEARS: Array<{
  year: PYQYear;
  label: string;
  subtitle: string;
  color: string;
}> = [
  { year: 2019, label: 'IPM 2019',  subtitle: '40 Qs · 60 min · Most Recent', color: 'from-[#1CB0F6] to-[#0a98dc]' },
  { year: 2018, label: 'IPM 2018',  subtitle: '40 Qs · 60 min',               color: 'from-[#58CC02] to-[#46a302]' },
  { year: 2017, label: 'IPM 2017',  subtitle: '40 Qs · 60 min',               color: 'from-[#FF9600] to-[#cc7800]' },
  { year: 2016, label: 'IPM 2016',  subtitle: '40 Qs · 60 min · First Year',  color: 'from-[#9B59B6] to-[#7D3C98]' },
];

// ── Component ──────────────────────────────────────────────────────────────────

export default function TestConfigPage() {
  const router = useRouter();
  // Default to 'ipm' for Grade 4, 'quick' for all other grades.
  // Initialise synchronously from localStorage to avoid a FOUC where the
  // Grade 4-only IPM Blueprint is briefly shown to non-Grade-4 students.
  const [selected, setSelected] = useState<TestType>(() => {
    if (typeof window === 'undefined') return 'ipm';
    const g = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    return g === 4 ? 'ipm' : 'quick';
  });
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
    fetch(`/api/home?studentId=${id}`)
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data?.student?.subscriptionTier != null) {
          setSubscriptionTier(data.student.subscriptionTier);
        }
        if (data?.student?.trialExpiresAt) {
          setTrialActive(new Date(data.student.trialExpiresAt) > new Date());
        }
      })
      .catch(() => {});
  }, [router]);

  const isGrade4 = studentGrade === 4;
  const IS_MEGA_ACCESSIBLE = subscriptionTier >= 2 || trialActive;

  // Start a synthetic test (quick / half / ipm / full)
  async function handleStart() {
    if (!studentId) return;
    setLoading(true);
    setError('');
    try {
      // For non-Grade-4 students on quick/half/full, scope questions to their grade pool
      const topicIds = !isGrade4 && selected !== 'ipm'
        ? [`grade${studentGrade}`]
        : undefined;

      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ studentId, type: selected, topicIds }),
      });
      if (!res.ok) throw new Error('Failed to create test');
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch {
      setError('Something went wrong. Please try again!');
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
        body: JSON.stringify({ studentId, type: 'pyq', year }),
      });
      if (!res.ok) throw new Error('Failed to create test');
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch {
      setError('Something went wrong. Please try again!');
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
        body: JSON.stringify({ studentId, type: 'mega', topicIds: [`grade${studentGrade}`] }),
      });
      if (!res.ok) throw new Error('Failed to create test');
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch {
      setError('Something went wrong. Please try again!');
      setMegaLoading(false);
    }
  }

  const opt = TEST_OPTIONS.find((o) => o.type === selected)!;

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col pb-28">
      {/* Header */}
      <div className="px-4 pt-8 pb-4">
        <button
          onClick={() => router.back()}
          className="text-white/60 text-sm font-semibold mb-4 flex items-center gap-1 hover:text-white transition-colors"
        >
          ← Back
        </button>
        <div className="flex items-center gap-3 mb-2">
          <div className="animate-sparky-bounce">
            <Sparky mood="thinking" size={48} />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-white">{isGrade4 ? 'IPM Mock Test' : 'Mock Test'}</h1>
            <p className="text-white/60 text-sm font-medium">No hints · Timed · Full simulation</p>
          </div>
        </div>
      </div>

      {/* ── Section: Synthetic tests ────────────────────────────────────────── */}
      <div className="px-4">
        <p className="text-xs font-extrabold text-white/40 uppercase tracking-widest mb-2">
          Synthetic Papers
        </p>
        <div className="space-y-2">
          {TEST_OPTIONS.map((o) => {
            const locked = !!o.grade4Only && !isGrade4;
            const isSelected = selected === o.type && !locked;
            const desc = !isGrade4 ? o.descGradePool : o.desc;
            return (
              <button
                key={o.type}
                onClick={() => !locked && setSelected(o.type)}
                disabled={locked}
                className={`w-full text-left rounded-2xl p-4 border-2 transition-all duration-150 ${
                  locked
                    ? 'bg-white/5 border-white/5 opacity-50 cursor-not-allowed'
                    : isSelected
                      ? `${o.color} ${o.border} shadow-md active:scale-[0.97]`
                      : 'bg-white/10 border-white/10 hover:border-white/30 active:scale-[0.97]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{o.emoji}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={`font-extrabold text-sm ${isSelected ? 'text-gray-800' : 'text-white'}`}>
                          {o.label}
                        </span>
                        {locked && (
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
                            Grade 4 only
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          isSelected ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                        }`}>{o.questions} Qs</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          isSelected ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                        }`}>{o.time}</span>
                      </div>
                    </div>
                    <p className={`text-xs mt-0.5 font-medium ${isSelected ? 'text-gray-600' : 'text-white/40'}`}>
                      {desc}
                    </p>
                  </div>
                  {isSelected && <span className="text-[#58CC02] text-base ml-1">✓</span>}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Rules callout */}
      <div className="px-4 mt-3">
        <div className="bg-white/5 border border-white/10 rounded-2xl p-3 space-y-1">
          <p className="text-white font-extrabold text-xs">📋 Exam Rules</p>
          <ul className="text-white/50 text-[11px] font-medium space-y-0.5">
            <li>• No hints or feedback during the test</li>
            <li>• Jump between questions freely · Flag for review</li>
            <li>• Full analytics shown after submission</li>
          </ul>
        </div>
      </div>

      {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold px-4 mt-2">{error}</p>}

      {/* Start CTA */}
      <div className="px-4 mt-4">
        <DuoButton variant="green" fullWidth loading={loading} onClick={handleStart}>
          Start {opt.label} {opt.emoji}
        </DuoButton>
      </div>

      {/* ── Section: Previous Year Papers ──────────────────────────────────── */}
      <div className="px-4 mt-6">
        <div className="flex items-center gap-2 mb-3">
          <p className="text-xs font-extrabold text-white/40 uppercase tracking-widest">
            Previous Year Papers
          </p>
          {!isGrade4 && (
            <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
              Grade 4 only
            </span>
          )}
        </div>
        <div className="grid grid-cols-2 gap-3">
          {PYQ_YEARS.map(({ year, label, subtitle, color }) => (
            <button
              key={year}
              onClick={() => isGrade4 && handlePYQ(year)}
              disabled={pyqLoading !== null || !isGrade4}
              className={`relative bg-gradient-to-br ${color} rounded-2xl p-4 text-left transition-all duration-150 min-h-[100px] flex flex-col justify-between ${
                isGrade4 ? 'active:scale-[0.97] disabled:opacity-60' : 'opacity-40 cursor-not-allowed'
              }`}
            >
              <div>
                <p className="text-white font-extrabold text-base leading-tight">{label}</p>
                <p className="text-white/70 text-xs font-semibold mt-1">{subtitle}</p>
              </div>
              <div className="flex items-center justify-between mt-3">
                {isGrade4 ? (
                  <>
                    <span className="text-white/80 text-xs font-bold">Original order</span>
                    {pyqLoading === year ? (
                      <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                      <span className="text-white/70 text-sm">→</span>
                    )}
                  </>
                ) : (
                  <span className="text-white/60 text-xs font-bold">Grade 4 students only</span>
                )}
              </div>
            </button>
          ))}
        </div>
        <p className="text-white/30 text-[11px] text-center mt-2 font-medium">
          {isGrade4
            ? 'Actual questions from 2016–2019 IPM papers · In original exam order'
            : 'IPM past papers are for Grade 4 students · Practice with synthetic papers above'}
        </p>
      </div>

      {/* ── Section: Mega Final ─────────────────────────────────────────────── */}
      <div className="px-4 mt-6">
        <div className="flex items-center gap-2 mb-3">
          <p className="text-xs font-extrabold text-white/40 uppercase tracking-widest">
            Mega Final Experience
          </p>
        </div>

        {/* Timed Mega Final card */}
        <div className="relative mb-3">
          <div className={`bg-gradient-to-br from-[#1a2040] to-[#0d1a20] border-2 ${IS_MEGA_ACCESSIBLE ? 'border-[#9B59B6]' : 'border-white/10'} rounded-2xl p-4 space-y-3`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="text-2xl">🏆</span>
                <div>
                  <p className="text-white font-extrabold text-sm leading-tight">THE ULTIMATE CHALLENGE</p>
                  <p className="text-white/50 text-[11px]">Full Mega Mock · 15 Qs · 45 min</p>
                </div>
              </div>
              <span className="text-[9px] font-bold px-2 py-1 rounded-full bg-[#9B59B6]/20 text-[#9B59B6] border border-[#9B59B6]/30 shrink-0">
                PRO
              </span>
            </div>
            <div className="space-y-1">
              <p className="text-white/50 text-[11px]">✦ Grade {studentGrade}-specific · Hard difficulty only</p>
              <p className="text-white/50 text-[11px]">✦ No repeats · No hints · Full simulation</p>
              <p className="text-white/50 text-[11px]">✦ Detailed performance report after</p>
            </div>
            <DuoButton variant="green" fullWidth loading={megaLoading} onClick={handleMega}>
              Begin Mega Final 🚀
            </DuoButton>
          </div>

          {/* Frosted overlay for non-subscribers */}
          {!IS_MEGA_ACCESSIBLE && (
            <div
              className="absolute inset-0 rounded-2xl flex flex-col items-center justify-center"
              style={{ backdropFilter: 'blur(6px)', background: 'rgba(13,26,32,0.75)' }}
            >
              <span className="text-3xl mb-2">🔒</span>
              <p className="text-white font-extrabold text-sm mb-1">Pro Feature</p>
              <p className="text-white/55 text-xs mb-3 text-center px-8">Start your free trial to unlock the Ultimate Challenge</p>
              <button
                onClick={() => router.push('/pricing')}
                className="bg-[#FF9600] border-b-[3px] border-[#cc7800] text-white font-extrabold px-5 py-2 rounded-2xl text-xs active:translate-y-[2px] active:border-b-0 transition-all"
              >
                Unlock with Pro Trial →
              </button>
            </div>
          )}
        </div>

        {/* Untimed Challenge card */}
        <div className="relative">
          <div className={`bg-white/5 border ${IS_MEGA_ACCESSIBLE ? 'border-white/20' : 'border-white/5'} rounded-2xl p-4`}>
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="text-white font-extrabold text-sm">MEGA CHALLENGE MODE</p>
                <p className="text-white/40 text-[11px]">Untimed · Random hard questions</p>
              </div>
              <span className="text-[9px] font-bold px-2 py-1 rounded-full bg-[#9B59B6]/20 text-[#9B59B6] border border-[#9B59B6]/30 shrink-0">
                PRO
              </span>
            </div>
            <DuoButton variant="blue" fullWidth loading={false} onClick={handleMega}>
              Start Challenge ⚡
            </DuoButton>
          </div>

          {!IS_MEGA_ACCESSIBLE && (
            <div
              className="absolute inset-0 rounded-2xl"
              style={{ backdropFilter: 'blur(4px)', background: 'rgba(13,26,32,0.6)' }}
            />
          )}
        </div>
      </div>

      {/* View history link */}
      <div className="px-4 mt-4">
        <button
          onClick={() => router.push('/test/history')}
          className="w-full text-white/40 text-sm font-semibold text-center py-2 hover:text-white/70 transition-colors"
        >
          View past tests →
        </button>
      </div>
    </div>
  );
}

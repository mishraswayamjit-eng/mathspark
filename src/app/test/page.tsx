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
    color: 'bg-purple-50',
    border: 'border-purple-400',
  },
  {
    type: 'full',
    label: 'Full Paper',
    emoji: '🏆',
    questions: 50,
    time: '60 min',
    desc: 'Extended paper — all 16 topics, max challenge',
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
  const [selected,   setSelected]   = useState<TestType>('ipm');
  const [loading,    setLoading]    = useState(false);
  const [pyqLoading, setPyqLoading] = useState<PYQYear | null>(null);
  const [error,      setError]      = useState('');
  const [studentId,  setStudentId]  = useState<string | null>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);
  }, [router]);

  // Start a synthetic test (quick / half / ipm / full)
  async function handleStart() {
    if (!studentId) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ studentId, type: selected }),
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
            <h1 className="text-2xl font-extrabold text-white">IPM Mock Test</h1>
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
          {TEST_OPTIONS.map((o) => (
            <button
              key={o.type}
              onClick={() => setSelected(o.type)}
              className={`w-full text-left rounded-2xl p-4 border-2 transition-all duration-150 active:scale-[0.97] ${
                selected === o.type
                  ? `${o.color} ${o.border} shadow-md`
                  : 'bg-white/10 border-white/10 hover:border-white/30'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{o.emoji}</span>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className={`font-extrabold text-sm ${selected === o.type ? 'text-gray-800' : 'text-white'}`}>
                      {o.label}
                    </span>
                    <div className="flex items-center gap-1.5">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        selected === o.type ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                      }`}>{o.questions} Qs</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        selected === o.type ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                      }`}>{o.time}</span>
                    </div>
                  </div>
                  <p className={`text-xs mt-0.5 font-medium ${selected === o.type ? 'text-gray-600' : 'text-white/40'}`}>
                    {o.desc}
                  </p>
                </div>
                {selected === o.type && <span className="text-[#58CC02] text-base ml-1">✓</span>}
              </div>
            </button>
          ))}
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
        <p className="text-xs font-extrabold text-white/40 uppercase tracking-widest mb-3">
          Previous Year Papers
        </p>
        <div className="grid grid-cols-2 gap-3">
          {PYQ_YEARS.map(({ year, label, subtitle, color }) => (
            <button
              key={year}
              onClick={() => handlePYQ(year)}
              disabled={pyqLoading !== null}
              className={`relative bg-gradient-to-br ${color} rounded-2xl p-4 text-left active:scale-[0.97] transition-all duration-150 disabled:opacity-60 min-h-[100px] flex flex-col justify-between`}
            >
              <div>
                <p className="text-white font-extrabold text-base leading-tight">{label}</p>
                <p className="text-white/70 text-xs font-semibold mt-1">{subtitle}</p>
              </div>
              <div className="flex items-center justify-between mt-3">
                <span className="text-white/80 text-xs font-bold">Original order</span>
                {pyqLoading === year ? (
                  <span className="inline-block w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <span className="text-white/70 text-sm">→</span>
                )}
              </div>
            </button>
          ))}
        </div>
        <p className="text-white/30 text-[11px] text-center mt-2 font-medium">
          Actual questions from 2016–2019 IPM papers · In original exam order
        </p>
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

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DuoButton from '@/components/DuoButton';
import Sparky from '@/components/Sparky';
import type { TestType } from '@/types';

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
    type: 'full',
    label: 'Full IPM Paper',
    emoji: '🏆',
    questions: 50,
    time: '60 min',
    desc: 'Complete exam simulation — all topics',
    color: 'bg-green-50',
    border: 'border-[#58CC02]',
  },
];

export default function TestConfigPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<TestType>('full');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');
  const [studentId, setStudentId] = useState<string | null>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);
  }, [router]);

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

  const opt = TEST_OPTIONS.find((o) => o.type === selected)!;

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col pb-24">
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

      {/* Test type picker */}
      <div className="px-4 space-y-3">
        {TEST_OPTIONS.map((opt) => (
          <button
            key={opt.type}
            onClick={() => setSelected(opt.type)}
            className={`w-full text-left rounded-2xl p-4 border-2 transition-all duration-150 active:scale-[0.97] ${
              selected === opt.type
                ? `${opt.color} ${opt.border} shadow-md`
                : 'bg-white/10 border-white/10 hover:border-white/30'
            }`}
          >
            <div className="flex items-center gap-3">
              <span className="text-3xl">{opt.emoji}</span>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className={`font-extrabold text-base ${selected === opt.type ? 'text-gray-800' : 'text-white'}`}>
                    {opt.label}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                      selected === opt.type ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                    }`}>
                      {opt.questions} Qs
                    </span>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                      selected === opt.type ? 'bg-white/60 text-gray-700' : 'bg-white/10 text-white/70'
                    }`}>
                      {opt.time}
                    </span>
                  </div>
                </div>
                <p className={`text-sm mt-0.5 font-medium ${selected === opt.type ? 'text-gray-600' : 'text-white/50'}`}>
                  {opt.desc}
                </p>
              </div>
              {selected === opt.type && (
                <span className="text-[#58CC02] text-xl">✓</span>
              )}
            </div>
          </button>
        ))}
      </div>

      {/* Rules callout */}
      <div className="px-4 mt-4">
        <div className="bg-white/5 border border-white/10 rounded-2xl p-4 space-y-2">
          <p className="text-white font-extrabold text-sm">📋 Exam Rules</p>
          <ul className="text-white/60 text-xs font-medium space-y-1">
            <li>• No hints or feedback during the test</li>
            <li>• You can jump between questions freely</li>
            <li>• Flag questions to review before submitting</li>
            <li>• Full analysis shown after submission</li>
          </ul>
        </div>
      </div>

      {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold px-4 mt-2">{error}</p>}

      {/* CTA */}
      <div className="px-4 mt-6">
        <DuoButton variant="green" fullWidth loading={loading} onClick={handleStart}>
          Start {opt.label} {opt.emoji}
        </DuoButton>
        <button
          onClick={() => router.push('/test/history')}
          className="w-full mt-3 text-white/50 text-sm font-semibold text-center py-2 hover:text-white/80 transition-colors"
        >
          View past tests →
        </button>
      </div>
    </div>
  );
}

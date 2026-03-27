'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

// ── Types ────────────────────────────────────────────────────────────────────

interface PaperMeta {
  paperId: string;
  title: string;
  grade: number;
  duration: number;
  totalQuestions: number;
  totalMarks: number;
  variantNumber: number;
  difficultyDistribution: {
    easy: number; medium: number; hard: number;
    easyPercent: number; mediumPercent: number; hardPercent: number;
  };
  topicsCovered: string[];
}

const DURATIONS = [
  { value: 15, label: '15 min', emoji: '⚡', desc: 'Quick Practice', color: '#1CB0F6' },
  { value: 30, label: '30 min', emoji: '📝', desc: 'Practice Paper', color: '#FF9600' },
  { value: 60, label: '60 min', emoji: '🏆', desc: 'IPM Mock Exam', color: '#FF4B4B' },
];

const GRADES = [2, 3, 4, 5, 6, 7, 8, 9];

// ── Page ─────────────────────────────────────────────────────────────────────

export default function PaperSelectionPage() {
  const [papers, setPapers] = useState<PaperMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [grade, setGrade] = useState(6);
  const [duration, setDuration] = useState(30);

  // Load student grade
  useEffect(() => {
    fetch('/api/student')
      .then((r) => r.ok ? r.json() : null)
      .then((s) => { if (s?.grade) setGrade(s.grade); })
      .catch((err) => console.error('[fetch]', err));
  }, []);

  // Load papers for selected grade
  useEffect(() => {
    setLoading(true);
    fetch(`/api/papers?grade=${grade}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d) => setPapers(d.papers ?? []))
      .catch(() => setPapers([]))
      .finally(() => setLoading(false));
  }, [grade]);

  const filtered = papers.filter((p) => p.duration === duration);
  const durInfo = DURATIONS.find((d) => d.value === duration)!;

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="bg-duo-dark px-4 py-4">
        <div className="max-w-lg mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-white font-extrabold text-lg">Exam Papers</h1>
            <p className="text-white/70 text-xs font-medium">240 pre-built practice papers</p>
          </div>
          <Link
            href="/home"
            className="text-white/60 text-sm font-bold hover:text-white transition-colors"
          >
            ← Home
          </Link>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
        {/* Grade selector */}
        <div>
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-2">Grade</p>
          <div className="flex gap-2 flex-wrap">
            {GRADES.map((g) => (
              <button
                key={g}
                onClick={() => setGrade(g)}
                className={`px-4 py-2 rounded-full text-sm font-extrabold transition-colors ${
                  g === grade
                    ? 'bg-duo-blue text-white shadow-md'
                    : 'bg-white text-gray-600 border border-gray-200 hover:border-duo-blue'
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* Duration tabs */}
        <div>
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-2">Format</p>
          <div className="grid grid-cols-3 gap-2">
            {DURATIONS.map((d) => (
              <button
                key={d.value}
                onClick={() => setDuration(d.value)}
                className={`rounded-2xl p-3 text-center transition-colors border-2 ${
                  d.value === duration
                    ? 'border-current shadow-md'
                    : 'border-transparent bg-white shadow-sm hover:shadow-md'
                }`}
                style={d.value === duration ? { borderColor: d.color, backgroundColor: `${d.color}10` } : {}}
              >
                <span className="text-2xl block">{d.emoji}</span>
                <p className="text-xs font-extrabold text-gray-800 mt-1">{d.desc}</p>
                <p className="text-[10px] text-gray-500 font-semibold">{d.label}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Paper list */}
        {loading ? (
          <div className="flex flex-col items-center py-12 gap-3">
            <Sparky mood="thinking" size={56} />
            <p className="text-sm text-gray-500 font-bold animate-pulse">Loading papers...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center py-12 gap-3">
            <Sparky mood="thinking" size={56} />
            <p className="text-sm text-gray-500 font-bold">No papers available for this combination.</p>
          </div>
        ) : (
          <div className="space-y-3">
            <p className="text-xs font-bold text-gray-500">
              {filtered.length} {filtered.length === 1 ? 'paper' : 'papers'} available
            </p>
            {filtered.map((paper) => (
              <Link
                key={paper.paperId}
                href={`/practice/papers/${paper.paperId}`}
                className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-xl font-extrabold text-white shrink-0"
                    style={{ backgroundColor: durInfo.color }}
                  >
                    {durInfo.emoji}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-extrabold text-gray-800 truncate">{paper.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[10px] font-bold text-gray-500">
                        {paper.totalQuestions} Qs
                      </span>
                      <span className="text-gray-300">·</span>
                      <span className="text-[10px] font-bold text-gray-500">
                        {paper.duration} min
                      </span>
                      <span className="text-gray-300">·</span>
                      <span className="text-[10px] font-bold text-gray-500">
                        {paper.totalMarks} marks
                      </span>
                    </div>
                    {/* Difficulty bar */}
                    <div className="flex h-1.5 rounded-full overflow-hidden mt-2 bg-gray-100">
                      <div
                        className="bg-duo-green"
                        style={{ width: `${paper.difficultyDistribution.easyPercent}%` }}
                      />
                      <div
                        className="bg-duo-orange"
                        style={{ width: `${paper.difficultyDistribution.mediumPercent}%` }}
                      />
                      <div
                        className="bg-duo-red"
                        style={{ width: `${paper.difficultyDistribution.hardPercent}%` }}
                      />
                    </div>
                  </div>
                  <span className="text-gray-300 text-lg shrink-0">→</span>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Legend */}
        <div className="flex items-center gap-4 justify-center pt-2">
          <span className="flex items-center gap-1 text-[10px] font-bold text-gray-500">
            <span className="w-2 h-2 rounded-full bg-duo-green" /> Easy
          </span>
          <span className="flex items-center gap-1 text-[10px] font-bold text-gray-500">
            <span className="w-2 h-2 rounded-full bg-duo-orange" /> Medium
          </span>
          <span className="flex items-center gap-1 text-[10px] font-bold text-gray-500">
            <span className="w-2 h-2 rounded-full bg-duo-red" /> Hard
          </span>
        </div>

        {/* Negative marking notice for 60-min */}
        {duration === 60 && (
          <div className="bg-red-50 border border-red-200 rounded-2xl px-4 py-3 flex items-start gap-3">
            <span className="text-lg shrink-0">⚠️</span>
            <div>
              <p className="text-xs font-extrabold text-red-700">IPM Format — Negative Marking</p>
              <p className="text-xs text-red-600 mt-0.5">
                -0.25 marks for each wrong answer. Leave blank if unsure!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

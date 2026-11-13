'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

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
  { value: 15, label: '15 min', emoji: '⚡', desc: 'Quick Practice', color: '#4f46e5' },
  { value: 30, label: '30 min', emoji: '📝', desc: 'Practice Paper', color: '#4f46e5' },
  { value: 60, label: '60 min', emoji: '🏆', desc: 'IPM Mock Exam', color: '#4f46e5' },
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
      .catch((err) => logError('[fetch]', err));
  }, []);

  // Load papers for selected grade
  useEffect(() => {
    setLoading(true);
    fetch(`/api/papers?grade=${grade}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d) => setPapers(d.papers ?? []))
      .catch((err) => { logError('[papers] fetch papers', err); setPapers([]); })
      .finally(() => setLoading(false));
  }, [grade]);

  const filtered = papers.filter((p) => p.duration === duration);
  const durInfo = DURATIONS.find((d) => d.value === duration)!;

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="bg-ink px-4 py-4">
        <div className="max-w-lg mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-white text-title">Exam Papers</h1>
            <p className="text-white/70 text-xs font-medium">240 pre-built practice papers</p>
          </div>
          <Link
            href="/home"
            className="text-white/70 text-sm font-bold hover:text-white transition-colors"
          >
            ← Home
          </Link>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
        {/* Grade selector */}
        <div>
          <p className="text-caption text-ink-muted mb-2">Grade</p>
          <div className="flex gap-2 flex-wrap">
            {GRADES.map((g) => (
              <button
                key={g}
                onClick={() => setGrade(g)}
                className={`px-4 py-2 rounded-full text-sm font-extrabold transition-colors ${
                  g === grade
                    ? 'bg-action text-white border-2 border-action'
                    : 'bg-white text-ink border-2 border-line hover:border-ink'
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* Duration tabs */}
        <div>
          <p className="text-caption text-ink-muted mb-2">Format</p>
          <div className="grid grid-cols-3 gap-2">
            {DURATIONS.map((d) => (
              <button
                key={d.value}
                onClick={() => setDuration(d.value)}
                className={`rounded-control p-3 text-center transition-colors border-2 ${
                  d.value === duration
                    ? 'border-current'
                    : 'border-line bg-white hover:border-ink'
                }`}
                style={d.value === duration ? { borderColor: d.color, backgroundColor: `${d.color}10` } : {}}
              >
                <span className="text-2xl block">{d.emoji}</span>
                <p className="text-xs font-extrabold text-ink mt-1">{d.desc}</p>
                <p className="text-xs text-ink-muted font-semibold">{d.label}</p>
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
                className="block bg-white rounded-card p-4 border-2 border-line hover:border-ink transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-tile flex items-center justify-center text-xl font-extrabold text-white shrink-0"
                    style={{ backgroundColor: durInfo.color }}
                  >
                    {durInfo.emoji}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-extrabold text-ink truncate">{paper.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs font-bold text-ink-muted">
                        {paper.totalQuestions} Qs
                      </span>
                      <span className="text-gray-300">·</span>
                      <span className="text-xs font-bold text-ink-muted">
                        {paper.duration} min
                      </span>
                      <span className="text-gray-300">·</span>
                      <span className="text-xs font-bold text-ink-muted">
                        {paper.totalMarks} marks
                      </span>
                    </div>
                    {/* Difficulty bar */}
                    <div className="flex h-1.5 rounded-full overflow-hidden mt-2 bg-soft">
                      <div
                        className="bg-success"
                        style={{ width: `${paper.difficultyDistribution.easyPercent}%` }}
                      />
                      <div
                        className="bg-star"
                        style={{ width: `${paper.difficultyDistribution.mediumPercent}%` }}
                      />
                      <div
                        className="bg-retry"
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
          <span className="flex items-center gap-1 text-xs font-bold text-ink-muted">
            <span className="w-2 h-2 rounded-full bg-success" /> Easy
          </span>
          <span className="flex items-center gap-1 text-xs font-bold text-ink-muted">
            <span className="w-2 h-2 rounded-full bg-star" /> Medium
          </span>
          <span className="flex items-center gap-1 text-xs font-bold text-ink-muted">
            <span className="w-2 h-2 rounded-full bg-retry" /> Hard
          </span>
        </div>

        {/* Negative marking notice for 60-min */}
        {duration === 60 && (
          <div className="bg-hint border-2 border-hint-ink/30 rounded-card px-4 py-3 flex items-start gap-3">
            <span className="text-lg shrink-0">⚠️</span>
            <div>
              <p className="text-xs font-extrabold text-hint-ink">IPM Format — Negative Marking</p>
              <p className="text-xs font-bold text-hint-ink mt-0.5">
                -0.25 marks for each wrong answer. Leave blank if unsure!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

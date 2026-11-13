'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Strategy {
  id: string;
  category: string;
  name: string;
  emoji: string;
  description: string;
  whenToUse: string;
  howItWorks: string;
  example: {
    scenario: string;
    action: string;
    result: string;
  };
  sparkyTip: string;
  difficulty: number;
  gradeRange: number[];
  tags: string[];
  estimatedTimeSaved: string;
}

// ── Category metadata ─────────────────────────────────────────────────────────

const CATEGORY_META: Record<string, { emoji: string; label: string; color: string; description: string }> = {
  time_management:    { emoji: '⏱️', label: 'Time Management',    color: '#3B82F6', description: 'Use your exam time wisely' },
  elimination:        { emoji: '✂️', label: 'Elimination',         color: '#EF4444', description: 'Narrow down the options' },
  estimation:         { emoji: '🎯', label: 'Estimation',          color: '#F59E0B', description: 'Quick approximate answers' },
  pattern_recognition:{ emoji: '🔍', label: 'Pattern Recognition', color: '#8B5CF6', description: 'Spot the question type fast' },
  negative_marking:   { emoji: '⚠️', label: 'Negative Marking',    color: '#DC2626', description: 'Protect your score' },
  speed_tricks:       { emoji: '⚡', label: 'Speed Tricks',        color: '#F97316', description: 'Calculate faster' },
  trap_avoidance:     { emoji: '🛡️', label: 'Trap Avoidance',      color: '#059669', description: 'Avoid common mistakes' },
  stress_management:  { emoji: '🧘', label: 'Stress Management',   color: '#6366F1', description: 'Stay calm and focused' },
};

function getCategoryMeta(cat: string) {
  return CATEGORY_META[cat] ?? { emoji: '📘', label: cat.replace(/_/g, ' '), color: '#94A3B8', description: '' };
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function StrategyBankPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (selectedCategory) params.set('category', selectedCategory);
    params.set('grade', localStorage.getItem('mathspark_student_grade') || '4');
    setLoading(true);
    fetch(`/api/strategies?${params.toString()}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setStrategies(data.strategies ?? []);
      })
      .catch((err) => logError('[fetch]', err))
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  // Group strategies by category
  const grouped = new Map<string, Strategy[]>();
  for (const s of strategies) {
    const list = grouped.get(s.category);
    if (list) list.push(s);
    else grouped.set(s.category, [s]);
  }

  const categories = Object.keys(CATEGORY_META);

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/chapters" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Strategy Bank</h1>
          <p className="text-white/70 text-xs font-medium">{strategies.length} exam strategies &middot; Solve like a topper!</p>
        </div>
        <span className="text-2xl">🧠</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">These aren&apos;t just math tricks...</p>
            <p className="text-xs text-ink-muted mt-0.5">
              They&apos;re exam strategies that toppers use. Each one can save you minutes!
            </p>
          </div>
        </div>

        {/* Category filter */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1 flex-wrap">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors ${
              selectedCategory === null
                ? 'bg-action text-white border-action'
                : 'bg-white text-ink border-line'
            }`}
          >
            All ({strategies.length || 35})
          </button>
          {categories.map((cat) => {
            const meta = getCategoryMeta(cat);
            const isActive = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors flex items-center gap-1 ${
                  isActive
                    ? 'text-white border-transparent'
                    : 'bg-white text-ink border-line'
                }`}
                style={isActive ? { backgroundColor: meta.color, borderColor: meta.color } : {}}
              >
                <span>{meta.emoji}</span>
                <span>{meta.label}</span>
              </button>
            );
          })}
        </div>

        {/* Loading */}
        {loading && (
          <div className="space-y-3">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-24" />
            ))}
          </div>
        )}

        {/* Strategy cards grouped by category */}
        {!loading && (
          <div className="space-y-6">
            {Array.from(grouped.entries()).map(([category, categoryStrategies]) => {
              const meta = getCategoryMeta(category);
              return (
                <div key={category}>
                  {/* Category header */}
                  {!selectedCategory && (
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-lg">{meta.emoji}</span>
                      <div>
                        <h2 className="text-title text-ink">{meta.label}</h2>
                        <p className="text-xs text-ink-muted font-medium">{meta.description}</p>
                      </div>
                      <span className="ml-auto text-xs font-bold text-ink-muted bg-soft rounded-full px-2 py-0.5">
                        {categoryStrategies.length}
                      </span>
                    </div>
                  )}

                  {/* Strategy cards */}
                  <div className="space-y-3">
                    {categoryStrategies.map((s) => {
                      const isExpanded = expandedId === s.id;
                      return (
                        <div
                          key={s.id}
                          className="bg-white rounded-card border-2 border-line overflow-hidden"
                          style={{ borderLeftWidth: '4px', borderLeftColor: meta.color }}
                        >
                          {/* Collapsed header */}
                          <button
                            onClick={() => setExpandedId(isExpanded ? null : s.id)}
                            className="w-full px-4 py-3.5 flex items-center gap-3 text-left active:bg-soft transition-colors"
                          >
                            <span className="text-xl shrink-0">{s.emoji}</span>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-extrabold text-ink leading-tight">{s.name}</p>
                              <p className="text-xs text-ink-muted font-medium mt-0.5 line-clamp-1">{s.description}</p>
                            </div>
                            <div className="flex items-center gap-2 shrink-0">
                              {s.estimatedTimeSaved && (
                                <span className="text-xs font-bold text-ink bg-soft px-2 py-0.5 rounded-full hidden sm:block">
                                  {s.estimatedTimeSaved}
                                </span>
                              )}
                              <span
                                className="text-ink-muted transition-transform duration-200 text-sm"
                                style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                              >
                                ▾
                              </span>
                            </div>
                          </button>

                          {/* Expanded detail */}
                          {isExpanded && (
                            <div className="px-4 pb-4 space-y-3 animate-fade-in">
                              {/* Divider */}
                              <div className="border-t-2 border-line" />

                              {/* When to use */}
                              <div className="flex items-start gap-2">
                                <span className="text-xs shrink-0 mt-0.5">🕐</span>
                                <div>
                                  <p className="text-[13px] font-extrabold text-ink-muted">When to Use</p>
                                  <p className="text-sm text-ink font-medium mt-0.5">{s.whenToUse}</p>
                                </div>
                              </div>

                              {/* How it works */}
                              <div className="flex items-start gap-2">
                                <span className="text-xs shrink-0 mt-0.5">⚙️</span>
                                <div>
                                  <p className="text-[13px] font-extrabold text-ink-muted">How It Works</p>
                                  <p className="text-sm text-ink font-medium mt-0.5 leading-relaxed">{s.howItWorks}</p>
                                </div>
                              </div>

                              {/* Example scenario */}
                              {s.example && (
                                <div className="bg-soft rounded-control p-3 border-2 border-line space-y-2">
                                  <p className="text-[13px] font-extrabold text-ink-muted">Example</p>
                                  <div className="space-y-1.5">
                                    <div className="flex items-start gap-2">
                                      <span className="text-xs text-ink-muted font-bold shrink-0 mt-0.5">Scenario:</span>
                                      <p className="text-[13px] text-ink font-medium">{s.example.scenario}</p>
                                    </div>
                                    <div className="flex items-start gap-2">
                                      <span className="text-xs text-ink-muted font-bold shrink-0 mt-0.5">Action:</span>
                                      <p className="text-[13px] text-ink font-medium">{s.example.action}</p>
                                    </div>
                                    <div className="flex items-start gap-2">
                                      <span className="text-xs text-ink-muted font-bold shrink-0 mt-0.5">Result:</span>
                                      <p className="text-[13px] text-ink font-bold">{s.example.result}</p>
                                    </div>
                                  </div>
                                </div>
                              )}

                              {/* Sparky tip */}
                              {s.sparkyTip && (
                                <div className="bg-soft rounded-control p-3 border-2 border-line flex items-start gap-2">
                                  <Sparky mood="happy" size={28} />
                                  <div>
                                    <p className="text-[13px] font-extrabold text-ink-muted">Sparky Says</p>
                                    <p className="text-[13px] text-ink font-medium mt-0.5 italic leading-snug">{s.sparkyTip}</p>
                                  </div>
                                </div>
                              )}

                              {/* Footer: time saved + difficulty + grade range */}
                              <div className="flex items-center gap-2 flex-wrap pt-1">
                                {s.estimatedTimeSaved && (
                                  <span className="text-xs font-bold text-ink bg-soft px-2 py-0.5 rounded-full border-2 border-line">
                                    Saves {s.estimatedTimeSaved}
                                  </span>
                                )}
                                <span className="text-xs font-bold text-ink-muted bg-soft px-2 py-0.5 rounded-full">
                                  {s.difficulty === 1 ? 'Beginner' : 'Advanced'}
                                </span>
                                <span className="text-xs font-bold text-ink-muted">
                                  Grades {s.gradeRange[0]}–{s.gradeRange[1]}
                                </span>
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Empty state */}
        {!loading && strategies.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-ink-muted">No strategies found.</p>
            <button
              onClick={() => setSelectedCategory(null)}
              className="text-sm text-action font-bold underline"
            >
              Show all
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

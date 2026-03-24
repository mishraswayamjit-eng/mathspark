'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

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
    const qs = selectedCategory ? `?category=${selectedCategory}` : '';
    setLoading(true);
    fetch(`/api/strategies${qs}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setStrategies(data.strategies ?? []);
      })
      .catch((err) => console.error('[fetch]', err))
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
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/chapters" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Strategy Bank</h1>
          <p className="text-white/70 text-xs font-medium">35 exam strategies &middot; Solve like a topper!</p>
        </div>
        <span className="text-2xl">🧠</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl px-4 py-3 border border-amber-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-amber-800">These aren&apos;t just math tricks...</p>
            <p className="text-xs text-amber-600 mt-0.5">
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
                ? 'bg-duo-dark text-white border-duo-dark'
                : 'bg-white text-gray-600 border-gray-200'
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
                    : 'bg-white text-gray-600 border-gray-200'
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
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-24" />
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
                        <h2 className="text-sm font-extrabold text-gray-800">{meta.label}</h2>
                        <p className="text-[10px] text-gray-500 font-medium">{meta.description}</p>
                      </div>
                      <span className="ml-auto text-[10px] font-bold text-gray-500 bg-gray-100 rounded-full px-2 py-0.5">
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
                          className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden transition-shadow"
                          style={{ borderLeftWidth: '4px', borderLeftColor: meta.color }}
                        >
                          {/* Collapsed header */}
                          <button
                            onClick={() => setExpandedId(isExpanded ? null : s.id)}
                            className="w-full px-4 py-3.5 flex items-center gap-3 text-left active:bg-gray-50 transition-colors"
                          >
                            <span className="text-xl shrink-0">{s.emoji}</span>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-extrabold text-gray-800 leading-tight">{s.name}</p>
                              <p className="text-xs text-gray-500 font-medium mt-0.5 line-clamp-1">{s.description}</p>
                            </div>
                            <div className="flex items-center gap-2 shrink-0">
                              {s.estimatedTimeSaved && (
                                <span className="text-[10px] font-bold text-duo-green bg-green-50 px-2 py-0.5 rounded-full hidden sm:block">
                                  {s.estimatedTimeSaved}
                                </span>
                              )}
                              <span
                                className="text-gray-500 transition-transform duration-200 text-sm"
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
                              <div className="border-t border-gray-100" />

                              {/* When to use */}
                              <div className="flex items-start gap-2">
                                <span className="text-xs shrink-0 mt-0.5">🕐</span>
                                <div>
                                  <p className="text-[10px] font-extrabold text-gray-500 uppercase tracking-wide">When to Use</p>
                                  <p className="text-sm text-gray-700 font-medium mt-0.5">{s.whenToUse}</p>
                                </div>
                              </div>

                              {/* How it works */}
                              <div className="flex items-start gap-2">
                                <span className="text-xs shrink-0 mt-0.5">⚙️</span>
                                <div>
                                  <p className="text-[10px] font-extrabold text-gray-500 uppercase tracking-wide">How It Works</p>
                                  <p className="text-sm text-gray-700 font-medium mt-0.5 leading-relaxed">{s.howItWorks}</p>
                                </div>
                              </div>

                              {/* Example scenario */}
                              {s.example && (
                                <div className="bg-blue-50 rounded-xl p-3 border border-blue-200 space-y-2">
                                  <p className="text-[10px] font-extrabold text-blue-500 uppercase tracking-wide">Example</p>
                                  <div className="space-y-1.5">
                                    <div className="flex items-start gap-2">
                                      <span className="text-[10px] text-blue-400 font-bold shrink-0 mt-0.5">Scenario:</span>
                                      <p className="text-xs text-blue-800 font-medium">{s.example.scenario}</p>
                                    </div>
                                    <div className="flex items-start gap-2">
                                      <span className="text-[10px] text-blue-400 font-bold shrink-0 mt-0.5">Action:</span>
                                      <p className="text-xs text-blue-800 font-medium">{s.example.action}</p>
                                    </div>
                                    <div className="flex items-start gap-2">
                                      <span className="text-[10px] text-duo-green font-bold shrink-0 mt-0.5">Result:</span>
                                      <p className="text-xs text-green-700 font-semibold">{s.example.result}</p>
                                    </div>
                                  </div>
                                </div>
                              )}

                              {/* Sparky tip */}
                              {s.sparkyTip && (
                                <div className="bg-purple-50 rounded-xl p-3 border border-purple-200 flex items-start gap-2">
                                  <Sparky mood="happy" size={28} />
                                  <div>
                                    <p className="text-[10px] font-extrabold text-purple-500 uppercase tracking-wide">Sparky Says</p>
                                    <p className="text-xs text-purple-800 font-medium mt-0.5 italic leading-snug">{s.sparkyTip}</p>
                                  </div>
                                </div>
                              )}

                              {/* Footer: time saved + difficulty + grade range */}
                              <div className="flex items-center gap-2 flex-wrap pt-1">
                                {s.estimatedTimeSaved && (
                                  <span className="text-[10px] font-bold text-duo-green bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                                    Saves {s.estimatedTimeSaved}
                                  </span>
                                )}
                                <span className="text-[10px] font-bold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                                  {s.difficulty === 1 ? 'Beginner' : 'Advanced'}
                                </span>
                                <span className="text-[10px] font-bold text-gray-500">
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
            <p className="text-sm font-bold text-gray-500">No strategies found.</p>
            <button
              onClick={() => setSelectedCategory(null)}
              className="text-sm text-blue-500 underline"
            >
              Show all
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

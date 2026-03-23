'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

// ── Types ─────────────────────────────────────────────────────────────────────

interface MistakePattern {
  id: string;
  name: string;
  emoji: string;
  category: string;
  description: string;
  whyItHappens: string;
  howToFix: string;
  example: {
    question: string;
    wrongAnswer: string;
    rightAnswer: string;
    wrongThinking: string;
    rightThinking: string;
  } | null;
  frequency: string;
  affectedTopics: string[];
  affectedGrades: number[];
  sparkyMessage: string;
  difficulty: number;
}

// ── Category metadata ─────────────────────────────────────────────────────────

const CATEGORY_META: Record<string, { emoji: string; label: string; color: string }> = {
  wrong_formula:      { emoji: '📝', label: 'Wrong Formula',      color: '#EF4444' },
  procedural_error:   { emoji: '🔄', label: 'Procedural Error',   color: '#F97316' },
  order_of_operations:{ emoji: '🔢', label: 'Order of Ops',       color: '#EAB308' },
  sign_error:         { emoji: '➖', label: 'Sign Error',          color: '#8B5CF6' },
  wrong_operation:    { emoji: '✖️', label: 'Wrong Operation',     color: '#3B82F6' },
  wrong_base:         { emoji: '🎯', label: 'Wrong Base',          color: '#14B8A6' },
  conceptual_error:   { emoji: '💭', label: 'Conceptual Error',    color: '#EC4899' },
  missing_step:       { emoji: '⏭️', label: 'Missing Step',        color: '#F59E0B' },
  notation_error:     { emoji: '✏️', label: 'Notation Error',      color: '#6366F1' },
  reading_error:      { emoji: '👀', label: 'Reading Error',       color: '#059669' },
  missing_knowledge:  { emoji: '❓', label: 'Missing Knowledge',   color: '#78716C' },
  unit_error:         { emoji: '📏', label: 'Unit Error',          color: '#0EA5E9' },
};

function getCatMeta(cat: string) {
  return CATEGORY_META[cat] ?? { emoji: '⚠️', label: cat.replace(/_/g, ' '), color: '#94A3B8' };
}

// ── Frequency badge ───────────────────────────────────────────────────────────

function FrequencyBadge({ freq }: { freq: string }) {
  const config: Record<string, { color: string; bg: string }> = {
    'Very High': { color: '#DC2626', bg: '#FEE2E2' },
    'High':      { color: '#EA580C', bg: '#FFF7ED' },
    'Medium':    { color: '#CA8A04', bg: '#FEF9C3' },
    'Low':       { color: '#16A34A', bg: '#DCFCE7' },
  };
  const c = config[freq] ?? { color: '#6B7280', bg: '#F3F4F6' };
  return (
    <span
      className="text-[9px] font-extrabold px-1.5 py-0.5 rounded-full"
      style={{ color: c.color, backgroundColor: c.bg }}
    >
      {freq}
    </span>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function MistakePatternsPage() {
  const [patterns, setPatterns] = useState<MistakePattern[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showRight, setShowRight] = useState<Set<string>>(new Set());

  useEffect(() => {
    const qs = selectedCategory ? `?category=${selectedCategory}` : '';
    setLoading(true);
    fetch(`/api/mistake-patterns${qs}`)
      .then((r) => r.json())
      .then((data) => setPatterns(data.patterns ?? []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  function toggleRight(id: string) {
    setShowRight((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }

  const categories = Object.keys(CATEGORY_META);

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/home" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Mistake Patterns</h1>
          <p className="text-white/50 text-xs font-medium">50 traps &middot; Learn from common errors!</p>
        </div>
        <span className="text-2xl">🚨</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-2xl px-4 py-3 border border-red-200 mb-5 flex items-start gap-3">
          <Sparky mood="thinking" size={36} />
          <div>
            <p className="text-sm font-bold text-red-800">Everyone makes mistakes — toppers learn from them!</p>
            <p className="text-xs text-red-600 mt-0.5">
              These 50 patterns are the most common traps in math exams. Know them = avoid them!
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
            All ({patterns.length || 50})
          </button>
          {categories.map((cat) => {
            const meta = getCatMeta(cat);
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
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-28" />
            ))}
          </div>
        )}

        {/* Pattern cards */}
        {!loading && (
          <div className="space-y-3">
            {patterns.map((pattern) => {
              const catMeta = getCatMeta(pattern.category);
              const isExpanded = expandedId === pattern.id;
              const rightShown = showRight.has(pattern.id);

              return (
                <div
                  key={pattern.id}
                  className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
                  style={{ borderLeftWidth: '4px', borderLeftColor: catMeta.color }}
                >
                  {/* Card header */}
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : pattern.id)}
                    className="w-full px-4 py-3.5 flex items-center gap-3 text-left active:bg-gray-50 transition-colors"
                  >
                    <span className="text-2xl shrink-0">{pattern.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 mb-0.5">
                        <span
                          className="text-[9px] font-extrabold px-1.5 py-0.5 rounded-full text-white"
                          style={{ backgroundColor: catMeta.color }}
                        >
                          {catMeta.label}
                        </span>
                        <FrequencyBadge freq={pattern.frequency} />
                      </div>
                      <p className="text-sm font-extrabold text-gray-800 leading-tight">{pattern.name}</p>
                      {!isExpanded && (
                        <p className="text-xs text-gray-400 font-medium mt-0.5 line-clamp-1">{pattern.description}</p>
                      )}
                    </div>
                    <span
                      className="text-gray-400 transition-transform duration-200 text-sm shrink-0"
                      style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                    >
                      ▾
                    </span>
                  </button>

                  {/* Expanded content */}
                  {isExpanded && (
                    <div className="px-4 pb-4 space-y-3 animate-fade-in">
                      <div className="border-t border-gray-100" />

                      {/* Description */}
                      <p className="text-sm text-gray-700 font-medium leading-relaxed">{pattern.description}</p>

                      {/* Why it happens */}
                      <div className="bg-red-50 rounded-xl p-3 border border-red-200">
                        <div className="flex items-start gap-2">
                          <span className="text-sm shrink-0">🤔</span>
                          <div>
                            <p className="text-[10px] font-extrabold text-red-500 uppercase tracking-wide">Why This Happens</p>
                            <p className="text-sm text-red-800 font-medium mt-0.5 leading-relaxed">{pattern.whyItHappens}</p>
                          </div>
                        </div>
                      </div>

                      {/* How to fix */}
                      <div className="bg-green-50 rounded-xl p-3 border border-green-200">
                        <div className="flex items-start gap-2">
                          <span className="text-sm shrink-0">✅</span>
                          <div>
                            <p className="text-[10px] font-extrabold text-green-600 uppercase tracking-wide">How to Fix It</p>
                            <p className="text-sm text-green-800 font-medium mt-0.5 leading-relaxed">{pattern.howToFix}</p>
                          </div>
                        </div>
                      </div>

                      {/* Example */}
                      {pattern.example && (
                        <div className="bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
                          <div className="px-3 pt-3 pb-2">
                            <p className="text-[10px] font-extrabold text-gray-500 uppercase tracking-wide mb-1.5">Example</p>
                            <p className="text-sm text-gray-800 font-semibold">{pattern.example.question}</p>
                          </div>

                          {/* Wrong answer */}
                          <div className="bg-red-50 px-3 py-2.5 border-t border-red-100">
                            <div className="flex items-start gap-2">
                              <span className="text-sm shrink-0">❌</span>
                              <div>
                                <p className="text-xs font-extrabold text-red-600">{pattern.example.wrongAnswer}</p>
                                <p className="text-[11px] text-red-500 font-medium mt-0.5 italic">{pattern.example.wrongThinking}</p>
                              </div>
                            </div>
                          </div>

                          {/* Right answer toggle */}
                          {!rightShown ? (
                            <button
                              onClick={(e) => { e.stopPropagation(); toggleRight(pattern.id); }}
                              className="w-full bg-green-50 px-3 py-2.5 border-t border-green-100 text-center"
                            >
                              <span className="text-xs font-bold text-green-600">Tap to see the right way →</span>
                            </button>
                          ) : (
                            <div className="bg-green-50 px-3 py-2.5 border-t border-green-100 animate-fade-in">
                              <div className="flex items-start gap-2">
                                <span className="text-sm shrink-0">✅</span>
                                <div>
                                  <p className="text-xs font-extrabold text-green-700">{pattern.example.rightAnswer}</p>
                                  <p className="text-[11px] text-green-600 font-medium mt-0.5 italic">{pattern.example.rightThinking}</p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Sparky's message */}
                      {pattern.sparkyMessage && (
                        <div className="bg-purple-50 rounded-xl p-3 border border-purple-200 flex items-start gap-2">
                          <Sparky mood="thinking" size={28} />
                          <div>
                            <p className="text-[10px] font-extrabold text-purple-500 uppercase tracking-wide">Sparky Says</p>
                            <p className="text-xs text-purple-800 font-medium mt-0.5 italic leading-snug">{pattern.sparkyMessage}</p>
                          </div>
                        </div>
                      )}

                      {/* Footer: topics + grades */}
                      <div className="space-y-2 pt-1">
                        {pattern.affectedTopics.length > 0 && (
                          <div className="flex items-start gap-1.5 flex-wrap">
                            <span className="text-[10px] font-bold text-gray-400 shrink-0">Topics:</span>
                            {pattern.affectedTopics.map((t) => (
                              <span key={t} className="text-[9px] font-bold text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded-full">
                                {t}
                              </span>
                            ))}
                          </div>
                        )}
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold text-gray-400">
                            Grades {pattern.affectedGrades[0]}–{pattern.affectedGrades[pattern.affectedGrades.length - 1]}
                          </span>
                          <span className="text-[10px] font-bold text-gray-400">
                            Difficulty: {'⭐'.repeat(pattern.difficulty)}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Empty state */}
        {!loading && patterns.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-gray-500">No patterns found for this category.</p>
            <button onClick={() => setSelectedCategory(null)} className="text-sm text-blue-500 underline">
              Show all
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

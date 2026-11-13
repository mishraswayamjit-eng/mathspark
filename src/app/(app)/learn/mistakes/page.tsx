'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

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
    'Very High': { color: '#5d6b8c', bg: '#eef3fb' },
    'High':      { color: '#5d6b8c', bg: '#eef3fb' },
    'Medium':    { color: '#5d6b8c', bg: '#eef3fb' },
    'Low':       { color: '#5d6b8c', bg: '#eef3fb' },
  };
  const c = config[freq] ?? { color: '#5d6b8c', bg: '#eef3fb' };
  return (
    <span
      className="text-xs font-extrabold px-1.5 py-0.5 rounded-full"
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
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => setPatterns(data.patterns ?? []))
      .catch((err) => logError('[fetch]', err))
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
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/chapters" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Mistake Patterns</h1>
          <p className="text-white/70 text-xs font-medium">50 traps &middot; Learn from common errors!</p>
        </div>
        <span className="text-2xl">🚨</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="thinking" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Everyone makes mistakes — toppers learn from them!</p>
            <p className="text-xs text-ink-muted mt-0.5">
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
                ? 'bg-action text-white border-action'
                : 'bg-white text-ink border-line'
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
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-28" />
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
                  className="bg-white rounded-card border-2 border-line overflow-hidden"
                  style={{ borderLeftWidth: '4px', borderLeftColor: catMeta.color }}
                >
                  {/* Card header */}
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : pattern.id)}
                    className="w-full px-4 py-3.5 flex items-center gap-3 text-left active:bg-soft transition-colors"
                  >
                    <span className="text-2xl shrink-0">{pattern.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 mb-0.5">
                        <span
                          className="text-xs font-extrabold px-1.5 py-0.5 rounded-full text-white"
                          style={{ backgroundColor: catMeta.color }}
                        >
                          {catMeta.label}
                        </span>
                        <FrequencyBadge freq={pattern.frequency} />
                      </div>
                      <p className="text-sm font-extrabold text-ink leading-tight">{pattern.name}</p>
                      {!isExpanded && (
                        <p className="text-xs text-ink-muted font-medium mt-0.5 line-clamp-1">{pattern.description}</p>
                      )}
                    </div>
                    <span
                      className="text-ink-muted transition-transform duration-200 text-sm shrink-0"
                      style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                    >
                      ▾
                    </span>
                  </button>

                  {/* Expanded content */}
                  {isExpanded && (
                    <div className="px-4 pb-4 space-y-3 animate-fade-in">
                      <div className="border-t-2 border-line" />

                      {/* Description */}
                      <p className="text-sm text-ink font-medium leading-relaxed">{pattern.description}</p>

                      {/* Why it happens */}
                      <div className="bg-retry-soft rounded-control p-3 border-2 border-retry">
                        <div className="flex items-start gap-2">
                          <span className="text-sm shrink-0">🤔</span>
                          <div>
                            <p className="text-[13px] font-extrabold text-retry">Why This Happens</p>
                            <p className="text-sm text-ink font-medium mt-0.5 leading-relaxed">{pattern.whyItHappens}</p>
                          </div>
                        </div>
                      </div>

                      {/* How to fix */}
                      <div className="bg-success-soft rounded-control p-3 border-2 border-success">
                        <div className="flex items-start gap-2">
                          <span className="text-sm shrink-0">✅</span>
                          <div>
                            <p className="text-[15px] font-extrabold text-success">How to Fix It</p>
                            <p className="text-sm text-ink font-medium mt-0.5 leading-relaxed">{pattern.howToFix}</p>
                          </div>
                        </div>
                      </div>

                      {/* Example */}
                      {pattern.example && (
                        <div className="bg-white rounded-control border-2 border-line overflow-hidden">
                          <div className="px-3 pt-3 pb-2">
                            <p className="text-[13px] font-extrabold text-ink-muted mb-1.5">Example</p>
                            <p className="text-sm text-ink font-semibold">{pattern.example.question}</p>
                          </div>

                          {/* Wrong answer */}
                          <div className="bg-retry-soft px-3 py-2.5 border-t-2 border-line">
                            <div className="flex items-start gap-2">
                              <span className="text-sm shrink-0">❌</span>
                              <div>
                                <p className="text-[13px] font-extrabold text-retry">{pattern.example.wrongAnswer}</p>
                                <p className="text-[13px] text-ink font-medium mt-0.5 italic">{pattern.example.wrongThinking}</p>
                              </div>
                            </div>
                          </div>

                          {/* Right answer toggle */}
                          {!rightShown ? (
                            <button
                              onClick={(e) => { e.stopPropagation(); toggleRight(pattern.id); }}
                              className="w-full bg-white px-3 py-2.5 border-t-2 border-line text-center"
                            >
                              <span className="text-[13px] font-bold text-action">Tap to see the right way →</span>
                            </button>
                          ) : (
                            <div className="bg-success-soft px-3 py-2.5 border-t-2 border-line animate-fade-in">
                              <div className="flex items-start gap-2">
                                <span className="text-sm shrink-0">✅</span>
                                <div>
                                  <p className="text-[15px] font-extrabold text-success">{pattern.example.rightAnswer}</p>
                                  <p className="text-[13px] text-ink font-medium mt-0.5 italic">{pattern.example.rightThinking}</p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Sparky's message */}
                      {pattern.sparkyMessage && (
                        <div className="bg-soft rounded-control p-3 border-2 border-line flex items-start gap-2">
                          <Sparky mood="thinking" size={28} />
                          <div>
                            <p className="text-[13px] font-extrabold text-ink-muted">Sparky Says</p>
                            <p className="text-[13px] text-ink font-medium mt-0.5 italic leading-snug">{pattern.sparkyMessage}</p>
                          </div>
                        </div>
                      )}

                      {/* Footer: topics + grades */}
                      <div className="space-y-2 pt-1">
                        {pattern.affectedTopics.length > 0 && (
                          <div className="flex items-start gap-1.5 flex-wrap">
                            <span className="text-xs font-bold text-ink-muted shrink-0">Topics:</span>
                            {pattern.affectedTopics.map((t) => (
                              <span key={t} className="text-xs font-bold text-ink-muted bg-soft px-1.5 py-0.5 rounded-full">
                                {t}
                              </span>
                            ))}
                          </div>
                        )}
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-ink-muted">
                            Grades {pattern.affectedGrades[0]}–{pattern.affectedGrades[pattern.affectedGrades.length - 1]}
                          </span>
                          <span className="text-xs font-bold text-ink-muted">
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
            <p className="text-sm font-bold text-ink-muted">No patterns found for this category.</p>
            <button onClick={() => setSelectedCategory(null)} className="text-sm text-action font-bold underline">
              Show all
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

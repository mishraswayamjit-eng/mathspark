'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

// ── Types ─────────────────────────────────────────────────────────────────────

interface Story {
  id: string;
  title: string;
  emoji: string;
  topicId: string;
  contextCategory: string;
  gradeRange: number[];
  storyText: string;
  mathConnection: string;
  sparkyQuestion: string;
  funFactor: number;
  linkedConcepts: string[];
}

// ── Category metadata ─────────────────────────────────────────────────────────

const CATEGORY_META: Record<string, { emoji: string; label: string; color: string }> = {
  sports:     { emoji: '🏏', label: 'Sports',     color: '#EF4444' },
  space:      { emoji: '🚀', label: 'Space',      color: '#8B5CF6' },
  nature:     { emoji: '🌿', label: 'Nature',     color: '#22C55E' },
  food:       { emoji: '🍕', label: 'Food',       color: '#F97316' },
  money:      { emoji: '💰', label: 'Money',      color: '#EAB308' },
  games:      { emoji: '🎮', label: 'Games',      color: '#3B82F6' },
  geography:  { emoji: '🌍', label: 'Geography',  color: '#14B8A6' },
  technology: { emoji: '💻', label: 'Technology',  color: '#6366F1' },
  history:    { emoji: '📜', label: 'History',     color: '#78716C' },
  culture:    { emoji: '🎭', label: 'Culture',     color: '#EC4899' },
  education:  { emoji: '📚', label: 'Education',   color: '#0EA5E9' },
};

function getCatMeta(cat: string) {
  return CATEGORY_META[cat] ?? { emoji: '📘', label: cat, color: '#94A3B8' };
}

// ── Fun factor stars ──────────────────────────────────────────────────────────

function FunStars({ level }: { level: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <span key={i} className={`text-[10px] ${i <= level ? 'text-yellow-400' : 'text-gray-200'}`}>★</span>
      ))}
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function MathStoriesPage() {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState<Set<string>>(new Set());

  useEffect(() => {
    const qs = selectedCategory ? `?category=${selectedCategory}` : '';
    setLoading(true);
    fetch(`/api/stories${qs}`)
      .then((r) => r.json())
      .then((data) => setStories(data.stories ?? []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  function toggleAnswer(id: string) {
    setShowAnswer((prev) => {
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
          <h1 className="text-white font-extrabold text-lg">Math Stories</h1>
          <p className="text-white/50 text-xs font-medium">30 stories &middot; Math in the real world!</p>
        </div>
        <span className="text-2xl">📖</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-gradient-to-r from-cyan-50 to-sky-50 rounded-2xl px-4 py-3 border border-cyan-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-cyan-800">Did you know math is everywhere?</p>
            <p className="text-xs text-cyan-600 mt-0.5">
              Cricket, rockets, pizza, money — every story ends with a Sparky challenge!
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
            All
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
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-32" />
            ))}
          </div>
        )}

        {/* Story cards */}
        {!loading && (
          <div className="space-y-4">
            {stories.map((story) => {
              const catMeta = getCatMeta(story.contextCategory);
              const isExpanded = expandedId === story.id;
              const answerShown = showAnswer.has(story.id);

              return (
                <div
                  key={story.id}
                  className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
                  style={{ borderTopWidth: '4px', borderTopColor: catMeta.color }}
                >
                  {/* Card header — always visible */}
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : story.id)}
                    className="w-full px-4 pt-4 pb-3 text-left active:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-3xl shrink-0">{story.emoji}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span
                            className="text-[10px] font-extrabold px-2 py-0.5 rounded-full text-white"
                            style={{ backgroundColor: catMeta.color }}
                          >
                            {catMeta.label}
                          </span>
                          <span className="text-[10px] font-bold text-gray-400 capitalize">
                            {story.topicId.replace(/_/g, ' ')}
                          </span>
                          <FunStars level={story.funFactor} />
                        </div>
                        <h3 className="text-sm font-extrabold text-gray-800 leading-tight">{story.title}</h3>
                        {!isExpanded && (
                          <p className="text-xs text-gray-400 font-medium mt-1 line-clamp-2">{story.storyText}</p>
                        )}
                      </div>
                      <span
                        className="text-gray-400 transition-transform duration-200 text-sm shrink-0 mt-1"
                        style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                      >
                        ▾
                      </span>
                    </div>
                  </button>

                  {/* Expanded content */}
                  {isExpanded && (
                    <div className="px-4 pb-4 space-y-3 animate-fade-in">
                      {/* Story text */}
                      <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                        <p className="text-sm text-gray-700 font-medium leading-relaxed">{story.storyText}</p>
                      </div>

                      {/* Math connection */}
                      <div className="bg-indigo-50 rounded-xl p-3 border border-indigo-200 flex items-start gap-2">
                        <span className="text-sm shrink-0">🔗</span>
                        <div>
                          <p className="text-[10px] font-extrabold text-indigo-500 uppercase tracking-wide">Math Connection</p>
                          <p className="text-sm text-indigo-800 font-medium mt-0.5">{story.mathConnection}</p>
                        </div>
                      </div>

                      {/* Sparky's question */}
                      <div className="bg-purple-50 rounded-xl p-3 border border-purple-200">
                        <div className="flex items-start gap-2">
                          <Sparky mood="thinking" size={28} />
                          <div className="flex-1">
                            <p className="text-[10px] font-extrabold text-purple-500 uppercase tracking-wide">Sparky&apos;s Challenge</p>
                            <p className="text-sm text-purple-800 font-semibold mt-0.5">{story.sparkyQuestion}</p>
                          </div>
                        </div>

                        {/* Think about it / show hint */}
                        <div className="mt-2 flex justify-end">
                          <button
                            onClick={(e) => { e.stopPropagation(); toggleAnswer(story.id); }}
                            className="text-[10px] font-bold text-purple-500 bg-purple-100 px-2.5 py-1 rounded-full hover:bg-purple-200 transition-colors"
                          >
                            {answerShown ? 'Hide hint' : 'Think about it... 🤔'}
                          </button>
                        </div>

                        {answerShown && (
                          <div className="mt-2 bg-white rounded-lg px-3 py-2 border border-purple-200 animate-fade-in">
                            <p className="text-xs text-purple-700 font-medium">
                              Try working it out! Re-read the story for the numbers you need.
                              {story.linkedConcepts.length > 0 && (
                                <span className="block mt-1 text-purple-400">
                                  Related: {story.linkedConcepts.join(', ')}
                                </span>
                              )}
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Footer */}
                      <div className="flex items-center gap-2 flex-wrap pt-1">
                        <span className="text-[10px] font-bold text-gray-400">
                          Grades {story.gradeRange[0]}–{story.gradeRange[story.gradeRange.length - 1]}
                        </span>
                        <FunStars level={story.funFactor} />
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Empty state */}
        {!loading && stories.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-gray-500">No stories found for this category.</p>
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

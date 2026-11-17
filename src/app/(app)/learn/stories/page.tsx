'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';
import { logContentView } from '@/lib/contentView';
import { useStudentGrade } from '@/components/lesson/useStudentGrade';

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
  nature:     { emoji: '🌿', label: 'Nature',     color: '#58CC02' },
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
        <span key={i} className={`text-xs ${i <= level ? 'text-star' : 'text-line'}`}>★</span>
      ))}
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function MathStoriesPage() {
  // Every story for the child's grade. The category chips filter this list on
  // the page, so only categories that have a story for this grade are offered.
  const [allStories, setAllStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState<Set<string>>(new Set());
  // The child's grade from the app shell (null for a moment when it is not known yet).
  const grade = useStudentGrade();

  useEffect(() => {
    if (grade === null) return;
    let live = true;
    const params = new URLSearchParams();
    params.set('grade', String(grade));
    setLoading(true);
    fetch(`/api/stories?${params.toString()}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => { if (live) setAllStories(data.stories ?? []); })
      .catch((err) => logError('[fetch]', err))
      .finally(() => { if (live) setLoading(false); });
    return () => { live = false; };
  }, [grade]);

  const stories = selectedCategory
    ? allStories.filter((s) => s.contextCategory === selectedCategory)
    : allStories;

  function toggleAnswer(id: string) {
    setShowAnswer((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  }

  // Only the categories that have at least one story for this grade.
  const categories = Object.keys(CATEGORY_META).filter((cat) => {
    for (let i = 0; i < allStories.length; i++) {
      if (allStories[i].contextCategory === cat) return true;
    }
    return false;
  });

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/learn" aria-label="Back" className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Math Stories</h1>
          <p className="text-white/70 text-sm font-medium">{stories.length} stories &middot; Math in the real world!</p>
        </div>
        <span className="text-2xl" aria-hidden="true">📖</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Did you know math is everywhere?</p>
            <p className="text-sm text-ink-muted mt-0.5">
              Cricket, rockets, pizza, money — every story ends with a Sparky challenge!
            </p>
          </div>
        </div>

        {/* Category filter */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1 flex-wrap">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors ${
              selectedCategory === null
                ? 'bg-action text-white border-ink'
                : 'bg-white text-ink border-line'
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
                className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors flex items-center gap-1 ${
                  isActive
                    ? 'bg-action text-white border-ink'
                    : 'bg-white text-ink border-line'
                }`}
              >
                <span aria-hidden="true">{meta.emoji}</span>
                <span>{meta.label}</span>
              </button>
            );
          })}
        </div>

        {/* Loading */}
        {loading && (
          <div className="space-y-3">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-32" />
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
                  className="bg-white rounded-card border-2 border-line border-l-[10px] overflow-hidden"
                  style={{ borderLeftColor: catMeta.color }}
                >
                  {/* Card header — always visible */}
                  <button
                    onClick={() => {
                      if (!isExpanded) logContentView('story', story.id);
                      setExpandedId(isExpanded ? null : story.id);
                    }}
                    className="w-full px-4 pt-4 pb-3 text-left active:bg-soft transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-3xl shrink-0">{story.emoji}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="ui-chip">
                            {catMeta.label}
                          </span>
                          <span className="text-sm font-bold text-ink-muted capitalize">
                            {story.topicId.replace(/_/g, ' ')}
                          </span>
                          <FunStars level={story.funFactor} />
                        </div>
                        <h3 className="text-title text-ink leading-tight">{story.title}</h3>
                        {!isExpanded && (
                          <p className="text-sm text-ink-muted font-medium mt-1 line-clamp-2">{story.storyText}</p>
                        )}
                      </div>
                      <span
                        className="text-ink-muted transition-transform duration-200 text-sm shrink-0 mt-1"
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
                      <div className="bg-soft rounded-control p-4 border-2 border-line">
                        <p className="text-sm text-ink font-medium leading-relaxed">{story.storyText}</p>
                      </div>

                      {/* Math connection */}
                      <div className="bg-white rounded-control p-3 border-2 border-line flex items-start gap-2">
                        <span className="text-sm shrink-0">🔗</span>
                        <div>
                          <p className="text-sm font-extrabold text-ink-muted">Math Connection</p>
                          <p className="text-sm text-ink font-medium mt-0.5">{story.mathConnection}</p>
                        </div>
                      </div>

                      {/* Sparky's question */}
                      <div className="bg-soft rounded-control p-3 border-2 border-line">
                        <div className="flex items-start gap-2">
                          <Sparky mood="thinking" size={28} />
                          <div className="flex-1">
                            <p className="text-sm font-extrabold text-ink-muted">Sparky&apos;s Challenge</p>
                            <p className="text-sm text-ink font-semibold mt-0.5">{story.sparkyQuestion}</p>
                          </div>
                        </div>

                        {/* Think about it / show hint */}
                        <div className="mt-2 flex justify-end">
                          <button
                            onClick={(e) => { e.stopPropagation(); toggleAnswer(story.id); }}
                            className="min-h-[48px] text-sm font-bold text-action bg-white border-2 border-line px-4 rounded-full hover:border-ink transition-colors"
                          >
                            {answerShown ? 'Hide hint' : 'Think about it... 🤔'}
                          </button>
                        </div>

                        {answerShown && (
                          <div className="mt-2 bg-hint rounded-control px-3 py-2 border-2 border-dashed border-hint-ink animate-fade-in">
                            <p className="text-sm text-hint-ink font-bold">
                              Try working it out! Re-read the story for the numbers you need.
                              {story.linkedConcepts.length > 0 && (
                                <span className="block mt-1 text-hint-ink">
                                  Related: {story.linkedConcepts.join(', ')}
                                </span>
                              )}
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Footer */}
                      <div className="flex items-center gap-2 flex-wrap pt-1">
                        <span className="text-sm font-bold text-ink-muted">
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
            <p className="text-sm font-bold text-ink-muted">No stories found for this category.</p>
            <button
              onClick={() => setSelectedCategory(null)}
              className="min-h-[48px] px-4 text-sm text-action font-bold underline"
            >
              Show all
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

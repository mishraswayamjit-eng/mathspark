'use client';

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';
import { useStudentGrade } from '@/components/lesson/useStudentGrade';

// ── Types ─────────────────────────────────────────────────────────────────────

interface ExampleListItem {
  id: string;
  grade: number;
  topic: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  correctAnswer: string;
  correctAnswerText: string;
}

interface TopicSummary {
  topic: string;
  count: number;
}

// ── Topic colors & emojis ─────────────────────────────────────────────────────

const TOPIC_META: Record<string, { emoji: string; color: string }> = {
  algebra: { emoji: '🔤', color: '#60A5FA' },
  geometry: { emoji: '📐', color: '#A78BFA' },
  fractions: { emoji: '🍕', color: '#F472B6' },
  percentage: { emoji: '💯', color: '#FB923C' },
  speed: { emoji: '🏎️', color: '#F59E0B' },
  ratio: { emoji: '⚖️', color: '#2DD4BF' },
  hcf_lcm: { emoji: '🔢', color: '#34D399' },
  mensuration: { emoji: '📏', color: '#818CF8' },
  bodmas: { emoji: '🧮', color: '#EF4444' },
  patterns: { emoji: '🔄', color: '#8B5CF6' },
  average: { emoji: '📊', color: '#06B6D4' },
  place_value: { emoji: '🏗️', color: '#58CC02' },
  squares: { emoji: '⬛', color: '#F97316' },
  money: { emoji: '💰', color: '#84CC16' },
  age: { emoji: '🎂', color: '#EC4899' },
  counting: { emoji: '🔢', color: '#14B8A6' },
  measurement: { emoji: '📐', color: '#FBBF24' },
  integers: { emoji: '➖', color: '#6366F1' },
  time_calendar: { emoji: '🕐', color: '#F43F5E' },
  roman: { emoji: '🏛️', color: '#78716C' },
  sets: { emoji: '🔵', color: '#0EA5E9' },
  data: { emoji: '📈', color: '#58CC02' },
};

function getTopicMeta(topic: string): { emoji: string; color: string } {
  const lower = topic.toLowerCase().replace(/[^a-z_]/g, '');
  return TOPIC_META[lower] ?? { emoji: '📘', color: '#94A3B8' };
}

const DIFF_COLORS: Record<string, string> = {
  Easy: '#5d6b8c',
  Medium: '#5d6b8c',
  Hard: '#5d6b8c',
};

// ── Page ──────────────────────────────────────────────────────────────────────

export default function WorkedExamplesPage() {
  const [examples, setExamples] = useState<ExampleListItem[]>([]);
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);
  // False until the starting filters have been chosen (see below).
  const [ready, setReady] = useState(false);
  // The child's grade from the app shell (null for a moment when it is not known yet).
  const studentGrade = useStudentGrade();
  // True once the first list has been shown (or the empty-grade fallback used).
  const fellBackRef = useRef(false);

  // The list opens on the child's own grade. A link from a topic page
  // (/learn/examples?topic=bodmas&grade=5) opens on that topic and grade.
  // Chosen once; after that the chips are in charge.
  useEffect(() => {
    if (ready || studentGrade === null) return;
    const params = new URLSearchParams(window.location.search);
    const topicParam = params.get('topic');
    const gradeParam = Number(params.get('grade'));
    if (topicParam && /^[a-z_]{1,40}$/.test(topicParam)) setSelectedTopic(topicParam);
    setSelectedGrade(gradeParam >= 2 && gradeParam <= 9 ? Math.floor(gradeParam) : studentGrade);
    setReady(true);
  }, [ready, studentGrade]);

  useEffect(() => {
    if (!ready) return;
    let live = true;
    let refetching = false;
    const params = new URLSearchParams();
    if (selectedTopic) params.set('topic', selectedTopic);
    if (selectedGrade) params.set('grade', String(selectedGrade));
    const qs = params.toString();

    fetch(`/api/worked-examples${qs ? `?${qs}` : ''}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        if (!live) return;
        // A grade with no examples of its own opens on every grade instead of an empty page.
        if (!fellBackRef.current && selectedGrade !== null && !selectedTopic && (data.examples ?? []).length === 0) {
          fellBackRef.current = true;
          refetching = true;
          setSelectedGrade(null);
          return;
        }
        fellBackRef.current = true;
        setExamples(data.examples ?? []);
        // The topic chips are the topics that have examples for the chosen grade.
        setTopics(data.topics ?? []);
      })
      .catch((err) => logError('[fetch]', err))
      .finally(() => { if (live && !refetching) setLoading(false); });
    return () => { live = false; };
  }, [ready, selectedTopic, selectedGrade]);

  // Available grades
  const grades = [2, 3, 4, 5, 6, 7, 8, 9];

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/learn" aria-label="Back" className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Sparky Explains</h1>
          <p className="text-white/70 text-sm font-medium">
            {loading ? 'Worked examples' : `${examples.length} worked examples`} with step-by-step solutions
          </p>
        </div>
        <span className="text-2xl" aria-hidden="true">💡</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Watch me solve it step-by-step!</p>
            <p className="text-sm text-ink-muted mt-0.5">
              Tap any example to see how I think through the problem. Includes trap warnings!
            </p>
          </div>
        </div>

        {/* Grade filter */}
        <div className="flex gap-1.5 mb-4 overflow-x-auto pb-1">
          <button
            onClick={() => { setSelectedGrade(null); setLoading(true); }}
            className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors ${
              selectedGrade === null
                ? 'bg-action text-white border-ink'
                : 'bg-white text-ink border-line'
            }`}
          >
            All Grades
          </button>
          {grades.map((g) => (
            <button
              key={g}
              onClick={() => { setSelectedGrade(g); setLoading(true); }}
              className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors ${
                selectedGrade === g
                  ? 'bg-action text-white border-ink'
                  : 'bg-white text-ink border-line'
              }`}
            >
              G{g}
            </button>
          ))}
        </div>

        {/* Topic chips */}
        {(
          <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1 flex-wrap">
            <button
              onClick={() => { setSelectedTopic(null); setLoading(true); }}
              className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors ${
                selectedTopic === null
                  ? 'bg-action text-white border-ink'
                  : 'bg-white text-ink border-line'
              }`}
            >
              All Topics
            </button>
            {topics.map((t) => {
              const meta = getTopicMeta(t.topic);
              return (
                <button
                  key={t.topic}
                  onClick={() => { setSelectedTopic(t.topic); setLoading(true); }}
                  className={`min-h-[48px] px-4 rounded-full text-sm font-bold border-2 shrink-0 transition-colors flex items-center gap-1 ${
                    selectedTopic === t.topic
                      ? 'bg-action text-white border-ink'
                      : 'bg-white text-ink border-line'
                  }`}
                >
                  <span aria-hidden="true">{meta.emoji}</span>
                  <span className="capitalize">{t.topic.replace(/_/g, ' ')}</span>
                  <span className="opacity-60">({t.count})</span>
                </button>
              );
            })}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="space-y-3">
            {[0, 1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-28" />
            ))}
          </div>
        )}

        {/* Examples list */}
        {!loading && examples.length > 0 && (
          <div className="space-y-3">
            {examples.map((ex) => {
              const meta = getTopicMeta(ex.topic);
              return (
                <Link
                  key={ex.id}
                  href={`/learn/examples/${ex.id}`}
                  className="block bg-white rounded-card p-4 border-2 border-line hover:border-ink transition-[border-color,transform] active:scale-[0.98]"
                >
                  <div className="flex items-start gap-3">
                    {/* Topic icon */}
                    <div
                      className="w-10 h-10 rounded-tile flex items-center justify-center text-lg shrink-0"
                      style={{ backgroundColor: meta.color + '20' }}
                    >
                      {meta.emoji}
                    </div>

                    <div className="flex-1 min-w-0">
                      {/* Tags */}
                      <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                        <span className="ui-chip">
                          {ex.topic.replace(/_/g, ' ')}
                        </span>
                        <span className="text-sm font-bold text-ink-muted">
                          Grade {ex.grade}
                        </span>
                        <span
                          className="text-sm font-bold px-1.5 py-0.5 rounded-full"
                          style={{
                            color: DIFF_COLORS[ex.difficulty] ?? '#999',
                            backgroundColor: (DIFF_COLORS[ex.difficulty] ?? '#999') + '15',
                          }}
                        >
                          {ex.difficulty}
                        </span>
                      </div>

                      {/* Question text */}
                      <p className="text-sm font-bold text-ink leading-snug line-clamp-2">
                        {ex.questionText}
                      </p>

                      {/* Sub-topic */}
                      <p className="text-sm text-ink-muted mt-1">{ex.subTopic}</p>
                    </div>

                    {/* Arrow */}
                    <span className="text-ink-muted text-sm shrink-0 mt-2">&rsaquo;</span>
                  </div>
                </Link>
              );
            })}
          </div>
        )}

        {/* Empty state */}
        {!loading && examples.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-ink-muted">No examples found for this filter.</p>
            <button
              onClick={() => { setSelectedTopic(null); setSelectedGrade(null); setLoading(true); }}
              className="min-h-[48px] px-4 text-sm text-action font-bold underline"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

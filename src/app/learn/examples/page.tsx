'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

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
  Easy: '#58CC02',
  Medium: '#FF9600',
  Hard: '#FF4B4B',
};

// ── Page ──────────────────────────────────────────────────────────────────────

export default function WorkedExamplesPage() {
  const [examples, setExamples] = useState<ExampleListItem[]>([]);
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (selectedTopic) params.set('topic', selectedTopic);
    if (selectedGrade) params.set('grade', String(selectedGrade));
    const qs = params.toString();

    fetch(`/api/worked-examples${qs ? `?${qs}` : ''}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setExamples(data.examples ?? []);
        if (!selectedTopic && !selectedGrade) setTopics(data.topics ?? []);
      })
      .catch((err) => console.error('[fetch]', err))
      .finally(() => setLoading(false));
  }, [selectedTopic, selectedGrade]);

  // Available grades
  const grades = [2, 3, 4, 5, 6, 7, 8, 9];

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/chapters" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Sparky Explains</h1>
          <p className="text-white/70 text-xs font-medium">212 worked examples with step-by-step solutions</p>
        </div>
        <span className="text-2xl">💡</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl px-4 py-3 border border-purple-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-purple-800">Watch me solve it step-by-step!</p>
            <p className="text-xs text-purple-600 mt-0.5">
              Tap any example to see how I think through the problem. Includes trap warnings!
            </p>
          </div>
        </div>

        {/* Grade filter */}
        <div className="flex gap-1.5 mb-4 overflow-x-auto pb-1">
          <button
            onClick={() => { setSelectedGrade(null); setLoading(true); }}
            className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors ${
              selectedGrade === null
                ? 'bg-duo-dark text-white border-duo-dark'
                : 'bg-white text-gray-600 border-gray-200'
            }`}
          >
            All Grades
          </button>
          {grades.map((g) => (
            <button
              key={g}
              onClick={() => { setSelectedGrade(g); setLoading(true); }}
              className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors ${
                selectedGrade === g
                  ? 'bg-duo-dark text-white border-duo-dark'
                  : 'bg-white text-gray-600 border-gray-200'
              }`}
            >
              G{g}
            </button>
          ))}
        </div>

        {/* Topic chips */}
        {topics.length > 0 && (
          <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1 flex-wrap">
            <button
              onClick={() => { setSelectedTopic(null); setLoading(true); }}
              className={`px-3 py-1.5 rounded-full text-xs font-bold border shrink-0 transition-colors ${
                selectedTopic === null
                  ? 'bg-purple-600 text-white border-purple-600'
                  : 'bg-white text-gray-600 border-gray-200'
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
                  className={`px-3 py-1.5 rounded-full text-xs font-bold border shrink-0 transition-colors flex items-center gap-1 ${
                    selectedTopic === t.topic
                      ? 'text-white border-transparent'
                      : 'bg-white text-gray-600 border-gray-200'
                  }`}
                  style={selectedTopic === t.topic ? { backgroundColor: meta.color } : {}}
                >
                  <span>{meta.emoji}</span>
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
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-28" />
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
                  className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-[box-shadow,transform] active:scale-[0.98]"
                >
                  <div className="flex items-start gap-3">
                    {/* Topic icon */}
                    <div
                      className="w-10 h-10 rounded-xl flex items-center justify-center text-lg shrink-0"
                      style={{ backgroundColor: meta.color + '20' }}
                    >
                      {meta.emoji}
                    </div>

                    <div className="flex-1 min-w-0">
                      {/* Tags */}
                      <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                        <span
                          className="text-[10px] font-extrabold px-2 py-0.5 rounded-full text-white"
                          style={{ backgroundColor: meta.color }}
                        >
                          {ex.topic.replace(/_/g, ' ')}
                        </span>
                        <span className="text-[10px] font-bold text-gray-500">
                          Grade {ex.grade}
                        </span>
                        <span
                          className="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                          style={{
                            color: DIFF_COLORS[ex.difficulty] ?? '#999',
                            backgroundColor: (DIFF_COLORS[ex.difficulty] ?? '#999') + '15',
                          }}
                        >
                          {ex.difficulty}
                        </span>
                      </div>

                      {/* Question text */}
                      <p className="text-sm font-semibold text-gray-800 leading-snug line-clamp-2">
                        {ex.questionText}
                      </p>

                      {/* Sub-topic */}
                      <p className="text-xs text-gray-500 mt-1">{ex.subTopic}</p>
                    </div>

                    {/* Arrow */}
                    <span className="text-gray-300 text-sm shrink-0 mt-2">&rsaquo;</span>
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
            <p className="text-sm font-bold text-gray-500">No examples found for this filter.</p>
            <button
              onClick={() => { setSelectedTopic(null); setSelectedGrade(null); setLoading(true); }}
              className="text-sm text-blue-500 underline"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

// ── Types ─────────────────────────────────────────────────────────────────────

interface TopicFreq {
  topic: string;
  count: number;
  percentage: number;
}

interface GradePrediction {
  grade: number;
  totalQuestionsAnalyzed: number;
  yearsAnalyzed: number;
  yearRange: string;
  topicFrequency: TopicFreq[];
  alwaysAppears: string[];
  frequentlyAppears: string[];
  rarelyAppears: string[];
  predictedFocusAreas: string[];
  predictedPaper: string | null;
}

interface Insights {
  topicsThatAlwaysAppear: string;
  difficultyTrend: string;
  topStrategicAdvice: string[];
}

interface GradeSummary {
  grade: number;
  totalQuestionsAnalyzed: number;
  yearsAnalyzed: number;
  yearRange: string;
  topTopics: string[];
  focusAreaCount: number;
}

// ── Topic bar colors ──────────────────────────────────────────────────────────

const TOPIC_COLORS: Record<string, string> = {
  'Number Sense':        '#3B82F6',
  'Fractions':           '#F97316',
  'Geometry & Angles':   '#06B6D4',
  'Algebra & Equations': '#8B5CF6',
  'Factors & Multiples': '#58CC02',
  'Squares & Roots':     '#EAB308',
  'Mensuration':         '#14B8A6',
  'Time & Calendar':     '#EC4899',
  'Arithmetic':          '#EF4444',
  'Roman Numerals':      '#78716C',
  'Speed & Distance':    '#F59E0B',
  'Patterns':            '#6366F1',
  'Money & Measurement': '#0EA5E9',
  'Age Problems':        '#A855F7',
  'Ratio & Proportion':  '#059669',
  'Percentage & Profit': '#DC2626',
  'Other':               '#94A3B8',
};

function topicColor(topic: string) {
  return TOPIC_COLORS[topic] ?? '#6B7280';
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function IPMPredictorPage() {
  const [gradeSummaries, setGradeSummaries] = useState<GradeSummary[]>([]);
  const [insights, setInsights] = useState<Insights | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<GradePrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);

  // Load overview
  useEffect(() => {
    fetch('/api/ipm-predictor')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setGradeSummaries(data.grades ?? []);
        setInsights(data.insights ?? null);
      })
      .catch((err) => logError('[fetch]', err))
      .finally(() => setLoading(false));
  }, []);

  // Load grade detail
  useEffect(() => {
    if (!selectedGrade) { setPrediction(null); return; }
    setDetailLoading(true);
    fetch(`/api/ipm-predictor?grade=${selectedGrade}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => setPrediction(data.prediction ?? null))
      .catch((err) => logError('[fetch]', err))
      .finally(() => setDetailLoading(false));
  }, [selectedGrade]);

  const grades = [2, 3, 4, 5, 6, 7, 8, 9];

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/home" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">IPM Exam Predictor</h1>
          <p className="text-white/70 text-xs font-medium">1,980 questions analyzed &middot; 10+ years of data</p>
        </div>
        <span className="text-2xl">🔮</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Know what&apos;s coming before the exam!</p>
            <p className="text-xs text-ink-muted mt-0.5">
              We analyzed 10+ years of IPM Mega Finals to predict which topics appear most. Focus smart!
            </p>
          </div>
        </div>

        {/* Grade selector */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
          {grades.map((g) => {
            const summary = gradeSummaries.find((s) => s.grade === g);
            const isActive = selectedGrade === g;
            return (
              <button
                key={g}
                onClick={() => setSelectedGrade(isActive ? null : g)}
                className={`flex flex-col items-center px-3.5 py-2.5 rounded-control border-2 shrink-0 transition-colors min-w-[72px] ${
                  isActive
                    ? 'bg-action text-white border-ink'
                    : 'bg-white text-ink border-line'
                }`}
              >
                <span className="text-xs font-extrabold">Grade {g}</span>
                {summary && (
                  <span className={`text-xs font-bold mt-0.5 ${isActive ? 'text-white/70' : 'text-ink-muted'}`}>
                    {summary.totalQuestionsAnalyzed} Qs
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Loading */}
        {(loading || detailLoading) && (
          <div className="space-y-3">
            {[0, 1, 2].map((i) => (
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-24" />
            ))}
          </div>
        )}

        {/* ── Grade Prediction Detail ────────────────────────────────── */}
        {!detailLoading && prediction && (
          <div className="space-y-4 animate-fade-in">
            {/* Overview card */}
            <div className="bg-white rounded-card p-4 border-2 border-line">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-title text-ink">
                  Grade {prediction.grade} Analysis
                </h2>
                {prediction.yearRange !== '?-?' && (
                  <span className="text-xs font-bold text-ink-muted bg-soft rounded-full px-2 py-0.5">
                    {prediction.yearRange}
                  </span>
                )}
              </div>
              <div className="grid grid-cols-3 gap-2">
                <div className="bg-soft rounded-tile p-2.5 text-center border-2 border-line">
                  <p className="text-lg font-extrabold text-ink">{prediction.totalQuestionsAnalyzed}</p>
                  <p className="text-xs font-bold text-ink-muted">Questions</p>
                </div>
                <div className="bg-soft rounded-tile p-2.5 text-center border-2 border-line">
                  <p className="text-lg font-extrabold text-ink">{prediction.yearsAnalyzed || '—'}</p>
                  <p className="text-xs font-bold text-ink-muted">Years</p>
                </div>
                <div className="bg-soft rounded-tile p-2.5 text-center border-2 border-line">
                  <p className="text-lg font-extrabold text-ink">
                    {prediction.topicFrequency.filter((t) => t.topic !== 'Other').length}
                  </p>
                  <p className="text-xs font-bold text-ink-muted">Topics</p>
                </div>
              </div>
            </div>

            {/* Topic frequency chart */}
            <div className="bg-white rounded-card p-4 border-2 border-line">
              <h3 className="text-title text-ink mb-3">Topic Frequency</h3>
              <div className="space-y-2.5">
                {prediction.topicFrequency
                  .filter((t) => t.topic !== 'Other')
                  .map((t) => {
                    return (
                      <div key={t.topic} className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-ink w-32 truncate shrink-0">{t.topic}</span>
                        <div className="flex-1 h-5 bg-soft rounded-full overflow-hidden relative">
                          <div
                            className="h-full rounded-full bg-action transition-[width] duration-700"
                            style={{ width: `${Math.max(t.percentage, 3)}%` }}
                          />
                          <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs font-extrabold text-ink-muted">
                            {t.percentage}%
                          </span>
                        </div>
                        <span className="text-xs font-bold text-ink-muted w-8 text-right shrink-0">{t.count}</span>
                      </div>
                    );
                  })}
                {/* Show "Other" separately */}
                {prediction.topicFrequency.find((t) => t.topic === 'Other') && (
                  <div className="flex items-center gap-2 opacity-50">
                    <span className="text-xs font-semibold text-gray-500 w-32 truncate shrink-0">Other / Mixed</span>
                    <div className="flex-1 h-5 bg-soft rounded-full overflow-hidden relative">
                      <div
                        className="h-full rounded-full bg-gray-300"
                        style={{
                          width: `${Math.max(prediction.topicFrequency.find((t) => t.topic === 'Other')!.percentage, 3)}%`,
                        }}
                      />
                      <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs font-extrabold text-ink-muted">
                        {prediction.topicFrequency.find((t) => t.topic === 'Other')!.percentage}%
                      </span>
                    </div>
                    <span className="text-xs font-bold text-ink-muted w-8 text-right shrink-0">
                      {prediction.topicFrequency.find((t) => t.topic === 'Other')!.count}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Always / Frequently / Rarely appears */}
            {prediction.alwaysAppears.length > 0 && (
              <div className="bg-white rounded-card p-4 border-2 border-line space-y-3">
                {prediction.alwaysAppears.length > 0 && (
                  <div>
                    <div className="flex items-center gap-1.5 mb-2">
                      <span className="text-sm">🔴</span>
                      <p className="text-caption text-ink">Always Appears</p>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {prediction.alwaysAppears.filter((t) => t !== 'Other').map((t) => (
                        <span key={t} className="ui-chip">
                          <span
                            className="w-2.5 h-2.5 rounded-full shrink-0"
                            style={{ backgroundColor: topicColor(t) }}
                            aria-hidden="true"
                          />
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {prediction.frequentlyAppears.length > 0 && (
                  <div>
                    <div className="flex items-center gap-1.5 mb-2">
                      <span className="text-sm">🟡</span>
                      <p className="text-caption text-ink">Frequently Appears</p>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {prediction.frequentlyAppears.map((t) => (
                        <span key={t} className="ui-chip">
                          <span
                            className="w-2.5 h-2.5 rounded-full shrink-0"
                            style={{ backgroundColor: topicColor(t) }}
                            aria-hidden="true"
                          />
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {prediction.rarelyAppears.length > 0 && (
                  <div>
                    <div className="flex items-center gap-1.5 mb-2">
                      <span className="text-sm">⚪</span>
                      <p className="text-caption text-ink-muted">Rarely Appears</p>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {prediction.rarelyAppears.map((t) => (
                        <span key={t} className="text-xs font-bold text-ink-muted bg-soft border-2 border-line px-2 py-1 rounded-full">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Predicted focus areas */}
            {prediction.predictedFocusAreas.length > 0 && (
              <div className="bg-white rounded-card p-4 border-2 border-ink shadow-hard-lg">
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-lg">🎯</span>
                  <h3 className="text-title text-ink">Focus These Topics</h3>
                </div>
                <div className="space-y-2">
                  {prediction.predictedFocusAreas.filter((t) => t !== 'Other').map((topic, i) => (
                    <div key={topic} className="flex items-center gap-2.5">
                      <span className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold bg-soft text-ink border-2 border-line shrink-0">
                        {i + 1}
                      </span>
                      <span className="text-sm font-bold text-ink">{topic}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── Overview (no grade selected) ───────────────────────────── */}
        {!loading && !selectedGrade && !detailLoading && (
          <div className="space-y-4">
            {/* Grade cards */}
            <div className="space-y-2.5">
              {gradeSummaries.map((s) => (
                <button
                  key={s.grade}
                  onClick={() => setSelectedGrade(s.grade)}
                  className="w-full bg-white rounded-card p-4 border-2 border-line flex items-center gap-3 text-left active:bg-soft transition-colors"
                >
                  <div className="w-12 h-12 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
                    <span className="text-lg font-extrabold text-ink">G{s.grade}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-extrabold text-ink">Grade {s.grade} Prediction</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs font-bold text-ink-muted">{s.totalQuestionsAnalyzed} Qs analyzed</span>
                      {s.yearsAnalyzed > 0 && (
                        <span className="text-xs font-bold text-ink-muted">&middot; {s.yearsAnalyzed} years</span>
                      )}
                    </div>
                    {s.topTopics.length > 0 && (
                      <div className="flex gap-1 mt-1 flex-wrap">
                        {s.topTopics.map((t) => (
                          <span key={t} className="ui-chip">
                            <span
                              className="w-2.5 h-2.5 rounded-full shrink-0"
                              style={{ backgroundColor: topicColor(t) }}
                              aria-hidden="true"
                            />
                            {t}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <span className="text-ink-muted text-sm shrink-0">→</span>
                </button>
              ))}
            </div>

            {/* Strategic insights */}
            {insights && (
              <div className="bg-white rounded-card p-4 border-2 border-line space-y-3">
                <div className="flex items-center gap-2">
                  <span className="text-lg">💡</span>
                  <h3 className="text-title text-ink">Strategic Insights</h3>
                </div>

                {insights.topicsThatAlwaysAppear && (
                  <div className="bg-soft rounded-control p-3 border-2 border-line">
                    <p className="text-caption text-ink-muted mb-1">Key Finding</p>
                    <p className="text-xs text-ink font-medium leading-relaxed">{insights.topicsThatAlwaysAppear}</p>
                  </div>
                )}

                {insights.difficultyTrend && (
                  <div className="bg-soft rounded-control p-3 border-2 border-line">
                    <p className="text-caption text-ink-muted mb-1">Difficulty Trend</p>
                    <p className="text-xs text-ink font-medium leading-relaxed">{insights.difficultyTrend}</p>
                  </div>
                )}

                {insights.topStrategicAdvice && insights.topStrategicAdvice.length > 0 && (
                  <div>
                    <p className="text-caption text-ink-muted mb-2">Top Tips</p>
                    <div className="space-y-2">
                      {insights.topStrategicAdvice.map((tip, i) => (
                        <div key={i} className="flex items-start gap-2">
                          <span className="text-sm shrink-0 mt-0.5">💎</span>
                          <p className="text-xs text-ink font-medium leading-relaxed">{tip}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Sparky encouragement */}
            <div className="bg-white rounded-card p-4 border-2 border-line flex items-start gap-3">
              <Sparky mood="happy" size={36} />
              <div>
                <p className="text-sm font-bold text-ink">Smart preparation = better scores!</p>
                <p className="text-xs text-ink-muted mt-0.5">
                  Tap any grade above to see exactly which topics appear most. Focus on what matters!
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

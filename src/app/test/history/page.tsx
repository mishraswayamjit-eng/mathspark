'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import DuoButton from '@/components/DuoButton';

interface TestSummary {
  id: string;
  type: string;
  totalQuestions: number;
  timeLimitMs: number;
  startedAt: string;
  completedAt?: string | null;
  score?: number | null;
  accuracy?: number | null;
  status: string;
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function TypeBadge({ type }: { type: string }) {
  const cfg =
    type === 'quick' ? { label: 'Quick',    bg: 'bg-blue-100',   text: 'text-blue-700' } :
    type === 'half'  ? { label: 'Half',     bg: 'bg-amber-100',  text: 'text-amber-700' } :
    type === 'ipm'   ? { label: 'IPM',      bg: 'bg-purple-100', text: 'text-purple-700' } :
    type === 'pyq'   ? { label: 'PYQ',      bg: 'bg-indigo-100', text: 'text-indigo-700' } :
    type === 'mega'  ? { label: 'Mega',     bg: 'bg-pink-100',   text: 'text-pink-700' } :
                       { label: 'Full',     bg: 'bg-green-100',  text: 'text-green-700' };
  return (
    <span className={`text-xs font-extrabold px-2 py-0.5 rounded-full ${cfg.bg} ${cfg.text}`}>
      {cfg.label}
    </span>
  );
}

export default function TestHistoryPage() {
  const router = useRouter();
  const [tests,   setTests]   = useState<TestSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    fetch('/api/mock-tests/history')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data: TestSummary[]) => { setTests(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const completed = tests.filter((t) => t.status === 'completed');

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-duo-blue/30 border-t-duo-blue rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white pb-28 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4">
        <button
          onClick={() => window.history.length > 1 ? router.back() : router.push('/test')}
          className="text-white/60 text-sm font-semibold mb-2 flex items-center gap-1 hover:text-white transition-colors"
        >
          ← Back
        </button>
        <h1 className="text-xl font-extrabold text-white">Test History 📋</h1>
        <p className="text-white/70 text-xs font-semibold mt-0.5">{completed.length} test{completed.length !== 1 ? 's' : ''} completed</p>
      </div>

      {/* Trend chart (≥ 2 completed tests) */}
      {completed.length >= 2 && (
        <div className="px-4 pt-4">
          <div className="bg-gray-50 rounded-2xl p-4">
            <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-3">Score Trend</p>
            <div className="flex items-end gap-2 h-20">
              {completed.slice(-8).map((t, i) => {
                const h = t.totalQuestions > 0 ? ((t.score ?? 0) / t.totalQuestions) * 100 : 0;
                return (
                  <div key={t.id} className="flex-1 flex flex-col items-center gap-1">
                    <div
                      className={`w-full rounded-t-lg transition-[height] ${
                        h >= 80 ? 'bg-duo-green' : h >= 60 ? 'bg-duo-orange' : 'bg-duo-red'
                      }`}
                      style={{ height: `${Math.max(4, h * 0.72)}px` }}
                    />
                    <span className="text-[10px] text-gray-500 font-bold">{Math.round(h)}%</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Tests list */}
      <div className="px-4 pt-4 space-y-3">
        {tests.length === 0 && (
          <div className="text-center py-12">
            <p className="text-4xl mb-3">📋</p>
            <p className="font-extrabold text-gray-700">No tests yet</p>
            <p className="text-gray-500 text-sm mt-1">Take your first mock test to see results here!</p>
          </div>
        )}

        {tests.map((t) => {
          const pct = t.totalQuestions > 0 ? Math.round(((t.score ?? 0) / t.totalQuestions) * 100) : null;
          const isCompleted = t.status === 'completed';
          return (
            <div
              key={t.id}
              className="bg-white border-2 border-gray-100 rounded-2xl p-4 flex items-center gap-3"
            >
              {/* Score circle */}
              <div className={`w-12 h-12 rounded-full flex items-center justify-center font-extrabold text-sm flex-shrink-0 ${
                pct == null ? 'bg-gray-100 text-gray-500'  :
                pct >= 80   ? 'bg-green-100 text-duo-green' :
                pct >= 60   ? 'bg-amber-100 text-duo-orange' :
                              'bg-red-100 text-duo-red'
              }`}>
                {isCompleted && pct != null ? `${pct}%` : '…'}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <TypeBadge type={t.type} />
                  {!isCompleted && (
                    <span className="text-xs font-extrabold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700">
                      {t.status === 'in_progress' ? 'In Progress' : 'Abandoned'}
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-500 font-semibold">
                  {formatDate(t.startedAt)}
                  {isCompleted && t.score != null && ` · ${t.score}/${t.totalQuestions}`}
                </p>
              </div>

              {isCompleted ? (
                <button
                  onClick={() => router.push(`/test/${t.id}/results`)}
                  className="text-xs font-extrabold text-duo-blue hover:text-duo-blue-dark flex-shrink-0"
                >
                  View Results →
                </button>
              ) : (
                <button
                  onClick={() => router.push(`/test/${t.id}`)}
                  className="text-xs font-extrabold text-duo-green hover:text-duo-green-dark flex-shrink-0"
                >
                  Resume →
                </button>
              )}
            </div>
          );
        })}
      </div>

      {/* CTA */}
      <div className="px-4 mt-6">
        <DuoButton variant="green" fullWidth onClick={() => router.push('/test')}>
          Take a New Test 📝
        </DuoButton>
      </div>
    </div>
  );
}

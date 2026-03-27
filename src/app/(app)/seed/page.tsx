'use client';

import { useState } from 'react';

type Status = 'idle' | 'running' | 'done' | 'error';

interface TopicStatus {
  id: string; name: string; grade: number; count: number;
}

interface FixReport {
  dryRun: boolean;
  written: boolean;
  stats: {
    total: number; tagged: number;
    byMethod: Record<string, number>;
    emptyCorrectAnswer: number; emptyOptions: number; totalUnusable: number; usableNonG4: number;
    emptyCorrectBySource: Record<string, number>; emptyOptsBySource: Record<string, number>;
    dbUpdated: number; pendingUpdates: number;
  };
  gradeReport: Record<string, { topic: string; label: string; count: number }[]>;
}

export default function SeedPage() {
  // ── Questions seed ──────────────────────────────────────────────────────────
  const [secret,   setSecret]   = useState('');
  const [status,   setStatus]   = useState<Status>('idle');
  const [seeded,   setSeeded]   = useState(0);
  const [total,    setTotal]    = useState(12500);
  const [skipped,  setSkipped]  = useState(0);
  const [message,  setMessage]  = useState('');

  // ── Test users seed ─────────────────────────────────────────────────────────
  const [testSecret,  setTestSecret]  = useState('');
  const [testStatus,  setTestStatus]  = useState<Status>('idle');
  const [testMessage, setTestMessage] = useState('');

  // ── DB verification ─────────────────────────────────────────────────────────
  const [verifyStatus,  setVerifyStatus]  = useState<'idle' | 'loading' | 'done' | 'error'>('idle');
  const [verifyData,    setVerifyData]    = useState<{ total: number; topicCount: number; topics: TopicStatus[]; emptyTopics: TopicStatus[]; healthy: boolean } | null>(null);

  // ── Fix subtopics ──────────────────────────────────────────────────────────
  const [fixSecret,  setFixSecret]  = useState('');
  const [fixStatus,  setFixStatus]  = useState<Status>('idle');
  const [fixMessage, setFixMessage] = useState('');
  const [fixReport,  setFixReport]  = useState<FixReport | null>(null);

  // ── Handlers ─────────────────────────────────────────────────────────────────
  async function runSeed() {
    if (!secret.trim()) { setMessage('Enter your SEED_SECRET first.'); return; }
    setStatus('running');
    setMessage('Ensuring topics exist…');
    setSeeded(0);
    setSkipped(0);
    let page = 0;
    while (true) {
      try {
        const res  = await fetch(`/api/seed?secret=${encodeURIComponent(secret)}&page=${page}`);
        const data = await res.json();
        if (!res.ok) { setMessage(data.error ?? 'Something went wrong.'); setStatus('error'); return; }
        setSeeded(data.seeded ?? 0);
        setTotal(data.total   ?? 6797);
        setSkipped((prev) => prev + (data.skipped ?? 0));
        setMessage(data.message ?? '');
        if (data.done) { setStatus('done'); return; }
        page = data.nextPage;
      } catch (err) {
        setMessage(`Network error: ${err}`);
        setStatus('error');
        return;
      }
    }
  }

  async function runTestSeed() {
    if (!testSecret.trim()) { setTestMessage('Enter your SEED_SECRET first.'); setTestStatus('error'); return; }
    setTestStatus('running');
    setTestMessage('');
    try {
      const res  = await fetch(`/api/seed-test?secret=${encodeURIComponent(testSecret)}`);
      const data = await res.json();
      if (!res.ok) { setTestMessage(data.error ?? 'Something went wrong.'); setTestStatus('error'); return; }
      const s = data.seeded;
      setTestMessage(`${s.parents} parents · ${s.students} students · ${s.orders} orders · ${s.progress} progress rows · ${s.usageLogs} usage logs`);
      setTestStatus('done');
    } catch (err) {
      setTestMessage(`Network error: ${err}`);
      setTestStatus('error');
    }
  }

  async function runFixSubtopics(dryRun: boolean) {
    const sec = fixSecret || secret || testSecret;
    if (!sec.trim()) { setFixMessage('Enter your SEED_SECRET first.'); setFixStatus('error'); return; }
    setFixStatus('running');
    setFixMessage(dryRun ? 'Running dry-run analysis...' : 'Re-tagging subtopics...');
    setFixReport(null);
    try {
      const res  = await fetch(`/api/fix-subtopics?secret=${encodeURIComponent(sec)}&dryRun=${dryRun}`);
      const data = await res.json();
      if (!res.ok) { setFixMessage(data.error ?? 'Something went wrong.'); setFixStatus('error'); return; }
      setFixReport(data as FixReport);
      setFixMessage(dryRun
        ? `Dry-run complete — ${(data as FixReport).stats.pendingUpdates} updates pending.`
        : `Done! ${(data as FixReport).stats.dbUpdated} questions updated in DB.`);
      setFixStatus('done');
    } catch (err) {
      setFixMessage(`Network error: ${err}`);
      setFixStatus('error');
    }
  }

  async function runVerify() {
    const sec = secret || testSecret;
    if (!sec.trim()) { alert('Enter your SEED_SECRET in either field above first.'); return; }
    setVerifyStatus('loading');
    try {
      const res  = await fetch(`/api/seed-status?secret=${encodeURIComponent(sec)}`);
      const data = await res.json();
      if (!res.ok) { setVerifyStatus('error'); return; }
      setVerifyData(data);
      setVerifyStatus('done');
    } catch {
      setVerifyStatus('error');
    }
  }

  const pct = total > 0 ? Math.round((seeded / total) * 100) : 0;

  return (
    <div className="min-h-screen flex flex-col items-center justify-start px-6 py-10 gap-8 max-w-md mx-auto animate-fade-in">

      {/* ── Section 1: Questions ───────────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-green-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🌱</span>
          <div>
            <p className="font-bold text-gray-800">Seed Questions</p>
            <p className="text-xs text-gray-500">Loads all ~12,500 questions (Grades 2–9) into the database</p>
          </div>
        </div>

        {status === 'idle' || status === 'error' ? (
          <>
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">SEED_SECRET</label>
              <input
                type="password"
                value={secret}
                onChange={(e) => setSecret(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && runSeed()}
                placeholder="your-secret-key"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 outline-none focus:border-green-400 text-sm"
              />
            </div>
            {message && <p className="text-sm text-red-500">{message}</p>}
            <button
              onClick={runSeed}
              className="w-full bg-duo-green hover:bg-green-600 text-white font-bold py-3.5 rounded-2xl transition-colors"
            >
              Start Seeding →
            </button>
          </>
        ) : status === 'running' ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-duo-green h-3 rounded-full transition-[width] duration-300"
                style={{ width: `${pct}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500">
              <span>{message}</span>
              <span className="font-semibold">{seeded} / {total}</span>
            </div>
          </>
        ) : (
          <div className="space-y-2">
            <div className="flex items-center gap-3 bg-green-50 rounded-xl px-4 py-3">
              <span className="text-2xl">🎉</span>
              <div>
                <p className="font-bold text-green-700 text-sm">{seeded} questions loaded!</p>
                {skipped > 0 && (
                  <p className="text-xs text-amber-600 font-medium">{skipped} skipped (malformed data)</p>
                )}
                <a href="/start" className="text-xs text-green-600 underline">Open MathSpark →</a>
              </div>
            </div>
            <button
              onClick={() => { setStatus('idle'); setMessage(''); setSkipped(0); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Re-seed (safe to run again)
            </button>
          </div>
        )}
      </div>

      {/* ── Section 2: Test Users ──────────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-blue-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">👨‍👩‍👧‍👦</span>
          <div>
            <p className="font-bold text-gray-800">Load Test Users</p>
            <p className="text-xs text-gray-500">10 families · 18 students (Gr 2–9) · subscriptions, orders, progress &amp; streaks</p>
          </div>
        </div>

        <div className="bg-blue-50 rounded-xl px-3 py-2 text-xs text-blue-700">
          All parent passwords: <code className="font-bold">test1234</code>
        </div>

        {testStatus === 'idle' || testStatus === 'error' ? (
          <>
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">SEED_SECRET</label>
              <input
                type="password"
                value={testSecret}
                onChange={(e) => setTestSecret(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && runTestSeed()}
                placeholder="your-secret-key"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 outline-none focus:border-blue-400 text-sm"
              />
            </div>
            {testMessage && <p className="text-sm text-red-500">{testMessage}</p>}
            <button
              onClick={runTestSeed}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3.5 rounded-2xl transition-colors"
            >
              Load Test Users →
            </button>
          </>
        ) : testStatus === 'running' ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div className="h-3 bg-blue-500 rounded-full animate-pulse w-full" />
            </div>
            <p className="text-xs text-gray-500 text-center">Hashing passwords &amp; writing to database…</p>
          </>
        ) : (
          <div className="space-y-2">
            <div className="flex items-start gap-3 bg-blue-50 rounded-xl px-4 py-3">
              <span className="text-2xl mt-0.5">✅</span>
              <div>
                <p className="font-bold text-blue-700 text-sm">Test users loaded!</p>
                <p className="text-xs text-gray-500 mt-0.5">{testMessage}</p>
                <a href="/dev" className="text-xs text-blue-600 underline mt-1 inline-block">Quick-login switcher →</a>
              </div>
            </div>
            <button
              onClick={() => { setTestStatus('idle'); setTestMessage(''); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Re-load (safe to run again)
            </button>
          </div>
        )}
      </div>

      {/* ── Section 3: Verify DB ───────────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-purple-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🔍</span>
          <div>
            <p className="font-bold text-gray-800">Verify Database</p>
            <p className="text-xs text-gray-500">Check question counts per topic to confirm seed is complete</p>
          </div>
        </div>

        {verifyStatus === 'idle' && (
          <button
            onClick={runVerify}
            className="w-full bg-purple-500 hover:bg-purple-600 text-white font-bold py-3.5 rounded-2xl transition-colors"
          >
            Check DB Status →
          </button>
        )}

        {verifyStatus === 'loading' && (
          <div className="h-3 bg-purple-200 rounded-full animate-pulse" />
        )}

        {verifyStatus === 'error' && (
          <p className="text-sm text-red-500">Failed to fetch status. Check secret.</p>
        )}

        {verifyStatus === 'done' && verifyData && (
          <div className="space-y-3">
            <div className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-bold ${
              verifyData.healthy ? 'bg-green-50 text-green-700' : 'bg-amber-50 text-amber-700'
            }`}>
              {verifyData.healthy ? '✅' : '⚠️'}
              {verifyData.total.toLocaleString()} questions · {verifyData.topicCount} topics
              {verifyData.emptyTopics.length > 0 && ` · ${verifyData.emptyTopics.length} empty`}
            </div>

            {verifyData.emptyTopics.length > 0 && (
              <div className="bg-red-50 rounded-xl px-3 py-2">
                <p className="text-xs font-bold text-red-600 mb-1">Empty topics (need seeding):</p>
                {verifyData.emptyTopics.map((t) => (
                  <p key={t.id} className="text-xs text-red-500">{t.id} — {t.name}</p>
                ))}
              </div>
            )}

            <div className="space-y-1 max-h-64 overflow-y-auto">
              {verifyData.topics.map((t) => (
                <div key={t.id} className="flex items-center justify-between text-xs py-1 border-b border-gray-50">
                  <span className={`font-medium ${t.count === 0 ? 'text-red-500' : 'text-gray-600'}`}>
                    {t.id}
                  </span>
                  <span className={`font-bold tabular-nums ${t.count === 0 ? 'text-red-500' : t.count < 50 ? 'text-amber-500' : 'text-green-600'}`}>
                    {t.count} Qs
                  </span>
                </div>
              ))}
            </div>

            <button
              onClick={() => { setVerifyStatus('idle'); setVerifyData(null); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Refresh
            </button>
          </div>
        )}
      </div>

      {/* ── Section 4: Fix SubTopics ──────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-amber-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🏷️</span>
          <div>
            <p className="font-bold text-gray-800">Fix SubTopics</p>
            <p className="text-xs text-gray-500">Re-tags question subtopics in DB to match curriculum lessons (Grades 2–9)</p>
          </div>
        </div>

        {fixStatus === 'idle' || fixStatus === 'error' ? (
          <>
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">SEED_SECRET</label>
              <input
                type="password"
                value={fixSecret}
                onChange={(e) => setFixSecret(e.target.value)}
                placeholder="your-secret-key"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 outline-none focus:border-amber-400 text-sm"
              />
            </div>
            {fixMessage && <p className="text-sm text-red-500">{fixMessage}</p>}
            <div className="flex gap-3">
              <button
                onClick={() => runFixSubtopics(true)}
                className="flex-1 bg-amber-100 hover:bg-amber-200 text-amber-800 font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Dry Run (preview)
              </button>
              <button
                onClick={() => runFixSubtopics(false)}
                className="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Apply Fix →
              </button>
            </div>
          </>
        ) : fixStatus === 'running' ? (
          <>
            <div className="h-3 bg-amber-200 rounded-full animate-pulse" />
            <p className="text-xs text-gray-500 text-center">{fixMessage}</p>
          </>
        ) : (
          <div className="space-y-3">
            {/* Summary banner */}
            <div className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-bold ${
              fixReport?.written ? 'bg-green-50 text-green-700' : 'bg-amber-50 text-amber-700'
            }`}>
              {fixReport?.written ? '✅ Written!' : '👀 Dry Run'}
              <span className="font-normal">— {fixMessage}</span>
            </div>

            {fixReport && (
              <>
                {/* Method breakdown */}
                <div className="bg-gray-50 rounded-xl px-3 py-2 text-xs space-y-1">
                  <p className="font-bold text-gray-700">Classification</p>
                  <p>Tagged: <b>{fixReport.stats.tagged}</b> · DB updated: <b>{fixReport.stats.dbUpdated || fixReport.stats.pendingUpdates}</b></p>
                  <p>
                    ID stem: <b>{fixReport.stats.byMethod.id_stem}</b> ·
                    Keyword: <b>{fixReport.stats.byMethod.keyword}</b> ·
                    Fallback: <b>{fixReport.stats.byMethod.fallback}</b>
                  </p>
                </div>

                {/* Data quality */}
                <div className="bg-red-50 rounded-xl px-3 py-2 text-xs space-y-1">
                  <p className="font-bold text-red-700">Data Quality Issues</p>
                  <p>Empty correctAnswer: <b>{fixReport.stats.emptyCorrectAnswer}</b>
                    {Object.entries(fixReport.stats.emptyCorrectBySource).map(([src, cnt]) => (
                      <span key={src} className="ml-2 text-red-500">({src}: {cnt})</span>
                    ))}
                  </p>
                  <p>Empty options: <b>{fixReport.stats.emptyOptions}</b>
                    {Object.entries(fixReport.stats.emptyOptsBySource).map(([src, cnt]) => (
                      <span key={src} className="ml-2 text-red-500">({src}: {cnt})</span>
                    ))}
                  </p>
                  <p>Total unusable: <b>{fixReport.stats.totalUnusable}</b> · Usable (non-G4-ch): <b>{fixReport.stats.usableNonG4}</b></p>
                </div>

                {/* Per-grade distribution */}
                <div className="space-y-2 max-h-80 overflow-y-auto">
                  {Object.entries(fixReport.gradeReport).map(([gradeKey, topics]) => {
                    const total = topics.reduce((s, t) => s + t.count, 0);
                    return (
                      <div key={gradeKey} className="bg-white border border-gray-100 rounded-xl px-3 py-2">
                        <p className="text-xs font-bold text-gray-700 mb-1">
                          {gradeKey.replace('grade', 'Grade ')} ({total} Qs)
                        </p>
                        {topics.map((t) => (
                          <div key={t.topic} className="flex items-center justify-between text-xs py-0.5">
                            <span className="text-gray-600">{t.label}</span>
                            <div className="flex items-center gap-2">
                              <div className="w-20 bg-gray-100 rounded-full h-1.5">
                                <div
                                  className="bg-amber-400 h-1.5 rounded-full"
                                  style={{ width: `${total > 0 ? Math.round((t.count / total) * 100) : 0}%` }}
                                />
                              </div>
                              <span className={`font-bold tabular-nums w-8 text-right ${t.count === 0 ? 'text-red-500' : 'text-gray-600'}`}>
                                {t.count}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    );
                  })}
                </div>
              </>
            )}

            <button
              onClick={() => { setFixStatus('idle'); setFixMessage(''); setFixReport(null); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Run again
            </button>
          </div>
        )}
      </div>

      <p className="text-xs text-gray-500 text-center pb-4">
        All operations use upsert — safe to run multiple times.
      </p>
    </div>
  );
}

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

  // ── Audit difficulty ──────────────────────────────────────────────────────
  const [diffSecret,  setDiffSecret]  = useState('');
  const [diffStatus,  setDiffStatus]  = useState<Status>('idle');
  const [diffMessage, setDiffMessage] = useState('');
  const [diffScored,  setDiffScored]  = useState(0);
  const [diffTotal,   setDiffTotal]   = useState(0);
  const [diffFixed,   setDiffFixed]   = useState(0);
  const [diffMismatches, setDiffMismatches] = useState(0);
  const [diffSummary, setDiffSummary] = useState<Record<string, number>>({});
  const [diffSamples, setDiffSamples] = useState<Array<{ id: string; topic: string; text: string; was: string; now: string; score: number }>>([]);

  // ── Topic Audit ──────────────────────────────────────────────────────────
  const [auditStatus, setAuditStatus] = useState<Status>('idle');
  const [auditMessage, setAuditMessage] = useState('');
  const [auditData, setAuditData] = useState<Record<string, {
    topics: Array<{
      topicId: string; name: string; subTopicKey?: string; examWeight: number;
      total: number; usable: number; easy: number; medium: number; hard: number;
      blueprintNeed: number; coverage: string;
    }>;
    totalQuestions: number; totalUsable: number;
  }> | null>(null);

  // ── Redistribute Grade 4 ─────────────────────────────────────────────────
  const [redistStatus,   setRedistStatus]   = useState<Status>('idle');
  const [redistMessage,  setRedistMessage]  = useState('');
  const [redistTotal,    setRedistTotal]    = useState(0);
  const [redistProcessed, setRedistProcessed] = useState(0);
  const [redistMoved,    setRedistMoved]    = useState(0);
  const [redistByMethod, setRedistByMethod] = useState<Record<string, number>>({});
  const [redistPerTopic, setRedistPerTopic] = useState<Record<string, number>>({});

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

  async function runAuditDifficulty(apply: boolean) {
    const sec = diffSecret || secret || testSecret || fixSecret;
    if (!sec.trim()) { setDiffMessage('Enter your SEED_SECRET first.'); setDiffStatus('error'); return; }
    setDiffStatus('running');
    setDiffMessage(apply ? 'Reclassifying questions…' : 'Scanning questions…');
    setDiffScored(0); setDiffTotal(0); setDiffFixed(0); setDiffMismatches(0);
    setDiffSummary({}); setDiffSamples([]);

    let page = 0;
    let totalQuestions = 0;
    let totalMismatches = 0;
    let totalFixed = 0;
    const cumulSummary: Record<string, number> = {};
    const cumulSamples: typeof diffSamples = [];

    while (true) {
      try {
        const url = `/api/admin/audit-difficulty?secret=${encodeURIComponent(sec)}&page=${page}${apply ? '&apply=1' : ''}`;
        const res  = await fetch(url);
        const text = await res.text();
        let data;
        try { data = JSON.parse(text); } catch {
          setDiffMessage(`Server error: ${text.slice(0, 200)}`);
          setDiffStatus('error');
          return;
        }
        if (!res.ok) { setDiffMessage(data.error ?? 'Something went wrong.'); setDiffStatus('error'); return; }

        // Accumulate stats
        if (data.total) totalQuestions = data.total;
        totalMismatches += data.pageMismatches;
        totalFixed += data.pageUpdated ?? 0;
        for (const [k, v] of Object.entries(data.summary)) {
          cumulSummary[k] = (cumulSummary[k] || 0) + (v as number);
        }
        if (cumulSamples.length < 50) {
          cumulSamples.push(...(data.samples || []));
        }

        // Update UI
        setDiffScored((prev) => prev + data.pageScored);
        setDiffTotal(totalQuestions);
        setDiffMismatches(totalMismatches);
        setDiffFixed(totalFixed);
        setDiffSummary({ ...cumulSummary });
        setDiffSamples([...cumulSamples.slice(0, 50)]);
        setDiffMessage(apply
          ? `Fixing… ${totalFixed} updated so far`
          : `Scanning… ${totalMismatches} mismatches found`);

        if (data.done) {
          setDiffMessage(apply
            ? `Done! ${totalFixed} questions reclassified out of ${totalQuestions}.`
            : `Found ${totalMismatches} misclassified out of ${totalQuestions} questions.`);
          setDiffStatus('done');
          return;
        }
        page = data.nextPage;
      } catch (err) {
        setDiffMessage(`Network error: ${err}`);
        setDiffStatus('error');
        return;
      }
    }
  }

  async function runRedistribute(apply: boolean) {
    const sec = diffSecret || fixSecret || secret || testSecret;
    if (!sec.trim()) { setRedistMessage('Enter your SEED_SECRET first.'); setRedistStatus('error'); return; }
    setRedistStatus('running');
    setRedistMessage(apply ? 'Moving questions to ch-topics...' : 'Analyzing grade4 pool...');
    setRedistProcessed(0); setRedistMoved(0);
    setRedistByMethod({}); setRedistPerTopic({});

    let page = 0;
    let totalQ = 0;
    let processed = 0;
    let moved = 0;
    const cumulMethod: Record<string, number> = {};
    const cumulTopic: Record<string, number> = {};

    while (true) {
      try {
        const url = `/api/admin/redistribute-grade4?secret=${encodeURIComponent(sec)}&page=${page}${apply ? '&apply=1' : ''}`;
        const res = await fetch(url);
        const text = await res.text();
        let data;
        try { data = JSON.parse(text); } catch {
          setRedistMessage(`Server error: ${text.slice(0, 200)}`);
          setRedistStatus('error');
          return;
        }
        if (!res.ok) { setRedistMessage(data.error ?? 'Something went wrong.'); setRedistStatus('error'); return; }

        if (data.total) totalQ = data.total;
        processed += data.pageQuestions;
        moved += data.pageUpdated ?? 0;
        for (const [k, v] of Object.entries(data.byMethod)) {
          cumulMethod[k] = (cumulMethod[k] || 0) + (v as number);
        }
        for (const [k, v] of Object.entries(data.perTopic)) {
          cumulTopic[k] = (cumulTopic[k] || 0) + (v as number);
        }

        setRedistTotal(totalQ);
        setRedistProcessed(processed);
        setRedistMoved(moved);
        setRedistByMethod({ ...cumulMethod });
        setRedistPerTopic({ ...cumulTopic });
        setRedistMessage(apply
          ? `Moving... ${moved} questions redistributed`
          : `Analyzing... ${processed} questions scanned`);

        if (data.done) {
          const totalMapped = Object.values(cumulMethod).reduce((s, v) => s + v, 0) - (cumulMethod.unclassified || 0);
          setRedistMessage(apply
            ? `Done! ${moved} questions moved to ch-topics.`
            : `Found ${totalMapped} classifiable out of ${processed} grade4 questions (${cumulMethod.unclassified || 0} unclassifiable).`);
          setRedistStatus('done');
          return;
        }
        page = data.nextPage;
      } catch (err) {
        setRedistMessage(`Network error: ${err}`);
        setRedistStatus('error');
        return;
      }
    }
  }

  async function runTopicAudit(grade?: number) {
    const sec = diffSecret || fixSecret || secret || testSecret;
    if (!sec.trim()) { setAuditMessage('Enter your SEED_SECRET first.'); setAuditStatus('error'); return; }
    setAuditStatus('running');
    setAuditMessage('Fetching topic coverage...');
    setAuditData(null);
    try {
      const gradeParam = grade ? `&grade=${grade}` : '';
      const res = await fetch(`/api/admin/topic-audit?secret=${encodeURIComponent(sec)}${gradeParam}`);
      const text = await res.text();
      let data;
      try { data = JSON.parse(text); } catch {
        setAuditMessage(`Server error: ${text.slice(0, 200)}`);
        setAuditStatus('error');
        return;
      }
      if (!res.ok) { setAuditMessage(data.error ?? 'Something went wrong.'); setAuditStatus('error'); return; }
      setAuditData(data);
      setAuditMessage('Audit complete.');
      setAuditStatus('done');
    } catch (err) {
      setAuditMessage(`Network error: ${err}`);
      setAuditStatus('error');
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

      {/* ── Section 5: Audit Difficulty ────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-rose-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">⚖️</span>
          <div>
            <p className="font-bold text-gray-800">Audit Difficulty</p>
            <p className="text-xs text-gray-500">Re-scores all questions with the heuristic classifier and fixes mismatches</p>
          </div>
        </div>

        {diffStatus === 'idle' || diffStatus === 'error' ? (
          <>
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">SEED_SECRET</label>
              <input
                type="password"
                value={diffSecret}
                onChange={(e) => setDiffSecret(e.target.value)}
                placeholder="your-secret-key"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 outline-none focus:border-rose-400 text-sm"
              />
            </div>
            {diffMessage && <p className="text-sm text-red-500">{diffMessage}</p>}
            <div className="flex gap-3">
              <button
                onClick={() => runAuditDifficulty(false)}
                className="flex-1 bg-rose-100 hover:bg-rose-200 text-rose-800 font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Dry Run (preview)
              </button>
              <button
                onClick={() => runAuditDifficulty(true)}
                className="flex-1 bg-rose-500 hover:bg-rose-600 text-white font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Apply Fix →
              </button>
            </div>
          </>
        ) : diffStatus === 'running' ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-rose-500 h-3 rounded-full transition-[width] duration-300"
                style={{ width: `${diffTotal > 0 ? Math.round((diffScored / diffTotal) * 100) : 0}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500">
              <span>{diffMessage}</span>
              <span className="font-semibold">{diffScored.toLocaleString()} / {diffTotal.toLocaleString()}</span>
            </div>
          </>
        ) : (
          <div className="space-y-3">
            {/* Summary banner */}
            <div className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-bold ${
              diffFixed > 0 ? 'bg-green-50 text-green-700' : 'bg-rose-50 text-rose-700'
            }`}>
              {diffFixed > 0 ? '✅ Applied!' : '👀 Dry Run'}
              <span className="font-normal">— {diffMessage}</span>
            </div>

            {/* Stats row */}
            <div className="flex gap-3 text-center">
              <div className="flex-1 bg-gray-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-gray-800">{diffScored.toLocaleString()}</p>
                <p className="text-[10px] font-semibold text-gray-500">Scanned</p>
              </div>
              <div className="flex-1 bg-rose-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-rose-600">{diffMismatches.toLocaleString()}</p>
                <p className="text-[10px] font-semibold text-gray-500">Mismatches</p>
              </div>
              {diffFixed > 0 && (
                <div className="flex-1 bg-green-50 rounded-xl px-2 py-2">
                  <p className="text-lg font-extrabold text-green-600">{diffFixed.toLocaleString()}</p>
                  <p className="text-[10px] font-semibold text-gray-500">Fixed</p>
                </div>
              )}
            </div>

            {/* Transition summary */}
            {Object.keys(diffSummary).length > 0 && (
              <div className="bg-gray-50 rounded-xl px-3 py-2 text-xs space-y-1">
                <p className="font-bold text-gray-700">Transitions</p>
                {Object.entries(diffSummary).map(([key, cnt]) => (
                  <p key={key}>{key}: <b>{cnt}</b></p>
                ))}
              </div>
            )}

            {/* Sample mismatches */}
            {diffSamples.length > 0 && (
              <div className="space-y-2 max-h-64 overflow-y-auto">
                <p className="text-xs font-bold text-gray-700">Sample Mismatches ({diffSamples.length})</p>
                {diffSamples.map((s) => (
                  <div key={s.id} className="bg-white border border-gray-100 rounded-xl px-3 py-2 text-xs">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-1.5 py-0.5 rounded-full font-bold ${
                        s.was === 'Easy' ? 'bg-green-50 text-green-700' : s.was === 'Medium' ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700'
                      }`}>{s.was}</span>
                      <span>→</span>
                      <span className={`px-1.5 py-0.5 rounded-full font-bold ${
                        s.now === 'Easy' ? 'bg-green-50 text-green-700' : s.now === 'Medium' ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700'
                      }`}>{s.now}</span>
                      <span className="text-gray-400 ml-auto">score: {s.score}</span>
                    </div>
                    <p className="text-gray-600 leading-snug">{s.text}</p>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={() => { setDiffStatus('idle'); setDiffMessage(''); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Run again
            </button>
          </div>
        )}
      </div>

      {/* ── Section 6: Redistribute Grade 4 ────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-indigo-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl" aria-hidden="true">🔀</span>
          <div>
            <p className="font-bold text-gray-800">Redistribute Grade 4</p>
            <p className="text-xs text-gray-500">Moves ~2,600 flat &ldquo;grade4&rdquo; pool questions into correct ch-topic buckets</p>
          </div>
        </div>

        {redistStatus === 'idle' || redistStatus === 'error' ? (
          <>
            {redistMessage && <p className="text-sm text-red-500">{redistMessage}</p>}
            <div className="flex gap-3">
              <button
                onClick={() => runRedistribute(false)}
                className="flex-1 bg-indigo-100 hover:bg-indigo-200 text-indigo-800 font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Dry Run (preview)
              </button>
              <button
                onClick={() => runRedistribute(true)}
                className="flex-1 bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Apply →
              </button>
            </div>
          </>
        ) : redistStatus === 'running' ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-indigo-500 h-3 rounded-full transition-[width] duration-300"
                style={{ width: `${redistTotal > 0 ? Math.round((redistProcessed / redistTotal) * 100) : 0}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500">
              <span>{redistMessage}</span>
              <span className="font-semibold">{redistProcessed} / {redistTotal}</span>
            </div>
          </>
        ) : (
          <div className="space-y-3">
            {/* Summary banner */}
            <div className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-bold ${
              redistMoved > 0 ? 'bg-green-50 text-green-700' : 'bg-indigo-50 text-indigo-700'
            }`}>
              {redistMoved > 0 ? '✅ Applied!' : '👀 Dry Run'}
              <span className="font-normal">— {redistMessage}</span>
            </div>

            {/* Stats row */}
            <div className="flex gap-3 text-center">
              <div className="flex-1 bg-gray-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-gray-800">{redistProcessed.toLocaleString()}</p>
                <p className="text-[10px] font-semibold text-gray-500">Scanned</p>
              </div>
              <div className="flex-1 bg-indigo-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-indigo-600">
                  {Object.values(redistByMethod).reduce((s, v) => s + v, 0) - (redistByMethod.unclassified || 0)}
                </p>
                <p className="text-[10px] font-semibold text-gray-500">Mapped</p>
              </div>
              {redistMoved > 0 && (
                <div className="flex-1 bg-green-50 rounded-xl px-2 py-2">
                  <p className="text-lg font-extrabold text-green-600">{redistMoved.toLocaleString()}</p>
                  <p className="text-[10px] font-semibold text-gray-500">Moved</p>
                </div>
              )}
            </div>

            {/* Method breakdown */}
            {Object.keys(redistByMethod).length > 0 && (
              <div className="bg-gray-50 rounded-xl px-3 py-2 text-xs space-y-1">
                <p className="font-bold text-gray-700">Classification Method</p>
                {Object.entries(redistByMethod).map(([key, cnt]) => (
                  <p key={key}>{key}: <b>{cnt}</b></p>
                ))}
              </div>
            )}

            {/* Per-topic distribution */}
            {Object.keys(redistPerTopic).length > 0 && (
              <div className="space-y-1 max-h-48 overflow-y-auto bg-gray-50 rounded-xl px-3 py-2">
                <p className="text-xs font-bold text-gray-700 mb-1">Target Topics</p>
                {Object.entries(redistPerTopic)
                  .sort(([, a], [, b]) => b - a)
                  .map(([topic, cnt]) => (
                    <div key={topic} className="flex items-center justify-between text-xs py-0.5">
                      <span className="text-gray-600">{topic}</span>
                      <span className="font-bold tabular-nums text-indigo-600">{cnt}</span>
                    </div>
                  ))}
              </div>
            )}

            <button
              onClick={() => { setRedistStatus('idle'); setRedistMessage(''); }}
              className="w-full text-xs text-gray-500 hover:text-gray-600 py-1"
            >
              Run again
            </button>
          </div>
        )}
      </div>

      {/* ── Section 7: Topic Audit ──────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-teal-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl" aria-hidden="true">📊</span>
          <div>
            <p className="font-bold text-gray-800">Topic Audit</p>
            <p className="text-xs text-gray-500">Per-topic question counts, difficulty breakdown, and blueprint coverage</p>
          </div>
        </div>

        {auditStatus === 'idle' || auditStatus === 'error' ? (
          <>
            {auditMessage && <p className="text-sm text-red-500">{auditMessage}</p>}
            <div className="flex gap-3">
              <button
                onClick={() => runTopicAudit()}
                className="flex-1 bg-teal-500 hover:bg-teal-600 text-white font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Audit All Grades
              </button>
              <button
                onClick={() => runTopicAudit(4)}
                className="flex-1 bg-teal-100 hover:bg-teal-200 text-teal-800 font-bold py-3.5 rounded-2xl transition-colors text-sm"
              >
                Grade 4 Only
              </button>
            </div>
          </>
        ) : auditStatus === 'running' ? (
          <>
            <div className="h-3 bg-teal-200 rounded-full animate-pulse" />
            <p className="text-xs text-gray-500 text-center">{auditMessage}</p>
          </>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-bold bg-teal-50 text-teal-700">
              ✅ {auditMessage}
            </div>

            {auditData && (
              <div className="space-y-4 max-h-[500px] overflow-y-auto">
                {Object.entries(auditData).map(([gradeKey, gradeData]) => (
                  <div key={gradeKey} className="bg-white border border-gray-100 rounded-xl px-3 py-3">
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-sm font-extrabold text-gray-800">
                        {gradeKey.replace('grade', 'Grade ')}
                      </p>
                      <p className="text-xs text-gray-500">
                        {gradeData.totalUsable} usable / {gradeData.totalQuestions} total
                      </p>
                    </div>

                    <div className="space-y-1.5">
                      {gradeData.topics.map((t) => {
                        const coverageColor = {
                          empty: 'text-red-600 bg-red-50',
                          low: 'text-red-500 bg-red-50',
                          thin: 'text-amber-600 bg-amber-50',
                          ok: 'text-gray-600 bg-gray-50',
                          rich: 'text-green-600 bg-green-50',
                        }[t.coverage] ?? 'text-gray-600 bg-gray-50';

                        return (
                          <div key={`${gradeKey}-${t.topicId}-${t.subTopicKey ?? ''}`} className="flex items-center gap-2 text-xs">
                            <div className="flex-1 min-w-0">
                              <p className="font-semibold text-gray-700 truncate">{t.name}</p>
                              <p className="text-gray-400">
                                {t.topicId}{t.subTopicKey ? ` → ${t.subTopicKey}` : ''}
                              </p>
                            </div>
                            <div className="flex items-center gap-1.5 flex-shrink-0">
                              <span className="text-green-600 font-bold">{t.easy}E</span>
                              <span className="text-amber-600 font-bold">{t.medium}M</span>
                              <span className="text-red-600 font-bold">{t.hard}H</span>
                            </div>
                            <div className="flex items-center gap-1.5 flex-shrink-0">
                              <span className="font-bold tabular-nums w-8 text-right text-gray-700">{t.usable}</span>
                              <span className="text-gray-400">/</span>
                              <span className="font-semibold tabular-nums w-6 text-gray-500">{t.blueprintNeed}</span>
                            </div>
                            <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-bold ${coverageColor}`}>
                              {t.coverage}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={() => { setAuditStatus('idle'); setAuditMessage(''); setAuditData(null); }}
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

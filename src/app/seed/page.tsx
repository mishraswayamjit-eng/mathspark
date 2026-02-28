'use client';

import { useState } from 'react';

type Status = 'idle' | 'running' | 'done' | 'error';

export default function SeedPage() {
  // ── Questions seed ──────────────────────────────────────────────────────────
  const [secret,  setSecret]  = useState('');
  const [status,  setStatus]  = useState<Status>('idle');
  const [seeded,  setSeeded]  = useState(0);
  const [total,   setTotal]   = useState(2505);
  const [message, setMessage] = useState('');

  // ── Test users seed (completely independent) ────────────────────────────────
  const [testSecret,  setTestSecret]  = useState('');
  const [testStatus,  setTestStatus]  = useState<Status>('idle');
  const [testMessage, setTestMessage] = useState('');

  // ── Handlers ────────────────────────────────────────────────────────────────
  async function runSeed() {
    if (!secret.trim()) { setMessage('Enter your SEED_SECRET first.'); return; }
    setStatus('running');
    setMessage('Seeding topics…');
    setSeeded(0);
    let page = 0;
    while (true) {
      try {
        const res  = await fetch(`/api/seed?secret=${encodeURIComponent(secret)}&page=${page}`);
        const data = await res.json();
        if (!res.ok) { setMessage(data.error ?? 'Something went wrong.'); setStatus('error'); return; }
        setSeeded(data.seeded ?? 0);
        setTotal(data.total   ?? 2505);
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

  const pct = total > 0 ? Math.round((seeded / total) * 100) : 0;

  return (
    <div className="min-h-screen flex flex-col items-center justify-start px-6 py-10 gap-8 max-w-md mx-auto">

      {/* ── Section 1: Questions ─────────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-green-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🌱</span>
          <div>
            <p className="font-bold text-gray-800">Seed Questions</p>
            <p className="text-xs text-gray-400">Loads all 2,505 questions into the database</p>
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
              className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3.5 rounded-2xl transition-colors"
            >
              Start Seeding →
            </button>
          </>
        ) : status === 'running' ? (
          <>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-green-500 h-3 rounded-full transition-all duration-300"
                style={{ width: `${pct}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500">
              <span>{message}</span>
              <span className="font-semibold">{seeded} / {total}</span>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-3 bg-green-50 rounded-xl px-4 py-3">
            <span className="text-2xl">🎉</span>
            <div>
              <p className="font-bold text-green-700 text-sm">All {total} questions loaded!</p>
              <a href="/start" className="text-xs text-green-600 underline">Open MathSpark →</a>
            </div>
          </div>
        )}
      </div>

      {/* ── Section 2: Test Users ─────────────────────────────────────────────── */}
      <div className="w-full bg-white border-2 border-blue-200 rounded-2xl p-6 space-y-4 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-3xl">👨‍👩‍👧‍👦</span>
          <div>
            <p className="font-bold text-gray-800">Load Test Users</p>
            <p className="text-xs text-gray-400">5 families · 10 students · subscriptions, orders, progress &amp; streaks</p>
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
            {/* Indeterminate animated bar */}
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div className="h-3 bg-blue-500 rounded-full animate-pulse w-full" />
            </div>
            <p className="text-xs text-gray-500 text-center">Hashing passwords &amp; writing to database…</p>
          </>
        ) : (
          <div className="flex items-start gap-3 bg-blue-50 rounded-xl px-4 py-3">
            <span className="text-2xl mt-0.5">✅</span>
            <div>
              <p className="font-bold text-blue-700 text-sm">Test users loaded!</p>
              <p className="text-xs text-gray-500 mt-0.5">{testMessage}</p>
            </div>
          </div>
        )}
      </div>

      <p className="text-xs text-gray-400 text-center pb-4">
        Both sections use upsert — safe to run multiple times.
      </p>
    </div>
  );
}

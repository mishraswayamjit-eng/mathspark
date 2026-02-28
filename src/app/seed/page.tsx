'use client';

import { useState } from 'react';

type Status = 'idle' | 'running' | 'done' | 'error';
type TestStatus = 'idle' | 'running' | 'done' | 'error';

export default function SeedPage() {
  const [secret,     setSecret]     = useState('');
  const [status,     setStatus]     = useState<Status>('idle');
  const [seeded,     setSeeded]     = useState(0);
  const [total,      setTotal]      = useState(2505);
  const [message,    setMessage]    = useState('');
  const [testStatus, setTestStatus] = useState<TestStatus>('idle');
  const [testMsg,    setTestMsg]    = useState('');

  async function runTestSeed() {
    if (!secret.trim()) { setTestMsg('Enter your SEED_SECRET first.'); setTestStatus('error'); return; }
    setTestStatus('running');
    setTestMsg('Hashing passwords & seeding test users…');
    try {
      const res  = await fetch(`/api/seed-test?secret=${encodeURIComponent(secret)}`);
      const data = await res.json();
      if (!res.ok) { setTestMsg(data.error ?? 'Something went wrong.'); setTestStatus('error'); return; }
      const s = data.seeded;
      setTestMsg(`Done! ${s.parents} parents · ${s.students} students · ${s.orders} orders · ${s.progress} progress rows · ${s.usageLogs} usage logs`);
      setTestStatus('done');
    } catch (err) {
      setTestMsg(`Network error: ${err}`);
      setTestStatus('error');
    }
  }

  async function runSeed() {
    if (!secret.trim()) { setMessage('Enter your SEED_SECRET first.'); return; }
    setStatus('running');
    setMessage('Seeding topics…');
    setSeeded(0);

    let page = 0;

    while (true) {
      try {
        const res = await fetch(`/api/seed?secret=${encodeURIComponent(secret)}&page=${page}`);
        const data = await res.json();

        if (!res.ok) {
          setMessage(data.error ?? 'Something went wrong.');
          setStatus('error');
          return;
        }

        setSeeded(data.seeded ?? 0);
        setTotal(data.total  ?? 2505);
        setMessage(data.message ?? '');

        if (data.done) {
          setStatus('done');
          return;
        }

        page = data.nextPage;
      } catch (err) {
        setMessage(`Network error: ${err}`);
        setStatus('error');
        return;
      }
    }
  }

  const pct = total > 0 ? Math.round((seeded / total) * 100) : 0;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-6 max-w-md mx-auto">
      <div className="text-5xl">🌱</div>
      <h1 className="text-2xl font-bold text-gray-800 text-center">Seed MathSpark Database</h1>
      <p className="text-gray-500 text-sm text-center">
        This page loads all 2,505 questions into the database.<br />
        Run it once after your first Vercel deploy.
      </p>

      {status === 'idle' || status === 'error' ? (
        <div className="w-full space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">
              SEED_SECRET (from Vercel env vars)
            </label>
            <input
              type="password"
              value={secret}
              onChange={(e) => setSecret(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && runSeed()}
              placeholder="your-secret-key"
              className="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 outline-none focus:border-blue-400"
            />
          </div>

          {message && (
            <p className={`text-sm ${status === 'error' ? 'text-red-500' : 'text-gray-500'}`}>
              {message}
            </p>
          )}

          <button
            onClick={runSeed}
            className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
          >
            Start Seeding →
          </button>
        </div>
      ) : status === 'running' ? (
        <div className="w-full space-y-4">
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="bg-green-500 h-4 rounded-full transition-all duration-300"
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="flex justify-between text-sm text-gray-600">
            <span>{message}</span>
            <span>{seeded} / {total}</span>
          </div>
          <div className="text-center text-2xl animate-spin">⚙️</div>
        </div>
      ) : (
        <div className="text-center space-y-4">
          <div className="text-6xl">🎉</div>
          <p className="text-xl font-bold text-green-700">All {total} questions loaded!</p>
          <a
            href="/start"
            className="block w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg text-center transition-colors"
          >
            Open MathSpark 🚀
          </a>
        </div>
      )}

      <p className="text-xs text-gray-400 text-center">
        This page is safe to run multiple times — it uses upsert so no duplicates.
      </p>

      {/* ── Test User Seed ── */}
      <div className="w-full border-t border-gray-200 pt-6 space-y-3">
        <p className="text-sm font-bold text-gray-700 text-center">Load Test Users</p>
        <p className="text-xs text-gray-400 text-center">
          5 families · 10 students · subscriptions, orders, progress &amp; streaks.<br />
          All parent passwords: <code className="bg-gray-100 px-1 rounded">test1234</code>
        </p>

        {testStatus === 'running' ? (
          <div className="text-center text-sm text-gray-500 animate-pulse">{testMsg}</div>
        ) : testStatus === 'done' ? (
          <div className="text-center text-sm text-green-600 font-semibold">✓ {testMsg}</div>
        ) : (
          <>
            {testMsg && (
              <p className={`text-sm text-center ${testStatus === 'error' ? 'text-red-500' : 'text-gray-500'}`}>
                {testMsg}
              </p>
            )}
            <button
              onClick={runTestSeed}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 rounded-2xl text-sm transition-colors"
            >
              Load Test Users →
            </button>
          </>
        )}
      </div>
    </div>
  );
}

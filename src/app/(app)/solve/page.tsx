'use client';

import { useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

type State = 'idle' | 'loading' | 'done' | 'error';

interface SolveResponse {
  explanation?: string;
  path?: 'grounded' | 'fresh';
  flagged?: boolean;
  error?: string;
}

/**
 * Feature 5a — Homework solve-on-demand.
 * Posts the typed problem to /api/solve (self-consistency verified). Always
 * carries a "double-check yourself" disclaimer from the server. Disabled unless
 * AI_SOLVE_ENABLED — the server returns 403, which we surface gently.
 */
export default function SolvePage() {
  const [problem, setProblem] = useState('');
  const [state, setState] = useState<State>('idle');
  const [answer, setAnswer] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  async function handleSolve() {
    const text = problem.trim();
    if (!text || state === 'loading') return;
    setState('loading');
    setAnswer('');
    setErrorMsg('');
    try {
      const res = await fetch('/api/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problemText: text }),
      });
      const data = (await res.json()) as SolveResponse;
      if (!res.ok || !data.explanation) {
        setErrorMsg(data.error ?? "I couldn't work this one out — try asking Sparky in Chat!");
        setState('error');
        return;
      }
      setAnswer(data.explanation);
      setState('done');
    } catch (err) {
      logError('[solve] request', err);
      setErrorMsg("Something went wrong — please try again in a moment.");
      setState('error');
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link
          href="/home"
          className="text-white/60 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <span className="text-lg" aria-hidden="true">🧮</span>
        <h1 className="text-white font-extrabold text-lg">Homework Helper</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        <div className="flex items-center gap-3 mb-4">
          <Sparky mood="encouraging" size={48} />
          <p className="text-sm text-gray-600 font-medium">
            Type a math problem and I&apos;ll work through it step by step. I&apos;ll
            even double-check my own work — but you should always check it too!
          </p>
        </div>

        <label htmlFor="problem" className="sr-only">Math problem</label>
        <textarea
          id="problem"
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          placeholder="e.g. What is 3/4 + 2/5?"
          rows={4}
          className="w-full rounded-2xl border border-gray-200 p-4 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-duo-blue/40 resize-none"
        />

        <button
          onClick={handleSolve}
          disabled={!problem.trim() || state === 'loading'}
          className="mt-3 w-full min-h-[48px] rounded-2xl bg-duo-green text-white font-extrabold text-sm active:scale-[0.98] transition-transform disabled:opacity-40"
        >
          {state === 'loading' ? 'Working it out…' : 'Solve it!'}
        </button>

        {state === 'loading' && (
          <div className="mt-6 flex flex-col items-center gap-3">
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={64} />
            </div>
            <p className="text-sm text-gray-500 font-semibold">
              Checking my work carefully…
            </p>
          </div>
        )}

        {state === 'error' && (
          <div className="mt-5 bg-amber-50 border border-amber-200 rounded-2xl px-4 py-3">
            <p className="text-sm text-amber-800 font-medium">{errorMsg}</p>
            <Link
              href="/chat"
              className="inline-block mt-2 text-sm font-bold text-duo-blue underline underline-offset-2"
            >
              Ask Sparky in Chat →
            </Link>
          </div>
        )}

        {state === 'done' && answer && (
          <div className="mt-5 bg-white border border-gray-100 rounded-2xl px-4 py-4 shadow-sm">
            <div className="flex items-center gap-2 mb-2">
              <Sparky mood="celebrating" size={28} />
              <p className="text-xs font-extrabold text-duo-green-dark uppercase tracking-wide">
                Here&apos;s how I&apos;d solve it
              </p>
            </div>
            <p className="text-sm text-gray-700 font-medium leading-snug whitespace-pre-wrap">
              {answer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

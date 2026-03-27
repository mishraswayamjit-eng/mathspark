'use client';

import { useState, useEffect } from 'react';

interface PreviewQ {
  id: string; questionText: string;
  option1: string; option2: string; option3: string; option4: string;
  correctAnswer: string;
}
const OPT_KEYS = ['A', 'B', 'C', 'D'] as const;

export default function HeroDemo() {
  const [q, setQ]               = useState<PreviewQ | null>(null);
  const [answered, setAnswered] = useState(false);
  const [badges,   setBadges]   = useState(false);

  useEffect(() => {
    fetch('/api/questions/preview')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then(d => { if (d.questions?.[0]) setQ(d.questions[0]); })
      .catch((err) => console.error('[fetch]', err));
  }, []);

  useEffect(() => {
    if (!q) return;
    const t1 = setTimeout(() => setAnswered(true), 2200);
    const t2 = setTimeout(() => setBadges(true),   2900);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [q]);

  if (!q) return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 space-y-3 animate-pulse shadow-lg">
      <div className="h-3 bg-gray-100 rounded w-1/2" />
      <div className="h-4 bg-gray-100 rounded w-full" />
      <div className="h-4 bg-gray-100 rounded w-4/5" />
      {[0,1,2,3].map(i => <div key={i} className="h-11 bg-gray-100 rounded-xl" />)}
    </div>
  );

  const opts = [q.option1, q.option2, q.option3, q.option4];

  return (
    <div className="relative mt-6 lg:mt-0">
      {badges && (
        <>
          <div className="absolute -top-3 right-3 bg-duo-orange text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
            🔥 12-Day Streak
          </div>
          <div className="absolute -bottom-3 left-3 bg-duo-green text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
            ⭐ +20 XP
          </div>
        </>
      )}
      <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-lg">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-[10px] font-bold text-duo-blue bg-blue-50 px-2 py-0.5 rounded-full uppercase tracking-wide">Real IPM Question</span>
        </div>
        <p className="text-duo-dark text-sm font-semibold leading-relaxed mb-4">{q.questionText}</p>
        <div className="space-y-2">
          {opts.map((opt, i) => {
            const key     = OPT_KEYS[i];
            const correct = key === q.correctAnswer;
            return (
              <div
                key={key}
                className={`flex items-center gap-3 border-2 rounded-xl px-3 py-2.5 transition-colors duration-500 ${
                  !answered ? 'border-gray-200 text-gray-500'
                  : correct  ? 'border-duo-green bg-green-50 text-duo-dark'
                  :            'border-gray-100 text-gray-300'
                }`}
              >
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${answered && correct ? 'bg-duo-green text-white' : 'bg-gray-100 text-gray-500'}`}>
                  {key}
                </span>
                <span className="text-sm">{opt}</span>
                {answered && correct && <span className="ml-auto text-duo-green">✓</span>}
              </div>
            );
          })}
        </div>
        {answered && (
          <div className="mt-3 flex items-center gap-2 bg-green-50 border border-green-200 rounded-xl px-3 py-2 animate-fade-in">
            <span className="text-duo-green text-sm font-extrabold">Excellent thinking! 🧠</span>
          </div>
        )}
      </div>
    </div>
  );
}

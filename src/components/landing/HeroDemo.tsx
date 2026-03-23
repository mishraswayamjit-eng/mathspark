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
      .then(r => r.json())
      .then(d => { if (d.questions?.[0]) setQ(d.questions[0]); })
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!q) return;
    const t1 = setTimeout(() => setAnswered(true), 2200);
    const t2 = setTimeout(() => setBadges(true),   2900);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [q]);

  if (!q) return (
    <div className="bg-[#1a2f3a] border border-white/10 rounded-2xl p-5 space-y-3 animate-pulse">
      <div className="h-3 bg-white/10 rounded w-1/2" />
      <div className="h-4 bg-white/10 rounded w-full" />
      <div className="h-4 bg-white/10 rounded w-4/5" />
      {[0,1,2,3].map(i => <div key={i} className="h-11 bg-white/10 rounded-xl" />)}
    </div>
  );

  const opts = [q.option1, q.option2, q.option3, q.option4];

  return (
    <div className="relative mt-6 lg:mt-0">
      {badges && (
        <>
          <div className="absolute -top-3 right-3 bg-[#FF9600] text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
            🔥 12-Day Streak
          </div>
          <div className="absolute -bottom-3 left-3 bg-[#58CC02] text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
            ⭐ +20 XP
          </div>
        </>
      )}
      <div className="bg-[#1a2f3a] border border-white/10 rounded-2xl p-5 shadow-2xl">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-[10px] font-bold text-[#1CB0F6] bg-[#1CB0F6]/10 px-2 py-0.5 rounded-full uppercase tracking-wide">Real IPM Question</span>
        </div>
        <p className="text-white text-sm font-semibold leading-relaxed mb-4">{q.questionText}</p>
        <div className="space-y-2">
          {opts.map((opt, i) => {
            const key     = OPT_KEYS[i];
            const correct = key === q.correctAnswer;
            return (
              <div
                key={key}
                className={`flex items-center gap-3 border-2 rounded-xl px-3 py-2.5 transition-colors duration-500 ${
                  !answered ? 'border-white/15 text-white/60'
                  : correct  ? 'border-[#58CC02] bg-[#58CC02]/10 text-white'
                  :            'border-white/5 text-white/25'
                }`}
              >
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${answered && correct ? 'bg-[#58CC02] text-white' : 'bg-white/10 text-white/40'}`}>
                  {key}
                </span>
                <span className="text-sm">{opt}</span>
                {answered && correct && <span className="ml-auto text-[#58CC02]">✓</span>}
              </div>
            );
          })}
        </div>
        {answered && (
          <div className="mt-3 flex items-center gap-2 bg-[#58CC02]/10 border border-[#58CC02]/20 rounded-xl px-3 py-2 animate-fade-in">
            <span className="text-[#58CC02] text-sm font-extrabold">Excellent thinking! 🧠</span>
          </div>
        )}
      </div>
    </div>
  );
}

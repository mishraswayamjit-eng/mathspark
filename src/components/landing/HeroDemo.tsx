'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface PreviewQ {
  id: string; questionText: string;
  option1: string; option2: string; option3: string; option4: string;
  correctAnswer: string;
}
const OPT_KEYS = ['A', 'B', 'C', 'D'] as const;

export default function HeroDemo() {
  const [q, setQ]               = useState<PreviewQ | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [showCta, setShowCta]   = useState(false);

  useEffect(() => {
    fetch('/api/questions/preview')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then(d => { if (d.questions?.[0]) setQ(d.questions[0]); })
      .catch((err) => console.error('[fetch]', err));
  }, []);

  if (!q) return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 space-y-3 animate-pulse shadow-lg">
      <div className="h-3 bg-gray-100 rounded w-1/2" />
      <div className="h-4 bg-gray-100 rounded w-full" />
      <div className="h-4 bg-gray-100 rounded w-4/5" />
      {[0,1,2,3].map(i => <div key={i} className="h-11 bg-gray-100 rounded-xl" />)}
    </div>
  );

  const opts = [q.option1, q.option2, q.option3, q.option4];
  const answered = selected !== null;
  const isCorrect = selected === q.correctAnswer;

  function handleSelect(key: string) {
    if (answered) return;
    setSelected(key);
    setTimeout(() => setShowCta(true), 800);
  }

  return (
    <div className="relative mt-6 lg:mt-0">
      {answered && (
        <>
          {isCorrect && (
            <div className="absolute -top-3 right-3 bg-duo-green text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
              ✓ Correct!
            </div>
          )}
          <div className="absolute -bottom-3 left-3 bg-duo-orange text-white text-xs font-extrabold px-3 py-1.5 rounded-full shadow-lg z-10 animate-pop-in whitespace-nowrap">
            <span aria-hidden="true">⭐ </span>+20 XP
          </div>
        </>
      )}
      <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-lg">
        <div className="flex items-center justify-between mb-3">
          <span className="text-[10px] font-bold text-duo-blue bg-blue-50 px-2 py-0.5 rounded-full uppercase tracking-wide">Real IPM Question</span>
          {!answered && (
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wide">Tap to answer</span>
          )}
        </div>
        <p className="text-duo-dark text-sm font-semibold leading-relaxed mb-4">{q.questionText}</p>
        <div className="space-y-2">
          {opts.map((opt, i) => {
            const key     = OPT_KEYS[i];
            const correct = key === q.correctAnswer;
            const isSelected = key === selected;
            return (
              <button
                key={key}
                onClick={() => handleSelect(key)}
                disabled={answered}
                className={`flex items-center gap-3 border-2 rounded-xl px-3 py-2.5 w-full text-left transition-colors duration-300 min-h-0 ${
                  !answered
                    ? 'border-gray-200 text-gray-600 hover:border-duo-blue hover:bg-blue-50/30 cursor-pointer active:scale-[0.98]'
                    : correct
                      ? 'border-duo-green bg-green-50 text-duo-dark'
                      : isSelected && !correct
                        ? 'border-duo-red bg-red-50 text-gray-500'
                        : 'border-gray-100 text-gray-300'
                }`}
              >
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                  answered && correct ? 'bg-duo-green text-white'
                  : answered && isSelected && !correct ? 'bg-duo-red text-white'
                  : 'bg-gray-100 text-gray-500'
                }`}>
                  {answered && correct ? '✓' : answered && isSelected && !correct ? '✗' : key}
                </span>
                <span className="text-sm">{opt}</span>
              </button>
            );
          })}
        </div>
        {answered && (
          <div className={`mt-3 flex items-center gap-2 border rounded-xl px-3 py-2 animate-fade-in ${
            isCorrect ? 'bg-green-50 border-green-200' : 'bg-amber-50 border-amber-200'
          }`}>
            <span className={`text-sm font-extrabold ${isCorrect ? 'text-duo-green' : 'text-duo-orange'}`}>
              {isCorrect ? 'Excellent thinking!' : 'Good try! The correct answer is shown above.'}
            </span>
          </div>
        )}
        {showCta && (
          <Link
            href="/start"
            className="mt-3 block w-full text-center bg-duo-green text-white font-extrabold py-3 rounded-xl transition-colors hover:bg-[#46a302] animate-fade-in text-sm"
          >
            Try More Questions — Free
          </Link>
        )}
      </div>
    </div>
  );
}

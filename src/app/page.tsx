'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface PreviewQuestion {
  id:            string;
  questionText:  string;
  questionLatex: string;
  option1: string; option2: string; option3: string; option4: string;
  correctAnswer: string;
  hint1: string;
}

const OPTIONS = ['A', 'B', 'C', 'D'] as const;

function MiniQuestion({
  q, onAnswer,
}: {
  q: PreviewQuestion;
  onAnswer: (correct: boolean) => void;
}) {
  const [selected, setSelected] = useState<string | null>(null);

  function pick(opt: string) {
    if (selected) return;
    setSelected(opt);
    setTimeout(() => onAnswer(opt === q.correctAnswer), 800);
  }

  const opts = [q.option1, q.option2, q.option3, q.option4];

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4">
      <p className="text-gray-800 font-semibold text-sm leading-relaxed mb-4">{q.questionText}</p>
      <div className="space-y-2">
        {opts.map((opt, i) => {
          const key   = OPTIONS[i];
          const state = !selected ? 'idle'
            : key === q.correctAnswer           ? 'correct'
            : key === selected                  ? 'wrong'
            : 'dim';
          return (
            <button
              key={key}
              onClick={() => pick(key)}
              className={`w-full text-left rounded-xl px-4 py-3 text-sm font-semibold border-2 transition-all ${
                state === 'idle'    ? 'border-gray-200 hover:border-[#1CB0F6] text-gray-700'
                : state === 'correct' ? 'border-[#58CC02] bg-[#58CC02]/10 text-[#2a7a00]'
                : state === 'wrong'   ? 'border-[#FF4B4B] bg-[#FF4B4B]/10 text-[#cc2222]'
                : 'border-gray-100 text-gray-300'
              }`}
            >
              <span className="font-bold mr-2">{key}.</span>{opt}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default function LandingPage() {
  const router = useRouter();

  // Redirect existing students directly to /chapters
  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (id) router.replace('/chapters');
  }, [router]);

  const [questions, setQuestions]   = useState<PreviewQuestion[]>([]);
  const [current,   setCurrent]     = useState(0);
  const [score,     setScore]       = useState(0);
  const [done,      setDone]        = useState(false);
  const [started,   setStarted]     = useState(false);
  const [loading,   setLoading]     = useState(false);

  async function startTrial() {
    setLoading(true);
    try {
      const res  = await fetch('/api/questions/preview');
      const data = await res.json();
      if (data.questions?.length) {
        setQuestions(data.questions);
        setStarted(true);
      }
    } catch { /* ignore */ }
    setLoading(false);
  }

  function handleAnswer(correct: boolean) {
    if (correct) setScore((s) => s + 1);
    if (current + 1 >= questions.length) setDone(true);
    else setCurrent((c) => c + 1);
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="bg-[#131F24] px-4 py-3 flex items-center justify-between sticky top-0 z-40">
        <span className="text-white font-extrabold text-lg">MathSpark ⭐</span>
        <div className="flex items-center gap-3">
          <Link href="/pricing" className="text-white/60 text-sm font-semibold hover:text-white transition-colors">Pricing</Link>
          <Link href="/auth/login" className="bg-[#58CC02] text-white text-sm font-extrabold px-4 py-1.5 rounded-xl hover:bg-[#46a302] transition-colors">
            Sign in
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <div className="bg-gradient-to-b from-[#131F24] to-[#1a3040] px-4 pt-12 pb-14 text-center">
        <div className="text-6xl mb-4">⭐</div>
        <h1 className="text-2xl font-extrabold text-white leading-tight">
          India's smartest IPM math practice — powered by AI
        </h1>
        <p className="text-white/60 text-sm mt-3 max-w-xs mx-auto">
          2,505 expert-crafted questions · 21 chapters · Adaptive AI that learns with your child
        </p>

        {/* Mini practice widget */}
        <div className="mt-8">
          {!started ? (
            <div>
              <button
                onClick={startTrial}
                disabled={loading}
                className="bg-[#58CC02] hover:bg-[#46a302] disabled:opacity-50 text-white font-extrabold px-8 py-4 rounded-2xl text-lg transition-colors shadow-lg"
              >
                {loading ? 'Loading…' : 'Try 3 questions FREE →'}
              </button>
              <p className="text-white/30 text-xs mt-2">No login required</p>
            </div>
          ) : done ? (
            <div className="bg-white/10 rounded-2xl p-6 max-w-xs mx-auto">
              <div className="text-4xl mb-2">{score === 3 ? '🏆' : score >= 2 ? '🎉' : '💪'}</div>
              <p className="text-white font-extrabold text-xl">{score}/3 correct!</p>
              <p className="text-white/60 text-sm mt-1 mb-4">
                {score === 3 ? "Perfect score! You're ready to master IPM!" : 'Great effort! Practice makes perfect.'}
              </p>
              <Link
                href="/pricing"
                className="block w-full bg-[#58CC02] hover:bg-[#46a302] text-white font-extrabold py-3 rounded-2xl transition-colors"
              >
                Love it? Pick your plan! →
              </Link>
              <Link href="/start" className="block text-white/40 text-xs mt-2 hover:text-white/70">
                Start for free with basic access →
              </Link>
            </div>
          ) : (
            <div className="max-w-xs mx-auto">
              <div className="flex justify-between text-white/40 text-xs mb-3">
                <span>Question {current + 1} of {questions.length}</span>
                <span>Score: {score}</span>
              </div>
              <MiniQuestion key={current} q={questions[current]} onAnswer={handleAnswer} />
            </div>
          )}
        </div>
      </div>

      {/* How it works */}
      <div className="px-4 py-10 bg-gray-50">
        <h2 className="text-xl font-extrabold text-gray-800 text-center mb-6">How MathSpark works</h2>
        <div className="space-y-4">
          {[
            { step: '1', emoji: '🔍', title: 'Take a diagnostic quiz',  desc: '15 questions across all topics to find exactly where your child is.' },
            { step: '2', emoji: '🎯', title: 'Practice adaptively',      desc: 'Our AI picks the right difficulty — not too easy, not too hard.' },
            { step: '3', emoji: '📈', title: 'Watch mastery grow',        desc: 'Track progress topic-by-topic. Parents get weekly reports.' },
          ].map((item) => (
            <div key={item.step} className="flex items-start gap-4 bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
              <div className="text-3xl shrink-0">{item.emoji}</div>
              <div>
                <p className="font-extrabold text-gray-800 text-sm">{item.title}</p>
                <p className="text-gray-500 text-xs mt-0.5">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Value prop */}
      <div className="px-4 py-8 bg-white">
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 text-center">
          <p className="text-2xl font-extrabold text-gray-800 mb-2">72% cheaper than coaching</p>
          <p className="text-gray-600 text-sm">
            Private coaching: <strong className="text-gray-800">₹18,000/month</strong><br />
            MathSpark Unlimited: <strong className="text-[#58CC02]">₹5,000/month</strong><br />
            Same results. Available 24/7. No commute.
          </p>
          <Link
            href="/pricing"
            className="inline-block mt-4 bg-[#131F24] text-white font-extrabold px-6 py-3 rounded-2xl text-sm hover:bg-[#1a3040] transition-colors"
          >
            See all plans →
          </Link>
        </div>
      </div>

      {/* Testimonials */}
      <div className="px-4 py-8 bg-gray-50">
        <h2 className="text-xl font-extrabold text-gray-800 text-center mb-6">What parents say</h2>
        <div className="space-y-3">
          {[
            { name: 'Priya M., Mumbai',   quote: '"My daughter went from 60% to 85% accuracy in 3 weeks. The hints are amazing!"' },
            { name: 'Rahul S., Bangalore',quote: '"Finally an app that teaches the WHY, not just the answer. Arjun loves Sparky the tutor!"' },
            { name: 'Anita K., Delhi',    quote: '"Worth every rupee. The mock tests match the actual IPM paper perfectly."' },
          ].map((t) => (
            <div key={t.name} className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
              <p className="text-gray-700 text-sm italic">{t.quote}</p>
              <p className="text-gray-400 text-xs mt-2 font-semibold">— {t.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Final CTA */}
      <div className="px-4 py-8 bg-[#131F24] text-center">
        <p className="text-white font-extrabold text-xl mb-2">Start your child's IPM journey today</p>
        <p className="text-white/50 text-sm mb-6">3-day free trial · No card required</p>
        <Link
          href="/auth/register"
          className="block w-full bg-[#58CC02] hover:bg-[#46a302] text-white font-extrabold py-4 rounded-2xl text-lg transition-colors mb-3"
        >
          Create Free Account →
        </Link>
        <Link href="/start" className="block text-white/40 text-sm hover:text-white/70 transition-colors">
          Try without account →
        </Link>
      </div>

      {/* Footer */}
      <footer className="px-4 py-6 bg-[#0d1a20] text-center">
        <p className="text-white font-extrabold mb-3">MathSpark ⭐</p>
        <div className="flex justify-center gap-6 text-white/40 text-xs font-semibold">
          <Link href="/pricing" className="hover:text-white/70 transition-colors">Pricing</Link>
          <Link href="/auth/register" className="hover:text-white/70 transition-colors">Sign up</Link>
          <Link href="/auth/login" className="hover:text-white/70 transition-colors">Login</Link>
          <Link href="/start" className="hover:text-white/70 transition-colors">Practice free</Link>
        </div>
        <p className="text-white/20 text-xs mt-4">© 2026 MathSpark. Child-safe learning for Grade 4 IPM.</p>
      </footer>
    </div>
  );
}

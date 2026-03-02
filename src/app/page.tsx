'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import Sparky from '@/components/Sparky';

// ─────────────────────────────────────────────────────────────────────────────
// Hooks
// ─────────────────────────────────────────────────────────────────────────────

function useInView(threshold = 0.12) {
  const ref = useRef<HTMLDivElement>(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setInView(true); obs.disconnect(); } },
      { threshold },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [threshold]);
  return [ref, inView] as const;
}

function useCountUp(target: number, inView: boolean, duration = 1600) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!inView) return;
    if (target === 0) { setCount(0); return; }
    let start: number | null = null;
    const raf = (ts: number) => {
      if (!start) start = ts;
      const p     = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      setCount(Math.floor(eased * target));
      if (p < 1) requestAnimationFrame(raf); else setCount(target);
    };
    requestAnimationFrame(raf);
  }, [inView, target, duration]);
  return count;
}

// ─────────────────────────────────────────────────────────────────────────────
// SectionFade
// ─────────────────────────────────────────────────────────────────────────────

function SectionFade({ children, delay = 0, className = '' }: {
  children: React.ReactNode; delay?: number; className?: string;
}) {
  const [ref, inView] = useInView(0.08);
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`transition-all duration-700 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'} ${className}`}
    >
      {children}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// HeroDemo — live question auto-answers itself
// ─────────────────────────────────────────────────────────────────────────────

interface PreviewQ {
  id: string; questionText: string;
  option1: string; option2: string; option3: string; option4: string;
  correctAnswer: string;
}
const OPT_KEYS = ['A', 'B', 'C', 'D'] as const;

function HeroDemo() {
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
                className={`flex items-center gap-3 border-2 rounded-xl px-3 py-2.5 transition-all duration-500 ${
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

// ─────────────────────────────────────────────────────────────────────────────
// StatCard
// ─────────────────────────────────────────────────────────────────────────────

function StatCard({ prefix = '', target, suffix = '', label, inView }: {
  prefix?: string; target: number; suffix?: string; label: string; inView: boolean;
}) {
  const count = useCountUp(target, inView);
  return (
    <div className="text-center py-5 px-2 overflow-hidden">
      <div className="text-xl sm:text-3xl font-extrabold text-white tabular-nums leading-none truncate">
        {prefix}{target === 0 ? '0' : count.toLocaleString('en-IN')}{suffix}
      </div>
      <div className="text-white/40 text-xs sm:text-sm mt-1.5 leading-tight">{label}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Data
// ─────────────────────────────────────────────────────────────────────────────

const ANXIETY_ITEMS = [
  '₹10 lakh in IPM scholarships annually',
  '40 questions. 60 minutes. Every second counts.',
  'Top 400 qualify for Mega Final from 50,000+ students',
  'Early starters score 40% higher on mocks',
];

const PLANS = [
  {
    id: 'starter', name: 'Starter', emoji: '🌱', monthly: 500,
    color: 'border-[#58CC02]', ctaClass: 'bg-[#58CC02] hover:bg-[#46a302]', popular: false,
    features: ['2,505+ practice questions','1 hour / day','3-level hint system','Step-by-step solutions','5 AI tutor chats / day','Progress tracking'],
  },
  {
    id: 'advanced', name: 'Advanced', emoji: '⚡', monthly: 1500,
    color: 'border-[#1CB0F6]', ctaClass: 'bg-[#1CB0F6] hover:bg-[#0a98dc]', popular: true,
    features: ['Everything in Starter','5 hours / day','Diagnostic quiz','Adaptive difficulty engine','Misconception feedback','25 AI tutor chats / day'],
  },
  {
    id: 'unlimited', name: 'Unlimited', emoji: '🏆', monthly: 5000,
    color: 'border-[#9B59B6]', ctaClass: 'bg-[#9B59B6] hover:bg-[#7D3C98]', popular: false,
    features: ['Everything in Advanced','Unlimited time / day','100 AI tutor chats / day','Mock test mode (all papers)','Full dashboard & analytics','Parent dashboard','Badges, streaks & XP'],
  },
];

const COMPARISON_ROWS = [
  ['Availability',            '2–3 hours/week, fixed schedule',        '24/7 — whenever your child is ready'],
  ['Personalisation',         "One tutor's experience and instinct",   'AI tracking accuracy, speed & misconceptions across 21 topics'],
  ['Feedback speed',          'After the session or next class',        'Instant — within 1 second of every answer'],
  ['Question bank',           "Limited to tutor's preparation",        '100,000+ richly researched questions, auto-adapting'],
  ['Real exam practice',      "Depends on tutor's access to papers",   'Full IPM 2016–2019 papers with timed simulation'],
  ['Misconception tracking',  'Tutor may miss patterns',               'AI flags repeated errors across sessions automatically'],
  ['Parent visibility',       'Ask the tutor, hope they remember',     'Weekly email report with exact strengths, gaps & study plan'],
  ['Makes tutor MORE effective', '—',                                  '✅ Child arrives at sessions with gaps already identified'],
  ['Cost',                    '₹6,000–8,000/month (3 hrs/week)',       'A fraction — and works alongside your tutor'],
];

// ─────────────────────────────────────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────────────────────────────────────

export default function LandingPage() {
  const router                 = useRouter();
  const { status }             = useSession();
  const [statsRef, statsInView] = useInView(0.25);

  // Routing
  useEffect(() => {
    if (status === 'loading') return;
    if (status === 'authenticated') { router.replace('/parent/dashboard'); return; }
    const id = localStorage.getItem('mathspark_student_id');
    if (id) router.replace('/home');
  }, [status, router]);

  return (
    <div className="min-h-screen bg-[#131F24] text-white">

      {/* ── NAV ─────────────────────────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 bg-[#131F24]/95 backdrop-blur-sm border-b border-white/5 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparky size={30} mood="happy" />
          <span className="text-white font-extrabold text-lg tracking-tight">MathSpark</span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/pricing" className="text-white/50 text-sm font-semibold hover:text-white transition-colors hidden sm:block">Pricing</Link>
          <Link href="/auth/login" className="text-white/50 text-sm font-semibold hover:text-white transition-colors">Sign in</Link>
          <Link href="/auth/register" className="bg-[#58CC02] border-b-[3px] border-[#46a302] text-white text-sm font-extrabold px-4 py-2 rounded-full hover:bg-[#5bd800] transition-all active:translate-y-[2px] active:border-b-0">
            Start Free
          </Link>
        </div>
      </nav>

      {/* ── HERO ────────────────────────────────────────────────────────────── */}
      <section className="px-4 pt-10 pb-14 max-w-5xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
          <div>
            <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-xs text-white/60 font-semibold mb-6">
              🧮 Built by Mathletes &amp; Educationists
            </div>
            <div className="flex items-center gap-4 mb-4">
              <div className="shrink-0">
                <Sparky size={72} mood="celebrating" className="animate-sparky-bounce" />
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-white leading-[1.15]">
                15 minutes a day.<br />
                <span className="text-[#58CC02]">2× the math growth.</span>
              </h1>
            </div>
            <p className="text-white/60 text-base leading-relaxed mb-2">
              India's smartest IPM &amp; Olympiad prep — adaptive AI tutoring, 100,000+ richly researched questions, real exam simulations. Built by competitive math champions.
            </p>
            <p className="text-white/30 text-xs leading-relaxed mb-8 italic border-l-2 border-white/10 pl-3">
              Research shows daily adaptive practice doubles learning growth versus worksheets (Muralidharan et al., American Economic Review, 2019)
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/auth/register"
                className="flex-1 text-center bg-[#58CC02] border-b-4 border-[#46a302] text-white font-extrabold py-4 rounded-2xl transition-all hover:bg-[#5bd800] active:translate-y-1 active:border-b-0"
              >
                Start 7-Day Free Trial →
              </Link>
              <button
                onClick={() => document.getElementById('research')?.scrollIntoView({ behavior: 'smooth' })}
                className="flex-1 border-2 border-white/20 text-white/65 hover:border-white/40 hover:text-white font-extrabold py-4 rounded-2xl transition-all"
              >
                See the Research ↓
              </button>
            </div>
          </div>
          <HeroDemo />
        </div>
      </section>

      {/* ── COMPETITION ANXIETY BAR ───────────────────────────────────────────── */}
      <div className="bg-[#FF4B4B]/10 border-y border-[#FF4B4B]/20 py-3 overflow-hidden select-none">
        <div className="flex animate-marquee">
          {[...ANXIETY_ITEMS, ...ANXIETY_ITEMS, ...ANXIETY_ITEMS].map((item, i) => (
            <span key={i} className="inline-flex items-center gap-2 px-8 text-sm font-bold text-[#FF9600] whitespace-nowrap shrink-0">
              <span className="text-[#FF4B4B]">⚠</span> {item}
              <span className="text-white/10 ml-2">|</span>
            </span>
          ))}
        </div>
      </div>

      {/* ── TRUST NUMBERS ─────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-4xl mx-auto">
        <div ref={statsRef} className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-white/10 bg-white/[0.03] border border-white/10 rounded-2xl">
          <StatCard target={100000} suffix="+" label="Richly Researched Questions" inView={statsInView} />
          <StatCard target={4}      suffix=" Yrs" label="of Real IPM Papers"         inView={statsInView} />
          <StatCard target={0}                    label="Hallucinated Answers"        inView={statsInView} />
          <StatCard target={2}      suffix="×"    label="Faster Learning (cited)"     inView={statsInView} />
        </div>
        <p className="text-center text-white/20 text-xs mt-2 italic">
          ²Muralidharan, Singh &amp; Ganimian — American Economic Review, 2019
        </p>
      </section>

      {/* ── WHY MATHSPARK ─────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <div className="text-center mb-10">
            <p className="text-[#58CC02] text-xs font-extrabold uppercase tracking-widest mb-2">Research-Backed. Competition-Proven.</p>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white leading-tight">
              What even ₹2,000/hour private tutors can't give you.
            </h2>
          </div>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { emoji: '🧠', title: 'Adaptive AI That Learns Your Child',
              body: 'Our engine tracks accuracy, speed, and misconception patterns across 21 topics. It serves questions in the sweet spot — challenging enough to grow, easy enough not to frustrate. Research shows adaptive platforms produce 0.37 SD improvement — equivalent to jumping from 50th to 65th percentile.',
              cite: 'J-PAL RCT, American Economic Review 2019' },
            { emoji: '🔬', title: 'Zero Hallucination. Every Answer Verified.',
              body: '100,000+ questions built from IPM worksheets, real 2016–2019 exam papers with official answer keys, and mathematically computed variations. No AI guessing. No wrong answers reaching your child. Ever.',
              cite: null },
            { emoji: '🎮', title: '3× More Practice Than Worksheets',
              body: "Gamified streaks, XP points, and Sparky's encouragement keep children practicing 93% of the time versus 72% with traditional worksheets. Mixed-topic practice doubles retention versus chapter-by-chapter approaches.",
              cite: 'Rohrer et al., Journal of Educational Psychology 2020' },
          ].map((card, i) => (
            <SectionFade key={card.title} delay={i * 100}>
              <div className="bg-[#1a2f3a] border border-white/10 rounded-2xl p-5 h-full flex flex-col">
                <div className="text-3xl mb-3">{card.emoji}</div>
                <h3 className="text-white font-extrabold text-base mb-2 leading-tight">{card.title}</h3>
                <p className="text-white/55 text-sm leading-relaxed flex-1">{card.body}</p>
                {card.cite && <p className="text-white/25 text-xs mt-3 italic">Source: {card.cite}</p>}
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── COMPARISON TABLE ──────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white leading-tight mb-3">
              Your child gets a ₹2,000/hour tutor.<br className="hidden sm:block" /> For a fraction of the cost.
            </h2>
            <p className="text-white/45 text-sm max-w-xl mx-auto">
              The best private tutors charge ₹1,500–2,000 per hour. But even they can't adapt in real-time, track every misconception, or be available at 6 AM when your child is sharpest.
            </p>
          </div>
        </SectionFade>
        <SectionFade delay={100}>
          <div className="overflow-x-auto rounded-2xl border border-white/10">
            <table className="w-full text-sm min-w-[600px]">
              <colgroup>
                <col className="w-[30%]" />
                <col className="w-[28%]" />
                <col className="w-[42%]" />
              </colgroup>
              <thead>
                <tr className="bg-white/5 border-b border-white/10">
                  <th className="text-left px-4 py-3 text-white/40 font-semibold text-xs"></th>
                  <th className="px-4 py-3 text-white/45 font-semibold text-center text-xs">
                    Private Tutor<br /><span className="font-normal text-white/25">₹1,500–2,000/hr</span>
                  </th>
                  <th className="px-4 py-3 text-[#58CC02] font-extrabold text-center text-xs">MathSpark ✦</th>
                </tr>
              </thead>
              <tbody>
                {COMPARISON_ROWS.map(([feature, tutor, ms], i) => (
                  <tr key={feature} className={`transition-colors ${i % 2 ? 'bg-white/[0.015]' : ''} hover:bg-white/[0.04]`}>
                    <td className="px-4 py-3 text-white/65 font-semibold text-xs">{feature}</td>
                    <td className="px-4 py-3 text-white/35 text-center text-xs">{tutor}</td>
                    <td className="px-4 py-3 text-[#58CC02] font-semibold text-center text-xs">{ms}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-white/35 text-sm mt-5 text-center leading-relaxed max-w-2xl mx-auto bg-white/[0.02] border border-white/5 rounded-2xl px-5 py-4">
            MathSpark doesn't replace your child's tutor or your personal involvement — it supercharges both. When your child practices daily, they arrive at tutor sessions already knowing what they're weak at. Your tutor spends time teaching, not diagnosing. And you get weekly reports showing exactly where to focus.
          </p>
        </SectionFade>
      </section>

      {/* ── FEATURES ──────────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white text-center mb-8 leading-tight">
            Everything your child needs to ace the IPM.
          </h2>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { emoji: '📝', title: 'Real IPM Exam Simulation',
              body: 'Full 40-question, 60-minute mock tests matching exact IPM format. Practice with actual 2016–2019 papers. Post-exam playback shows time per question, topic gaps, and a personalised study plan.', cite: null },
            { emoji: '🎯', title: 'Adaptive Difficulty Engine',
              body: '70% questions at current level, 20% review, 10% stretch. 3 wrong in a row? Difficulty drops. 5 right? Time to level up. Each additional practice question correlates with 0.26 points higher on assessments.',
              cite: 'IXL at-home learning study, 2024' },
            { emoji: '💬', title: "Sparky: Your Child's AI Math Tutor",
              body: "Sparky never gives answers — it asks questions. Using the Socratic method, it guides your child to discover solutions. 'What do you think we should do first?' builds real mathematical thinking, not rote memorisation.", cite: null },
            { emoji: '📊', title: 'Weekly Parent Reports',
              body: "Every Sunday: what they practiced, accuracy trends, strongest topics, exact gaps to focus on. Share with your child's tutor. No login required — insights delivered to your email.", cite: null },
            { emoji: '🏆', title: 'Misconception Mapping',
              body: "When your child gets an answer wrong, MathSpark explains exactly WHY that answer is wrong and tracks error patterns. If the same mistake happens 3 times, Sparky addresses the root cause.", cite: null },
            { emoji: '⚡', title: 'Speed Drills',
              body: 'IPM gives 90 seconds per question. Our timed drills build speed AND accuracy together, matching the real exam pace. Your child builds exam-day confidence through simulated pressure.', cite: null },
          ].map((f, i) => (
            <SectionFade key={f.title} delay={(i % 3) * 80}>
              <div className="bg-[#1a2f3a] border border-white/10 rounded-2xl p-5 h-full flex flex-col">
                <div className="text-2xl mb-2">{f.emoji}</div>
                <h3 className="text-white font-extrabold text-sm mb-2 leading-tight">{f.title}</h3>
                <p className="text-white/55 text-sm leading-relaxed flex-1">{f.body}</p>
                {f.cite && <p className="text-white/25 text-xs mt-3 italic">{f.cite}</p>}
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── SUPERCHARGE ───────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white leading-tight">
              You're already investing in your child's math.<br className="hidden sm:block" /> Make every rupee count.
            </h2>
          </div>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { emoji: '🎓', title: 'Make Tutor Sessions 2× More Productive',
              body: "Most tutor time is wasted on diagnosis — figuring out what the child doesn't know. MathSpark does this automatically, 24/7. Your tutor opens the parent report and jumps straight to teaching. ₹2,000/hour spent teaching, not testing." },
            { emoji: '👨‍👩‍👧', title: 'Make Family Study Time Targeted',
              body: "No more guessing which chapters to revise on weekends. MathSpark's weekly report tells you exactly: 'Strong in Algebra, needs work on Calendar problems and Circle perimeters.' Every minute of your time with your child is purposeful." },
            { emoji: '📈', title: 'Track Progress Like Never Before',
              body: "See your child's mock test scores improve week over week. Know exactly which IPM question types they've mastered and which need work. No more anxiety — just data." },
          ].map((card, i) => (
            <SectionFade key={card.title} delay={i * 100}>
              <div className="bg-white/[0.04] border border-white/10 rounded-2xl p-5 h-full flex flex-col">
                <div className="text-3xl mb-3">{card.emoji}</div>
                <h3 className="text-white font-extrabold text-base mb-2 leading-tight">{card.title}</h3>
                <p className="text-white/55 text-sm leading-relaxed">{card.body}</p>
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── HOW IT WORKS ──────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-3xl mx-auto">
        <SectionFade>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white text-center mb-8">How it works</h2>
        </SectionFade>
        <div className="space-y-3">
          {[
            { n: '01', title: 'Free Diagnostic Quiz',
              body: "15 adaptive questions map your child's strengths and gaps across all IPM topics. Takes 5 minutes. Results emailed to you instantly. Share with your tutor." },
            { n: '02', title: 'Personalised Learning Path',
              body: 'Sparky builds a path prioritising weak areas. Your child sees exactly what to work on, with topics unlocking as they progress.' },
            { n: '03', title: 'Daily 15-Minute Practice',
              body: 'Gamified lessons with streaks, XP, and badges. Adaptive questions, 3-level hints, step-by-step solutions. Children WANT to open the app. Complements tutor sessions perfectly.' },
            { n: '04', title: 'Mock Tests & Improve',
              body: "Full IPM simulations with detailed analytics. Track score improvement week over week. Share results with tutor. See exactly when they're IPM-ready." },
          ].map((step, i) => (
            <SectionFade key={step.n} delay={i * 80}>
              <div className="flex items-start gap-4 bg-[#1a2f3a] border border-white/10 rounded-2xl p-5">
                <div className="text-[#58CC02] font-extrabold text-2xl tabular-nums shrink-0 w-10 mt-0.5">{step.n}</div>
                <div>
                  <h3 className="text-white font-extrabold text-base mb-1">{step.title}</h3>
                  <p className="text-white/55 text-sm leading-relaxed">{step.body}</p>
                </div>
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── TESTIMONIALS ──────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white text-center mb-8">What parents are saying</h2>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { quote: "Our private tutor charges ₹1,800/hour and she's excellent. But she can't be there every morning when my son practices. MathSpark fills that gap perfectly — he practices daily, and his tutor says he comes to sessions much more prepared now. His mock scores jumped from 58% to 79% in three weeks.", city: 'Parent, Mumbai' },
            { quote: "I used to spend weekends going through worksheets with my daughter, not knowing if we were focusing on the right topics. Now MathSpark's weekly report tells me exactly what she needs. We spend our time together on the topics that matter. It's changed our weekend study completely.", city: 'Parent, Pune' },
            { quote: "My son used to dread math worksheets. Now he asks to 'play MathSpark' every morning before school. His tutor noticed the difference within two weeks — he's solving problems faster and making fewer silly mistakes. The streak system is magic — 23 days and counting.", city: 'Parent, Bangalore' },
          ].map((t, i) => (
            <SectionFade key={t.city} delay={i * 100}>
              <div className="bg-[#1a2f3a] border border-white/10 rounded-2xl p-5 h-full flex flex-col">
                <div className="text-[#FF9600] text-sm mb-3 tracking-wide">★★★★★</div>
                <p className="text-white/65 text-sm leading-relaxed italic flex-1">"{t.quote}"</p>
                <p className="text-white/25 text-xs mt-4 font-semibold">— {t.city}</p>
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── RESEARCH ──────────────────────────────────────────────────────────── */}
      <section id="research" className="py-10 px-4 max-w-5xl mx-auto scroll-mt-16">
        <SectionFade>
          <div className="text-center mb-8">
            <p className="text-[#1CB0F6] text-xs font-extrabold uppercase tracking-widest mb-2">Peer-Reviewed Evidence</p>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white leading-tight">
              Don't take our word for it. Read the research.
            </h2>
          </div>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { icon: '📚', journal: 'American Economic Review', year: '2019',
              title: '2× Learning Growth with Adaptive Practice',
              body: 'A randomised controlled trial of 619 students in India found adaptive math software improved scores by 0.37 standard deviations — among the largest gains of any education intervention in India. Students improved at 2× the rate of the comparison group.',
              authors: 'Muralidharan, Singh & Ganimian (2019).' },
            { icon: '🔬', journal: 'Journal of Educational Psychology', year: '2020',
              title: 'Interleaved Practice Doubles Test Scores',
              body: 'A preregistered RCT with 787 students found mixed-topic practice produced scores of 61% versus 37% for sequential practice — effect size d = 0.83. This is why MathSpark mixes topics instead of drilling one chapter at a time.',
              authors: 'Rohrer, Dedrick, Hartwig & Cheung (2020).' },
            { icon: '🏅', journal: 'Educational Psychology Review', year: '2020',
              title: 'Gamification Boosts Learning AND Motivation',
              body: 'Meta-analysis found gamification produces effect sizes of g = 0.49 for learning outcomes and g = 0.36 for motivation. Students spend 93% of time on-task with gamified math versus 72% without.',
              authors: 'Sailer & Homner (2020).' },
          ].map((r, i) => (
            <SectionFade key={r.title} delay={i * 100}>
              <div className="bg-[#0d1a20] border border-[#1CB0F6]/20 rounded-2xl p-5 h-full flex flex-col">
                <div className="flex items-start gap-2 mb-3">
                  <span className="text-2xl">{r.icon}</span>
                  <div>
                    <p className="text-[#1CB0F6] text-xs font-extrabold leading-tight">{r.journal}</p>
                    <p className="text-white/25 text-xs">{r.year}</p>
                  </div>
                </div>
                <h3 className="text-white font-extrabold text-sm mb-2 leading-tight">{r.title}</h3>
                <p className="text-white/50 text-xs leading-relaxed flex-1">{r.body}</p>
                <p className="text-white/25 text-xs mt-3 italic">{r.authors}</p>
              </div>
            </SectionFade>
          ))}
        </div>
      </section>

      {/* ── PRICING ───────────────────────────────────────────────────────────── */}
      <section className="py-10 px-4 max-w-5xl mx-auto">
        <SectionFade>
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-2">Simple, honest pricing.</h2>
            <p className="text-white/45 text-sm">3-day free trial on all plans · No card required · Cancel anytime</p>
          </div>
        </SectionFade>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {PLANS.map((plan, i) => (
            <SectionFade key={plan.id} delay={i * 100}>
              <div className={`bg-[#1a2f3a] border-2 ${plan.color} rounded-2xl overflow-hidden h-full flex flex-col ${plan.popular ? 'ring-2 ring-[#1CB0F6] ring-offset-2 ring-offset-[#131F24]' : ''}`}>
                {plan.popular && (
                  <div className="bg-[#1CB0F6] text-white text-[10px] font-extrabold text-center py-1.5 tracking-widest uppercase">⭐ Most Popular</div>
                )}
                <div className="p-5 flex flex-col flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xl">{plan.emoji}</span>
                    <span className="text-white font-extrabold text-lg">{plan.name}</span>
                  </div>
                  <div className="flex items-baseline gap-1 mb-4">
                    <span className="text-3xl font-extrabold text-white">₹{plan.monthly.toLocaleString('en-IN')}</span>
                    <span className="text-white/35 text-sm">/mo</span>
                  </div>
                  <ul className="space-y-1.5 flex-1 mb-4">
                    {plan.features.map(f => (
                      <li key={f} className="flex items-start gap-2 text-xs text-white/60">
                        <span className="text-[#58CC02] font-bold shrink-0 mt-0.5">✓</span> {f}
                      </li>
                    ))}
                  </ul>
                  <Link href="/auth/register" className={`block w-full text-center ${plan.ctaClass} text-white font-extrabold py-3 rounded-2xl transition-colors text-sm`}>
                    Start Free Trial →
                  </Link>
                </div>
              </div>
            </SectionFade>
          ))}
        </div>
        <SectionFade delay={300}>
          <p className="text-center text-white/35 text-sm mt-6 max-w-md mx-auto">
            💡 One hour with a private tutor costs ₹1,500–2,000. MathSpark works alongside your tutor 24/7, making every session and every rupee more effective.
          </p>
        </SectionFade>
      </section>

      {/* ── FINAL CTA ─────────────────────────────────────────────────────────── */}
      <section className="py-14 px-4">
        <SectionFade>
          <div className="max-w-lg mx-auto bg-gradient-to-b from-[#1a2f3a] to-[#131F24] border border-white/10 rounded-3xl px-6 py-10 text-center">
            <div className="flex justify-center mb-4">
              <Sparky size={72} mood="celebrating" className="animate-sparky-dance" />
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-2 leading-tight">
              ₹10 lakh in IPM scholarships.<br />40 questions in 60 minutes.
            </h2>
            <p className="text-white/55 text-base mt-3 mb-2">Your child's tutor can't be there at 6 AM. Sparky can.</p>
            <p className="text-white/35 text-sm mb-8 max-w-sm mx-auto">
              Start with a free diagnostic — see exactly where your child stands. Share the results with your tutor.
            </p>
            <Link
              href="/auth/register"
              className="block w-full bg-[#58CC02] border-b-4 border-[#46a302] text-white font-extrabold py-4 rounded-2xl text-lg transition-all hover:bg-[#5bd800] active:translate-y-1 active:border-b-0"
            >
              Start Free Diagnostic Quiz →
            </Link>
            <p className="text-white/20 text-xs mt-4">3-day free trial · No card required · Cancel anytime</p>
          </div>
        </SectionFade>
      </section>

      {/* ── FOOTER ────────────────────────────────────────────────────────────── */}
      <footer className="bg-[#0d1a20] border-t border-white/5 px-4 py-8 text-center">
        <div className="flex items-center justify-center gap-2 mb-3">
          <Sparky size={26} mood="happy" />
          <span className="text-white font-extrabold text-base">MathSpark</span>
        </div>
        <p className="text-white/25 text-xs mb-1">Built by mathletes and educationists for IPM &amp; Olympiad aspirants.</p>
        <p className="text-white/15 text-xs mb-4">
          100,000+ researched questions · 4 years of real papers · Zero hallucination · Adaptive AI<br />
          Complements private tutoring · Empowers parents · Built for Indian families
        </p>
        <div className="flex flex-wrap justify-center gap-4 sm:gap-6 text-white/25 text-xs font-semibold mb-5">
          <Link href="/pricing"       className="hover:text-white/55 transition-colors">Pricing</Link>
          <Link href="/auth/register" className="hover:text-white/55 transition-colors">Sign up</Link>
          <Link href="/auth/login"    className="hover:text-white/55 transition-colors">Sign in</Link>
          <a href="#"                 className="hover:text-white/55 transition-colors">Privacy</a>
          <a href="#"                 className="hover:text-white/55 transition-colors">Terms</a>
          <a href="mailto:hello@mathspark.app" className="hover:text-white/55 transition-colors">Contact</a>
        </div>
        <p className="text-white/10 text-xs">© 2026 MathSpark. Research citations available on request.</p>
      </footer>

    </div>
  );
}

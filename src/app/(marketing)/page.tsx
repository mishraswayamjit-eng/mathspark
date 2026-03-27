import Link from 'next/link';
import Sparky from '@/components/Sparky';
import AuthRedirect from '@/components/landing/AuthRedirect';
import HeroDemo from '@/components/landing/HeroDemo';
import SectionFade from '@/components/landing/SectionFade';
import StatsBar from '@/components/landing/StatsBar';
import ScrollButton from '@/components/landing/ScrollButton';

// ─────────────────────────────────────────────────────────────────────────────
// Data (server-only — never shipped to client JS bundle)
// ─────────────────────────────────────────────────────────────────────────────

const PLANS = [
  {
    id: 'starter', name: 'Starter', emoji: '🌱', monthly: 500,
    borderColor: 'border-duo-green', ctaClass: 'bg-duo-green hover:bg-[#46a302]', popular: false,
    features: ['2,505+ practice questions','1 hour / day','3-level hint system','Step-by-step solutions','5 AI tutor chats / day','Progress tracking'],
  },
  {
    id: 'advanced', name: 'Advanced', emoji: '⚡', monthly: 1500,
    borderColor: 'border-duo-blue', ctaClass: 'bg-duo-blue hover:bg-[#0a98dc]', popular: true,
    features: ['Everything in Starter','5 hours / day','Diagnostic quiz','Adaptive difficulty engine','Misconception feedback','25 AI tutor chats / day'],
  },
  {
    id: 'unlimited', name: 'Unlimited', emoji: '🏆', monthly: 5000,
    borderColor: 'border-purple-500', ctaClass: 'bg-purple-500 hover:bg-purple-600', popular: false,
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
  ['Makes tutor MORE effective', '—',                                  'Child arrives at sessions with gaps already identified'],
  ['Cost',                    '₹6,000–8,000/month (3 hrs/week)',       'A fraction — and works alongside your tutor'],
];

// ─────────────────────────────────────────────────────────────────────────────
// Page (Server Component)
// ─────────────────────────────────────────────────────────────────────────────

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      <AuthRedirect />

      {/* ── NAV ─────────────────────────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-200/50 px-4 sm:px-6 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparky size={30} mood="happy" />
            <span className="text-duo-dark font-extrabold text-lg tracking-tight">MathSpark</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/pricing" className="text-gray-600 text-sm font-semibold hover:text-gray-900 transition-colors hidden sm:block">Pricing</Link>
            <Link href="/auth/login" className="text-gray-600 text-sm font-semibold hover:text-gray-900 transition-colors">Sign in</Link>
            <Link href="/auth/register" className="bg-duo-green text-white text-sm font-extrabold px-5 py-2 rounded-full hover:bg-[#46a302] transition-colors">
              Start Free
            </Link>
          </div>
        </div>
      </nav>

      {/* ── HERO ────────────────────────────────────────────────────────────── */}
      <section className="gradient-mesh-hero px-4 sm:px-6 pt-16 pb-20">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-duo-dark leading-[1.1] mb-4">
              Math that adapts<br />
              <span className="text-duo-green">to your child.</span>
            </h1>
            <p className="text-gray-600 text-lg leading-relaxed mb-8 max-w-md">
              Adaptive AI tutoring, 100,000+ questions, and real IPM exam simulations — built by competitive math champions.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/auth/register"
                className="flex-1 text-center bg-duo-green text-white font-extrabold py-4 rounded-2xl transition-colors hover:bg-[#46a302] active:translate-y-0.5"
              >
                Start 7-Day Free Trial
              </Link>
              <ScrollButton
                targetId="research"
                className="flex-1 border-2 border-gray-200 text-gray-500 hover:border-gray-300 hover:text-gray-700 font-extrabold py-4 rounded-2xl transition-colors"
              >
                See the Research
              </ScrollButton>
            </div>
          </div>
          <HeroDemo />
        </div>
      </section>

      {/* ── TRUST NUMBERS ─────────────────────────────────────────────────────── */}
      <StatsBar />

      {/* ── WHY MATHSPARK ─────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-12">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark leading-tight">
                What makes MathSpark different
              </h2>
            </div>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { emoji: '🧠', bg: 'bg-green-50', title: 'Adaptive AI That Learns Your Child',
                body: 'Tracks accuracy, speed, and misconceptions across 21 topics. Serves questions in the sweet spot — challenging enough to grow, easy enough not to frustrate.' },
              { emoji: '🔬', bg: 'bg-blue-50', title: 'Zero Hallucination. Every Answer Verified.',
                body: '100,000+ questions built from real IPM papers and official answer keys. No AI guessing — no wrong answers ever reach your child.' },
              { emoji: '🎮', bg: 'bg-orange-50', title: '3x More Practice Than Worksheets',
                body: 'Gamified streaks, XP, and encouragement keep children practicing 93% of the time. Mixed-topic practice doubles retention.' },
            ].map((card, i) => (
              <SectionFade key={card.title} delay={i * 100}>
                <div className="bg-white border border-gray-100 rounded-2xl p-6 h-full flex flex-col shadow-sm hover:shadow-md transition-shadow">
                  <div className={`w-12 h-12 ${card.bg} rounded-xl flex items-center justify-center text-2xl mb-4`} aria-hidden="true">{card.emoji}</div>
                  <h3 className="text-duo-dark font-extrabold text-base mb-2 leading-tight">{card.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed flex-1">{card.body}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── COMPARISON TABLE ──────────────────────────────────────────────────── */}
      <section className="bg-gray-50 py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-10">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark leading-tight mb-3">
                How MathSpark compares to private tutoring
              </h2>
              <p className="text-gray-500 text-sm max-w-xl mx-auto">
                Even ₹2,000/hour tutors can&apos;t adapt in real-time, track every misconception, or be available at 6 AM when your child is sharpest.
              </p>
            </div>
          </SectionFade>
          <SectionFade delay={100}>
            <div className="overflow-x-auto rounded-2xl border border-gray-100 shadow-sm bg-white">
              <table className="w-full text-sm min-w-[600px]">
                <colgroup>
                  <col className="w-[30%]" />
                  <col className="w-[28%]" />
                  <col className="w-[42%]" />
                </colgroup>
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-100">
                    <th className="text-left px-4 py-3 text-gray-400 font-semibold text-xs"></th>
                    <th className="px-4 py-3 text-gray-400 font-semibold text-center text-xs">
                      Private Tutor<br /><span className="font-normal text-gray-300">₹1,500–2,000/hr</span>
                    </th>
                    <th className="px-4 py-3 text-duo-green font-extrabold text-center text-xs">MathSpark</th>
                  </tr>
                </thead>
                <tbody>
                  {COMPARISON_ROWS.map(([feature, tutor, ms], i) => (
                    <tr key={feature} className={`transition-colors ${i % 2 ? 'bg-gray-50/50' : ''} hover:bg-gray-50`}>
                      <td className="px-4 py-3 text-gray-700 font-semibold text-xs">{feature}</td>
                      <td className="px-4 py-3 text-gray-400 text-center text-xs">{tutor}</td>
                      <td className="px-4 py-3 text-duo-green font-semibold text-center text-xs">{ms}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </SectionFade>
        </div>
      </section>

      {/* ── FEATURES ──────────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark text-center mb-10 leading-tight">
              Everything your child needs to ace the IPM
            </h2>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { emoji: '📝', bg: 'bg-red-50', title: 'Real IPM Exam Simulation',
                body: 'Full 40-question, 60-minute mock tests matching exact IPM format with actual 2016–2019 papers.' },
              { emoji: '🎯', bg: 'bg-green-50', title: 'Adaptive Difficulty Engine',
                body: '70% at current level, 20% review, 10% stretch. Difficulty adjusts in real-time to keep your child in flow.' },
              { emoji: '💬', bg: 'bg-purple-50', title: "Sparky: AI Math Tutor",
                body: 'Never gives answers — asks guiding questions using the Socratic method to build real mathematical thinking.' },
              { emoji: '📊', bg: 'bg-blue-50', title: 'Weekly Parent Reports',
                body: 'Every Sunday: accuracy trends, strongest topics, exact gaps. Share with your tutor — no login required.' },
              { emoji: '🏆', bg: 'bg-yellow-50', title: 'Misconception Mapping',
                body: 'Tracks error patterns and explains exactly why wrong answers are wrong. Addresses root causes automatically.' },
              { emoji: '⚡', bg: 'bg-orange-50', title: 'Speed Drills',
                body: 'Timed drills matching real IPM pace — 90 seconds per question. Builds speed, accuracy, and exam confidence.' },
            ].map((f, i) => (
              <SectionFade key={f.title} delay={(i % 3) * 80}>
                <div className="bg-white border border-gray-100 rounded-2xl p-6 h-full flex flex-col shadow-sm hover:shadow-md transition-shadow">
                  <div className={`w-10 h-10 ${f.bg} rounded-lg flex items-center justify-center text-xl mb-3`} aria-hidden="true">{f.emoji}</div>
                  <h3 className="text-duo-dark font-extrabold text-sm mb-2 leading-tight">{f.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed flex-1">{f.body}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ──────────────────────────────────────────────────────── */}
      <section className="bg-gray-50 py-16 px-4 sm:px-6">
        <div className="max-w-3xl mx-auto">
          <SectionFade>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark text-center mb-10">How it works</h2>
          </SectionFade>
          <div className="space-y-4">
            {[
              { n: '01', title: 'Free Diagnostic Quiz',
                body: '15 adaptive questions map strengths and gaps across all IPM topics. Takes 5 minutes.' },
              { n: '02', title: 'Personalised Learning Path',
                body: 'Sparky builds a path prioritising weak areas. Topics unlock as your child progresses.' },
              { n: '03', title: 'Daily 15-Minute Practice',
                body: 'Gamified lessons with streaks, XP, and badges. Adaptive questions with 3-level hints and solutions.' },
              { n: '04', title: 'Mock Tests & Improve',
                body: 'Full IPM simulations with detailed analytics. Track score improvement week over week.' },
            ].map((step, i) => (
              <SectionFade key={step.n} delay={i * 80}>
                <div className="flex items-start gap-4 bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
                  <div className="text-duo-green font-extrabold text-2xl tabular-nums shrink-0 w-10 mt-0.5">{step.n}</div>
                  <div>
                    <h3 className="text-duo-dark font-extrabold text-base mb-1">{step.title}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed">{step.body}</p>
                  </div>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── TESTIMONIALS ──────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark text-center mb-10">What parents are saying</h2>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { quote: "Our private tutor charges ₹1,800/hour and she's excellent. But she can't be there every morning. MathSpark fills that gap — he practices daily, and his mock scores jumped from 58% to 79% in three weeks.", city: 'Parent, Mumbai' },
              { quote: "I used to spend weekends going through worksheets, not knowing if we were focusing on the right topics. Now MathSpark's weekly report tells me exactly what she needs. It's changed our weekend study completely.", city: 'Parent, Pune' },
              { quote: "My son used to dread math worksheets. Now he asks to 'play MathSpark' every morning before school. His tutor noticed the difference within two weeks. The streak system is magic — 23 days and counting.", city: 'Parent, Bangalore' },
            ].map((t, i) => (
              <SectionFade key={t.city} delay={i * 100}>
                <div className="bg-white border border-gray-100 rounded-2xl p-6 h-full flex flex-col shadow-sm">
                  <div className="text-duo-orange text-sm mb-3 tracking-wide" aria-hidden="true">★★★★★</div>
                  <p className="text-gray-600 text-sm leading-relaxed italic flex-1">&ldquo;{t.quote}&rdquo;</p>
                  <p className="text-gray-400 text-xs mt-4 font-semibold">— {t.city}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── RESEARCH ──────────────────────────────────────────────────────────── */}
      <section id="research" className="bg-gray-50 py-16 px-4 sm:px-6 scroll-mt-16">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-10">
              <p className="text-duo-blue text-xs font-extrabold uppercase tracking-widest mb-2">Peer-Reviewed Evidence</p>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark leading-tight">
                Don&apos;t take our word for it. Read the research.
              </h2>
            </div>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { icon: '📚', journal: 'American Economic Review', year: '2019',
                title: '2x Learning Growth with Adaptive Practice',
                body: 'A randomised controlled trial of 619 students in India found adaptive math software improved scores by 0.37 standard deviations — students improved at 2x the rate of the comparison group.',
                authors: 'Muralidharan, Singh & Ganimian (2019).' },
              { icon: '🔬', journal: 'Journal of Educational Psychology', year: '2020',
                title: 'Interleaved Practice Doubles Test Scores',
                body: 'A preregistered RCT with 787 students found mixed-topic practice produced scores of 61% versus 37% for sequential practice — effect size d = 0.83.',
                authors: 'Rohrer, Dedrick, Hartwig & Cheung (2020).' },
              { icon: '🏅', journal: 'Educational Psychology Review', year: '2020',
                title: 'Gamification Boosts Learning & Motivation',
                body: 'Meta-analysis found gamification produces effect sizes of g = 0.49 for learning outcomes and g = 0.36 for motivation. Students spend 93% of time on-task with gamified math.',
                authors: 'Sailer & Homner (2020).' },
            ].map((r, i) => (
              <SectionFade key={r.title} delay={i * 100}>
                <div className="bg-blue-50/50 border border-blue-100 rounded-2xl p-6 h-full flex flex-col">
                  <div className="flex items-start gap-2 mb-3">
                    <span className="text-2xl" aria-hidden="true">{r.icon}</span>
                    <div>
                      <p className="text-duo-blue text-xs font-extrabold leading-tight">{r.journal}</p>
                      <p className="text-gray-400 text-xs">{r.year}</p>
                    </div>
                  </div>
                  <h3 className="text-duo-dark font-extrabold text-sm mb-2 leading-tight">{r.title}</h3>
                  <p className="text-gray-600 text-xs leading-relaxed flex-1">{r.body}</p>
                  <p className="text-gray-400 text-xs mt-3 italic">{r.authors}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRICING ───────────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-10">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-duo-dark mb-2">Simple, honest pricing.</h2>
              <p className="text-gray-500 text-sm">3-day free trial on all plans · No card required · Cancel anytime</p>
            </div>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {PLANS.map((plan, i) => (
              <SectionFade key={plan.id} delay={i * 100}>
                <div className={`bg-white border-2 ${plan.borderColor} rounded-2xl overflow-hidden h-full flex flex-col shadow-sm ${plan.popular ? 'ring-2 ring-duo-blue ring-offset-2' : ''}`}>
                  {plan.popular && (
                    <div className="bg-duo-blue text-white text-[10px] font-extrabold text-center py-1.5 tracking-widest uppercase">Most Popular</div>
                  )}
                  <div className="p-6 flex flex-col flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xl" aria-hidden="true">{plan.emoji}</span>
                      <span className="text-duo-dark font-extrabold text-lg">{plan.name}</span>
                    </div>
                    <div className="flex items-baseline gap-1 mb-5">
                      <span className="text-3xl font-extrabold text-duo-dark">₹{plan.monthly.toLocaleString('en-IN')}</span>
                      <span className="text-gray-400 text-sm">/mo</span>
                    </div>
                    <ul className="space-y-2 flex-1 mb-5">
                      {plan.features.map(f => (
                        <li key={f} className="flex items-start gap-2 text-xs text-gray-600">
                          <span className="text-duo-green font-bold shrink-0 mt-0.5" aria-hidden="true">✓</span> {f}
                        </li>
                      ))}
                    </ul>
                    <Link href="/auth/register" className={`block w-full text-center ${plan.ctaClass} text-white font-extrabold py-3 rounded-2xl transition-colors text-sm`}>
                      Start Free Trial
                    </Link>
                  </div>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── FINAL CTA ─────────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <SectionFade>
          <div className="max-w-2xl mx-auto bg-gradient-to-br from-duo-green to-emerald-500 rounded-3xl px-8 py-12 text-center">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-3 leading-tight">
              Your child&apos;s math journey starts here.
            </h2>
            <p className="text-white/80 text-base mb-8 max-w-md mx-auto">
              Start with a free diagnostic — see exactly where your child stands. Share the results with your tutor.
            </p>
            <Link
              href="/auth/register"
              className="inline-block bg-white text-duo-green font-extrabold py-4 px-10 rounded-2xl text-lg transition-colors hover:bg-gray-50 active:translate-y-0.5"
            >
              Start Free Diagnostic Quiz
            </Link>
            <p className="text-white/60 text-xs mt-4">3-day free trial · No card required · Cancel anytime</p>
          </div>
        </SectionFade>
      </section>

      {/* ── FOOTER ────────────────────────────────────────────────────────────── */}
      <footer className="bg-duo-dark border-t border-white/5 px-4 sm:px-6 py-10 text-center">
        <div className="flex items-center justify-center gap-2 mb-3">
          <Sparky size={26} mood="happy" />
          <span className="text-white font-extrabold text-base">MathSpark</span>
        </div>
        <p className="text-white/40 text-xs mb-1">Built by mathletes and educationists for IPM &amp; Olympiad aspirants.</p>
        <p className="text-white/25 text-xs mb-5">
          100,000+ researched questions · 4 years of real papers · Zero hallucination · Adaptive AI
        </p>
        <div className="flex flex-wrap justify-center gap-4 sm:gap-6 text-white/40 text-xs font-semibold mb-5">
          <Link href="/pricing"       className="hover:text-white/70 transition-colors">Pricing</Link>
          <Link href="/auth/register" className="hover:text-white/70 transition-colors">Sign up</Link>
          <Link href="/auth/login"    className="hover:text-white/70 transition-colors">Sign in</Link>
          <a href="#"                 className="hover:text-white/70 transition-colors">Privacy</a>
          <a href="#"                 className="hover:text-white/70 transition-colors">Terms</a>
          <a href="mailto:hello@mathspark.app" className="hover:text-white/70 transition-colors">Contact</a>
        </div>
        <p className="text-white/15 text-xs">© 2026 MathSpark. Research citations available on request.</p>
      </footer>

    </div>
  );
}

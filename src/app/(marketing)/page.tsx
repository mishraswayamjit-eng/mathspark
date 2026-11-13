import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { MONETIZATION_ENABLED } from '@/lib/monetization';
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
    borderColor: 'border-line', ctaClass: 'bg-white text-ink hover:bg-soft', popular: false,
    features: ['2,505+ practice questions','1 hour / day','3-level hint system','Step-by-step solutions','5 AI tutor chats / day','Progress tracking'],
  },
  {
    id: 'advanced', name: 'Advanced', emoji: '⚡', monthly: 1500,
    borderColor: 'border-ink', ctaClass: 'bg-action text-white hover:bg-action-dark', popular: true,
    features: ['Everything in Starter','5 hours / day','Diagnostic quiz','Adaptive difficulty engine','Misconception feedback','25 AI tutor chats / day'],
  },
  {
    id: 'unlimited', name: 'Unlimited', emoji: '🏆', monthly: 5000,
    borderColor: 'border-line', ctaClass: 'bg-white text-ink hover:bg-soft', popular: false,
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
    <div className="min-h-screen bg-paper text-ink">
      <AuthRedirect />

      {/* ── NAV ─────────────────────────────────────────────────────────────── */}
      <nav className="sticky top-0 z-50 bg-ink px-4 sm:px-6 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparky size={30} mood="happy" />
            <span className="text-white font-extrabold text-lg tracking-tight">MathSpark</span>
          </div>
          <div className="flex items-center gap-3">
            {MONETIZATION_ENABLED && (
              <Link href="/pricing" className="text-white/70 text-sm font-semibold hover:text-white transition-colors hidden sm:block">Pricing</Link>
            )}
            <Link href="/auth/login" className="text-white/70 text-sm font-semibold hover:text-white transition-colors">Sign in</Link>
            <Link href="/start" className="bg-white text-ink text-sm font-extrabold px-5 py-2 rounded-control border-2 border-white hover:bg-soft transition-colors">
              Try It Free
            </Link>
          </div>
        </div>
      </nav>

      {/* ── HERO ────────────────────────────────────────────────────────────── */}
      <section className="px-4 sm:px-6 pt-16 pb-20">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-ink leading-[1.1] mb-4">
              Try a real IPM question<br />
              <span className="text-action">right now.</span>
            </h1>
            <p className="text-ink-muted text-lg leading-relaxed mb-8 max-w-md">
              No sign up. No email. Just tap an answer and see how adaptive math practice works.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/start"
                className="flex-1 text-center bg-action text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm transition-colors hover:bg-action-dark active:translate-y-0.5"
              >
                Start Practicing — Free
              </Link>
              <ScrollButton
                targetId="how-it-works"
                className="flex-1 bg-white border-2 border-ink text-ink shadow-hard-sm hover:bg-soft font-extrabold py-4 rounded-control transition-colors"
              >
                How It Works
              </ScrollButton>
            </div>
            <p className="text-ink-muted text-xs mt-3 font-medium">No account needed to start. Create one later to save progress.</p>
          </div>
          <HeroDemo />
        </div>
      </section>

      {/* ── TRUST NUMBERS ─────────────────────────────────────────────────────── */}
      <StatsBar />

      {/* ── HOW IT WORKS ──────────────────────────────────────────────────────── */}
      <section id="how-it-works" className="bg-soft border-y-2 border-line py-16 px-4 sm:px-6 scroll-mt-16">
        <div className="max-w-3xl mx-auto">
          <SectionFade>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-ink text-center mb-10">How it works</h2>
          </SectionFade>
          <div className="space-y-4">
            {[
              { n: '01', title: 'Try a Question — Right Now',
                body: 'Answer the question above. No sign up, no email — just see how it feels to learn with MathSpark.' },
              { n: '02', title: '2-Minute Setup',
                body: 'Pick your grade, tell us what you want to improve, and take a quick 5-question diagnostic. We build your personalised path.' },
              { n: '03', title: 'Daily 15-Minute Practice',
                body: 'Gamified lessons with streaks, XP, and badges. Adaptive questions with 3-level hints and solutions.' },
              { n: '04', title: 'Mock Tests & Improve',
                body: 'Full IPM simulations with detailed analytics. Track score improvement week over week.' },
            ].map((s, i) => (
              <SectionFade key={s.n} delay={i * 80}>
                <div className="flex items-start gap-4 bg-white border-2 border-line rounded-card p-5">
                  <div className="text-ink-muted font-extrabold text-2xl tabular-nums shrink-0 w-10 mt-0.5">{s.n}</div>
                  <div>
                    <h3 className="text-ink font-extrabold text-base mb-1">{s.title}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed">{s.body}</p>
                  </div>
                </div>
              </SectionFade>
            ))}
          </div>
          <SectionFade delay={320}>
            <div className="mt-8 text-center">
              <Link
                href="/start"
                className="inline-block bg-action text-white font-extrabold py-4 px-10 rounded-control border-2 border-ink shadow-hard-sm transition-colors hover:bg-action-dark active:translate-y-0.5 text-base"
              >
                Start Your Free Diagnostic
              </Link>
              <p className="text-ink-muted text-xs mt-2">Takes 2 minutes. No sign up required.</p>
            </div>
          </SectionFade>
        </div>
      </section>

      {/* ── WHY MATHSPARK ─────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-12">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-ink leading-tight">
                What makes MathSpark different
              </h2>
            </div>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { emoji: '🧠', bg: 'bg-soft', title: 'Adaptive AI That Learns Your Child',
                body: 'Tracks accuracy, speed, and misconceptions across 21 topics. Serves questions in the sweet spot — challenging enough to grow, easy enough not to frustrate.' },
              { emoji: '🔬', bg: 'bg-soft', title: 'Zero Hallucination. Every Answer Verified.',
                body: '100,000+ questions built from real IPM papers and official answer keys. No AI guessing — no wrong answers ever reach your child.' },
              { emoji: '🎮', bg: 'bg-soft', title: '3x More Practice Than Worksheets',
                body: 'Gamified streaks, XP, and encouragement keep children practicing 93% of the time. Mixed-topic practice doubles retention.' },
            ].map((card, i) => (
              <SectionFade key={card.title} delay={i * 100}>
                <div className="bg-white border-2 border-line rounded-card p-6 h-full flex flex-col hover:border-ink transition-colors">
                  <div className={`w-12 h-12 ${card.bg} rounded-tile flex items-center justify-center text-2xl mb-4`} aria-hidden="true">{card.emoji}</div>
                  <h3 className="text-ink font-extrabold text-base mb-2 leading-tight">{card.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed flex-1">{card.body}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── COMPARISON TABLE ──────────────────────────────────────────────────── */}
      <section className="bg-soft border-y-2 border-line py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-10">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-ink leading-tight mb-3">
                How MathSpark compares to private tutoring
              </h2>
              <p className="text-gray-500 text-sm max-w-xl mx-auto">
                Even ₹2,000/hour tutors can&apos;t adapt in real-time, track every misconception, or be available at 6 AM when your child is sharpest.
              </p>
            </div>
          </SectionFade>
          <SectionFade delay={100}>
            <div className="overflow-x-auto rounded-card border-2 border-line bg-white">
              <table className="w-full text-sm min-w-[600px]">
                <colgroup>
                  <col className="w-[30%]" />
                  <col className="w-[28%]" />
                  <col className="w-[42%]" />
                </colgroup>
                <thead>
                  <tr className="bg-soft border-b-2 border-line">
                    <th className="text-left px-4 py-3 text-ink-muted font-semibold text-xs"></th>
                    <th className="px-4 py-3 text-ink-muted font-semibold text-center text-xs">
                      Private Tutor<br /><span className="font-normal text-ink-muted">₹1,500–2,000/hr</span>
                    </th>
                    <th className="px-4 py-3 text-ink font-extrabold text-center text-xs">MathSpark</th>
                  </tr>
                </thead>
                <tbody>
                  {COMPARISON_ROWS.map(([feature, tutor, ms], i) => (
                    <tr key={feature} className={`transition-colors ${i % 2 ? 'bg-soft/50' : ''} hover:bg-soft`}>
                      <td className="px-4 py-3 text-ink font-semibold text-xs">{feature}</td>
                      <td className="px-4 py-3 text-ink-muted text-center text-xs">{tutor}</td>
                      <td className="px-4 py-3 text-ink font-bold text-center text-xs">{ms}</td>
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
            <h2 className="text-2xl sm:text-3xl font-extrabold text-ink text-center mb-10 leading-tight">
              Everything your child needs to ace the IPM
            </h2>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { emoji: '📝', bg: 'bg-soft', title: 'Real IPM Exam Simulation',
                body: 'Full 40-question, 60-minute mock tests matching exact IPM format with actual 2016–2019 papers.' },
              { emoji: '🎯', bg: 'bg-soft', title: 'Adaptive Difficulty Engine',
                body: '70% at current level, 20% review, 10% stretch. Difficulty adjusts in real-time to keep your child in flow.' },
              { emoji: '💬', bg: 'bg-soft', title: "Sparky: AI Math Tutor",
                body: 'Never gives answers — asks guiding questions using the Socratic method to build real mathematical thinking.' },
              { emoji: '📊', bg: 'bg-soft', title: 'Weekly Parent Reports',
                body: 'Every Sunday: accuracy trends, strongest topics, exact gaps. Share with your tutor — no login required.' },
              { emoji: '🏆', bg: 'bg-soft', title: 'Misconception Mapping',
                body: 'Tracks error patterns and explains exactly why wrong answers are wrong. Addresses root causes automatically.' },
              { emoji: '⚡', bg: 'bg-soft', title: 'Speed Drills',
                body: 'Timed drills matching real IPM pace — 90 seconds per question. Builds speed, accuracy, and exam confidence.' },
            ].map((f, i) => (
              <SectionFade key={f.title} delay={(i % 3) * 80}>
                <div className="bg-white border-2 border-line rounded-card p-6 h-full flex flex-col hover:border-ink transition-colors">
                  <div className={`w-10 h-10 ${f.bg} rounded-tile flex items-center justify-center text-xl mb-3`} aria-hidden="true">{f.emoji}</div>
                  <h3 className="text-ink font-extrabold text-sm mb-2 leading-tight">{f.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed flex-1">{f.body}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── TESTIMONIALS ──────────────────────────────────────────────────────── */}
      <section className="bg-soft border-y-2 border-line py-16 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-ink text-center mb-10">What parents are saying</h2>
          </SectionFade>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { quote: "Our private tutor charges ₹1,800/hour and she's excellent. But she can't be there every morning. MathSpark fills that gap — he practices daily, and his mock scores jumped from 58% to 79% in three weeks.", city: 'Parent, Mumbai' },
              { quote: "I used to spend weekends going through worksheets, not knowing if we were focusing on the right topics. Now MathSpark's weekly report tells me exactly what she needs. It's changed our weekend study completely.", city: 'Parent, Pune' },
              { quote: "My son used to dread math worksheets. Now he asks to 'play MathSpark' every morning before school. His tutor noticed the difference within two weeks. The streak system is magic — 23 days and counting.", city: 'Parent, Bangalore' },
            ].map((t, i) => (
              <SectionFade key={t.city} delay={i * 100}>
                <div className="bg-white border-2 border-line rounded-card p-6 h-full flex flex-col">
                  <div className="text-star text-sm mb-3 tracking-wide" aria-hidden="true">★★★★★</div>
                  <p className="text-gray-600 text-sm leading-relaxed italic flex-1">&ldquo;{t.quote}&rdquo;</p>
                  <p className="text-ink-muted text-xs mt-4 font-semibold">— {t.city}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── RESEARCH ──────────────────────────────────────────────────────────── */}
      <section id="research" className="py-16 px-4 sm:px-6 scroll-mt-16">
        <div className="max-w-6xl mx-auto">
          <SectionFade>
            <div className="text-center mb-10">
              <p className="text-ink-muted text-xs font-extrabold mb-2">Peer-Reviewed Evidence</p>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-ink leading-tight">
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
                <div className="bg-white border-2 border-line rounded-card p-6 h-full flex flex-col">
                  <div className="flex items-start gap-2 mb-3">
                    <span className="text-2xl" aria-hidden="true">{r.icon}</span>
                    <div>
                      <p className="text-ink text-xs font-extrabold leading-tight">{r.journal}</p>
                      <p className="text-ink-muted text-xs">{r.year}</p>
                    </div>
                  </div>
                  <h3 className="text-ink font-extrabold text-sm mb-2 leading-tight">{r.title}</h3>
                  <p className="text-gray-600 text-xs leading-relaxed flex-1">{r.body}</p>
                  <p className="text-ink-muted text-xs mt-3 italic">{r.authors}</p>
                </div>
              </SectionFade>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRICING ───────────────────────────────────────────────────────────── */}
      {MONETIZATION_ENABLED && (
        <section className="bg-soft border-y-2 border-line py-16 px-4 sm:px-6">
          <div className="max-w-6xl mx-auto">
            <SectionFade>
              <div className="text-center mb-10">
                <h2 className="text-2xl sm:text-3xl font-extrabold text-ink mb-2">Simple, honest pricing.</h2>
                <p className="text-gray-500 text-sm">Start free — upgrade when you&apos;re ready. No card required.</p>
              </div>
            </SectionFade>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {PLANS.map((plan, i) => (
                <SectionFade key={plan.id} delay={i * 100}>
                  <div className={`bg-white border-2 ${plan.borderColor} rounded-card overflow-hidden h-full flex flex-col ${plan.popular ? 'shadow-hard-lg' : ''}`}>
                    {plan.popular && (
                      <div className="bg-star text-ink text-xs font-extrabold text-center py-1.5">Most Popular</div>
                    )}
                    <div className="p-6 flex flex-col flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xl" aria-hidden="true">{plan.emoji}</span>
                        <span className="text-ink font-extrabold text-lg">{plan.name}</span>
                      </div>
                      <div className="flex items-baseline gap-1 mb-5">
                        <span className="text-3xl font-extrabold text-ink">₹{plan.monthly.toLocaleString('en-IN')}</span>
                        <span className="text-ink-muted text-sm">/mo</span>
                      </div>
                      <ul className="space-y-2 flex-1 mb-5">
                        {plan.features.map(f => (
                          <li key={f} className="flex items-start gap-2 text-xs text-gray-600">
                            <span className="text-success font-bold shrink-0 mt-0.5" aria-hidden="true">✓</span> {f}
                          </li>
                        ))}
                      </ul>
                      <Link href="/start" className={`block w-full text-center ${plan.ctaClass} border-2 border-ink shadow-hard-sm font-extrabold py-3 rounded-control transition-colors text-sm`}>
                        Start Free
                      </Link>
                    </div>
                  </div>
                </SectionFade>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ── FINAL CTA ─────────────────────────────────────────────────────────── */}
      <section className="py-16 px-4 sm:px-6">
        <SectionFade>
          <div className="max-w-2xl mx-auto bg-ink rounded-card px-8 py-12 text-center">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-3 leading-tight">
              See it for yourself in 2 minutes.
            </h2>
            <p className="text-white/80 text-base mb-8 max-w-md mx-auto">
              Pick your grade, answer 5 questions, and get a personalised learning path — no sign up needed.
            </p>
            <Link
              href="/start"
              className="inline-block bg-action text-white border-2 border-white font-extrabold py-4 px-10 rounded-control text-lg transition-colors hover:bg-action-dark active:translate-y-0.5"
            >
              Start Free Diagnostic
            </Link>
            <p className="text-white/70 text-xs mt-4">No account required. Save progress later.</p>
          </div>
        </SectionFade>
      </section>

      {/* ── FOOTER ────────────────────────────────────────────────────────────── */}
      <footer className="bg-ink px-4 sm:px-6 py-10 text-center">
        <div className="flex items-center justify-center gap-2 mb-3">
          <Sparky size={26} mood="happy" />
          <span className="text-white font-extrabold text-base">MathSpark</span>
        </div>
        <p className="text-white/70 text-xs mb-1">Built by mathletes and educationists for IPM &amp; Olympiad aspirants.</p>
        <p className="text-white/70 text-xs mb-5">
          100,000+ researched questions · 4 years of real papers · Zero hallucination · Adaptive AI
        </p>
        <div className="flex flex-wrap justify-center gap-4 sm:gap-6 text-white/70 text-xs font-semibold mb-5">
          {MONETIZATION_ENABLED && (
            <Link href="/pricing"     className="hover:text-white transition-colors">Pricing</Link>
          )}
          <Link href="/start"         className="hover:text-white transition-colors">Try it free</Link>
          <Link href="/auth/login"    className="hover:text-white transition-colors">Sign in</Link>
          <a href="#"                 className="hover:text-white transition-colors">Privacy</a>
          <a href="#"                 className="hover:text-white transition-colors">Terms</a>
          <a href="mailto:hello@mathspark.app" className="hover:text-white transition-colors">Contact</a>
        </div>
        <p className="text-white/70 text-xs">© 2026 MathSpark. Research citations available on request.</p>
      </footer>

    </div>
  );
}

'use client';

import { useState } from 'react';
import Link from 'next/link';

// ── Plan data ──────────────────────────────────────────────────────────────

const PLANS = [
  {
    id:      'starter',
    emoji:   '🌱',
    name:    'Starter',
    monthly: 500,
    annual:  4800,
    annualMonthly: 400,
    color:   'border-[#58CC02]',
    badge:   'bg-[#58CC02]/10 text-[#58CC02]',
    ctaClass:'bg-[#58CC02] hover:bg-[#46a302]',
    popular: false,
    features: [
      '2,505+ practice questions',
      '1 hour / day',
      '3-level hint system',
      'Step-by-step solutions',
      '5 AI tutor chats / day',
      'Progress tracking',
    ],
    locked: [
      'Diagnostic quiz',
      'Adaptive difficulty',
      'Misconception feedback',
      'Mock test mode',
      'Parent dashboard',
      'Badges & streaks',
    ],
  },
  {
    id:      'advanced',
    emoji:   '⚡',
    name:    'Advanced',
    monthly: 1500,
    annual:  14400,
    annualMonthly: 1200,
    color:   'border-[#1CB0F6]',
    badge:   'bg-[#1CB0F6]/10 text-[#1CB0F6]',
    ctaClass:'bg-[#1CB0F6] hover:bg-[#0a98dc]',
    popular: true,
    features: [
      'Everything in Starter',
      '5 hours / day',
      'Diagnostic quiz',
      'Adaptive difficulty engine',
      'Misconception feedback',
      '25 AI tutor chats / day',
    ],
    locked: [
      'Mock test mode',
      'Full dashboard & analytics',
      'Parent dashboard',
      'Badges & streaks',
    ],
  },
  {
    id:      'unlimited',
    emoji:   '🏆',
    name:    'Unlimited',
    monthly: 5000,
    annual:  48000,
    annualMonthly: 4000,
    color:   'border-[#9B59B6]',
    badge:   'bg-purple-100 text-purple-700',
    ctaClass:'bg-[#9B59B6] hover:bg-[#7D3C98]',
    popular: false,
    features: [
      'Everything in Advanced',
      'Unlimited time / day',
      '100 AI tutor chats / day',
      'Mock test mode (all papers)',
      'Full dashboard & analytics',
      'Parent dashboard',
      'Badges, streaks & XP',
      'Monthly new content',
    ],
    locked: [],
  },
];

const FAQS = [
  { q: 'Is there a free trial?',            a: 'Yes! All plans come with a 3-day free trial. No payment required to start.' },
  { q: 'Can I switch plans?',               a: 'Yes, upgrade or downgrade anytime. We'll prorate the difference automatically.' },
  { q: 'What happens when my plan expires?',a: 'You keep all your progress but can't practice new questions until you renew.' },
  { q: 'Do you offer sibling discounts?',   a: 'Yes! Get 50% off for a second child on the same parent account.' },
  { q: 'Can I get a refund?',               a: 'Full refund within 7 days if you're not satisfied — no questions asked.' },
];

const COMPARISON_ROWS = [
  { feature: 'Practice questions',      starter: '2,505+',   advanced: '2,505+',   unlimited: '2,505+' },
  { feature: 'Daily time limit',        starter: '1 hour',   advanced: '5 hours',  unlimited: 'Unlimited' },
  { feature: 'Hint system',             starter: true,        advanced: true,        unlimited: true },
  { feature: 'Step-by-step solutions',  starter: true,        advanced: true,        unlimited: true },
  { feature: 'AI tutor chats / day',    starter: '5',         advanced: '25',        unlimited: '100' },
  { feature: 'Diagnostic quiz',         starter: false,       advanced: true,        unlimited: true },
  { feature: 'Adaptive difficulty',     starter: false,       advanced: true,        unlimited: true },
  { feature: 'Misconception feedback',  starter: false,       advanced: true,        unlimited: true },
  { feature: 'Progress tracking',       starter: true,        advanced: true,        unlimited: true },
  { feature: 'Full dashboard',          starter: false,       advanced: false,       unlimited: true },
  { feature: 'Mock test mode',          starter: false,       advanced: false,       unlimited: true },
  { feature: 'Parent dashboard',        starter: false,       advanced: false,       unlimited: true },
  { feature: 'Badges & streaks',        starter: false,       advanced: false,       unlimited: true },
];

function Check() { return <span className="text-[#58CC02] font-bold">✓</span>; }
function Cross() { return <span className="text-gray-300">✕</span>; }
function Cell({ v }: { v: boolean | string }) {
  if (typeof v === 'string') return <span className="text-gray-700 font-semibold text-sm">{v}</span>;
  return v ? <Check /> : <Cross />;
}

export default function PricingPage() {
  const [annual,      setAnnual]      = useState(false);
  const [openFaq,     setOpenFaq]     = useState<number | null>(null);
  const [showCompare, setShowCompare] = useState(false);

  return (
    <div className="min-h-screen bg-white pb-20">
      {/* Nav */}
      <div className="bg-[#131F24] px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-white font-extrabold text-lg">MathSpark ⭐</Link>
        <Link href="/auth/login" className="text-white/60 text-sm font-semibold hover:text-white transition-colors">
          Sign in →
        </Link>
      </div>

      {/* Hero */}
      <div className="bg-[#131F24] px-4 pt-8 pb-12 text-center">
        <h1 className="text-2xl font-extrabold text-white leading-tight">
          IPM prep that actually works —<br />for a fraction of coaching costs
        </h1>
        <p className="text-white/60 text-sm mt-3 max-w-sm mx-auto">
          One coaching session = ₹1,500. MathSpark gives you more for less.
        </p>

        {/* Monthly / Annual toggle */}
        <div className="flex items-center justify-center gap-3 mt-6">
          <span className={`text-sm font-bold ${!annual ? 'text-white' : 'text-white/40'}`}>Monthly</span>
          <button
            onClick={() => setAnnual(!annual)}
            className={`relative w-12 h-6 rounded-full transition-colors ${annual ? 'bg-[#58CC02]' : 'bg-white/20'}`}
          >
            <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${annual ? 'translate-x-6' : 'translate-x-0.5'}`} />
          </button>
          <span className={`text-sm font-bold ${annual ? 'text-white' : 'text-white/40'}`}>
            Annual
            <span className="ml-1.5 bg-[#FF9600] text-white text-[10px] font-extrabold px-1.5 py-0.5 rounded-full">SAVE 20%</span>
          </span>
        </div>
      </div>

      {/* Plan cards */}
      <div className="px-4 -mt-4 space-y-4">
        {PLANS.map((plan) => (
          <div
            key={plan.id}
            className={`bg-white rounded-2xl border-2 ${plan.color} shadow-lg overflow-hidden ${plan.popular ? 'ring-2 ring-[#1CB0F6] ring-offset-2' : ''}`}
          >
            {plan.popular && (
              <div className="bg-[#1CB0F6] text-white text-xs font-extrabold text-center py-1.5 tracking-widest uppercase">
                ⭐ Most Popular
              </div>
            )}
            <div className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-2xl">{plan.emoji}</span>
                    <span className="text-xl font-extrabold text-gray-800">{plan.name}</span>
                  </div>
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-extrabold text-gray-900">
                      ₹{annual ? plan.annualMonthly.toLocaleString('en-IN') : plan.monthly.toLocaleString('en-IN')}
                    </span>
                    <span className="text-gray-400 text-sm">/mo</span>
                    {annual && (
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ml-2 ${plan.badge}`}>
                        ₹{plan.annual.toLocaleString('en-IN')}/yr
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <ul className="mt-4 space-y-1.5">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-[#58CC02] font-bold mt-0.5 shrink-0">✓</span>
                    {f}
                  </li>
                ))}
                {plan.locked.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-gray-400">
                    <span className="mt-0.5 shrink-0">✕</span>
                    {f}
                  </li>
                ))}
              </ul>

              <Link
                href="/auth/register"
                className={`block w-full text-center ${plan.ctaClass} text-white font-extrabold py-3.5 rounded-2xl mt-5 transition-colors`}
              >
                Start Free Trial →
              </Link>
              <p className="text-center text-gray-400 text-xs mt-1.5">3-day free trial · No card required</p>
            </div>
          </div>
        ))}
      </div>

      {/* Value comparison */}
      <div className="mx-4 mt-6 bg-amber-50 border border-amber-200 rounded-2xl p-4">
        <p className="text-amber-800 text-sm leading-relaxed">
          💡 <strong>Compare:</strong> Private coaching costs ₹18,000/month for 3 sessions/week.
          MathSpark Unlimited gives you 24/7 AI-powered practice, adaptive learning, and detailed analytics
          for <strong>₹5,000/month</strong> — <strong>72% less than coaching</strong>, available anytime.
        </p>
      </div>

      {/* Feature comparison table */}
      <div className="mx-4 mt-6">
        <button
          onClick={() => setShowCompare(!showCompare)}
          className="w-full flex items-center justify-between bg-gray-50 rounded-2xl px-4 py-3 text-gray-700 font-semibold text-sm"
        >
          <span>Compare all features</span>
          <span className="text-gray-400">{showCompare ? '▲' : '▼'}</span>
        </button>

        {showCompare && (
          <div className="mt-2 overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left px-3 py-2 font-semibold text-gray-500 text-xs">Feature</th>
                  <th className="text-center px-2 py-2 font-extrabold text-[#58CC02] text-xs">🌱</th>
                  <th className="text-center px-2 py-2 font-extrabold text-[#1CB0F6] text-xs">⚡</th>
                  <th className="text-center px-2 py-2 font-extrabold text-[#9B59B6] text-xs">🏆</th>
                </tr>
              </thead>
              <tbody>
                {COMPARISON_ROWS.map((row, i) => (
                  <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-3 py-2 text-gray-600 text-xs">{row.feature}</td>
                    <td className="text-center px-2 py-2"><Cell v={row.starter} /></td>
                    <td className="text-center px-2 py-2"><Cell v={row.advanced} /></td>
                    <td className="text-center px-2 py-2"><Cell v={row.unlimited} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* FAQ */}
      <div className="mx-4 mt-6">
        <h2 className="text-lg font-extrabold text-gray-800 mb-3">Frequently asked questions</h2>
        <div className="space-y-2">
          {FAQS.map((faq, i) => (
            <div key={i} className="border border-gray-200 rounded-xl overflow-hidden">
              <button
                onClick={() => setOpenFaq(openFaq === i ? null : i)}
                className="w-full flex items-center justify-between px-4 py-3 text-left text-gray-800 font-semibold text-sm bg-white hover:bg-gray-50 transition-colors"
              >
                <span>{faq.q}</span>
                <span className="text-gray-400 ml-2">{openFaq === i ? '▲' : '▼'}</span>
              </button>
              {openFaq === i && (
                <div className="px-4 pb-3 text-gray-600 text-sm bg-gray-50">{faq.a}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* CTA footer */}
      <div className="mx-4 mt-8 bg-[#131F24] rounded-2xl p-6 text-center">
        <p className="text-white font-extrabold text-lg mb-1">Ready to get started?</p>
        <p className="text-white/50 text-sm mb-4">Join thousands of Grade 4 students mastering IPM math</p>
        <Link
          href="/auth/register"
          className="block w-full bg-[#58CC02] hover:bg-[#46a302] text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
        >
          Start Free Trial →
        </Link>
        <p className="text-white/30 text-xs mt-2">3-day free trial · No card required · Cancel anytime</p>
      </div>
    </div>
  );
}

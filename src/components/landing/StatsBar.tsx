'use client';

import { useState, useEffect, useRef } from 'react';

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

function StatCard({ prefix = '', target, suffix = '', label, color, inView }: {
  prefix?: string; target: number; suffix?: string; label: string; color: string; inView: boolean;
}) {
  const count = useCountUp(target, inView);
  return (
    <div className="text-center py-5 px-2 overflow-hidden">
      <div className={`text-xl sm:text-3xl font-extrabold ${color} tabular-nums leading-none truncate`}>
        {prefix}{target === 0 ? '0' : count.toLocaleString('en-IN')}{suffix}
      </div>
      <div className="text-gray-500 text-xs sm:text-sm mt-1.5 leading-tight">{label}</div>
    </div>
  );
}

export default function StatsBar() {
  const [ref, inView] = useInView(0.25);
  return (
    <section className="py-10 px-4 sm:px-6">
      <div className="max-w-4xl mx-auto">
        <div ref={ref} className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-gray-100 bg-white border border-gray-100 rounded-2xl shadow-sm">
          <StatCard target={100000} suffix="+" label="Richly Researched Questions" color="text-duo-green" inView={inView} />
          <StatCard target={4}      suffix=" Yrs" label="of Real IPM Papers"       color="text-duo-blue"  inView={inView} />
          <StatCard target={0}                    label="Hallucinated Answers"      color="text-duo-dark"  inView={inView} />
          <StatCard target={2}      suffix="×"    label="Faster Learning (cited)"   color="text-duo-orange" inView={inView} />
        </div>
        <p className="text-center text-gray-400 text-xs mt-2 italic">
          Muralidharan, Singh &amp; Ganimian — American Economic Review, 2019
        </p>
      </div>
    </section>
  );
}

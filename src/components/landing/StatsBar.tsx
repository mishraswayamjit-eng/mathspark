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

function StatCard({ prefix = '', target, suffix = '', label, inView }: {
  prefix?: string; target: number; suffix?: string; label: string; inView: boolean;
}) {
  const count = useCountUp(target, inView);
  return (
    <div className="text-center py-5 px-2 overflow-hidden">
      <div className="text-xl sm:text-3xl font-extrabold text-white tabular-nums leading-none truncate">
        {prefix}{target === 0 ? '0' : count.toLocaleString('en-IN')}{suffix}
      </div>
      <div className="text-white/60 text-xs sm:text-sm mt-1.5 leading-tight">{label}</div>
    </div>
  );
}

export default function StatsBar() {
  const [ref, inView] = useInView(0.25);
  return (
    <section className="py-10 px-4 max-w-4xl mx-auto">
      <div ref={ref} className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-white/10 bg-white/[0.03] border border-white/10 rounded-2xl">
        <StatCard target={100000} suffix="+" label="Richly Researched Questions" inView={inView} />
        <StatCard target={4}      suffix=" Yrs" label="of Real IPM Papers"         inView={inView} />
        <StatCard target={0}                    label="Hallucinated Answers"        inView={inView} />
        <StatCard target={2}      suffix="×"    label="Faster Learning (cited)"     inView={inView} />
      </div>
      <p className="text-center text-white/20 text-xs mt-2 italic">
        ²Muralidharan, Singh &amp; Ganimian — American Economic Review, 2019
      </p>
    </section>
  );
}

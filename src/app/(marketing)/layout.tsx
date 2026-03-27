import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'MathSpark — Adaptive Math Learning for IPM & Olympiad Prep',
  description:
    'India\'s smartest IPM & Olympiad prep — adaptive AI tutoring, 100,000+ questions, real exam simulations. Built by competitive math champions.',
};

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

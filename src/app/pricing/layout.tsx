import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Pricing',
  description: 'Choose a MathSpark plan that fits your learning needs.',
};

export default function PricingLayout({ children }: { children: React.ReactNode }) {
  return children;
}

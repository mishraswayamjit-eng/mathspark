import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Worked Examples',
  description: 'Browse step-by-step worked examples for math problems.',
};

export default function ExamplesLayout({ children }: { children: React.ReactNode }) {
  return children;
}

import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Test',
  description: 'Take timed math tests and past-year exam papers.',
};

export default function TestLayout({ children }: { children: React.ReactNode }) {
  return children;
}

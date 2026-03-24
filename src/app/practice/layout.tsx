import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Practice',
  description: 'Practice math problems with step-by-step Socratic guidance.',
};

export default function PracticeLayout({ children }: { children: React.ReactNode }) {
  return children;
}

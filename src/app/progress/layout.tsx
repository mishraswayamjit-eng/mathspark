import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Progress',
  description: 'Track your math mastery and learning progress over time.',
};

export default function ProgressLayout({ children }: { children: React.ReactNode }) {
  return children;
}

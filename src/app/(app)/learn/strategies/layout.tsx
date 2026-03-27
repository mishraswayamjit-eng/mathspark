import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Strategies',
  description: 'Learn effective problem-solving strategies for math.',
};

export default function StrategiesLayout({ children }: { children: React.ReactNode }) {
  return children;
}

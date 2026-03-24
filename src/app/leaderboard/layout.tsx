import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Leaderboard',
  description: 'See how you rank against other MathSpark learners.',
};

export default function LeaderboardLayout({ children }: { children: React.ReactNode }) {
  return children;
}

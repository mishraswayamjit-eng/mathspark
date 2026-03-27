import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Home',
  description: 'Your personalized MathSpark dashboard with daily goals and progress.',
};

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  return children;
}

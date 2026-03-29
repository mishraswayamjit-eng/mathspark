import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Concept Lessons | MathSpark',
  description: 'Learn new math concepts step-by-step with interactive lessons and quizzes.',
};

export default function LessonsLayout({ children }: { children: React.ReactNode }) {
  return children;
}

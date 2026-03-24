import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Flashcards',
  description: 'Review math concepts with spaced-repetition flashcards.',
};

export default function FlashcardsLayout({ children }: { children: React.ReactNode }) {
  return children;
}

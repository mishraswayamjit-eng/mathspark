import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Create Account',
  description: 'Create a new MathSpark account for your child.',
};

export default function RegisterLayout({ children }: { children: React.ReactNode }) {
  return children;
}

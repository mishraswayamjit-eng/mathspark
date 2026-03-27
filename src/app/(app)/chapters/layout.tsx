import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Chapters',
  description: 'Browse math chapters and topics organized by grade.',
};

export default function ChaptersLayout({ children }: { children: React.ReactNode }) {
  return children;
}

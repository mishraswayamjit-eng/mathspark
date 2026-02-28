import type { Metadata } from 'next';
import './globals.css';
import BottomNav from '@/components/BottomNav';

export const metadata: Metadata = {
  title: 'MathSpark — Grade 4 Math',
  description: 'Fun, safe math learning and IPM exam prep for Grade 4 students',
  manifest: '/manifest.json',
  themeColor: '#58CC02',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#131F24] min-h-screen font-sans">
        <main className="bg-white max-w-lg mx-auto min-h-screen pb-20">
          {children}
        </main>
        <BottomNav />
      </body>
    </html>
  );
}

import type { Metadata } from 'next';
import './globals.css';
import BottomNav from '@/components/BottomNav';
import PageTransitionWrapper from '@/components/PageTransitionWrapper';

export const metadata: Metadata = {
  title: 'MathSpark — Grade 4 Math',
  description: 'Fun, safe math learning and IPM exam prep for Grade 4 students',
  manifest: '/manifest.json',
};

export const viewport = {
  themeColor: '#3b82f6',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen font-sans">
        <main className="max-w-lg mx-auto min-h-screen pb-20">
          <PageTransitionWrapper>{children}</PageTransitionWrapper>
        </main>
        <BottomNav />
        <script
          dangerouslySetInnerHTML={{
            __html: `
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
          navigator.serviceWorker.register('/sw.js');
        });
      }
    `,
          }}
        />
      </body>
    </html>
  );
}

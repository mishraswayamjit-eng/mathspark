import type { Metadata } from 'next';
import { Inter, Baloo_2, Nunito } from 'next/font/google';
import './globals.css';
import BottomNav from '@/components/BottomNav';
import PageTransitionWrapper from '@/components/PageTransitionWrapper';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

// MathSpark design system: Baloo 2 (display) + Nunito (body)
const baloo = Baloo_2({
  subsets: ['latin'],
  display: 'swap',
  weight: ['500', '600', '700', '800'],
  variable: '--font-display',
});

const nunito = Nunito({
  subsets: ['latin'],
  display: 'swap',
  weight: ['400', '600', '700', '800'],
  variable: '--font-body',
});

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
    <html lang="en" className={`${inter.variable} ${baloo.variable} ${nunito.variable}`}>
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

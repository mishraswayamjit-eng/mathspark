import type { Metadata, Viewport } from 'next';
import './fonts.css';
import './tokens.css';
import './globals.css';
import SessionProvider from '@/components/SessionProvider';
import { Analytics } from '@vercel/analytics/next';

// Fonts are self-hosted: see ./fonts.css (no request to Google Fonts at build time).

export const viewport: Viewport = {
  themeColor: '#1d2a4d',
  viewportFit: 'cover',
};

export const metadata: Metadata = {
  metadataBase: new URL('https://mathspark.vercel.app'),
  title: {
    default: 'MathSpark — Fun Math Practice for Grade 4 IPM',
    template: '%s | MathSpark',
  },
  description:
    'Adaptive math learning and IPM exam prep for Grade 4. 2,345 questions with hints and step-by-step solutions. Free & child-safe.',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'MathSpark',
  },
  openGraph: {
    title: 'MathSpark — Fun Math Practice for Grade 4 IPM',
    description: 'Adaptive math, 2,345 questions, IPM prep, child-safe.',
    type: 'website',
    locale: 'en_IN',
  },
  twitter: {
    card: 'summary_large_image',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-paper text-gray-800 min-h-screen font-sans">
        <SessionProvider>
          {children}
          <Analytics />
        </SessionProvider>
      </body>
    </html>
  );
}

import type { Metadata, Viewport } from 'next';
import { Nunito } from 'next/font/google';
import './globals.css';
import SessionProvider from '@/components/SessionProvider';
import { Analytics } from '@vercel/analytics/next';

const nunito = Nunito({
  subsets: ['latin'],
  weight: ['400', '700', '800', '900'],
  display: 'swap',
});

export const viewport: Viewport = {
  themeColor: '#58CC02',
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
      <body className={`bg-duo-dark min-h-screen ${nunito.className}`}>
        <SessionProvider>
          {children}
          <Analytics />
        </SessionProvider>
      </body>
    </html>
  );
}

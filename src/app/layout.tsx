import type { Metadata } from 'next';
import './globals.css';
import BottomNav from '@/components/BottomNav';
import ServiceWorkerRegistrar from '@/components/ServiceWorkerRegistrar';
import AddToHomeScreen from '@/components/AddToHomeScreen';
import { Analytics } from '@vercel/analytics/next';

export const metadata: Metadata = {
  metadataBase: new URL('https://mathspark.vercel.app'),
  title: {
    default: 'MathSpark — Fun Math Practice for Grade 4 IPM',
    template: '%s | MathSpark',
  },
  description:
    'Adaptive math learning and IPM exam prep for Grade 4. 2,345 questions with hints and step-by-step solutions. Free & child-safe.',
  manifest: '/manifest.json',
  themeColor: '#58CC02',
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
      <body className="bg-[#131F24] min-h-screen font-sans">
        <main className="bg-white max-w-lg mx-auto min-h-screen pb-20">
          {children}
        </main>
        <BottomNav />
        <AddToHomeScreen />
        <ServiceWorkerRegistrar />
        <Analytics />
      </body>
    </html>
  );
}

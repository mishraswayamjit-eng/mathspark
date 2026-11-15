import type { Metadata, Viewport } from 'next';
import './fonts.css';
import './tokens.css';
import './globals.css';
import SessionProvider from '@/components/SessionProvider';
import { Analytics } from '@vercel/analytics/next';
import localFont from 'next/font/local';

// Fonts are self-hosted: see ./fonts.css (no request to Google Fonts at build time).
//
// The two Latin files carry almost every glyph the app shows, so they are also
// loaded through next/font, which adds <link rel="preload"> for them on every
// page: text paints in Nunito/Fredoka straight away instead of in a fallback
// that is swapped out later. Each sets the same CSS variable fonts.css defines
// (--font-nunito / --font-fredoka) on <body>, with the fonts.css family as the
// next choice, so the extended-Latin files (rupee sign) still apply and nothing
// in tailwind.config.ts or globals.css changes.
const nunito = localFont({
  src: './fonts/Nunito-latin-variable.woff2',
  weight: '400 900',
  style: 'normal',
  display: 'swap',
  variable: '--font-nunito',
  fallback: ['Nunito'],
  adjustFontFallback: false,
  preload: true,
});

const fredoka = localFont({
  src: './fonts/Fredoka-latin-variable.woff2',
  weight: '500 700',
  style: 'normal',
  display: 'swap',
  variable: '--font-fredoka',
  fallback: ['Fredoka'],
  adjustFontFallback: false,
  preload: true,
});

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
      <body className={`${nunito.variable} ${fredoka.variable} bg-paper text-gray-800 min-h-screen font-sans`}>
        <SessionProvider>
          {children}
          <Analytics />
        </SessionProvider>
      </body>
    </html>
  );
}

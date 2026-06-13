import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        // New MathSpark design system (Brilliant-style premium minimal)
        display: ['var(--font-display)', 'var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        body: ['var(--font-body)', 'var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        'duo-blue': '#1cb0f6',
        // ── MathSpark design tokens ──────────────────────────────
        spark: {
          indigo: '#5B5BD6',
          'indigo-dark': '#3D3DAA',
          'indigo-soft': '#ECECFB',
          yellow: '#FFC53D',
          coral: '#FF7A59',
          green: '#3DBE7A',
          'green-soft': '#E4F6EC',
          amber: '#F5A623',
          'amber-soft': '#FDF2DD',
        },
        surface: {
          cream: '#FBF7F0',
          card: '#FFFFFF',
          muted: '#F0EDE6',
        },
        ink: {
          DEFAULT: '#2A2A40',
          muted: '#6B6B85',
          faint: '#A3A3B8',
        },
      },
      boxShadow: {
        soft: '0 4px 16px rgba(42,42,64,0.08)',
        'soft-lg': '0 8px 28px rgba(42,42,64,0.10)',
        press: '0 4px 0 #3D3DAA',
        'press-sm': '0 2px 0 #3D3DAA',
      },
      borderRadius: {
        spark: '1.25rem',
      },
    },
  },
  plugins: [],
};

export default config;

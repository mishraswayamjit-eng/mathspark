import type { Config } from 'tailwindcss';

// Theme convention:
// - Light mode (bg-gray-50/bg-white): home, chapters, learn/*, leaderboard, profile, progress
// - Dark mode (bg-[#0F172A]): flashcards, flashcard sessions
// - Dark header (bg-duo-dark) + light body: all pages use duo-dark sticky header

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Nunito', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        duo: {
          green:        '#58CC02',
          'green-dark': '#46a302',
          blue:         '#1CB0F6',
          'blue-dark':  '#0a98dc',
          orange:       '#FF9600',
          'orange-dark':'#cc7800',
          red:          '#FF4B4B',
          'red-dark':   '#cc3333',
          gold:         '#FFC800',
          dark:         '#131F24',
        },
      },
    },
  },
  plugins: [],
};

export default config;

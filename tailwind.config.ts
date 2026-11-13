import type { Config } from 'tailwindcss';
import tokens from './design/tokens.json';

// Socratic design system — see design/DESIGN.md.
//
// design/tokens.json is the single source of truth. This file maps it onto
// Tailwind; scripts/build_tokens.py emits the same values as CSS variables
// (src/app/tokens.css) for the hand-written classes in globals.css.
//
// Use the role names: ink, canvas, card, soft, line, action, success, retry,
// hint, star. The `duo-*` names and the re-tinted `gray` scale exist only so
// the hundreds of older call sites pick up the palette; do not use `duo-*` in
// new code.
//
// Dark mode (bg-[#0F172A]) is used only by flashcards and is outside this system.

const color = (name: keyof typeof tokens.color): string => tokens.color[name].$value;
const radius = (name: keyof typeof tokens.radius): string => tokens.radius[name].$value;
const shadow = (name: keyof typeof tokens.shadow): string => tokens.shadow[name].$value;

type TypeStep = keyof typeof tokens.typography;
const type = (name: TypeStep): [string, { lineHeight: string; fontWeight: string }] => {
  const v = tokens.typography[name].$value;
  return [v.fontSize, { lineHeight: String(v.lineHeight), fontWeight: String(v.fontWeight) }];
};

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-nunito)', 'Nunito', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        display: ['var(--font-fredoka)', 'var(--font-nunito)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        caption:  type('caption'),
        label:    type('label'),
        body:     type('body'),
        question: type('question'),
        title:    type('title'),
        heading:  type('heading'),
        display:  type('display'),
      },
      borderRadius: {
        note:    radius('note'),
        tile:    radius('tile'),
        control: radius('control'),
        card:    radius('card'),
      },
      boxShadow: {
        'hard-xs': shadow('hard-xs'),
        'hard-sm': shadow('hard-sm'),
        hard:      shadow('hard'),
        'hard-lg': shadow('hard-lg'),
      },
      colors: {
        // ── Role tokens (use these) ────────────────────────────────────────
        ink:     { DEFAULT: color('ink'), muted: color('ink-muted') },
        canvas:  { DEFAULT: color('canvas'), grid: color('canvas-grid') },
        card:    color('card'),
        soft:    color('soft'),
        line:    color('line'),
        action:  { DEFAULT: color('action'), dark: color('action-dark') },
        success: { DEFAULT: color('success'), soft: color('success-soft') },
        retry:   { DEFAULT: color('retry'), soft: color('retry-soft') },
        hint:    { DEFAULT: color('hint'), ink: color('hint-ink') },
        star:    color('star'),

        // ── Neutral ramp: Tailwind `gray` re-tinted to the ink/line family ──
        gray: {
          50:  color('canvas'),
          100: '#e6eef8',
          200: color('line'),
          300: '#b9c7de',
          400: '#8e9bb8',
          500: color('ink-muted'),
          600: '#47557a',
          700: '#33416a',
          800: color('ink'),
          900: '#141d38',
          950: '#0c1226',
        },

        // ── Legacy aliases (older call sites only — do not use in new code) ─
        duo: {
          // Lighter than `success` on purpose: it is still used as text on ink headers.
          green:        '#15966a',
          'green-dark': '#0f7552',
          blue:         '#1CB0F6',
          'blue-dark':  '#0a98dc',
          orange:       '#FF9600',
          'orange-dark':'#cc7800',
          red:          '#FF4B4B',
          'red-dark':   '#cc3333',
          gold:         '#FFC800',
          dark:         color('ink'),
          mint:         color('success-soft'),
          'mint-dark':  '#bdebd3',
          blush:        color('retry-soft'),
          'blush-dark': '#f8c9ce',
        },
      },
    },
  },
  plugins: [],
};

export default config;

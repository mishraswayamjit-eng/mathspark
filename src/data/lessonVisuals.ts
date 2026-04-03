import type { SlideIllustration } from '@/types/lesson';

/**
 * Maps the existing lesson.visual string values to SlideIllustration objects.
 * These turn the old monospace text placeholders into real SVG diagrams.
 *
 * Only visuals with a natural diagram-component mapping are included.
 * Unmapped visuals gracefully fall back to no illustration.
 */
export const LESSON_VISUALS: Record<string, SlideIllustration> = {
  // ── Fractions ────────────────────────────────────────────────
  'roti-split-half': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 2, shadedParts: 1, label: '1 roti → 2 equal parts' },
  },
  'fraction-anatomy': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 4, shadedParts: 3, columns: 4, label: '3 out of 4' },
  },
  'fraction-names-chart': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'circle', totalParts: 2, shadedParts: 1, label: '½' },
        { shape: 'circle', totalParts: 3, shadedParts: 1, label: '⅓' },
        { shape: 'circle', totalParts: 4, shadedParts: 1, label: '¼' },
      ],
    },
  },
  'unit-fraction-bars': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 2, shadedParts: 1, columns: 2, label: '1/2' },
        { shape: 'rectangle', totalParts: 3, shadedParts: 1, columns: 3, label: '1/3' },
        { shape: 'rectangle', totalParts: 4, shadedParts: 1, columns: 4, label: '1/4' },
      ],
    },
  },
  'bar-model-equivalence': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 2, shadedParts: 1, columns: 2, label: '1/2' },
        { shape: 'rectangle', totalParts: 4, shadedParts: 2, columns: 4, label: '2/4' },
      ],
    },
  },
  'multiply-top-bottom': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'rectangle', totalParts: 3, shadedParts: 1, columns: 3, label: '1/3' },
        { shape: 'rectangle', totalParts: 6, shadedParts: 2, columns: 6, label: '2/6' },
      ],
    },
  },
  'simplify-fraction': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 6, shadedParts: 4, columns: 6, label: '4/6 = 2/3' },
  },
  'add-same-denom': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 5, shadedParts: 3, columns: 5, label: '1/5 + 2/5 = 3/5' },
  },
  'subtract-same-denom': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 4, shadedParts: 1, columns: 4, label: '3/4 − 2/4 = 1/4' },
  },
  'fraction-of-whole': {
    type: 'fraction',
    props: { shape: 'circle', totalParts: 4, shadedParts: 3, label: '3/4 of the whole' },
  },
  'multiply-two-fractions': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 6, shadedParts: 2, columns: 3, label: '2/3 × 1/2 = 2/6' },
  },
  'mixed-to-improper': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'circle', totalParts: 4, shadedParts: 4, label: '1 whole' },
        { shape: 'circle', totalParts: 4, shadedParts: 3, label: '3/4' },
      ],
    },
  },
  'improper-to-mixed': {
    type: 'multiFraction',
    props: {
      figures: [
        { shape: 'circle', totalParts: 3, shadedParts: 3, label: '3/3 = 1' },
        { shape: 'circle', totalParts: 3, shadedParts: 2, label: '2/3' },
      ],
    },
  },

  // ── Time & Calendar ──────────────────────────────────────────
  'clock-hands': {
    type: 'clock',
    props: { hour: 3, minute: 0 },
  },
  'clock-oclock': {
    type: 'clock',
    props: { hour: 9, minute: 0 },
  },
  'clock-half-quarter': {
    type: 'clock',
    props: { hour: 6, minute: 30 },
  },
  'clock-any-time': {
    type: 'clock',
    props: { hour: 10, minute: 25 },
  },
  'clock-add-minutes': {
    type: 'clock',
    props: { hour: 2, minute: 45 },
  },
  'clock-subtract-time': {
    type: 'clock',
    props: { hour: 4, minute: 15 },
  },
  'elapsed-time-number-line': {
    type: 'numberLine',
    props: { min: 0, max: 60, points: [{ value: 15, label: '15 min' }, { value: 45, label: '45 min' }] },
  },

  // ── Equations ────────────────────────────────────────────────
  'balance-scale': {
    type: 'balance',
    props: {
      scales: [{ left: [{ label: 'x' }, { label: '3' }], right: [{ label: '7' }] }],
    },
  },
  'add-both-sides': {
    type: 'balance',
    props: {
      scales: [{ left: [{ label: 'x' }, { label: '-2' }], right: [{ label: '5' }] }],
    },
  },

  // ── Area & Perimeter ─────────────────────────────────────────
  'rectangle-fence': {
    type: 'compositeShape',
    props: {
      rects: [{ x: 10, y: 10, width: 120, height: 80, label: 'Garden' }],
      dimensions: [
        { x1: 10, y1: 95, x2: 130, y2: 95, label: '12 m' },
        { x1: 135, y1: 10, x2: 135, y2: 90, label: '8 m' },
      ],
    },
  },
  'rectangle-labelled': {
    type: 'compositeShape',
    props: {
      rects: [{ x: 10, y: 10, width: 100, height: 60 }],
      dimensions: [
        { x1: 10, y1: 75, x2: 110, y2: 75, label: 'length' },
        { x1: 115, y1: 10, x2: 115, y2: 70, label: 'width' },
      ],
    },
  },
  'triangle-area': {
    type: 'triangle',
    props: {
      variant: 'labeled',
      vertices: [{ x: 70, y: 10 }, { x: 10, y: 110 }, { x: 130, y: 110 }],
      labels: [{ text: 'base', x: 70, y: 125 }, { text: 'height', x: 45, y: 60 }],
    },
  },
  'l-shape': {
    type: 'compositeShape',
    props: {
      rects: [
        { x: 10, y: 10, width: 60, height: 100, shaded: true },
        { x: 70, y: 60, width: 60, height: 50, shaded: true },
      ],
      dimensions: [
        { x1: 10, y1: 115, x2: 130, y2: 115, label: '12 cm' },
        { x1: 135, y1: 10, x2: 135, y2: 110, label: '10 cm' },
      ],
    },
  },
  'circle-parts': {
    type: 'circle',
    props: { variant: 'sector', radius: 50, angle: 90 },
  },

  // ── Ratios ───────────────────────────────────────────────────
  'hundred_grid': {
    type: 'fraction',
    props: { shape: 'rectangle', totalParts: 100, shadedParts: 25, columns: 10, label: '25%' },
  },
  'proportion_balance': {
    type: 'balance',
    props: {
      scales: [{ left: [{ label: '2' }, { label: ':' }, { label: '3' }], right: [{ label: '4' }, { label: ':' }, { label: '6' }] }],
    },
  },
};

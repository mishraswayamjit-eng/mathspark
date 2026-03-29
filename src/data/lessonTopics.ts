import type { LessonTopicMeta } from '@/types/lesson';

/** Lightweight topic list for the grid — avoids loading full JSON data. */
export const LESSON_TOPICS: LessonTopicMeta[] = [
  {
    id: 'fractions',
    topic: 'Fractions',
    emoji: '🍕',
    color: '#F472B6',
    gradeRange: [2, 6],
    description: 'From pizza slices to mixed numbers',
  },
  {
    id: 'area-perimeter',
    topic: 'Area & Perimeter',
    emoji: '📐',
    color: '#A78BFA',
    gradeRange: [3, 7],
    description: 'Shapes, spaces, and boundaries',
  },
  {
    id: 'equations',
    topic: 'Equations',
    emoji: '⚖️',
    color: '#8B5CF6',
    gradeRange: [4, 7],
    description: 'From balance puzzles to multi-step equations',
  },
  {
    id: 'time-calendar',
    topic: 'Time & Calendar',
    emoji: '🕐',
    color: '#FBBF24',
    gradeRange: [2, 5],
    description: 'Clocks, calendars, and speed-distance-time',
  },
  {
    id: 'ratios',
    topic: 'Ratios & Proportions',
    emoji: '⚖️',
    color: '#FB923C',
    gradeRange: [5, 8],
    description: 'Comparing quantities and scaling',
  },
  {
    id: 'geometry',
    topic: 'Geometry',
    emoji: '📏',
    color: '#60A5FA',
    gradeRange: [3, 7],
    description: 'Angles, triangles, and quadrilaterals',
  },
];

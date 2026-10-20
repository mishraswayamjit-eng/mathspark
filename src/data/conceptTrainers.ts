import type { ConceptTrainerMeta } from '@/types/conceptTrainer';

/**
 * Lightweight catalog for the Concept Trainer grid — avoids loading the full
 * (large) trainer JSON just to render the picker. One entry per `data/
 * concept-trainers/<slug>.json` file.
 */
export const CONCEPT_TRAINERS: ConceptTrainerMeta[] = [
  {
    slug: 'percent',
    title: 'Percent Sense',
    emoji: '🎯',
    color: '#F59E0B',
    gradeRange: [5, 9],
    description: 'Build percentage reasoning step by step — name the whole, find the part, avoid the classic traps',
  },
  {
    slug: 'fractions-g4',
    title: 'Fraction Sense · Grade 4',
    emoji: '🍕',
    color: '#1CB0F6',
    gradeRange: [4, 4],
    description: 'Meet fractions as equal parts — name the whole, compare sizes, and spot equivalent fractions',
  },
  {
    slug: 'fractions-g5',
    title: 'Fraction Sense · Grade 5',
    emoji: '🍕',
    color: '#CE82FF',
    gradeRange: [5, 5],
    description: 'Add, subtract, and compare fractions — common denominators, mixed numbers, and the classic traps',
  },
  {
    slug: 'fractions-g6',
    title: 'Fraction Sense · Grade 6',
    emoji: '🍕',
    color: '#2EC4B6',
    gradeRange: [6, 6],
    description: 'Multiply, divide, and operate on fractions — mixed numbers and fractions of a quantity',
  },
];

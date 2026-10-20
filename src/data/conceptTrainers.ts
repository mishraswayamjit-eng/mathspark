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
];

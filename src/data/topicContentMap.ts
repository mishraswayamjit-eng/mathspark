/**
 * Which learning content belongs to which Grade 5 topic-tree node.
 *
 * Built by reading the content itself (src/data/lessonTopics.ts,
 * src/data/handsOn/fractions.json, data/skill-drills.json, data/math-stories.json,
 * data/strategy-bank.json, data/concept_flashcards_all_grades.json) against the
 * Grade 5 nodes in src/data/topicTree.ts. A field is present only where the
 * content really is about that node; nothing is guessed, so gaps are real gaps.
 *
 * Grade 5 only for now. Other grades have no entry and so get no content actions.
 *
 * Server-side use only (it reads the hands-on lesson list through
 * src/lib/handsOn/partition.ts). Do not import it into a client component.
 */

import { HANDS_ON_LESSONS } from '@/lib/handsOn/partition';

export interface TopicContent {
  /** Concept lesson slug (src/data/lessonTopics.ts) → /learn/lessons/[slug]. */
  lessonSlug?: string;
  /** Hands-on lesson ids, in teaching order → /learn/hands-on/[id]. */
  handsOnLessonIds?: string[];
  /** Skill-drill topic (data/skill-drills.json). */
  drillTopicId?: string;
  /**
   * The lowest drill level whose gradeRange covers Grade 5. Only 'L1' is open to
   * every child: higher levels unlock on the device once the level before is
   * passed, and that state lives in localStorage where the server cannot see it.
   */
  drillLevelId?: string;
  /** `topicId` values in data/math-stories.json with a story tagged for Grade 5. */
  storyTopicIds?: string[];
  /** Strategy ids (data/strategy-bank.json) that are a trick for this topic and cover Grade 5. */
  strategyIds?: string[];
  /** Grade 5 flashcard deck (`topicId` in data/concept_flashcards_all_grades.json). */
  flashcardTopicId?: string;
}

const GRADE5_HANDS_ON_FRACTIONS: string[] = HANDS_ON_LESSONS
  .filter((l) => l.grades.indexOf(5) !== -1)
  .map((l) => l.id);

export const TOPIC_CONTENT_MAP: Record<string, TopicContent> = {
  gr5_placevalue: {
    lessonSlug: 'place-value',
    drillTopicId: 'place_value_number_system',
    drillLevelId: 'L2',
  },
  gr5_operations1: {
    drillTopicId: 'arithmetic_operations',
    drillLevelId: 'L2',
    strategyIds: ['STR_017'],
  },
  gr5_operations2: {
    drillTopicId: 'arithmetic_operations',
    drillLevelId: 'L2',
    strategyIds: ['STR_014', 'STR_016', 'STR_023', 'STR_030'],
  },
  gr5_divisibility: {
    lessonSlug: 'factors-primes',
    drillTopicId: 'factors_multiples',
    drillLevelId: 'L2',
    strategyIds: ['STR_024', 'STR_025'],
  },
  gr5_integers: {
    lessonSlug: 'integers',
    storyTopicIds: ['integers'],
  },
  gr5_bodmas: {
    lessonSlug: 'bodmas',
    drillTopicId: 'arithmetic_operations',
    drillLevelId: 'L2',
  },
  gr5_squares: {
    lessonSlug: 'squares-roots',
    drillTopicId: 'squares_roots_indices',
    drillLevelId: 'L1',
    storyTopicIds: ['squares'],
    strategyIds: ['STR_015'],
  },
  gr5_hcflcm: {
    lessonSlug: 'hcf-lcm',
    drillTopicId: 'factors_multiples',
    drillLevelId: 'L2',
    flashcardTopicId: 'lcmhcf',
  },
  gr5_algebra: {
    drillTopicId: 'algebra_equations',
    drillLevelId: 'L2',
    flashcardTopicId: 'alg',
  },
  gr5_equations: {
    lessonSlug: 'equations',
    drillTopicId: 'algebra_equations',
    drillLevelId: 'L2',
    strategyIds: ['STR_007'],
  },
  gr5_fractions: {
    lessonSlug: 'fractions',
    handsOnLessonIds: GRADE5_HANDS_ON_FRACTIONS,
    drillTopicId: 'fractions_decimals',
    drillLevelId: 'L2',
    storyTopicIds: ['fractions'],
    strategyIds: ['STR_026'],
  },
  gr5_decimals: {
    lessonSlug: 'decimals',
    drillTopicId: 'fractions_decimals',
    drillLevelId: 'L2',
    flashcardTopicId: 'dec',
  },
  gr5_sequences: {
    lessonSlug: 'sequences',
    drillTopicId: 'patterns_sequences',
    drillLevelId: 'L2',
    storyTopicIds: ['patterns'],
  },
  gr5_variation: {
    lessonSlug: 'ratios',
    drillTopicId: 'ratio_proportion',
    drillLevelId: 'L1',
    storyTopicIds: ['ratio'],
  },
  gr5_percentage: {
    lessonSlug: 'percentage',
    drillTopicId: 'percentage_profit_loss',
    drillLevelId: 'L1',
    storyTopicIds: ['percentage'],
    strategyIds: ['STR_009', 'STR_031'],
    flashcardTopicId: 'pct',
  },
  gr5_profitloss: {
    lessonSlug: 'profit-loss',
    drillTopicId: 'percentage_profit_loss',
    drillLevelId: 'L1',
    flashcardTopicId: 'pl',
  },
  gr5_interest: {
    lessonSlug: 'simple-interest',
    flashcardTopicId: 'si',
  },
  gr5_speed: {
    lessonSlug: 'time-calendar',
    drillTopicId: 'speed_time_distance',
    drillLevelId: 'L1',
    storyTopicIds: ['speed_distance'],
    flashcardTopicId: 'speed',
  },
  gr5_angles: {
    lessonSlug: 'geometry',
    drillTopicId: 'geometry_angles',
    drillLevelId: 'L1',
  },
  gr5_triangles: {
    lessonSlug: 'geometry',
    drillTopicId: 'geometry_angles',
    drillLevelId: 'L1',
  },
  gr5_area: {
    lessonSlug: 'area-perimeter',
    drillTopicId: 'area_perimeter_mensuration',
    drillLevelId: 'L1',
    storyTopicIds: ['mensuration'],
  },
};

const NO_CONTENT: TopicContent = {};

/** The content mapped to a tree node. An empty object when nothing is mapped. */
export function getTopicContent(nodeId: string): TopicContent {
  return Object.prototype.hasOwnProperty.call(TOPIC_CONTENT_MAP, nodeId)
    ? TOPIC_CONTENT_MAP[nodeId]
    : NO_CONTENT;
}

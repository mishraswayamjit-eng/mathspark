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
 * The topic page (src/app/(app)/topic/[nodeId]) reads every field; the
 * next-action rules read all but conceptTrainerSlug and exampleTopic.
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
   * The lowest drill level that has sessions and whose gradeRange covers Grade 5.
   * That level is always open to a Grade 5 child: levels below their grade are
   * not shown to them, and the lowest level shown needs nothing finished first
   * (src/lib/drillUnlock.ts). Higher levels unlock on the device, in
   * localStorage where the server cannot see it, so they are never linked to.
   */
  drillLevelId?: string;
  /** `topicId` values in data/math-stories.json with a story tagged for Grade 5. */
  storyTopicIds?: string[];
  /**
   * Strategy ids (data/strategy-bank.json) that are a trick for this topic and
   * cover Grade 5, simplest first: the first one the child has not opened is the
   * one suggested.
   */
  strategyIds?: string[];
  /** Grade 5 flashcard deck (`topicId` in data/concept_flashcards_all_grades.json). */
  flashcardTopicId?: string;
  /** Concept trainer slug (src/data/conceptTrainers.ts) → /learn/concept-trainer/[slug]. */
  conceptTrainerSlug?: string;
  /**
   * `topic` in data/worked-examples.json that has Grade 5 examples about this
   * node. Shown on the topic page only; the next-action rules do not read it.
   */
  exampleTopic?: string;
}

const GRADE5_HANDS_ON_FRACTIONS: string[] = HANDS_ON_LESSONS
  .filter((l) => l.grades.indexOf(5) !== -1)
  .map((l) => l.id);

export const TOPIC_CONTENT_MAP: Record<string, TopicContent> = {
  gr5_placevalue: {
    lessonSlug: 'place-value',
    drillTopicId: 'place_value_number_system',
    drillLevelId: 'L2',
    exampleTopic: 'place_value',
  },
  gr5_operations1: {
    lessonSlug: 'addition-subtraction',
    drillTopicId: 'arithmetic_operations',
    drillLevelId: 'L2',
    strategyIds: ['STR_017'],
  },
  gr5_operations2: {
    lessonSlug: 'multiplication-division',
    drillTopicId: 'arithmetic_operations',
    drillLevelId: 'L2',
    strategyIds: ['STR_016', 'STR_014', 'STR_030', 'STR_023'],
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
    exampleTopic: 'bodmas',
  },
  gr5_squares: {
    lessonSlug: 'squares-roots',
    drillTopicId: 'squares_roots_indices',
    drillLevelId: 'L1',
    storyTopicIds: ['squares'],
    strategyIds: ['STR_015'],
    exampleTopic: 'squares',
  },
  gr5_hcflcm: {
    lessonSlug: 'hcf-lcm',
    drillTopicId: 'factors_multiples',
    drillLevelId: 'L2',
    flashcardTopicId: 'lcmhcf',
    exampleTopic: 'hcf_lcm',
  },
  gr5_algebra: {
    lessonSlug: 'algebraic-expressions',
    drillTopicId: 'algebra_equations',
    drillLevelId: 'L2',
    flashcardTopicId: 'alg',
    exampleTopic: 'algebra',
  },
  gr5_equations: {
    lessonSlug: 'equations',
    drillTopicId: 'algebra_equations',
    drillLevelId: 'L2',
  },
  gr5_fractions: {
    lessonSlug: 'fractions',
    handsOnLessonIds: GRADE5_HANDS_ON_FRACTIONS,
    drillTopicId: 'fractions_decimals',
    drillLevelId: 'L2',
    storyTopicIds: ['fractions'],
    strategyIds: ['STR_026'],
    conceptTrainerSlug: 'fractions-g5',
    exampleTopic: 'fractions',
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
    exampleTopic: 'patterns',
  },
  gr5_variation: {
    lessonSlug: 'ratios',
    drillTopicId: 'ratio_proportion',
    drillLevelId: 'L1',
    storyTopicIds: ['ratio'],
    exampleTopic: 'ratio',
  },
  gr5_percentage: {
    lessonSlug: 'percentage',
    drillTopicId: 'percentage_profit_loss',
    drillLevelId: 'L1',
    storyTopicIds: ['percentage'],
    strategyIds: ['STR_009', 'STR_031'],
    flashcardTopicId: 'pct',
    conceptTrainerSlug: 'percent',
  },
  gr5_profitloss: {
    lessonSlug: 'profit-loss',
    drillTopicId: 'percentage_profit_loss',
    drillLevelId: 'L1',
    strategyIds: ['STR_031'],
    flashcardTopicId: 'pl',
  },
  gr5_interest: {
    lessonSlug: 'simple-interest',
    flashcardTopicId: 'si',
  },
  gr5_speed: {
    lessonSlug: 'speed-distance-time',
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
    strategyIds: ['STR_029'],
  },
};

const NO_CONTENT: TopicContent = {};

/** The content mapped to a tree node. An empty object when nothing is mapped. */
export function getTopicContent(nodeId: string): TopicContent {
  return Object.prototype.hasOwnProperty.call(TOPIC_CONTENT_MAP, nodeId)
    ? TOPIC_CONTENT_MAP[nodeId]
    : NO_CONTENT;
}

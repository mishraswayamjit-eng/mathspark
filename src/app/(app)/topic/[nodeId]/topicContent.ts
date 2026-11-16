/**
 * Everything a topic page can link to, for one topic-tree node.
 *
 * Server only: it reads the content files themselves (strategy bank, stories,
 * flashcards, hands-on lessons) so every row carries the content's real name.
 * Nothing is fetched and no model is called; this only points at content that
 * already exists. A section with nothing mapped is simply left out.
 *
 * Where the mapping comes from:
 *   - a node listed in src/data/topicContentMap.ts (Grade 5 today) uses that
 *     map and nothing else;
 *   - any other node gets what src/data/conceptTopicMap.ts already links to
 *     exactly this node (flashcards and solved examples).
 */

import type { TopicNode } from '@/data/topicTree';
import { TOPIC_CONTENT_MAP } from '@/data/topicContentMap';
import type { TopicContent } from '@/data/topicContentMap';
import { CONCEPT_TOPIC_MAP } from '@/data/conceptTopicMap';
import { LESSON_TOPICS } from '@/data/lessonTopics';
import { CONCEPT_TRAINERS } from '@/data/conceptTrainers';
import { getFlashcardsByTopic } from '@/data/flashcardData';
import { getLesson } from '@/lib/handsOn/partition';
import { gradeInRange } from '@/lib/sharedUtils';
import { isExtraTopic } from '@/components/topics/TopicList';
import strategyBank from '../../../../../data/strategy-bank.json';
import storyBank from '../../../../../data/math-stories.json';

export interface TopicLink {
  href: string;
  emoji: string;
  title: string;
  sub: string;
}

export interface TopicSection {
  /** Stable key, also used in tests: learn | drill | tricks | stories | flashcards | examples. */
  key: string;
  title: string;
  links: TopicLink[];
}

interface StrategyMeta {
  id: string;
  name: string;
  emoji?: string;
  description?: string;
}

interface StoryMeta {
  id: string;
  title: string;
  topicId: string;
  gradeRange?: number[];
}

const STRATEGIES: StrategyMeta[] = (strategyBank as unknown as { strategies: StrategyMeta[] }).strategies || [];
const STORIES: StoryMeta[] = (storyBank as unknown as { stories: StoryMeta[] }).stories || [];

/** How a worked-example topic is written for a child. */
const EXAMPLE_LABEL: Record<string, string> = {
  hcf_lcm: 'HCF & LCM',
  bodmas: 'BODMAS',
  place_value: 'Place value',
  time_calendar: 'Time & calendar',
  speed_distance: 'Speed & distance',
};

function exampleLabel(topic: string): string {
  if (Object.prototype.hasOwnProperty.call(EXAMPLE_LABEL, topic)) return EXAMPLE_LABEL[topic];
  const words = topic.replace(/_/g, ' ');
  return words.charAt(0).toUpperCase() + words.slice(1);
}

function pushUnique(list: string[], value: string): void {
  if (list.indexOf(value) === -1) list.push(value);
}

/**
 * The content for a node: its entry in the topic content map, or, when it has
 * none, the flashcard decks and example topics the concept map links to it.
 */
function contentFor(node: TopicNode): { content: TopicContent; flashcardDecks: string[]; exampleTopics: string[] } {
  if (Object.prototype.hasOwnProperty.call(TOPIC_CONTENT_MAP, node.id)) {
    const content = TOPIC_CONTENT_MAP[node.id];
    return {
      content,
      flashcardDecks: content.flashcardTopicId ? [content.flashcardTopicId] : [],
      exampleTopics: content.exampleTopic ? [content.exampleTopic] : [],
    };
  }

  const flashcardDecks: string[] = [];
  const exampleTopics: string[] = [];
  const wantedKey = node.subTopicKey || '';
  const conceptIds = Object.keys(CONCEPT_TOPIC_MAP);
  for (let i = 0; i < conceptIds.length; i++) {
    const mapping = CONCEPT_TOPIC_MAP[conceptIds[i]];
    let linked = false;
    for (let k = 0; k < mapping.practiceLinks.length; k++) {
      const link = mapping.practiceLinks[k];
      if (link.grade === node.grade && link.topicId === node.dbTopicId && (link.subTopicKey || '') === wantedKey) {
        linked = true;
        break;
      }
    }
    if (!linked) continue;
    if (mapping.exampleTopic) pushUnique(exampleTopics, mapping.exampleTopic);
    for (let k = 0; k < mapping.flashcardLinks.length; k++) {
      if (mapping.flashcardLinks[k].grade === node.grade) pushUnique(flashcardDecks, mapping.flashcardLinks[k].topicId);
    }
  }
  return { content: {}, flashcardDecks: flashcardDecks.slice(0, 3), exampleTopics: exampleTopics.slice(0, 3) };
}

/** What the practice for this topic is, in one line. */
export function practiceSummary(node: TopicNode): string {
  if (!node.subTopicKey) return 'Questions that start where you are and grow with you';
  // An extra-practice topic is not a chapter of the real paper, so it has no exam step.
  return isExtraTopic(node)
    ? 'Warm-up → Build → Challenge'
    : 'Warm-up → Build → Challenge → Real exam questions';
}

/** The sections of a topic page after Practise, in display order. Empty ones are left out. */
export function buildTopicSections(node: TopicNode): TopicSection[] {
  const { content, flashcardDecks, exampleTopics } = contentFor(node);
  const sections: TopicSection[] = [];

  // ── Learn it: concept lesson, hands-on lessons, concept trainer ──
  const learn: TopicLink[] = [];
  if (content.lessonSlug) {
    for (let i = 0; i < LESSON_TOPICS.length; i++) {
      if (LESSON_TOPICS[i].id !== content.lessonSlug) continue;
      learn.push({
        href: `/learn/lessons/${LESSON_TOPICS[i].id}`,
        emoji: '📖',
        title: `Lesson: ${LESSON_TOPICS[i].topic}`,
        sub: LESSON_TOPICS[i].description,
      });
      break;
    }
  }
  const handsOnIds = content.handsOnLessonIds || [];
  for (let i = 0; i < handsOnIds.length; i++) {
    const lesson = getLesson(handsOnIds[i]);
    if (!lesson) continue;
    learn.push({
      href: `/learn/hands-on/${lesson.id}`,
      emoji: '🖐️',
      title: `Hands-on: ${lesson.title}`,
      sub: lesson.blurb,
    });
  }
  if (content.conceptTrainerSlug) {
    for (let i = 0; i < CONCEPT_TRAINERS.length; i++) {
      if (CONCEPT_TRAINERS[i].slug !== content.conceptTrainerSlug) continue;
      learn.push({
        href: `/learn/concept-trainer/${CONCEPT_TRAINERS[i].slug}`,
        emoji: '🎯',
        title: `Concept trainer: ${CONCEPT_TRAINERS[i].title}`,
        sub: 'Think it through in three steps',
      });
      break;
    }
  }
  if (learn.length > 0) sections.push({ key: 'learn', title: 'Learn it', links: learn });

  // ── Drill ──
  if (content.drillTopicId && content.drillLevelId) {
    const level = content.drillLevelId.replace(/^L/, '');
    sections.push({
      key: 'drill',
      title: 'Drill',
      links: [{
        href: `/practice/skill-drill/${content.drillTopicId}/${content.drillLevelId}`,
        emoji: '⚡',
        title: `Skill drill · Level ${level}`,
        sub: 'Short, quick questions on one skill at a time',
      }],
    });
  }

  // ── Tricks ──
  const tricks: TopicLink[] = [];
  const strategyIds = content.strategyIds || [];
  for (let i = 0; i < strategyIds.length; i++) {
    for (let k = 0; k < STRATEGIES.length; k++) {
      if (STRATEGIES[k].id !== strategyIds[i]) continue;
      tricks.push({
        href: `/learn/strategies?open=${encodeURIComponent(STRATEGIES[k].id)}`,
        emoji: '🧠',
        title: STRATEGIES[k].name,
        sub: STRATEGIES[k].description || 'A neat trick that makes this topic feel easier',
      });
      break;
    }
  }
  if (tricks.length > 0) sections.push({ key: 'tricks', title: 'Tricks', links: tricks });

  // ── Stories (the stories page has no link to one story, so this is one row) ──
  const storyTopicIds = content.storyTopicIds || [];
  const storyTitles: string[] = [];
  for (let i = 0; i < STORIES.length; i++) {
    if (storyTopicIds.indexOf(STORIES[i].topicId) === -1) continue;
    if (!gradeInRange(STORIES[i].gradeRange, node.grade)) continue;
    storyTitles.push(STORIES[i].title);
  }
  if (storyTitles.length > 0) {
    const shown = storyTitles.slice(0, 3).join(', ');
    const more = storyTitles.length > 3 ? ` and ${storyTitles.length - 3} more` : '';
    sections.push({
      key: 'stories',
      title: 'Stories',
      links: [{
        href: '/learn/stories',
        emoji: '📚',
        title: storyTitles.length === 1 ? 'A maths story' : `${storyTitles.length} maths stories`,
        sub: `Look for: ${shown}${more}`,
      }],
    });
  }

  // ── Flashcards ──
  const cards: TopicLink[] = [];
  for (let i = 0; i < flashcardDecks.length; i++) {
    const deck = getFlashcardsByTopic(node.grade, flashcardDecks[i]);
    if (deck.length === 0) continue;
    cards.push({
      href: `/flashcards/session?deck=${encodeURIComponent(flashcardDecks[i])}&mode=classic&grade=${node.grade}`,
      emoji: '🃏',
      title: `Flashcards: ${deck[0].topicName}`,
      sub: 'Quick cards to flip and remember',
    });
  }
  if (cards.length > 0) sections.push({ key: 'flashcards', title: 'Flashcards', links: cards });

  // ── Solved examples ──
  const examples: TopicLink[] = [];
  for (let i = 0; i < exampleTopics.length; i++) {
    examples.push({
      href: `/learn/examples?topic=${encodeURIComponent(exampleTopics[i])}&grade=${node.grade}`,
      emoji: '💡',
      title: `Solved examples: ${exampleLabel(exampleTopics[i])}`,
      sub: 'Watch Sparky solve a question, one step at a time',
    });
  }
  if (examples.length > 0) sections.push({ key: 'examples', title: 'Solved examples', links: examples });

  return sections;
}

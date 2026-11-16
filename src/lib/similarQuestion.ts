import { prisma, USABLE_QUESTION_FILTER, aiSourceFilter } from './db';
import { TOPIC_TREE } from '@/data/topicTree';
import { matchesSubTopicKey } from './sharedUtils';

type Difficulty = 'Easy' | 'Medium' | 'Hard';
const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

export interface FindSimilarParams {
  questionId: string;
  subTopic:   string;
  topicId:    string;
  difficulty: string;
  wasCorrect: boolean;
}

type QuestionRow = Awaited<ReturnType<typeof prisma.question.findMany>>[number];

function none(): Promise<QuestionRow[]> {
  return Promise.resolve([]);
}

function pickRandom<T>(arr: T[]): T | null {
  if (arr.length === 0) return null;
  return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * The topic-tree keys this question's sub-topic falls under, for grades whose
 * questions all share one database topic ("grade5"). Empty for a chapter topic
 * such as "ch11", which is already one topic.
 */
function topicKeysFor(topicId: string, subTopic: string): string[] {
  const keys: string[] = [];
  for (let i = 0; i < TOPIC_TREE.length; i++) {
    const node = TOPIC_TREE[i];
    if (node.dbTopicId !== topicId || !node.subTopicKey) continue;
    if (matchesSubTopicKey(subTopic, node.subTopicKey) && keys.indexOf(node.subTopicKey) === -1) {
      keys.push(node.subTopicKey);
    }
  }
  return keys;
}

/**
 * Find a "try one like it" question: the same concept as the one just answered.
 *
 * Priority order:
 *  1. The same sub-topic label, at a suitable difficulty.
 *  2. The same topic of the child's grade (e.g. every "HCF and LCM" question of
 *     Grade 5), at a suitable difficulty, then at any difficulty.
 *  3. For a chapter topic only (Grade 4's "ch11" and so on): the same chapter.
 *  4. null: nothing of the same concept is left. A question from a different
 *     topic is never returned, because the screen promises the same concept.
 *
 * Sources that are switched off (see aiSourceFilter) are never served.
 *
 * Difficulty:
 *  - the child missed it  → the same level or one easier (reinforce)
 *  - the child got it     → the same level or one harder (stretch)
 */
export async function findSimilarQuestion(
  params: FindSimilarParams,
  excludeIds: string[],
) {
  const { questionId, subTopic, topicId, difficulty, wasCorrect } = params;

  // Always leave out the question just answered.
  const excluded = Array.from(new Set<string>([questionId, ...excludeIds]));

  const found = DIFFICULTIES.indexOf(difficulty as Difficulty);
  const origIdx = found === -1 ? 1 : found;
  const lo = wasCorrect ? origIdx : Math.max(origIdx - 1, 0);
  const hi = wasCorrect ? Math.min(origIdx + 1, 2) : origIdx;
  const allowedDiff: string[] = DIFFICULTIES.slice(lo, hi + 1);

  const base = {
    id: { notIn: excluded },
    ...aiSourceFilter(),
    ...USABLE_QUESTION_FILTER,
  };
  const keys = topicKeysFor(topicId, subTopic);

  // A generated variant names its family in its id (VAR_G5_vary_hcf_lcm_V07),
  // and some carry only the label "Auto-generated variant", which says nothing
  // about the topic. Its siblings in the same family are the same concept.
  const family = /^(VAR_G\d+_vary_.+_V)\d+/.exec(questionId);
  if (family) {
    const siblings = await prisma.question.findMany({
      where: { ...base, id: { notIn: excluded, startsWith: family[1] } },
      take: 60,
    });
    const atLevel = siblings.filter((q) => allowedDiff.indexOf(q.difficulty) !== -1);
    if (atLevel.length > 0) return pickRandom(atLevel);
    if (siblings.length > 0) return pickRandom(siblings);
    // A label that names no topic must not be used to find "the same concept".
    if (keys.length === 0 && /^grade\d+$/.test(topicId)) return null;
  }

  const [sameLabel, sameTopic, sameChapter] = await Promise.all([
    // 1. The same sub-topic label.
    prisma.question.findMany({
      where: { ...base, ...(topicId ? { topicId } : {}), subTopic, difficulty: { in: allowedDiff } },
      take: 40,
    }),
    // 2. The same topic of the grade. `contains` narrows the read; the word-start
    //    rule the rest of the app uses is applied below.
    keys.length > 0
      ? prisma.question.findMany({
          where: {
            ...base,
            topicId,
            OR: keys.map((key) => ({ subTopic: { contains: key, mode: 'insensitive' as const } })),
          },
          take: 300,
        })
      : none(),
    // 3. A chapter topic is one topic already.
    keys.length === 0 && topicId && !/^grade\d+$/.test(topicId)
      ? prisma.question.findMany({
          where: { ...base, topicId, difficulty: { in: allowedDiff } },
          take: 20,
        })
      : none(),
  ]);

  if (sameLabel.length > 0) return pickRandom(sameLabel);

  const inTopic = sameTopic.filter((q) => keys.some((key) => matchesSubTopicKey(q.subTopic, key)));
  const inTopicAtLevel = inTopic.filter((q) => allowedDiff.indexOf(q.difficulty) !== -1);
  if (inTopicAtLevel.length > 0) return pickRandom(inTopicAtLevel);
  if (inTopic.length > 0) return pickRandom(inTopic);

  if (sameChapter.length > 0) return pickRandom(sameChapter);
  return null;
}

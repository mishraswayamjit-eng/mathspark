// Pure presentation helpers for the Home screen: no database, no browser APIs.
// They only reorder and label numbers the Brain Engine already verified.

import { TOPIC_TREE } from '@/data/topicTree';
import type { TopicNode } from '@/data/topicTree';
import type { TopicMasteryEntry, TopicPriority } from '@/lib/brain/engine';
import type { HomeData } from '@/lib/student/homeData';

/** A link is only used when it is a path inside this app. */
export function isAppPath(url: unknown): url is string {
  return typeof url === 'string' && url.charAt(0) === '/' && url.charAt(1) !== '/';
}

/**
 * Practice link for a topic-tree node. Keyed grades (e.g. Grade 5) share one DB
 * topic across all their topics, so the sub-topic must travel in the query
 * string or the child lands in whole-grade practice. Same form as the Chapters
 * page uses.
 */
export function practiceUrlForTopic(treeTopicId: string, dbTopicId: string): string {
  let node: TopicNode | null = null;
  for (let i = 0; i < TOPIC_TREE.length; i++) {
    if (TOPIC_TREE[i].id === treeTopicId) { node = TOPIC_TREE[i]; break; }
  }
  const db = node ? node.dbTopicId : dbTopicId;
  const key = node && node.subTopicKey ? node.subTopicKey : '';
  return `/practice/${db}${key ? `?subTopic=${encodeURIComponent(key)}` : ''}`;
}

/** Softer wording for the engine's plan reasons. */
export function reframePlanReason(reason: string): string {
  if (reason.includes('Very low accuracy'))             return 'Great topic to build on!';
  if (reason.includes('Not practiced in'))              return "Time to refresh — it's been a while!";
  if (reason.includes('% of question types explored'))  return 'New question types to discover!';
  if (reason.includes('High exam frequency'))           return 'Appears often in exams — high impact!';
  if (reason.includes('You marked this as a focus'))    return 'Your focus area — keep going!';
  if (reason.includes('No mock test in'))               return 'Time for a fresh mock test';
  if (reason.includes('Very few question types'))       return 'New question types to discover!';
  return reason;
}

/**
 * Feature 5c: apply the LLM surfacing order over the verified Brain Engine
 * priorities. Topics and numbers are unchanged, only the order. Anything the
 * surfacing plan left out is appended, so nothing verified is lost.
 */
export function orderPriorities(data: HomeData): TopicPriority[] {
  const priorities = Array.isArray(data.topicPriorities) ? data.topicPriorities : [];
  const order = data.surfacePlan && Array.isArray(data.surfacePlan.orderedTopicIds)
    ? data.surfacePlan.orderedTopicIds
    : [];
  if (order.length === 0) return priorities;

  const ordered: TopicPriority[] = [];
  const taken: Record<string, boolean> = {};
  order.forEach((id) => {
    priorities.forEach((p) => {
      // The plan may name a topic by its tree id or by its DB topic id.
      if ((p.topicId === id || p.dbTopicId === id) && !taken[p.topicId]) {
        taken[p.topicId] = true;
        ordered.push(p);
      }
    });
  });
  priorities.forEach((p) => {
    if (!taken[p.topicId]) {
      taken[p.topicId] = true;
      ordered.push(p);
    }
  });
  return ordered;
}

export interface ContinueTopic {
  topicName: string;
  emoji: string;
  reason: string;
  url: string;
}

/** The topic the hero card offers to continue, or null when there is none yet. */
export function pickContinueTopic(data: HomeData): ContinueTopic | null {
  const top = orderPriorities(data)[0];
  if (!top || !top.dbTopicId) return null;
  // Prefer a URL the engine provides; otherwise build the sub-topic link here.
  const fromEngine = (top as TopicPriority & { targetUrl?: unknown }).targetUrl;
  return {
    topicName: top.topicName,
    emoji: top.emoji,
    reason: reframePlanReason(top.reason || ''),
    url: isAppPath(fromEngine) ? fromEngine : practiceUrlForTopic(top.topicId, top.dbTopicId),
  };
}

/** Up to three topics for "Your Topics": most recently practised first, then strongest. */
export function pickDisplayTopics(data: HomeData): TopicMasteryEntry[] {
  const mastery = Array.isArray(data.topicMastery) ? data.topicMastery : [];
  const picked: TopicMasteryEntry[] = [];
  const has = (topicId: string) => picked.some((e) => e.topicId === topicId);

  data.recentTopicIds.forEach((id) => {
    if (picked.length >= 3 || has(id)) return;
    for (let i = 0; i < mastery.length; i++) {
      if (mastery[i].topicId === id) { picked.push(mastery[i]); break; }
    }
  });

  if (picked.length < 3) {
    const strongest = mastery
      .filter((t) => t.attemptsCount > 0)
      .sort((a, b) => b.mastery - a.mastery);
    strongest.forEach((entry) => {
      if (picked.length < 3 && !has(entry.topicId)) picked.push(entry);
    });
  }
  return picked;
}

/** True when a "2h ago" style label is within the last 12 hours. */
export function isRecentWin(timeAgo: string): boolean {
  if (timeAgo === 'just now') return true;
  if (timeAgo.endsWith('h ago')) {
    const hours = parseInt(timeAgo, 10);
    return !isNaN(hours) && hours <= 12;
  }
  return false;
}

/**
 * Greeting by India time. The page is rendered on the server (whose clock is
 * not the child's), and the app is for students in India, so the hour is taken
 * in IST (UTC+5:30) rather than from the server's own time zone.
 */
export function greetingForIndia(now: Date): string {
  const istHour = new Date(now.getTime() + 5.5 * 60 * 60 * 1000).getUTCHours();
  return istHour < 12 ? 'Good morning' : istHour < 17 ? 'Good afternoon' : 'Good evening';
}

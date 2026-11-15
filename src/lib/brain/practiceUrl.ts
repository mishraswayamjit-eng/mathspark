// One place that builds a practice link.
//
// Keyed grades (grade2/3/5/6/7/8/9) share ONE database topic ("grade5") across
// all their sub-topics; a sub-topic is picked with `?subTopic=<key>`, which
// `/api/questions/next` hands to the adaptive engine (`matchesSubTopicKey`).
// A link without the key opens whole-grade mixed practice, so every link that
// means "practise THIS topic" must be built here.
//
// Pure (no database), so both server code and client components may import it.

import { TOPIC_TREE } from '@/data/topicTree';

/** The practice link for a database topic and, optionally, one sub-topic in it. */
export function buildPracticeUrl(dbTopicId: string, subTopicKey?: string | null): string {
  const base = `/practice/${encodeURIComponent(dbTopicId)}`;
  return subTopicKey ? `${base}?subTopic=${encodeURIComponent(subTopicKey)}` : base;
}

/** The practice link that serves exactly one topic-tree node's questions. */
export function practiceUrlForNode(node: { dbTopicId: string; subTopicKey?: string }): string {
  return buildPracticeUrl(node.dbTopicId, node.subTopicKey);
}

/** The same, from a node id such as `gr5_fractions`. Null when the id is not in the tree. */
export function practiceUrlForNodeId(nodeId: string | null | undefined): string | null {
  if (!nodeId) return null;
  for (let i = 0; i < TOPIC_TREE.length; i++) {
    if (TOPIC_TREE[i].id === nodeId) return practiceUrlForNode(TOPIC_TREE[i]);
  }
  return null;
}

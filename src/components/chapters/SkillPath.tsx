'use client';

import React from 'react';
import type { TopicWithProgress } from '@/types';
import { getTopicColor } from '@/data/topicColors';
import { TOPIC_TREE } from '@/data/topicTree';

// ── Topic list ───────────────────────────────────────────────────────────────
// Every topic is open: a child can start anywhere. The list only suggests where
// to go next (the first topic that is not yet mastered is marked "Start here").

type NodeState = 'completed' | 'current' | 'available';

interface SkillNode {
  topic: TopicWithProgress;
  state: NodeState;
  emoji: string;
  color: string;
  /** True for the one topic we suggest doing next. */
  suggested: boolean;
  /**
   * Sub-topics of a whole-grade pool share one progress record, so their
   * numbers describe the grade, not this topic. Hide per-topic stats for them.
   */
  sharesProgress: boolean;
}

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06':    '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11':    '📊', 'ch12':    '📏', 'ch13':    '🔤', 'ch14':    '⚖️',
  'ch15':    '🧩', 'ch16':    '🔗', 'ch17':    '🕐', 'ch18':    '📐',
  'ch19':    '🔺', 'ch20':    '⬜', 'ch21':    '⭕', 'dh':      '📈',
};

function emojiFor(topic: TopicWithProgress): string {
  const byId = TOPIC_EMOJI[topic.id];
  if (byId) return byId;
  for (let i = 0; i < TOPIC_TREE.length; i++) {
    if (TOPIC_TREE[i].name === topic.name) return TOPIC_TREE[i].emoji;
  }
  return '📚';
}

function deriveNodes(topics: TopicWithProgress[]): SkillNode[] {
  let suggestedGiven = false;
  return topics.map((topic) => {
    const state: NodeState =
      topic.mastery === 'Mastered' ? 'completed' :
      topic.mastery === 'Practicing' ? 'current' : 'available';
    const suggested = !suggestedGiven && state !== 'completed';
    if (suggested) suggestedGiven = true;
    return {
      topic,
      state,
      emoji: emojiFor(topic),
      color: getTopicColor(topic.name),
      suggested,
      sharesProgress: topic.id.indexOf('__') !== -1,
    };
  });
}

function statusLine(node: SkillNode): string {
  if (node.sharesProgress) return node.suggested ? 'A good place to start' : 'Tap to practise';
  const { attempted, correct } = node.topic;
  const pct = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;
  if (node.state === 'completed') return `Mastered · ${pct}% right`;
  if (node.state === 'current') return `${correct} solved · ${pct}% right`;
  return node.suggested ? 'A good place to start' : 'Not started yet';
}

// ── Main component ───────────────────────────────────────────────────────────

interface SkillPathProps {
  topics: TopicWithProgress[];
  onTopicClick: (topicId: string, subTopicKey?: string) => void;
}

export default function SkillPath({ topics, onTopicClick }: SkillPathProps) {
  const nodes = deriveNodes(topics);

  return (
    <div className="space-y-3">
      {nodes.map((node) => {
        const { topic } = node;
        const pct = topic.attempted > 0 ? Math.round((topic.correct / topic.attempted) * 100) : 0;
        const showMeter = !node.sharesProgress && node.state === 'current';

        return (
          <button
            key={topic.id}
            type="button"
            onClick={() => onTopicClick(topic.id)}
            className={`w-full text-left bg-white rounded-card border-2 border-l-[10px] p-3 flex items-center gap-3 min-h-[72px] transition-transform active:scale-[0.98] ${
              node.suggested ? 'border-ink shadow-hard-sm' : 'border-line hover:border-ink'
            }`}
            style={{ borderLeftColor: node.color }}
          >
            {/* Emoji tile, tinted with the topic colour */}
            <span
              className="w-11 h-11 rounded-tile flex items-center justify-center text-xl leading-none flex-shrink-0 select-none"
              style={{ backgroundColor: `${node.color}33` }}
              aria-hidden="true"
            >
              {node.emoji}
            </span>

            <span className="flex-1 min-w-0">
              <span className="block font-display text-title text-ink">{topic.name}</span>
              <span className="block text-[13px] font-bold text-ink-muted mt-0.5">{statusLine(node)}</span>
              {showMeter && (
                <span className="block ui-meter h-2.5 mt-2">
                  <span className="block h-full bg-action rounded-full" style={{ width: `${Math.max(4, pct)}%` }} />
                </span>
              )}
            </span>

            {/* Status badge */}
            {node.state === 'completed' && !node.sharesProgress && (
              <span className="ui-chip flex-shrink-0 !bg-success-soft !border-success !text-ink">
                <span aria-hidden="true">✓</span> Mastered
              </span>
            )}
            {node.suggested && (
              <span className="ui-chip flex-shrink-0 !bg-action !border-ink !text-white">Start here</span>
            )}

            <span className="text-2xl leading-none text-ink-muted flex-shrink-0" aria-hidden="true">›</span>
          </button>
        );
      })}
    </div>
  );
}

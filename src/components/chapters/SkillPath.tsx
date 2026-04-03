'use client';

import React from 'react';
import type { TopicWithProgress } from '@/types';

// ── Node state derivation ────────────────────────────────────────────────────

type NodeState = 'completed' | 'current' | 'available' | 'locked';

interface SkillNode {
  topic: TopicWithProgress;
  state: NodeState;
  emoji: string;
}

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06':    '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11':    '📊', 'ch12':    '📏', 'ch13':    '🔤', 'ch14':    '⚖️',
  'ch15':    '🧩', 'ch16':    '🔗', 'ch17':    '🕐', 'ch18':    '📐',
  'ch19':    '🔺', 'ch20':    '⬜', 'ch21':    '⭕', 'dh':      '📈',
};

function deriveNodes(topics: TopicWithProgress[]): SkillNode[] {
  let foundFirstIncomplete = false;
  return topics.map((topic) => {
    const emoji = TOPIC_EMOJI[topic.id] ?? '📚';

    if (topic.mastery === 'Mastered') {
      return { topic, state: 'completed' as const, emoji };
    }
    if (topic.mastery === 'Practicing') {
      foundFirstIncomplete = true;
      return { topic, state: 'current' as const, emoji };
    }
    // NotStarted
    if (!foundFirstIncomplete) {
      foundFirstIncomplete = true;
      return { topic, state: 'available' as const, emoji };
    }
    return { topic, state: 'locked' as const, emoji };
  });
}

// ── Sub-components ───────────────────────────────────────────────────────────

const NodeCircle = React.memo(function NodeCircle({ node }: { node: SkillNode }) {
  switch (node.state) {
    case 'completed':
      return (
        <div className="w-14 h-14 rounded-full bg-duo-green flex items-center justify-center shadow-md shadow-green-200">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M5 12l5 5L19 7" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      );
    case 'current':
      return (
        <div className="relative w-14 h-14">
          <div className="absolute inset-0 rounded-full bg-duo-green/20 animate-ping" style={{ animationDuration: '2s' }} />
          <div className="relative w-14 h-14 rounded-full bg-white border-4 border-duo-green flex items-center justify-center shadow-md">
            <span className="text-xl leading-none select-none" aria-hidden="true">{node.emoji}</span>
          </div>
        </div>
      );
    case 'available':
      return (
        <div className="w-14 h-14 rounded-full bg-white border-2 border-gray-300 flex items-center justify-center shadow-sm">
          <span className="text-xl leading-none select-none" aria-hidden="true">{node.emoji}</span>
        </div>
      );
    case 'locked':
      return (
        <div className="w-14 h-14 rounded-full bg-gray-100 border-2 border-gray-200 flex items-center justify-center opacity-60">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <rect x="5" y="11" width="14" height="10" rx="2" stroke="#9CA3AF" strokeWidth="2" />
            <path d="M8 11V7a4 4 0 018 0v4" stroke="#9CA3AF" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
      );
  }
});

function NodeLabel({ node }: { node: SkillNode }) {
  const accuracyPct = node.topic.attempted > 0
    ? Math.round((node.topic.correct / node.topic.attempted) * 100)
    : 0;

  return (
    <div className="flex-1 min-w-0">
      <p className={`text-sm font-extrabold leading-snug line-clamp-2 ${
        node.state === 'locked' ? 'text-gray-400' : 'text-gray-800'
      }`}>
        {node.topic.name}
      </p>
      <p className={`text-xs font-semibold mt-0.5 ${
        node.state === 'completed' ? 'text-duo-green-dark' :
        node.state === 'current' ? 'text-duo-orange-dark' :
        node.state === 'available' ? 'text-gray-500' :
        'text-gray-400'
      }`}>
        {node.state === 'completed' && `Mastered · ${accuracyPct}%`}
        {node.state === 'current' && `${node.topic.correct} solved · ${accuracyPct}%`}
        {node.state === 'available' && 'Ready to start'}
        {node.state === 'locked' && 'Complete previous topics'}
      </p>
    </div>
  );
}

// ── Connector line ───────────────────────────────────────────────────────────

function Connector({ fromState }: { fromState: NodeState }) {
  const color = fromState === 'completed' ? 'bg-duo-green' : 'bg-gray-200';
  return (
    <div className="flex justify-center py-0">
      <div className={`w-1 h-8 ${color} rounded-full`} />
    </div>
  );
}

// ── Main component ───────────────────────────────────────────────────────────

interface SkillPathProps {
  topics: TopicWithProgress[];
  onTopicClick: (topicId: string, subTopicKey?: string) => void;
}

export default function SkillPath({ topics, onTopicClick }: SkillPathProps) {
  const nodes = deriveNodes(topics);

  return (
    <div className="relative px-2">
      {nodes.map((node, idx) => {
        const isRight = idx % 2 === 1;
        const isClickable = node.state !== 'locked';

        return (
          <React.Fragment key={node.topic.id}>
            {idx > 0 && <Connector fromState={nodes[idx - 1].state} />}

            <button
              disabled={!isClickable}
              onClick={() => isClickable && onTopicClick(node.topic.id)}
              className={`w-full flex items-center gap-3 rounded-2xl px-3 py-3 transition-transform ${
                isRight ? 'flex-row-reverse pl-4 pr-3' : 'flex-row pl-3 pr-4'
              } ${
                isClickable
                  ? 'active:scale-[0.97] hover:bg-gray-50'
                  : 'cursor-default'
              }`}
              style={{ marginLeft: isRight ? 'auto' : 0 }}
            >
              <NodeCircle node={node} />
              <NodeLabel node={node} />
            </button>
          </React.Fragment>
        );
      })}
    </div>
  );
}

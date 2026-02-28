'use client';

import Link from 'next/link';
import ProgressBar from './ProgressBar';
import type { TopicWithProgress } from '@/types';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

interface ChapterGridProps {
  topics: TopicWithProgress[];
}

function masteryStyle(mastery: string) {
  if (mastery === 'Mastered')  return 'bg-green-50 border-green-300';
  if (mastery === 'Practicing') return 'bg-amber-50 border-amber-300';
  return 'bg-white border-gray-200';
}

function masteryBadge(mastery: string) {
  if (mastery === 'Mastered')  return <span className="text-xs font-semibold text-green-700 bg-green-100 px-2 py-0.5 rounded-full">⭐ Mastered</span>;
  if (mastery === 'Practicing') return <span className="text-xs font-semibold text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">📚 Practicing</span>;
  return <span className="text-xs font-semibold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">🆕 Start</span>;
}

function barColor(mastery: string) {
  if (mastery === 'Mastered')   return 'bg-green-500';
  if (mastery === 'Practicing') return 'bg-amber-400';
  return 'bg-gray-300';
}

export default function ChapterGrid({ topics }: ChapterGridProps) {
  const sorted = [...topics].sort(
    (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
  );

  return (
    <div className="grid grid-cols-2 gap-3 px-4">
      {sorted.map((topic) => {
        const pct =
          topic.attempted > 0
            ? Math.round((topic.correct / topic.attempted) * 100)
            : 0;

        return (
          <Link
            key={topic.id}
            href={`/practice/${topic.id}`}
            className={`rounded-2xl border-2 p-4 flex flex-col gap-2 hover:shadow-md transition-shadow ${masteryStyle(topic.mastery)}`}
          >
            <span className="text-xs font-bold text-gray-400 uppercase tracking-wide">
              Ch {topic.chapterNumber}
            </span>
            <p className="text-sm font-semibold text-gray-800 leading-tight">
              {topic.name}
            </p>
            {masteryBadge(topic.mastery)}
            <ProgressBar
              value={pct}
              color={barColor(topic.mastery)}
              height="h-1.5"
            />
            {topic.attempted > 0 && (
              <p className="text-xs text-gray-400">
                {topic.correct}/{topic.attempted} correct
              </p>
            )}
          </Link>
        );
      })}
    </div>
  );
}

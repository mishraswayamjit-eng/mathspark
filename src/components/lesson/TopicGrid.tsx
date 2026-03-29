'use client';

import React from 'react';
import Link from 'next/link';
import type { LessonTopicMeta } from '@/types/lesson';

interface TopicProgress {
  topicSlug: string;
  completed: number; // levels with ≥75%
  total: number;     // always 5
}

interface TopicGridProps {
  topics: LessonTopicMeta[];
  progress: TopicProgress[];
}

export default function TopicGrid({ topics, progress }: TopicGridProps) {
  const progressMap = new Map(progress.map((p) => [p.topicSlug, p]));

  return (
    <div className="grid grid-cols-2 gap-3">
      {topics.map((topic) => {
        const prog = progressMap.get(topic.id);
        const completed = prog?.completed ?? 0;
        const total = prog?.total ?? 5;

        return (
          <Link
            key={topic.id}
            href={`/learn/lessons/${topic.id}`}
            className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-[box-shadow] active:scale-[0.97] flex flex-col gap-2"
          >
            {/* Emoji + progress badge */}
            <div className="flex items-start justify-between">
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                style={{ backgroundColor: topic.color + '20' }}
              >
                <span aria-hidden="true">{topic.emoji}</span>
              </div>
              {completed > 0 && (
                <span
                  className="text-[10px] font-extrabold px-2 py-0.5 rounded-full text-white"
                  style={{ backgroundColor: topic.color }}
                >
                  {completed}/{total}
                </span>
              )}
            </div>

            {/* Topic name */}
            <p className="text-sm font-extrabold text-gray-800 leading-snug line-clamp-2">
              {topic.topic}
            </p>

            {/* Grade range */}
            <span className="text-[10px] font-bold text-gray-400">
              Grades {topic.gradeRange[0]}–{topic.gradeRange[1]}
            </span>

            {/* Description */}
            <p className="text-xs text-gray-500 leading-snug line-clamp-2">
              {topic.description}
            </p>

            {/* Progress bar */}
            <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden mt-auto">
              <div
                className="h-full rounded-full transition-[width] duration-500"
                style={{
                  width: `${(completed / total) * 100}%`,
                  backgroundColor: topic.color,
                }}
              />
            </div>
          </Link>
        );
      })}
    </div>
  );
}

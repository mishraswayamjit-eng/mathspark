'use client';

import React from 'react';
import Link from 'next/link';
import type { LessonLevel } from '@/types/lesson';

interface LevelProgress {
  levelId: number;
  quizScore: number;
}

interface LevelMapProps {
  topicSlug: string;
  levels: LessonLevel[];
  progress: LevelProgress[];
}

export default function LevelMap({ topicSlug, levels, progress }: LevelMapProps) {
  const progressMap = new Map(progress.map((p) => [p.levelId, p.quizScore]));

  return (
    <div className="relative">
      {/* Connecting line */}
      <div className="absolute left-7 top-8 bottom-8 w-0.5 bg-gray-200" />

      <div className="space-y-4">
        {levels.map((level) => {
          const score = progressMap.get(level.id);
          const hasScore = score !== undefined;
          const passed = hasScore && score >= 75;

          return (
            <Link
              key={level.id}
              href={`/learn/lessons/${topicSlug}/${level.id}`}
              className="relative flex items-start gap-4 bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-[box-shadow] active:scale-[0.98]"
            >
              {/* Level icon */}
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shrink-0 relative z-10"
                style={{ backgroundColor: level.color + '20' }}
              >
                {passed ? '⭐' : level.emoji}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <h3 className="text-sm font-extrabold text-gray-800 truncate">
                    {level.label}
                  </h3>
                  {hasScore && (
                    <span
                      className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${
                        passed
                          ? 'bg-green-100 text-green-700'
                          : 'bg-orange-100 text-orange-700'
                      }`}
                    >
                      {score}%
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-500 font-semibold mb-2">
                  {level.subtitle}
                </p>

                {/* Progress bar */}
                <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-[width] duration-500"
                    style={{
                      width: hasScore ? `${score}%` : '0%',
                      backgroundColor: passed ? '#58CC02' : hasScore ? '#FF9600' : '#E5E7EB',
                    }}
                  />
                </div>
              </div>

              {/* Chevron */}
              <span className="text-gray-300 text-lg shrink-0 mt-3" aria-hidden="true">
                &rsaquo;
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}

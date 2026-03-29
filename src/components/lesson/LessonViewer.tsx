'use client';

import React, { useState, useCallback } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import LessonStepper from './LessonStepper';
import type { Lesson } from '@/types/lesson';

interface LessonViewerProps {
  lessons: Lesson[];
  accentColor: string;
  onDone: () => void;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

export default function LessonViewer({ lessons, accentColor, onDone }: LessonViewerProps) {
  const [lessonIndex, setLessonIndex] = useState(0);
  const lesson = lessons[lessonIndex];
  const isLast = lessonIndex === lessons.length - 1;

  const nextLesson = useCallback(() => {
    if (isLast) {
      onDone();
    } else {
      setLessonIndex((i) => i + 1);
    }
  }, [isLast, onDone]);

  const prevLesson = useCallback(() => {
    setLessonIndex((i) => Math.max(0, i - 1));
  }, []);

  return (
    <div className="animate-fade-in">
      {/* Progress bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1.5">
          <p className="text-xs font-bold text-gray-500">
            Lesson {lessonIndex + 1} of {lessons.length}
          </p>
          <p className="text-xs font-bold text-gray-400">
            {Math.round(((lessonIndex + 1) / lessons.length) * 100)}%
          </p>
        </div>
        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-500"
            style={{
              width: `${((lessonIndex + 1) / lessons.length) * 100}%`,
              backgroundColor: accentColor,
            }}
          />
        </div>
      </div>

      {/* Lesson title */}
      <div key={lessonIndex} className="animate-fade-in">
        <h2 className="text-lg font-extrabold text-gray-800 mb-2">{lesson.title}</h2>
        <p className="text-sm text-gray-600 mb-4">{lesson.intro}</p>

        {/* Visual (monospace box) */}
        {lesson.visual && (
          <div className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 mb-4 font-mono text-sm text-gray-700 whitespace-pre-wrap">
            {lesson.visual}
          </div>
        )}

        {/* Explanation paragraphs */}
        {lesson.explanation && lesson.explanation.length > 0 && (
          <div className="space-y-3 mb-4">
            {lesson.explanation.map((para, i) => (
              <div
                key={i}
                className="border-l-4 pl-4 py-1"
                style={{ borderColor: accentColor + '80' }}
              >
                <p className="text-sm text-gray-700 leading-relaxed">
                  {hasLatex(para) ? (
                    <KatexRenderer latex={para} className="text-sm" />
                  ) : (
                    para
                  )}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Steps (delegate to LessonStepper) */}
        {lesson.steps && lesson.steps.length > 0 && (
          <LessonStepper
            steps={lesson.steps}
            onDone={nextLesson}
          />
        )}

        {/* Rule callout */}
        {lesson.rule && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl px-4 py-3 mb-4">
            <p className="text-xs font-extrabold text-yellow-800 mb-1">
              <span aria-hidden="true">📝 </span>Rule
            </p>
            <p className="text-sm font-semibold text-yellow-900">
              {hasLatex(lesson.rule) ? (
                <KatexRenderer latex={lesson.rule} className="text-sm" />
              ) : (
                lesson.rule
              )}
            </p>
          </div>
        )}

        {/* Tip callout */}
        {lesson.tip && (
          <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 mb-4">
            <p className="text-xs font-bold text-blue-800">
              <span aria-hidden="true">💡 </span>
              {lesson.tip}
            </p>
          </div>
        )}

        {/* Navigation (only for explanation-style lessons; steps-style uses Stepper buttons) */}
        {(!lesson.steps || lesson.steps.length === 0) && (
          <div className="flex gap-3 mt-6">
            {lessonIndex > 0 && (
              <button
                onClick={prevLesson}
                className="flex-1 py-3 rounded-2xl text-sm font-extrabold border-2 border-gray-200 text-gray-600 active:scale-95 transition-transform"
              >
                Back
              </button>
            )}
            <button
              onClick={nextLesson}
              className="flex-1 py-3 rounded-2xl text-sm font-extrabold text-white active:scale-95 transition-transform"
              style={{ backgroundColor: accentColor }}
            >
              {isLast ? 'Start Quiz!' : 'Next Lesson'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

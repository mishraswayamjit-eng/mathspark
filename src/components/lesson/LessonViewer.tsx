'use client';

import React, { useState, useCallback, useMemo, useRef } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import LessonStepper from './LessonStepper';
import SlideRenderer from './SlideRenderer';
import { toSlides } from '@/lib/lessonSlideAdapter';
import type { Lesson, Slide } from '@/types/lesson';

interface LessonViewerProps {
  lessons: Lesson[];
  accentColor: string;
  onDone: () => void;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

// ── Slide Mode ────────────────────────────────────────────────────────────────

function SlideModeViewer({
  lessons,
  accentColor,
  onDone,
}: LessonViewerProps) {
  const [lessonIndex, setLessonIndex] = useState(0);
  const [slideIndex, setSlideIndex] = useState(0);
  const touchStartX = useRef<number | null>(null);

  const lesson = lessons[lessonIndex];
  const isLastLesson = lessonIndex === lessons.length - 1;

  // Get slides: prefer authored slides, fall back to auto-generated
  const slides: Slide[] = useMemo(
    () => (lesson.slides?.length ? lesson.slides : toSlides(lesson)),
    [lesson],
  );

  const isLastSlide = slideIndex === slides.length - 1;

  const nextSlide = useCallback(() => {
    if (isLastSlide) {
      // Advance to next lesson or finish
      if (isLastLesson) {
        onDone();
      } else {
        setLessonIndex((i) => i + 1);
        setSlideIndex(0);
      }
    } else {
      setSlideIndex((i) => i + 1);
    }
  }, [isLastSlide, isLastLesson, onDone]);

  const prevSlide = useCallback(() => {
    if (slideIndex > 0) {
      setSlideIndex((i) => i - 1);
    } else if (lessonIndex > 0) {
      // Go back to previous lesson's last slide
      const prevLesson = lessons[lessonIndex - 1];
      const prevSlides = prevLesson.slides?.length
        ? prevLesson.slides
        : toSlides(prevLesson);
      setLessonIndex((i) => i - 1);
      setSlideIndex(prevSlides.length - 1);
    }
  }, [slideIndex, lessonIndex, lessons]);

  // Swipe gesture
  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  }, []);

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    if (touchStartX.current === null) return;
    const diff = touchStartX.current - e.changedTouches[0].clientX;
    touchStartX.current = null;
    if (diff > 50) nextSlide();      // swipe left → next
    else if (diff < -50) prevSlide(); // swipe right → prev
  }, [nextSlide, prevSlide]);

  // Progress calculations
  const totalSlidesAllLessons = useMemo(() => {
    return lessons.reduce((sum, l) => {
      const s = l.slides?.length ? l.slides : toSlides(l);
      return sum + s.length;
    }, 0);
  }, [lessons]);

  const completedSlides = useMemo(() => {
    let count = 0;
    for (let i = 0; i < lessonIndex; i++) {
      const l = lessons[i];
      const s = l.slides?.length ? l.slides : toSlides(l);
      count += s.length;
    }
    return count + slideIndex;
  }, [lessons, lessonIndex, slideIndex]);

  // Button label
  const buttonLabel = isLastSlide
    ? isLastLesson
      ? 'Start Quiz!'
      : 'Next Lesson'
    : 'Continue';

  return (
    <div className="animate-fade-in flex flex-col min-h-[80vh]">
      {/* ── Progress section ── */}
      <div className="mb-2">
        {/* Lesson dots */}
        <div className="flex items-center justify-center gap-1.5 mb-2">
          {lessons.map((_, i) => (
            <div
              key={i}
              className={`h-2 rounded-full transition-all duration-300 ${
                i === lessonIndex
                  ? 'w-6'
                  : 'w-2'
              }`}
              style={{
                backgroundColor:
                  i < lessonIndex
                    ? accentColor
                    : i === lessonIndex
                    ? accentColor
                    : '#E5E7EB',
                opacity: i === lessonIndex ? 1 : i < lessonIndex ? 0.6 : 0.3,
              }}
            />
          ))}
        </div>

        {/* Slide progress bar */}
        <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-500"
            style={{
              width: `${((completedSlides + 1) / totalSlidesAllLessons) * 100}%`,
              backgroundColor: accentColor,
            }}
          />
        </div>
      </div>

      {/* ── Slide content ── */}
      <div
        key={`${lessonIndex}-${slideIndex}`}
        className="flex-1 animate-fade-in"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        <SlideRenderer slide={slides[slideIndex]} accentColor={accentColor} />
      </div>

      {/* ── Navigation ── */}
      <div className="flex gap-3 mt-4 pb-2">
        {(slideIndex > 0 || lessonIndex > 0) && (
          <button
            onClick={prevSlide}
            className="flex-1 py-3 rounded-2xl text-sm font-extrabold border-2 border-gray-200 text-gray-600 active:scale-95 transition-transform"
          >
            Back
          </button>
        )}
        <button
          onClick={nextSlide}
          className="flex-1 py-3 rounded-2xl text-sm font-extrabold text-white active:scale-95 transition-transform"
          style={{ backgroundColor: accentColor }}
        >
          {buttonLabel}
        </button>
      </div>
    </div>
  );
}

// ── Classic Mode (original text-based rendering) ──────────────────────────────

function ClassicModeViewer({
  lessons,
  accentColor,
  onDone,
}: LessonViewerProps) {
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

// ── Main LessonViewer ─────────────────────────────────────────────────────────

export default function LessonViewer(props: LessonViewerProps) {
  // Use slide mode for all lessons — the adapter auto-generates slides
  // from old-format lessons, so every lesson gets the slide treatment.
  return <SlideModeViewer {...props} />;
}

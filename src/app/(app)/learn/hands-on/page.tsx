'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { DONE_KEY } from '@/components/handsOn/HandsOnPlayer';
import PartitionShape from '@/components/handsOn/PartitionShape';
import { HANDS_ON_LESSONS, HANDS_ON_TOPIC, getFigure } from '@/lib/handsOn/partition';
import { C } from '@/components/visuals/parts';

type Done = Record<string, { score: number; outOf: number }>;

export default function HandsOnLessonsPage() {
  const [done, setDone] = useState<Done>({});

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DONE_KEY);
      if (raw) setDone(JSON.parse(raw) as Done);
    } catch {
      // Nothing remembered: every lesson simply shows as not started.
    }
  }, []);

  // The first lesson not yet finished is the one to start.
  let startIndex = 0;
  while (startIndex < HANDS_ON_LESSONS.length && done[HANDS_ON_LESSONS[startIndex].id]) startIndex += 1;

  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/practice" className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center" aria-label="Back">
          &larr;
        </Link>
        <h1 className="text-white text-title">Hands-on lessons</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Learn by doing.</p>
            <p className="text-xs text-ink-muted mt-0.5">
              Short lessons where you colour and build the answer yourself. Each one takes about two minutes and ends with a skill check.
            </p>
          </div>
        </div>

        <h2 className="font-display text-heading text-ink mb-3">{HANDS_ON_TOPIC} <span className="text-label text-ink-muted">· Grades 4–5</span></h2>

        <ol className="space-y-3">
          {HANDS_ON_LESSONS.map((lesson, i) => {
            const result = done[lesson.id];
            // A small picture from the lesson itself.
            const first = lesson.screens[lesson.screens.length - 1];
            const fig = first.kind !== 'see' ? getFigure(first.figure) : null;
            const marks: boolean[] = [];
            if (fig) for (let k = 0; k < fig.pieces.length; k++) marks.push(k % 2 === 0);
            return (
              <li key={lesson.id}>
                <Link
                  href={`/learn/hands-on/${lesson.id}`}
                  className="flex items-center gap-4 bg-white rounded-card border-2 border-line hover:border-ink p-4 min-h-[96px] transition-colors"
                >
                  <span className="w-[68px] flex-shrink-0 flex items-center justify-center" aria-hidden="true">
                    {fig && <PartitionShape figure={fig} shaded={marks} fill={C.action} size={60} label="" />}
                  </span>
                  <span className="flex-1 min-w-0">
                    <span className="block text-caption text-ink-muted">Lesson {i + 1}</span>
                    <span className="block font-display text-title text-ink">{lesson.title}</span>
                    <span className="block text-[13px] font-semibold text-ink-muted mt-0.5">{lesson.blurb}</span>
                  </span>
                  <span className="flex-shrink-0 text-right">
                    {result ? (
                      <span className="inline-block text-[13px] font-extrabold text-success bg-success-soft rounded-full px-2.5 py-1">
                        Done · {result.score}/{result.outOf}
                      </span>
                    ) : i === startIndex ? (
                      <span className="inline-block text-[13px] font-extrabold text-white bg-action rounded-full px-2.5 py-1">Start here</span>
                    ) : (
                      <span className="text-2xl leading-none text-ink-muted" aria-hidden="true">›</span>
                    )}
                  </span>
                </Link>
              </li>
            );
          })}
        </ol>

        <p className="text-caption text-ink-muted mt-5">
          More lessons and topics are on the way. These lessons are for learning; they do not change your XP or practice scores.
        </p>
      </div>
    </div>
  );
}

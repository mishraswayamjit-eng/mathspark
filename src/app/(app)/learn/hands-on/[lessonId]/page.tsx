'use client';

import Link from 'next/link';
import HandsOnPlayer from '@/components/handsOn/HandsOnPlayer';
import { getLesson } from '@/lib/handsOn/partition';

export default function HandsOnLessonPage({ params }: { params: { lessonId: string } }) {
  const lesson = getLesson(params.lessonId);

  if (!lesson) {
    return (
      <div className="min-h-screen bg-paper pb-24 px-4 pt-10 text-center">
        <p className="font-display text-heading text-ink">We could not find that lesson.</p>
        <Link href="/learn/hands-on" className="inline-flex items-center justify-center min-h-[48px] px-5 mt-4 rounded-control border-2 border-ink bg-white text-ink font-extrabold">
          All hands-on lessons
        </Link>
      </div>
    );
  }

  // The key gives each lesson a fresh player when moving on to the next one.
  return <HandsOnPlayer key={lesson.id} lesson={lesson} />;
}

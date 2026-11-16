'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AvatarLink from '@/components/shell/AvatarLink';
import { useStudent } from '@/components/shell/StudentProvider';
import TopicList from '@/components/topics/TopicList';
import TopicLinkRow from '@/components/topics/TopicLinkRow';
import { useTopicProgress } from '@/components/topics/useTopicProgress';

// The Learn tab leads with the child's topics: the very same list as
// Practise → By topic (src/components/topics/TopicList.tsx). Tapping a topic
// opens its page, which holds the lesson, practice, drill and the rest.
// Browsing by kind of content stays below as "More ways to learn".

interface LearnCard {
  href: string;
  emoji: string;
  label: string;
  sub: string;
}

const MORE_WAYS: LearnCard[] = [
  { href: '/learn/lessons',         emoji: '📖', label: 'Concept Lessons',  sub: 'Learn a new idea step by step' },
  { href: '/learn/hands-on',        emoji: '🖐️', label: 'Hands-on Lessons', sub: 'Colour and build the answer yourself' },
  { href: '/learn/concept-trainer', emoji: '🎯', label: 'Concept Trainer',  sub: 'Think it through in three steps' },
  { href: '/learn/examples',        emoji: '💡', label: 'Solved examples',  sub: 'Watch Sparky solve a question, one step at a time' },
  { href: '/learn/stories',         emoji: '📚', label: 'Math Stories',     sub: 'Maths in the real world' },
  { href: '/learn/concept-map',     emoji: '🗺️', label: 'Concept Map',      sub: 'See how the ideas in maths join up' },
];

function validGrade(grade: number | null | undefined): number | null {
  return typeof grade === 'number' && grade >= 2 && grade <= 9 ? grade : null;
}

export default function LearnIndexPage() {
  const router = useRouter();
  // The child's grade comes from the student the app shell loaded on the
  // server, so the list is in the very first paint. The stored grade is only a
  // fallback for the moment after sign-in, before the shell has caught up.
  const { student } = useStudent();
  const [storedGrade, setStoredGrade] = useState<number | null>(null);
  const progress = useTopicProgress();

  useEffect(() => {
    if (!localStorage.getItem('mathspark_student_id')) { router.replace('/start'); return; }
    setStoredGrade(validGrade(Number(localStorage.getItem('mathspark_student_grade'))));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const grade = validGrade(student ? student.grade : null) || storedGrade;

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 min-h-[80px] flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-white text-title">Learn</h1>
          <p className="text-white/70 text-[13px] font-semibold">Pick something new to learn</p>
        </div>
        <AvatarLink />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-6">
        <p className="text-label text-ink-muted">
          Tap a topic to find its lesson, practice, drill and more.
        </p>

        {/* The shared topic list. Until the grade is known (rare: just after
            sign-in) the same space is held by plain placeholder rows. */}
        {grade !== null ? (
          <TopicList grade={grade} from="learn" progress={progress} />
        ) : (
          <div className="space-y-3" aria-hidden="true">
            <div className="h-7 w-40 rounded-full bg-soft" />
            {[0, 1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-[76px] bg-white rounded-card border-2 border-line" />
            ))}
          </div>
        )}

        <section>
          <h2 className="text-heading text-ink mb-3">More ways to learn</h2>
          <ul className="space-y-3">
            {MORE_WAYS.map((c) => (
              <li key={c.href}>
                <TopicLinkRow href={c.href} emoji={c.emoji} title={c.label} sub={c.sub} />
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}

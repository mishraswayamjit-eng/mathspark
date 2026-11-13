'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { CONCEPT_TRAINERS } from '@/data/conceptTrainers';
import { gradeInRange } from '@/lib/sharedUtils';

export default function ConceptTrainerCatalog() {
  const [grade, setGrade] = useState(4);

  useEffect(() => {
    setGrade(Number(localStorage.getItem('mathspark_student_grade')) || 4);
  }, []);

  const visible = useMemo(
    () => CONCEPT_TRAINERS.filter((t) => gradeInRange(t.gradeRange, grade)),
    [grade],
  );

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href="/chapters"
          className="text-white/70 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <h1 className="text-white text-title">Concept Trainer</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        {/* Intro box */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">
              Train how you think, not just the answer!
            </p>
            <p className="text-xs text-ink-muted mt-0.5">
              Each item walks you through three thinking steps with pictures.
            </p>
          </div>
        </div>

        {visible.length === 0 && (
          <p className="text-center text-ink-muted text-sm py-10">
            No concept trainers for your grade yet — check back soon! 🌟
          </p>
        )}

        <div className="grid grid-cols-1 gap-3">
          {visible.map((t) => (
            <Link
              key={t.slug}
              href={`/learn/concept-trainer/${t.slug}`}
              className="bg-white rounded-card p-4 border-2 border-line flex items-center gap-4 active:scale-[0.98] transition-transform"
            >
              <div
                className="w-14 h-14 rounded-tile flex items-center justify-center text-3xl flex-shrink-0"
                style={{ backgroundColor: `${t.color}22` }}
                aria-hidden="true"
              >
                {t.emoji}
              </div>
              <div className="min-w-0">
                <p className="font-extrabold text-ink">{t.title}</p>
                <p className="text-xs text-ink-muted mt-0.5 leading-snug">{t.description}</p>
                <p className="text-xs font-bold text-ink-muted mt-1">
                  Grades {t.gradeRange[0]}–{t.gradeRange[1]}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

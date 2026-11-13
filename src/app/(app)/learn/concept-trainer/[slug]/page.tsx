'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import Sparky from '@/components/Sparky';
import ConceptItemView from '@/components/concept-trainer/ConceptItemView';
import { logError } from '@/lib/logger';
import type { ConceptTrainer } from '@/types/conceptTrainer';

export default function ConceptTrainerRunner() {
  const params = useParams();
  const slug = String(params.slug);

  const [trainer, setTrainer] = useState<ConceptTrainer | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  const [openModule, setOpenModule] = useState<number | null>(0);
  // Currently-open item: [moduleIndex, itemIndex] or null for the list view.
  const [active, setActive] = useState<[number, number] | null>(null);

  useEffect(() => {
    fetch(`/api/concept-trainers/${slug}`)
      .then((r) => {
        if (!r.ok) { setNotFound(true); return null; }
        return r.json();
      })
      .then((d: ConceptTrainer | null) => { if (d) setTrainer(d); })
      .catch((err) => { logError('[concept-trainer] fetch', err); setNotFound(true); })
      .finally(() => setLoading(false));
  }, [slug]);

  // ── Loading / not-found ─────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-3">
        <div className="animate-sparky-bounce"><Sparky mood="thinking" size={64} /></div>
        <p className="text-ink-muted font-semibold text-sm">Loading…</p>
      </div>
    );
  }

  if (notFound || !trainer) {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-3 px-6 text-center">
        <Sparky mood="thinking" size={64} />
        <p className="text-ink font-bold">This trainer isn&apos;t available yet.</p>
        <Link href="/learn/concept-trainer" className="text-action font-bold text-sm">
          ← Back to trainers
        </Link>
      </div>
    );
  }

  // ── Item view ───────────────────────────────────────────────────────────
  if (active) {
    const [mi, ii] = active;
    const mod = trainer.modules[mi];
    const item = mod.items[ii];
    const hasNext = ii + 1 < mod.items.length;
    return (
      <div className="min-h-screen bg-paper">
        <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
          <button
            onClick={() => setActive(null)}
            className="text-white/70 hover:text-white text-lg font-bold"
            aria-label="Back to list"
          >
            &larr;
          </button>
          <h1 className="text-white text-title truncate">{trainer.title}</h1>
        </div>
        <ConceptItemView
          module={mod}
          item={item}
          index={ii + 1}
          total={mod.items.length}
          onBack={() => setActive(null)}
          onNext={hasNext ? () => setActive([mi, ii + 1]) : null}
        />
      </div>
    );
  }

  // ── Module accordion (list) ─────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href="/learn/concept-trainer"
          className="text-white/70 hover:text-white text-lg font-bold"
          aria-label="Back"
        >
          &larr;
        </Link>
        <h1 className="text-white text-title">{trainer.title}</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 animate-fade-in">
        <p className="text-sm text-ink-muted font-medium mb-4">
          {trainer.modules.length} modules — each trains one way of thinking about{' '}
          {trainer.concept.toLowerCase()}.
        </p>

        <div className="space-y-2.5">
          {trainer.modules.map((mod, mi) => {
            const isOpen = openModule === mi;
            return (
              <div key={mod.code} className="bg-white rounded-card border-2 border-line overflow-hidden">
                <button
                  onClick={() => setOpenModule(isOpen ? null : mi)}
                  className="w-full flex items-center gap-3 px-4 py-3.5 text-left min-h-[56px]"
                >
                  <span className="w-8 h-8 rounded-full bg-soft text-ink flex items-center justify-center text-sm font-extrabold flex-shrink-0">
                    {mod.number}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="font-extrabold text-ink text-sm leading-tight">{mod.title}</p>
                    {mod.skill && (
                      <p className="text-xs text-ink-muted mt-0.5 leading-snug">{mod.skill}</p>
                    )}
                  </div>
                  {mod.level && (
                    <span className="text-xs font-bold text-ink-muted bg-soft px-2 py-0.5 rounded-full border-2 border-line flex-shrink-0">
                      {mod.level}
                    </span>
                  )}
                  <span className="text-ink-muted text-sm flex-shrink-0">{isOpen ? '▾' : '▸'}</span>
                </button>

                {isOpen && (
                  <div className="px-4 pb-4 border-t-2 border-line pt-3">
                    {mod.rule && (
                      <p className="text-[13px] text-ink bg-soft border-2 border-line rounded-note px-3 py-2 mb-3 font-medium leading-snug">
                        📏 {mod.rule}
                      </p>
                    )}
                    <div className="space-y-1.5">
                      {mod.items.map((item, ii) => (
                        <button
                          key={item.code}
                          onClick={() => setActive([mi, ii])}
                          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-control border-2 border-line bg-white hover:border-ink text-left min-h-[48px] active:scale-[0.99] transition-transform"
                        >
                          <span className="text-xs font-bold text-ink-muted flex-shrink-0">{ii + 1}</span>
                          <span className="text-sm text-ink font-semibold flex-1 leading-tight">{item.title}</span>
                          <span className="text-ink-muted text-sm flex-shrink-0">→</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

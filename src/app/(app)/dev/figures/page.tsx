'use client';

import { useEffect, useState } from 'react';
import FigureView from '@/components/figures/FigureView';
import KatexRenderer from '@/components/KatexRenderer';
import type { FigureSpec, ServedVisual } from '@/lib/figures/types';

// ── What /api/figures/gallery returns ─────────────────────────────────────────

interface GalleryStep { step: number; text: string; latex?: string }

interface GalleryItem {
  id: string;
  found: boolean;
  subTopic: string;
  questionText: string;
  options: string[];
  correctAnswer: string;
  steps: GalleryStep[];
  visual: ServedVisual;
}

interface GalleryPage {
  total: number;
  offset: number;
  limit: number;
  kind: string;
  kindCounts: Record<string, number>;
  items: GalleryItem[];
}

const PAGE_SIZE = 10;
const LETTERS = ['A', 'B', 'C', 'D'];

const KINDS = [
  'triangle', 'rectangle', 'polygon', 'circle', 'angles', 'clock', 'compass', 'fractionBars', 'set', 'barModel',
  'numberLine', 'journey', 'placeChart', 'grid', 'barChart', 'table', 'venn', 'balance', 'factorTree',
];

// ── One question beside its figures ───────────────────────────────────────────

interface StepRow { text: string; latex?: string; figure: FigureSpec | null }

function FigureBox({ spec }: { spec: FigureSpec | null | undefined }) {
  if (!spec) {
    return <p className="text-caption text-ink-muted text-center py-3">No figure for this step</p>;
  }
  return (
    <div className="rounded-control border-2 border-line bg-white p-3">
      <p className="text-caption text-ink-muted mb-1">{spec.kind}</p>
      <FigureView spec={spec} />
    </div>
  );
}

function QuestionReview({ item }: { item: GalleryItem }) {
  const visual = item.visual || {};
  const stepFigures = Array.isArray(visual.stepFigures) ? visual.stepFigures : [];
  const computed = Array.isArray(visual.steps) ? visual.steps : [];

  // The question's own steps with their figures, or the computed steps when it has none.
  const rows: StepRow[] = [];
  if (item.steps.length > 0) {
    for (let i = 0; i < item.steps.length; i++) {
      rows.push({ text: item.steps[i].text, latex: item.steps[i].latex, figure: stepFigures[i] || null });
    }
  } else {
    for (let i = 0; i < computed.length; i++) {
      rows.push({ text: computed[i].text, figure: computed[i].figure || null });
    }
  }
  const uneven = item.steps.length > 0 && stepFigures.length > 0 && stepFigures.length !== item.steps.length;

  return (
    <article className="ui-card space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <span className="ui-chip">{item.id}</span>
        {item.subTopic !== '' && <span className="ui-chip">{item.subTopic}</span>}
        {item.steps.length === 0 && computed.length > 0 && <span className="ui-chip">computed steps</span>}
      </div>

      {!item.found && (
        <p className="ui-hint">This question is not in the database yet, so only its figures are shown.</p>
      )}
      {uneven && (
        <p className="ui-hint">
          Check this one: {stepFigures.length} step figures for {item.steps.length} steps.
        </p>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-3">
          <p className="text-[17px] leading-snug font-bold text-ink whitespace-pre-wrap">{item.questionText}</p>
          <ul className="space-y-2">
            {item.options.map((option, i) => {
              const correct = LETTERS[i] === item.correctAnswer;
              return (
                <li
                  key={i}
                  className={`flex items-start gap-2 rounded-control border-2 px-3 py-2 text-[15px] font-bold ${correct ? 'border-success bg-success-soft text-ink' : 'border-line bg-white text-ink'}`}
                >
                  <span className="flex-shrink-0 w-6 text-ink-muted">{LETTERS[i]}</span>
                  <span className="flex-1 min-w-0 break-words">{option}</span>
                  {correct && <span className="flex-shrink-0 text-caption text-success">answer</span>}
                </li>
              );
            })}
          </ul>
        </div>
        <div>
          <p className="text-label text-ink-muted mb-1">Before answering</p>
          {visual.figure ? (
            <FigureBox spec={visual.figure} />
          ) : (
            <p className="text-caption text-ink-muted py-3">No figure before answering</p>
          )}
        </div>
      </div>

      {rows.length > 0 && (
        <div className="space-y-3">
          <p className="text-label text-ink-muted">After answering</p>
          {rows.map((row, i) => (
            <div key={i} className="grid gap-3 md:grid-cols-2 border-t-2 border-line pt-3">
              <div>
                <p className="text-caption text-ink-muted">Step {i + 1}</p>
                <p className="text-[15px] leading-snug font-bold text-ink whitespace-pre-wrap">{row.text}</p>
                {row.latex ? <KatexRenderer latex={row.latex} className="block mt-1 text-ink" /> : null}
              </div>
              <FigureBox spec={row.figure} />
            </div>
          ))}
        </div>
      )}
    </article>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function FigureGalleryPage() {
  const [kind, setKind] = useState('');
  const [offset, setOffset] = useState(0);
  const [page, setPage] = useState<GalleryPage | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    let live = true;
    setLoading(true);
    setMessage('');
    const query = new URLSearchParams({ offset: String(offset), limit: String(PAGE_SIZE) });
    if (kind !== '') query.set('kind', kind);
    fetch(`/api/figures/gallery?${query.toString()}`)
      .then((res) => {
        if (res.status === 401) throw new Error('Log in as a student first (the quick-login page is at /dev), then come back.');
        if (res.status === 429) throw new Error('Too many requests. Wait a minute and try again.');
        if (!res.ok) throw new Error('The gallery could not be loaded. Try again.');
        return res.json();
      })
      .then((data: GalleryPage) => {
        if (!live) return;
        setPage(data);
        setLoading(false);
      })
      .catch((err: unknown) => {
        if (!live) return;
        setPage(null);
        setMessage(err instanceof Error ? err.message : 'The gallery could not be loaded. Try again.');
        setLoading(false);
      });
    return () => { live = false; };
  }, [kind, offset]);

  const total = page ? page.total : 0;
  const shown = page ? page.items.length : 0;
  const counts: Record<string, number> = page && page.kindCounts ? page.kindCounts : {};
  const canGoBack = offset > 0;
  const canGoOn = offset + PAGE_SIZE < total;

  const pager = (
    <div className="flex items-center gap-3">
      <button type="button" className="ui-btn flex-1" disabled={!canGoBack || loading} onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}>
        Previous
      </button>
      <p className="text-label text-ink-muted text-center min-w-[110px]">
        {total === 0 ? '0 of 0' : `${offset + 1} to ${offset + shown} of ${total}`}
      </p>
      <button type="button" className="ui-btn flex-1" disabled={!canGoOn || loading} onClick={() => setOffset(offset + PAGE_SIZE)}>
        Next
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-paper px-4 py-8 pb-24 max-w-4xl mx-auto space-y-4">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <h1 className="text-xl font-bold text-ink">Question figures</h1>
          <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded-full font-semibold">DEV ONLY</span>
        </div>
        <p className="text-sm text-ink-muted">Every question that has a figure, beside its figure and its step figures.</p>
      </div>

      <label className="block">
        <span className="text-caption text-ink-muted">Figure kind</span>
        <select
          value={kind}
          onChange={(e) => { setKind(e.target.value); setOffset(0); }}
          className="mt-1 w-full min-h-[48px] rounded-control border-2 border-line bg-white px-3 font-extrabold text-[15px] text-ink"
        >
          <option value="">All kinds</option>
          {KINDS.map((k) => (
            <option key={k} value={k}>{`${k} (${counts[k] || 0})`}</option>
          ))}
        </select>
      </label>

      {pager}

      {message !== '' && <p className="ui-hint">{message}</p>}
      {loading && <div className="ui-card h-40 animate-pulse" aria-label="Loading" />}
      {!loading && message === '' && shown === 0 && (
        <p className="ui-card text-ink-muted text-center">No questions with figures here yet.</p>
      )}
      {!loading && page ? page.items.map((item) => <QuestionReview key={item.id} item={item} />) : null}

      {!loading && shown > 3 && pager}
    </div>
  );
}

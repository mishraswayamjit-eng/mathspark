'use client';

import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import type { CSSProperties } from 'react';
import type { BoardOp } from '@/lib/teach/types';
import FigureView from '@/components/figures/FigureView';
import { C } from '@/components/visuals/parts';
import RowMarks from './board/Marks';
import { measureBoard } from './board/measure';
import type { BoardLayout, RowLayout } from './board/measure';
import { buildModel, timingFor } from './board/model';
import type { BoardMark, LineRow, Timing } from './board/model';
import { BOARD_CSS } from './board/styles';

export interface WorkingBoardProps {
  /** Everything done on the board so far, in order. The board draws the result of all of it. */
  ops: BoardOp[];
  /**
   * Ops from this index onwards are new: they are written or drawn with an
   * animation, one after another. Ops before it are shown as already done.
   */
  animateFrom: number;
  /** How long the new ops have to appear, in milliseconds (the length of the sentence being spoken). */
  beatMs: number;
  /** Extra classes for the outer element. */
  className?: string;
}

// The server render has no layout to measure, and React warns about useLayoutEffect there.
const useIsoLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;

/** Font size used until the board has been measured (and on the server). */
const FALLBACK_FONT = 24;

function animation(name: string, t: Timing | null): CSSProperties | undefined {
  if (!t) return undefined;
  return { animation: name + ' ' + t.dur + 'ms ease-out ' + t.delay + 'ms both' };
}

interface LineProps {
  row: LineRow;
  marks: BoardMark[];
  layout: BoardLayout | null;
  timing: (opIndex: number) => Timing | null;
}

/** One line of working, with the marks made on it drawn over the top. */
function Line({ row, marks, layout, timing }: LineProps) {
  const placed: RowLayout | undefined = layout ? layout.rows[row.key] : undefined;
  const base = layout ? layout.base : FALLBACK_FONT;
  const f = placed ? placed.f : FALLBACK_FONT;
  const t = timing(row.opIndex);

  const textStyle: CSSProperties = {
    color: row.tone === 'given' ? C.ink : C.action,
    fontSize: f,
    left: placed ? placed.left : 0,
  };
  const write = animation('wb-write', t);
  if (write) textStyle.animation = write.animation;

  return (
    <div
      data-row={row.key}
      className="relative"
      style={{
        // Room above for arcs and small notes; room below only when something is written under the line.
        paddingTop: Math.round(base * 0.62),
        paddingBottom: Math.round(base * (row.below ? 1.05 : 0.3)),
        transition: 'padding-bottom 200ms ease-out',
      }}
    >
      <div
        data-text=""
        className={'relative inline-block whitespace-pre font-display font-semibold leading-[1.2]' + (t ? ' wb-anim' : '')}
        style={textStyle}
      >
        {row.eq >= 0 ? (
          <>
            <span data-seg="">{row.text.slice(0, row.eq)}</span>
            <span data-seg="">=</span>
            <span data-seg="">{row.text.slice(row.eq + 1)}</span>
          </>
        ) : (
          <span data-seg="">{row.text}</span>
        )}
      </div>
      <RowMarks marks={marks} rects={layout ? layout.rects : null} f={f} base={base} timing={timing} />
    </div>
  );
}

/**
 * The teacher's board: lines of working written one under another, with the
 * marks a teacher makes as they talk (arcs, strike-throughs with a note, bars
 * for dividing both sides, a ring round the answer).
 *
 * Lines are real text, lined up on their equals signs. Marks are drawn over
 * each line from the measured position of the text they point at (see
 * `board/measure.ts`). Give the board a height or a max-height through
 * `className` and it scrolls itself to keep the newest line in view.
 */
export default function WorkingBoard({ ops, animateFrom, beatMs, className }: WorkingBoardProps) {
  const model = useMemo(() => buildModel(ops), [ops]);
  const modelRef = useRef(model);
  modelRef.current = model;

  const scrollerRef = useRef<HTMLDivElement | null>(null);
  const contentRef = useRef<HTMLDivElement | null>(null);
  const widthRef = useRef(0);
  const [layout, setLayout] = useState<BoardLayout | null>(null);

  const measure = useCallback(() => {
    const root = contentRef.current;
    if (!root) return;
    const next = measureBoard(root, modelRef.current);
    if (!next) return;
    widthRef.current = next.width;
    setLayout(next);
  }, []);

  // Measure before the browser paints, so a new line is never seen in the wrong place.
  useIsoLayoutEffect(() => {
    measure();
  }, [model, measure]);

  // Measure again when the board changes width, and when the display font arrives.
  useEffect(() => {
    const root = contentRef.current;
    if (!root) return undefined;
    let alive = true;
    let frame = 0;
    const onResize = () => {
      if (root.clientWidth === widthRef.current) return;
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(measure);
    };
    const onFonts = () => {
      if (alive) measure();
    };
    let observer: ResizeObserver | null = null;
    if (typeof ResizeObserver !== 'undefined') {
      observer = new ResizeObserver(onResize);
      observer.observe(root);
    }
    window.addEventListener('resize', onResize);
    const fonts = document.fonts;
    if (fonts && fonts.ready) fonts.ready.then(onFonts);
    if (fonts && typeof fonts.addEventListener === 'function') fonts.addEventListener('loadingdone', onFonts);
    return () => {
      alive = false;
      window.cancelAnimationFrame(frame);
      if (observer) observer.disconnect();
      window.removeEventListener('resize', onResize);
      if (fonts && typeof fonts.removeEventListener === 'function') fonts.removeEventListener('loadingdone', onFonts);
    };
  }, [measure]);

  // Keep the row the teacher is working on in view.
  useEffect(() => {
    const scroller = scrollerRef.current;
    const root = contentRef.current;
    if (!scroller || !root) return;
    if (!model.focusKey) {
      scroller.scrollTop = 0;
      return;
    }
    const row = root.querySelector('[data-row="' + model.focusKey + '"]');
    if (!row) return;
    const view = scroller.getBoundingClientRect();
    const box = row.getBoundingClientRect();
    let delta = 0;
    if (box.bottom > view.bottom - 8) delta = box.bottom - view.bottom + 16;
    else if (box.top < view.top + 8) delta = box.top - view.top - 16;
    if (delta === 0) return;
    const top = Math.max(0, scroller.scrollTop + delta);
    const calm = typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!calm && typeof scroller.scrollTo === 'function') scroller.scrollTo({ top: top, behavior: 'smooth' });
    else scroller.scrollTop = top;
  }, [model]);

  // The time for this batch of new ops is fixed when the batch arrives, so a
  // later change to beatMs alone cannot restart drawing that is under way.
  const batch = useRef({ from: -1, length: -1, ms: 0 });
  if (batch.current.from !== animateFrom || batch.current.length !== ops.length) {
    batch.current = { from: animateFrom, length: ops.length, ms: beatMs };
  }
  const ms = batch.current.ms;
  const total = ops.length;
  const timing = (opIndex: number) => timingFor(opIndex, animateFrom, total, ms);

  const marksByRow: Record<string, BoardMark[]> = {};
  for (let i = 0; i < model.marks.length; i++) {
    const mark = model.marks[i];
    if (!marksByRow[mark.rowKey]) marksByRow[mark.rowKey] = [];
    marksByRow[mark.rowKey].push(mark);
  }

  return (
    <div
      ref={scrollerRef}
      role="img"
      aria-label={model.spoken ? 'The working so far. ' + model.spoken : 'The board is empty'}
      className={`relative min-h-[120px] overflow-y-auto overflow-x-hidden rounded-card border-2 border-line bg-white px-4 py-3 ${className ?? ''}`}
    >
      <style>{BOARD_CSS}</style>
      <div ref={contentRef} className="relative">
        {model.rows.map((row) => {
          if (row.kind === 'figure') {
            const t = timing(row.opIndex);
            return (
              <div
                key={row.key}
                data-row={row.key}
                className={'flex justify-center py-3' + (t ? ' wb-anim' : '')}
                style={animation('wb-fade', t)}
              >
                <div className="w-full max-w-[300px]">
                  <FigureView spec={row.spec} />
                </div>
              </div>
            );
          }
          return <Line key={row.key} row={row} marks={marksByRow[row.key] || []} layout={layout} timing={timing} />;
        })}
      </div>
    </div>
  );
}

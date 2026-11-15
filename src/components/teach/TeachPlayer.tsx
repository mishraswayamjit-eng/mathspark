'use client';

import { useEffect, useState, type ReactNode } from 'react';
import Sparky from '@/components/Sparky';
import WorkingBoard from '@/components/teach/WorkingBoard';
import type { TeachBeat } from '@/lib/teach/types';
import LessonAsk from './player/LessonAsk';
import LessonControls from './player/LessonControls';
import { useLessonPlayer } from './player/useLessonPlayer';
import { rememberTeachAvailability } from './player/useTeachAvailable';
import { logContentView } from '@/lib/contentView';

/**
 * "Explain it to me": plays the teacher's lesson for one question.
 *
 * The lesson is fetched from /api/teach/[questionId] and played a beat at a
 * time: the sentence is spoken and shown as a caption while the board is
 * written. It never starts talking before it is put on screen, and all speech
 * stops when it is taken off or given a different question.
 *
 * Everything shown and said is pre-written, pre-checked content. The choices
 * a child taps here are part of the lesson only: nothing is recorded or scored.
 */

export interface TeachPlayerProps {
  questionId: string;
  /** Close the lesson: back to the question, or on to the next one. */
  onClose?: () => void;
  /** Words for the button that closes the lesson at its end. */
  closeLabel?: string;
  /** Shown in place of the lesson when this question has none (the written steps, usually). */
  fallback?: ReactNode;
  /** Extra classes for the outer element. */
  className?: string;
}

type Load =
  | { status: 'loading' }
  | { status: 'ready'; beats: TeachBeat[] }
  | { status: 'none' }
  | { status: 'held' }
  | { status: 'trouble' };

const NO_BEATS: TeachBeat[] = [];

export default function TeachPlayer({ questionId, onClose, closeLabel, fallback, className }: TeachPlayerProps) {
  const [load, setLoad] = useState<Load>({ status: 'loading' });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let live = true;
    setLoad({ status: 'loading' });
    (async () => {
      try {
        const res = await fetch(`/api/teach/${encodeURIComponent(questionId)}`);
        if (!live) return;
        if (res.status === 404) {
          rememberTeachAvailability(questionId, false);
          setLoad({ status: 'none' });
          return;
        }
        if (res.status === 403) {
          setLoad({ status: 'held' });
          return;
        }
        if (!res.ok) {
          setLoad({ status: 'trouble' });
          return;
        }
        const data = (await res.json()) as { beats?: TeachBeat[] };
        if (!live) return;
        const beats = Array.isArray(data.beats) ? data.beats : [];
        setLoad(beats.length > 0 ? { status: 'ready', beats } : { status: 'none' });
      } catch {
        if (live) setLoad({ status: 'trouble' });
      }
    })();
    return () => { live = false; };
  }, [questionId, attempt]);

  // With no beats the player below is idle and silent.
  const beats = load.status === 'ready' ? load.beats : NO_BEATS;
  const player = useLessonPlayer(beats);
  const { view, togglePause, back, forward } = player;
  const playing = load.status === 'ready';

  // A record that the lesson was opened and, later, finished. Nothing is scored.
  const finished = playing && view.stage === 'done';
  useEffect(() => { if (playing) logContentView('teach', questionId); }, [playing, questionId]);
  useEffect(() => { if (finished) logContentView('teach', questionId, true); }, [finished, questionId]);

  // Keyboard: Space pauses and carries on, the arrow keys step.
  useEffect(() => {
    if (!playing) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      const el = e.target as HTMLElement | null;
      const tag = el && el.tagName ? el.tagName : '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (el && el.isContentEditable)) return;
      if (e.key === ' ' || e.key === 'Spacebar') {
        // On a button, Space presses that button as usual.
        if (tag === 'BUTTON' || tag === 'A') return;
        e.preventDefault();
        togglePause();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        back();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        forward();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [playing, togglePause, back, forward]);

  const closeButton = onClose ? (
    <button
      type="button"
      onClick={onClose}
      aria-label="Close the lesson"
      className="w-12 h-12 flex-shrink-0 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg hover:border-ink"
    >
      <span aria-hidden="true">✕</span>
    </button>
  ) : null;

  const header = (
    <div className="flex items-center gap-3">
      <div className="flex-shrink-0" aria-hidden="true">
        <Sparky mood={view.stage === 'done' ? 'celebrating' : view.stage === 'asking' ? 'thinking' : 'happy'} size={44} />
      </div>
      <div className="flex-1 min-w-0">
        <h2 className="font-display text-title text-ink leading-tight">Explain it to me</h2>
        {playing && view.stage !== 'ready' && (
          <p className="text-[14px] font-extrabold text-ink-muted">
            Part {view.index + 1} of {player.total}
          </p>
        )}
      </div>
      {closeButton}
    </div>
  );

  const outer = `space-y-3 ${className ?? ''}`;

  // ── Before there is a lesson to play ────────────────────────────────────────

  if (load.status === 'loading' || (playing && view.stage === 'ready')) {
    return (
      <section className={outer} aria-label="Explain it to me">
        {header}
        <div className="rounded-card border-2 border-line bg-soft px-4 py-8 text-center animate-pulse" role="status">
          <p className="text-[16px] font-bold text-ink">Getting the board ready…</p>
        </div>
      </section>
    );
  }

  if (load.status === 'none') {
    return (
      <section className={outer} aria-label="Explain it to me">
        {header}
        {fallback ? (
          <>
            <p className="text-[15px] font-semibold text-ink-muted leading-relaxed">
              Sparky has not made a lesson for this one yet. Here are the steps instead.
            </p>
            {fallback}
          </>
        ) : (
          <div className="rounded-control border-2 border-line bg-soft px-4 py-5 text-center">
            <p className="text-[16px] font-bold text-ink leading-relaxed">
              <span aria-hidden="true">🌟</span> Sparky has not made a lesson for this one yet.
            </p>
          </div>
        )}
      </section>
    );
  }

  if (load.status === 'held' || load.status === 'trouble') {
    return (
      <section className={outer} aria-label="Explain it to me">
        {header}
        <div className="rounded-control border-2 border-line bg-soft px-4 py-5 text-center space-y-3">
          <p className="text-[16px] font-bold text-ink leading-relaxed">
            {load.status === 'held'
              ? 'This question is in a test you are still doing. The lesson opens once the test is finished.'
              : 'The lesson did not open this time. Shall we try once more?'}
          </p>
          {load.status === 'trouble' && (
            <button type="button" onClick={() => setAttempt(attempt + 1)} className="ui-btn ui-btn-primary w-full">
              <span aria-hidden="true">↺</span> Try again
            </button>
          )}
          {onClose && (
            <button type="button" onClick={onClose} className="ui-btn w-full">
              {closeLabel || 'Back to the question'}
            </button>
          )}
        </div>
      </section>
    );
  }

  // ── The lesson ──────────────────────────────────────────────────────────────

  const beat = beats[Math.min(view.index, beats.length - 1)];
  const ask = beat.ask;
  const done = view.stage === 'done';
  const showAsk = !!ask && (view.stage === 'asking' || (view.stage === 'reply' && ask.kind === 'choose'));

  return (
    <section className={outer} aria-label="Explain it to me">
      {header}

      {/* Where we are in the lesson */}
      <div className="flex items-center gap-1.5" aria-hidden="true">
        {beats.map((_, i) => (
          <span
            key={i}
            className={`h-2 flex-1 rounded-full border-2 ${
              i < view.index || done ? 'bg-ink border-ink' : i === view.index ? 'bg-action border-ink' : 'bg-white border-line'
            }`}
          />
        ))}
      </div>

      {/* The board. A new key draws it afresh (say it again, back a step, watch again). */}
      <WorkingBoard key={view.boardRun} ops={player.ops} animateFrom={player.animateFrom} beatMs={view.beatMs} />

      {/* What the teacher is saying. Read out by a screen reader only when the voice is off. */}
      <div
        className="rounded-control border-2 border-line bg-soft px-4 py-3 min-h-[76px] flex items-center"
        aria-live={player.muted ? 'polite' : 'off'}
      >
        <p key={`${view.index}-${view.stage === 'reply' ? 'r' : 's'}`} className="animate-fade-in text-[17px] font-bold text-ink leading-relaxed [overflow-wrap:anywhere]">
          {view.caption}
        </p>
      </div>

      {player.voiceLost && (
        <p className="text-[14px] font-semibold text-ink-muted leading-snug">
          The voice is having a rest, so read along with the words. Tap the speaker to try the voice again.
        </p>
      )}

      {/* The child's turn */}
      {showAsk && ask && (
        <LessonAsk
          ask={ask}
          answered={view.stage === 'reply'}
          picked={view.picked}
          onChoose={player.choose}
          onReady={player.moveOn}
          onShowMe={player.moveOn}
        />
      )}

      {/* The end: the last beat stays up */}
      {done && (
        <div className="flex flex-col sm:flex-row gap-2">
          <button type="button" onClick={player.restart} className="ui-btn flex-1">
            <span aria-hidden="true">↺</span> Watch again
          </button>
          {onClose && (
            <button type="button" onClick={onClose} className="ui-btn ui-btn-primary flex-1">
              {closeLabel || 'Back to the question'} <span aria-hidden="true">→</span>
            </button>
          )}
        </div>
      )}

      <LessonControls
        paused={view.paused}
        canPause={view.stage === 'saying' || view.stage === 'reply'}
        canGoBack={view.index > 0}
        atEnd={done}
        muted={player.muted}
        slow={player.slow}
        onTogglePause={togglePause}
        onReplay={player.replay}
        onBack={back}
        onSkipToEnd={player.skipToEnd}
        onToggleSlow={player.toggleSlow}
        onToggleMute={player.toggleMute}
      />
    </section>
  );
}

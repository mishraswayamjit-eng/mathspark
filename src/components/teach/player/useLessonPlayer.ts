'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';
import { fetchServerVoice } from '@/lib/speech/serverVoice';
import type { BoardOp, TeachBeat } from '@/lib/teach/types';
import { GAP_MS, SLOW_FACTOR, SLOW_GAP_MS, START_WAIT_MS, audioLengthMs, praiseLine, sayMs } from './timing';

/**
 * Plays a lesson: one beat at a time, the teacher's sentence spoken while the
 * board is written, a stop wherever the child is asked something.
 *
 *   ready    the lesson has arrived and the first sentence is being fetched
 *   saying   a beat's sentence is being spoken (or timed, when the voice is off)
 *   asking   waiting for the child's turn
 *   reply    saying the short line that follows the child's choice
 *   done     the last beat stays up
 *
 * The voice is `useReadAloud().speak`. It cannot be paused part-way or slowed
 * down, so "resume" says the current sentence again from its start, and the
 * slower speed leaves longer pauses between beats (and longer captions when
 * the voice is off). If the voice does not start, the lesson carries on with
 * captions timed by the length of each sentence.
 */

export type LessonStage = 'ready' | 'saying' | 'asking' | 'reply' | 'done';

export interface LessonView {
  /** The beat on screen. */
  index: number;
  stage: LessonStage;
  /** What the teacher is saying now: the beat's sentence, or the reply to a choice. */
  caption: string;
  paused: boolean;
  /** How long this beat's board ops have to appear. */
  beatMs: number;
  /** False when this beat's ops should be shown as already done (after a pause, at the end). */
  animate: boolean;
  /** Changes whenever the board should be drawn afresh (replay, back, watch again). */
  boardRun: number;
  /** The choice the child tapped on this beat, if any. */
  picked: number | null;
}

const INITIAL: LessonView = {
  index: 0,
  stage: 'ready',
  caption: '',
  paused: false,
  beatMs: 2000,
  animate: true,
  boardRun: 0,
  picked: null,
};

type Enter = (index: number, animate: boolean, fresh: boolean) => void;

export function useLessonPlayer(beats: TeachBeat[]) {
  const { speak, stop } = useReadAloud();
  const [view, setView] = useState<LessonView>(INITIAL);
  const [muted, setMuted] = useState(false);
  const [slow, setSlow] = useState(false);
  // True when the voice was switched off for the child because it would not start.
  const [voiceLost, setVoiceLost] = useState(false);

  // The engine reads these, so a timer or a voice callback never sees old values.
  const beatsRef = useRef<TeachBeat[]>(beats);
  beatsRef.current = beats;
  const viewRef = useRef<LessonView>(INITIAL);
  const mutedRef = useRef(false);
  const slowRef = useRef(false);
  // Bumped on every move; a timer or callback from before the move does nothing.
  const tokenRef = useRef(0);
  const timersRef = useRef<Array<ReturnType<typeof setTimeout>>>([]);
  // Real audio lengths, by sentence, once known.
  const lengthsRef = useRef<Record<string, number>>({});
  const praiseTurnRef = useRef(0);
  // True once the current sentence has been said and only the pause after it is left.
  const saidRef = useRef(false);
  const replyRef = useRef('');
  // How many sentences in a row the voice has not started for.
  const voiceMissesRef = useRef(0);
  // The sentence in the air: when it began, how long it should take, how to end it.
  const currentRef = useRef<{ startedAt: number; ms: number; done: () => void } | null>(null);
  const enterRef = useRef<Enter>(() => undefined);

  const apply = useCallback((patch: Partial<LessonView>) => {
    const next: LessonView = { ...viewRef.current, ...patch };
    viewRef.current = next;
    setView(next);
  }, []);

  /** Start a new move: everything scheduled by the last one is cancelled. */
  const begin = useCallback(() => {
    tokenRef.current += 1;
    const timers = timersRef.current;
    for (let i = 0; i < timers.length; i++) clearTimeout(timers[i]);
    timersRef.current = [];
    currentRef.current = null;
  }, []);

  const later = useCallback((fn: () => void, ms: number) => {
    const token = tokenRef.current;
    timersRef.current.push(setTimeout(() => {
      if (tokenRef.current === token) fn();
    }, ms));
  }, []);

  /** How long a sentence gets: the real audio length when known, otherwise an estimate. */
  const spanFor = useCallback((text: string): number => {
    if (mutedRef.current) {
      return Math.round(sayMs(text) * (slowRef.current ? SLOW_FACTOR : 1));
    }
    const measured = lengthsRef.current[text];
    return typeof measured === 'number' ? measured : sayMs(text);
  }, []);

  const gap = useCallback((): number => (slowRef.current ? SLOW_GAP_MS : GAP_MS), []);

  /** Fetch a sentence's audio ahead of time (the voice module caches it) and note its length. */
  const prepare = useCallback((text: string): Promise<void> => {
    if (!text || mutedRef.current) return Promise.resolve();
    return fetchServerVoice(text)
      .then((src) => (src ? audioLengthMs(src) : null))
      .then((ms) => {
        if (ms) lengthsRef.current[text] = ms;
      })
      .catch(() => { /* the device voice, or the caption timing, takes over */ });
  }, []);

  /** Say one sentence (or time it when the voice is off), then call `onDone` once. */
  const utter = useCallback((text: string, ms: number, onDone: () => void) => {
    const token = tokenRef.current;
    let finished = false;
    const done = () => {
      if (finished || tokenRef.current !== token) return;
      finished = true;
      onDone();
    };
    currentRef.current = { startedAt: Date.now(), ms, done };

    if (mutedRef.current) {
      later(done, ms);
      return;
    }

    let started = false;
    speak(text, {
      onStart: () => {
        started = true;
        voiceMissesRef.current = 0;
      },
      onEnd: done,
    });
    // The voice did not start in time (slow, blocked, offline): this one
    // sentence carries on with its caption alone, and the next one is still
    // fetched ahead and tried. Only when two sentences in a row get no voice
    // does the lesson switch to captions, so later beats do not each wait for
    // a voice that is not coming. The speaker button brings the voice back.
    later(() => {
      if (started || finished) return;
      stop();
      voiceMissesRef.current += 1;
      if (voiceMissesRef.current >= 2) {
        mutedRef.current = true;
        setMuted(true);
        setVoiceLost(true);
      }
      later(done, Math.max(800, ms - START_WAIT_MS));
    }, START_WAIT_MS);
    // The voice started but never reported its end.
    later(done, ms * 2 + 8000);
  }, [later, speak, stop]);

  /** After a sentence (a beat's, or a reply): pause briefly, then the next beat, or the end. */
  const carryOn = useCallback((withGap: boolean) => {
    const i = viewRef.current.index;
    if (i >= beatsRef.current.length - 1) {
      begin();
      apply({ stage: 'done', paused: false });
      return;
    }
    if (withGap) {
      later(() => enterRef.current(i + 1, true, false), gap());
    } else {
      enterRef.current(i + 1, true, false);
    }
  }, [apply, begin, gap, later]);

  const afterSay = useCallback((i: number) => {
    saidRef.current = true;
    const beat = beatsRef.current[i];
    if (beat && beat.ask) {
      begin();
      apply({ stage: 'asking' });
      return;
    }
    carryOn(true);
  }, [apply, begin, carryOn]);

  const enterBeat = useCallback<Enter>((i, animate, fresh) => {
    const all = beatsRef.current;
    if (i < 0 || i >= all.length) return;
    begin();
    const beat = all[i];
    const ms = spanFor(beat.say);
    saidRef.current = false;
    apply({
      index: i,
      stage: 'saying',
      caption: beat.say,
      paused: false,
      beatMs: ms,
      animate,
      picked: null,
      boardRun: viewRef.current.boardRun + (fresh ? 1 : 0),
    });
    // No dead air: have the next sentence's audio ready before this one ends.
    if (i + 1 < all.length) void prepare(all[i + 1].say);
    utter(beat.say, ms, () => afterSay(i));
  }, [afterSay, apply, begin, prepare, spanFor, utter]);
  enterRef.current = enterBeat;

  const sayReply = useCallback((line: string) => {
    saidRef.current = false;
    utter(line, spanFor(line), () => {
      saidRef.current = true;
      carryOn(true);
    });
  }, [carryOn, spanFor, utter]);

  // ── The child's turn ────────────────────────────────────────────────────────

  /** A choice was tapped: a brief "that's it", or the beat's own second look, then on. Never asked twice. */
  const choose = useCallback((choice: number) => {
    const v = viewRef.current;
    if (v.stage !== 'asking') return;
    const beat = beatsRef.current[v.index];
    const ask = beat ? beat.ask : undefined;
    if (!ask || ask.kind !== 'choose') return;
    let line = ask.ifNot;
    if (choice === ask.answer) {
      line = praiseLine(praiseTurnRef.current);
      praiseTurnRef.current += 1;
    }
    begin();
    replyRef.current = line;
    apply({ stage: 'reply', caption: line, picked: choice, paused: false });
    sayReply(line);
  }, [apply, begin, sayReply]);

  /** "I've got an idea" and "Show me": the lesson carries on. */
  const moveOn = useCallback(() => {
    if (viewRef.current.stage !== 'asking') return;
    begin();
    carryOn(false);
  }, [begin, carryOn]);

  // ── Controls ────────────────────────────────────────────────────────────────

  const pause = useCallback(() => {
    const v = viewRef.current;
    if (v.paused || (v.stage !== 'saying' && v.stage !== 'reply')) return;
    begin();
    stop();
    apply({ paused: true });
  }, [apply, begin, stop]);

  const resume = useCallback(() => {
    const v = viewRef.current;
    if (!v.paused) return;
    begin();
    if (saidRef.current) {
      // Paused in the gap after the sentence: straight on to the next beat.
      apply({ paused: false });
      carryOn(false);
    } else if (v.stage === 'reply') {
      apply({ paused: false });
      sayReply(replyRef.current);
    } else {
      // Say the sentence again; its board work is already up.
      enterRef.current(v.index, false, false);
    }
  }, [apply, begin, carryOn, sayReply]);

  // The child looks away (another tab, another app, the screen locked): the
  // lesson waits, voice included, and is there paused when they come back.
  useEffect(() => {
    if (typeof document === 'undefined') return undefined;
    const onVisibility = () => {
      if (document.hidden) pause();
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => document.removeEventListener('visibilitychange', onVisibility);
  }, [pause]);

  const togglePause = useCallback(() => {
    if (viewRef.current.paused) resume();
    else pause();
  }, [pause, resume]);

  const replay = useCallback(() => {
    if (viewRef.current.stage === 'ready') return;
    enterRef.current(viewRef.current.index, true, true);
  }, []);

  const back = useCallback(() => {
    if (viewRef.current.stage === 'ready') return;
    enterRef.current(Math.max(0, viewRef.current.index - 1), true, true);
  }, []);

  const skipToEnd = useCallback(() => {
    const all = beatsRef.current;
    if (all.length === 0 || viewRef.current.stage === 'ready') return;
    begin();
    stop();
    const last = all.length - 1;
    apply({
      index: last,
      stage: 'done',
      caption: all[last].say,
      paused: false,
      animate: false,
      picked: null,
      boardRun: viewRef.current.boardRun + 1,
    });
  }, [apply, begin, stop]);

  const forward = useCallback(() => {
    const v = viewRef.current;
    if (v.stage === 'ready' || v.stage === 'done') return;
    if (v.index >= beatsRef.current.length - 1) {
      skipToEnd();
      return;
    }
    enterRef.current(v.index + 1, true, false);
  }, [skipToEnd]);

  const restart = useCallback(() => {
    if (beatsRef.current.length === 0) return;
    enterRef.current(0, true, true);
  }, []);

  const toggleMute = useCallback(() => {
    const next = !mutedRef.current;
    mutedRef.current = next;
    setMuted(next);
    setVoiceLost(false);
    voiceMissesRef.current = 0;
    if (!next) return;
    // Voice off part-way through a sentence: the caption stays for the time that was left.
    stop();
    const cur = currentRef.current;
    const v = viewRef.current;
    if (cur && !v.paused && !saidRef.current && (v.stage === 'saying' || v.stage === 'reply')) {
      later(cur.done, Math.max(600, cur.ms - (Date.now() - cur.startedAt)));
    }
  }, [later, stop]);

  const toggleSlow = useCallback(() => {
    const next = !slowRef.current;
    slowRef.current = next;
    setSlow(next);
  }, []);

  // ── Start, and stop for good ────────────────────────────────────────────────

  // A lesson arrives: begin at the first beat. A different lesson, or the
  // player going away: everything stops, the voice included.
  useEffect(() => {
    apply({ ...INITIAL, boardRun: viewRef.current.boardRun });
    saidRef.current = false;
    if (beats.length === 0) return;

    let waiting = true;
    const go = () => {
      if (!waiting) return;
      waiting = false;
      enterRef.current(0, true, true);
    };
    // Have the first sentence's audio in hand (briefly), so voice and board start together.
    const giveUp = setTimeout(go, 3000);
    prepare(beats[0].say).then(go);

    return () => {
      waiting = false;
      clearTimeout(giveUp);
      begin();
      stop();
    };
  }, [apply, beats, begin, prepare, stop]);

  // ── The board for the beat on screen ────────────────────────────────────────

  // starts[i] is how many ops come before beat i; the last entry is the total.
  const starts = useMemo(() => {
    const out: number[] = [];
    let n = 0;
    for (let i = 0; i < beats.length; i++) {
      out.push(n);
      const board = beats[i].board;
      n += board ? board.length : 0;
    }
    out.push(n);
    return out;
  }, [beats]);

  const allOps = useMemo(() => {
    let out: BoardOp[] = [];
    for (let i = 0; i < beats.length; i++) {
      const board = beats[i].board;
      if (board) out = out.concat(board);
    }
    return out;
  }, [beats]);

  const showing = view.stage !== 'ready' && view.index < beats.length;
  const opsEnd = showing ? starts[view.index + 1] : 0;
  const opsStart = showing ? starts[view.index] : 0;
  // Everything done on the board up to and including this beat. Going back a
  // beat simply recomputes this from the start, so the board goes back too.
  const ops = useMemo(() => allOps.slice(0, opsEnd), [allOps, opsEnd]);
  const animateFrom = view.animate ? opsStart : opsEnd;

  return {
    view,
    muted,
    slow,
    voiceLost,
    total: beats.length,
    ops,
    animateFrom,
    choose,
    moveOn,
    togglePause,
    replay,
    back,
    forward,
    skipToEnd,
    restart,
    toggleMute,
    toggleSlow,
  };
}

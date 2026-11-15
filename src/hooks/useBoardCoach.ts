'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * The live board coach, seen from the pencil pad.
 *
 * Watches for a pause in the child's writing, sends a small picture of the pad
 * to `/api/coach/board`, and hands back what the tutor said. It decides only
 * WHEN to ask; what is said, and every rule about it, is the server's.
 *
 * The pad tells the hook what is happening through `penDown`, `penUp`,
 * `askNow` and `reset`.
 */

export type BoardCoachStatus = 'blank' | 'unclear' | 'on_track' | 'slip' | 'stuck' | 'complete';

export interface BoardCoachRemark {
  text: string;
  status: BoardCoachStatus;
  /** Goes up by one with every new remark, so the same words twice still count as new. */
  seq: number;
}

interface UseBoardCoachOptions {
  questionId: string;
  /** A base64 JPEG of the pad (no data-URL prefix), or null when nothing is written. */
  getImage: () => string | null;
  /** False switches the coach off: nothing is sent. */
  enabled: boolean;
}

export interface BoardCoach {
  /** The latest remark on this question, or null. */
  remark: BoardCoachRemark | null;
  /** True while the tutor is looking at the pad. */
  thinking: boolean;
  /** False once the server has said the coach is not on offer (for the rest of this visit). */
  available: boolean;
  /** How many more looks this question allows. */
  looksLeft: number;
  /** True once a picture of the pad has been sent at least once. */
  hasSent: boolean;
  /** The child has started a stroke. */
  penDown: () => void;
  /** The child has finished a stroke. */
  penUp: () => void;
  /** "Check my working": ask straight away (the limits still apply). */
  askNow: () => void;
  /** The pad was cleared: forget what was said about this question. */
  reset: () => void;
}

/** How long the child must have stopped writing before the tutor looks. */
export const COACH_PAUSE_MS = 4000;
/** The shortest time between two looks. */
export const COACH_MIN_GAP_MS = 12000;
/** The most looks one question gets. */
export const COACH_MAX_PER_QUESTION = 6;
/** Give up on a look that takes longer than this. */
const REQUEST_TIMEOUT_MS = 15000;

const STATUSES: BoardCoachStatus[] = ['blank', 'unclear', 'on_track', 'slip', 'stuck', 'complete'];

// Set when the server answers 503 (switched off, or no key). It is the same
// answer for every question, so no pad asks again until the page is reloaded.
let notConfigured = false;

function readReply(data: unknown): { status: BoardCoachStatus; say: string; quiet: boolean } | null {
  if (!data || typeof data !== 'object') return null;
  const o = data as Record<string, unknown>;
  if (typeof o.status !== 'string' || STATUSES.indexOf(o.status as BoardCoachStatus) === -1) return null;
  const say = typeof o.say === 'string' ? o.say.trim() : '';
  return { status: o.status as BoardCoachStatus, say, quiet: o.quiet !== false || !say };
}

export function useBoardCoach({ questionId, getImage, enabled }: UseBoardCoachOptions): BoardCoach {
  const [remark, setRemark] = useState<BoardCoachRemark | null>(null);
  const [thinking, setThinking] = useState(false);
  const [available, setAvailable] = useState(!notConfigured);
  const [looksLeft, setLooksLeft] = useState(COACH_MAX_PER_QUESTION);
  const [hasSent, setHasSent] = useState(false);

  // The latest props, for callbacks that outlive a render.
  const questionIdRef = useRef(questionId);
  const getImageRef = useRef(getImage);
  const enabledRef = useRef(enabled);
  questionIdRef.current = questionId;
  getImageRef.current = getImage;
  enabledRef.current = enabled;

  const timerRef = useRef<number | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const attemptRef = useRef<(manual: boolean) => void>(() => undefined);
  /** New strokes since the last look. */
  const dirtyRef = useRef(false);
  const penIsDownRef = useRef(false);
  const inFlightRef = useRef(false);
  /** "Check my working" was pressed and is waiting for the gap to pass. */
  const manualRef = useRef(false);
  /** The server refused (403: a test is in progress). Stop for this visit. */
  const refusedRef = useRef(false);
  const lastAskAtRef = useRef(0);
  const countRef = useRef(0);
  const spokenRef = useRef(0);
  const lastSayRef = useRef('');
  const seqRef = useRef(0);
  /** Bumped on every reset, so a reply about the old pad is ignored. */
  const generationRef = useRef(0);

  const clearTimer = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const schedule = useCallback((ms: number) => {
    clearTimer();
    timerRef.current = window.setTimeout(() => {
      timerRef.current = null;
      attemptRef.current(manualRef.current);
    }, ms);
  }, [clearTimer]);

  const attempt = useCallback((manual: boolean) => {
    if (!enabledRef.current || notConfigured || refusedRef.current) return;
    // Never two looks at once. Strokes made meanwhile are picked up afterwards.
    if (inFlightRef.current) return;
    if (countRef.current >= COACH_MAX_PER_QUESTION) {
      manualRef.current = false;
      setThinking(false);
      return;
    }
    if (!manual && !dirtyRef.current) return;

    // Too soon after the last look: wait out the rest of the gap.
    const wait = COACH_MIN_GAP_MS - (Date.now() - lastAskAtRef.current);
    if (wait > 0) {
      if (manual) {
        manualRef.current = true;
        setThinking(true);
      }
      schedule(wait);
      return;
    }

    const image = getImageRef.current();
    manualRef.current = false;
    if (!image) {
      setThinking(false);
      return;
    }

    dirtyRef.current = false;
    inFlightRef.current = true;
    countRef.current += 1;
    lastAskAtRef.current = Date.now();
    setLooksLeft(COACH_MAX_PER_QUESTION - countRef.current);
    setThinking(true);
    setHasSent(true);

    const generation = generationRef.current;
    const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    abortRef.current = controller;
    const timeout = window.setTimeout(() => {
      if (controller) controller.abort();
    }, REQUEST_TIMEOUT_MS);

    const done = () => {
      window.clearTimeout(timeout);
      inFlightRef.current = false;
      if (abortRef.current === controller) abortRef.current = null;
      setThinking(false);
      // The child wrote more while the tutor was looking: look again after a pause.
      if (dirtyRef.current && !penIsDownRef.current && timerRef.current === null) schedule(COACH_PAUSE_MS);
    };

    fetch('/api/coach/board', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        questionId: questionIdRef.current,
        image,
        spoken: spokenRef.current,
        lastSay: lastSayRef.current,
        asked: manual,
      }),
      signal: controller ? controller.signal : undefined,
    })
      .then((res) => {
        if (res.status === 503) {
          notConfigured = true;
          setAvailable(false);
          return null;
        }
        if (res.status === 403) {
          refusedRef.current = true;
          setAvailable(false);
          return null;
        }
        if (!res.ok) return null;
        return res.json();
      })
      .then((data: unknown) => {
        if (generation !== generationRef.current) return;
        const reply = readReply(data);
        if (!reply || reply.quiet || !reply.say) return;
        spokenRef.current += 1;
        lastSayRef.current = reply.say;
        seqRef.current += 1;
        setRemark({ text: reply.say, status: reply.status, seq: seqRef.current });
      })
      .catch(() => {
        // A look that did not come back (offline, timed out, or the pad was
        // cleared meanwhile) is simply a quiet tutor. Nothing to show a child.
      })
      .then(done);
  }, [schedule]);

  useEffect(() => {
    attemptRef.current = attempt;
  }, [attempt]);

  /** Forget everything said so far and drop any look that is under way. */
  const reset = useCallback(() => {
    generationRef.current += 1;
    clearTimer();
    if (abortRef.current) abortRef.current.abort();
    dirtyRef.current = false;
    manualRef.current = false;
    spokenRef.current = 0;
    lastSayRef.current = '';
    setRemark(null);
    setThinking(false);
  }, [clearTimer]);

  // A new question: a clean memory and a fresh allowance of looks.
  useEffect(() => {
    reset();
    countRef.current = 0;
    setLooksLeft(COACH_MAX_PER_QUESTION);
  }, [questionId, reset]);

  // Switched off: stop waiting and stop looking.
  useEffect(() => {
    if (enabled) return;
    clearTimer();
    if (abortRef.current) abortRef.current.abort();
    manualRef.current = false;
    setThinking(false);
  }, [enabled, clearTimer]);

  // Leaving the page: nothing left running.
  useEffect(() => {
    return () => {
      clearTimer();
      if (abortRef.current) abortRef.current.abort();
    };
  }, [clearTimer]);

  const penDown = useCallback(() => {
    penIsDownRef.current = true;
    // Still writing, so not a pause. (A pressed "Check my working" keeps its turn.)
    if (!manualRef.current) clearTimer();
  }, [clearTimer]);

  const penUp = useCallback(() => {
    penIsDownRef.current = false;
    dirtyRef.current = true;
    if (!enabledRef.current || notConfigured || refusedRef.current) return;
    if (manualRef.current) return;
    schedule(COACH_PAUSE_MS);
  }, [schedule]);

  const askNow = useCallback(() => {
    clearTimer();
    attempt(true);
  }, [attempt, clearTimer]);

  return { remark, thinking, available, looksLeft, hasSent, penDown, penUp, askNow, reset };
}

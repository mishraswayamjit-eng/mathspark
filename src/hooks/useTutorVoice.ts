'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';
import { lineSaysName, tutorLineWith, type TutorContext, type TutorEvent } from '@/lib/tutor/reactions';

export interface TutorVoice {
  /** React to something the child did: picks a line and says it (when the voice is on). Returns the line. */
  react: (event: TutorEvent, ctx: TutorContext) => string;
  /** Say any line as the tutor. */
  say: (text: string) => void;
  stop: () => void;
  /** True while the tutor is talking. */
  speaking: boolean;
  /** Whether the tutor talks at all. Remembered on the device. */
  enabled: boolean;
  setEnabled: (on: boolean) => void;
  /** The last line the tutor said, for showing as a caption. */
  lastLine: string;
}

const STORAGE_KEY = 'mathspark_tutor_voice';
/** A reaction waits this long, so it does not land on the tap sound or the screen change. */
const REACTION_GAP_MS = 400;
/** How many recent lines are remembered, so the tutor does not repeat itself. */
const RECENT_LINES = 24;

/** A reaction to an answer (and anything said with `say`) may replace whatever is being said. */
const ANSWER_WEIGHT = 5;
const SILENT = -1;

/** How much a line matters. A line only replaces one that matters less. */
function weightOf(kind: TutorEvent['kind']): number {
  switch (kind) {
    case 'correct':
    case 'miss':
    case 'sessionEnd':
      return ANSWER_WEIGHT;
    case 'hint':
      return 3;
    case 'question':
      return 2;
    case 'startedWorking':
      return 1;
    default:
      return 0; // an idle nudge never interrupts anything
  }
}

interface Talking {
  weight: number;
  /** A backstop: after this moment the line is taken to be over, whatever else happened. */
  until: number;
}

interface Waiting {
  timer: number;
  weight: number;
}

function weightNow(talking: Talking | null): number {
  return talking && Date.now() < talking.until ? talking.weight : SILENT;
}

/**
 * Whether the device's own voice is busy. Only called when the tutor itself is
 * silent, so a busy voice then belongs to another reader on the page. A reader
 * playing a recording or the server voice cannot be seen from here.
 */
function deviceVoiceBusy(): boolean {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return false;
  return window.speechSynthesis.speaking || window.speechSynthesis.pending;
}

/**
 * The tutor's voice for a screen.
 *
 * One line at a time. A reaction waits a moment before it is spoken and is
 * dropped if the next question has appeared by then. A new line replaces one
 * still being said only when it matters more; a reaction to an answer always
 * may, because it is about what the child has just done. A quiet event
 * changes nothing. With the voice off, lines are still returned and kept in
 * `lastLine` for the caption.
 */
export function useTutorVoice(): TutorVoice {
  const { speak, stop: stopReading, speaking } = useReadAloud();
  const [enabled, setEnabledState] = useState(true);
  const [lastLine, setLastLine] = useState('');

  const enabledRef = useRef(true);
  const mountedRef = useRef(false);
  const talkingRef = useRef<Talking | null>(null);
  const waitingRef = useRef<Waiting | null>(null);
  const recentRef = useRef<string[]>([]);
  const lastAnswerRef = useRef<'correct' | 'miss' | null>(null);

  const cancelWaiting = useCallback(() => {
    if (waitingRef.current) {
      window.clearTimeout(waitingRef.current.timer);
      waitingRef.current = null;
    }
  }, []);

  // Read the saved choice after mount, so server rendering is unaffected.
  useEffect(() => {
    mountedRef.current = true;
    try {
      if (window.localStorage.getItem(STORAGE_KEY) === 'off') {
        enabledRef.current = false;
        setEnabledState(false);
      }
    } catch {
      // Storage is blocked (private mode): the voice stays on, the default.
    }
    return () => {
      mountedRef.current = false;
      cancelWaiting();
    };
  }, [cancelWaiting]);

  // When the sound stops for any reason (finished, could not play, another
  // reader took over), the tutor is no longer talking.
  useEffect(() => {
    if (!speaking) talkingRef.current = null;
  }, [speaking]);

  // `personal` lines are made for this child alone and never stored for others:
  // a stock reaction is the same for every child and is stored once, but a
  // line with the child's name in it, or one written for them just now, is not.
  const speakNow = useCallback((text: string, weight: number, personal: boolean) => {
    talkingRef.current = { weight, until: Date.now() + 4000 + text.length * 120 };
    speak(text, {
      personal,
      onEnd: () => {
        talkingRef.current = null;
      },
    });
  }, [speak]);

  const remember = useCallback((line: string) => {
    const recent = recentRef.current;
    recent.push(line);
    if (recent.length > RECENT_LINES) recent.shift();
    setLastLine(line);
  }, []);

  const say = useCallback((text: string) => {
    if (!text) return;
    setLastLine(text);
    if (!enabledRef.current) return;
    cancelWaiting();
    // Whatever a screen asks the tutor to say may have been written for this
    // child (the board coach's remark is), so it is always treated as personal.
    speakNow(text, ANSWER_WEIGHT, true);
  }, [cancelWaiting, speakNow]);

  const react = useCallback((event: TutorEvent, ctx: TutorContext): string => {
    if (event.kind === 'question') {
      // The screen has moved on: a reaction still waiting belongs to the last question.
      cancelWaiting();
      if (event.first) {
        recentRef.current = [];
        lastAnswerRef.current = null;
      }
    }

    const line = tutorLineWith(event, ctx, {
      afterMiss: lastAnswerRef.current === 'miss',
      recent: recentRef.current,
    });
    if (event.kind === 'correct' || event.kind === 'miss') lastAnswerRef.current = event.kind;

    // Staying quiet changes nothing: the caption and any line being said carry on.
    if (!line) return '';

    const weight = weightOf(event.kind);
    if (!enabledRef.current) {
      remember(line);
      return line;
    }

    // Never talk over a line that matters at least as much (answers excepted).
    const waiting = waitingRef.current ? waitingRef.current.weight : SILENT;
    const busy = Math.max(weightNow(talkingRef.current), waiting);
    if (busy > SILENT && weight <= busy && weight < ANSWER_WEIGHT) return '';

    remember(line);
    cancelWaiting();
    const personal = lineSaysName(line, ctx.name);
    const timer = window.setTimeout(() => {
      waitingRef.current = null;
      if (!mountedRef.current || !enabledRef.current) return;
      const current = weightNow(talkingRef.current);
      if (current > SILENT) {
        if (weight <= current && weight < ANSWER_WEIGHT) return;
      } else if (deviceVoiceBusy()) {
        // Another reader on the page is speaking: leave the line as a caption only.
        return;
      }
      speakNow(line, weight, personal);
    }, REACTION_GAP_MS);
    waitingRef.current = { timer, weight };
    return line;
  }, [cancelWaiting, remember, speakNow]);

  const stop = useCallback(() => {
    cancelWaiting();
    talkingRef.current = null;
    stopReading();
  }, [cancelWaiting, stopReading]);

  const setEnabled = useCallback((on: boolean) => {
    enabledRef.current = on;
    setEnabledState(on);
    try {
      window.localStorage.setItem(STORAGE_KEY, on ? 'on' : 'off');
    } catch {
      // Storage is blocked: the choice lasts for this visit only.
    }
    if (!on) {
      cancelWaiting();
      talkingRef.current = null;
      stopReading();
    }
  }, [cancelWaiting, stopReading]);

  return { react, say, stop, speaking, enabled, setEnabled, lastLine };
}

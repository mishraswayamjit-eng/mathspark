'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Read-aloud for verified content.
 *
 * Plays a pre-recorded narration file when one is configured, otherwise speaks
 * with the browser's built-in voice (no network call, nothing recorded, no
 * data leaves the device). The caller passes text that has already been made
 * speakable by `@/lib/speech/mathToSpeech`.
 *
 * Only one thing is ever read at a time across the whole page: starting a new
 * reading stops whichever instance was reading before.
 */

interface SpeakOptions {
  /** Pre-recorded audio to try first; falls back to the browser voice if it cannot play. */
  audioSrc?: string;
  /** Called once sound has actually started. */
  onStart?: () => void;
  /** Called when playback finishes naturally (not when it is stopped or interrupted). */
  onEnd?: () => void;
}

/**
 * URL of the pre-recorded narration for one part of a question, or undefined
 * when no narration library is configured (NEXT_PUBLIC_NARRATION_AUDIO_BASE unset).
 * Layout: `<base>/<questionId>/<part>.<ext>`, part = "question" or "step-N"
 * (written by scripts/generate_narration.py). The extension defaults to mp3
 * and can be changed with NEXT_PUBLIC_NARRATION_AUDIO_EXT.
 */
export function narrationAudioSrc(questionId: string, part: string): string | undefined {
  const base = process.env.NEXT_PUBLIC_NARRATION_AUDIO_BASE;
  if (!base) return undefined;
  const ext = process.env.NEXT_PUBLIC_NARRATION_AUDIO_EXT || 'mp3';
  return `${base.replace(/\/+$/, '')}/${encodeURIComponent(questionId)}/${part}.${ext}`;
}

// The stop() of whichever hook instance is currently reading, if any.
let stopActiveReader: (() => void) | null = null;

function pickVoice(): SpeechSynthesisVoice | null {
  const voices = window.speechSynthesis.getVoices();
  const prefer = ['en-IN', 'en_IN', 'en-GB', 'en_GB', 'en-US', 'en_US'];
  for (let p = 0; p < prefer.length; p++) {
    for (let i = 0; i < voices.length; i++) {
      if (voices[i].lang === prefer[p]) return voices[i];
    }
  }
  for (let i = 0; i < voices.length; i++) {
    if (voices[i].lang.toLowerCase().indexOf('en') === 0) return voices[i];
  }
  return null;
}

export function useReadAloud() {
  const [speaking,  setSpeaking]  = useState(false);
  const [supported, setSupported] = useState(false);

  // Bumped on every speak()/stop(); a playback whose id is stale must not report back.
  const playIdRef = useRef(0);
  const audioRef  = useRef<HTMLAudioElement | null>(null);
  // True only while THIS instance owns the sound, so stopping an idle button
  // never cancels another button's (or the walkthrough's) reading.
  const activeRef = useRef(false);

  useEffect(() => {
    const ok = typeof window !== 'undefined' && 'speechSynthesis' in window;
    setSupported(ok);
    // Some browsers load voices lazily; asking once warms the list.
    if (ok) window.speechSynthesis.getVoices();
  }, []);

  const halt = useCallback(() => {
    playIdRef.current += 1;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    if (activeRef.current && typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    activeRef.current = false;
  }, []);

  const stop = useCallback(() => {
    halt();
    setSpeaking(false);
  }, [halt]);

  const speak = useCallback((text: string, opts?: SpeakOptions) => {
    // Silence whoever was reading (another button, or this one's previous reading).
    if (stopActiveReader && stopActiveReader !== stop) stopActiveReader();
    halt();
    stopActiveReader = stop;
    activeRef.current = true;

    const myId = playIdRef.current;
    const isCurrent = () => playIdRef.current === myId;
    const started = () => {
      if (isCurrent() && opts && opts.onStart) opts.onStart();
    };
    const finish = (natural: boolean) => {
      if (!isCurrent()) return;
      activeRef.current = false;
      setSpeaking(false);
      if (natural && opts && opts.onEnd) opts.onEnd();
    };

    const speakWithBrowserVoice = () => {
      if (typeof window === 'undefined' || !('speechSynthesis' in window) || !text) {
        finish(false);
        return;
      }
      const utter = new SpeechSynthesisUtterance(text);
      const voice = pickVoice();
      if (voice) utter.voice = voice;
      utter.lang  = voice ? voice.lang : 'en-IN';
      utter.rate  = 0.92;
      utter.onstart = started;
      utter.onend   = () => finish(true);
      utter.onerror = () => finish(false);
      window.speechSynthesis.speak(utter);
    };

    setSpeaking(true);

    if (opts && opts.audioSrc) {
      const audio = new Audio(opts.audioSrc);
      audioRef.current = audio;
      // A missing recording fires both `error` and a rejected play(): fall back once only.
      let fellBack = false;
      const fallBack = () => {
        if (fellBack || !isCurrent()) return;
        fellBack = true;
        audioRef.current = null;
        speakWithBrowserVoice();
      };
      audio.onplaying = started;
      audio.onended   = () => finish(true);
      audio.onerror   = fallBack;
      audio.play().catch(fallBack);
      return;
    }

    speakWithBrowserVoice();
  }, [halt, stop]);

  // Never keep talking after the component that started it has gone.
  useEffect(() => {
    return () => {
      halt();
      if (stopActiveReader === stop) stopActiveReader = null;
    };
  }, [halt, stop]);

  return { speak, stop, speaking, supported };
}

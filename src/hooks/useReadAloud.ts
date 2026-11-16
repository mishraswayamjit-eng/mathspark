'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { fetchServerVoice, serverVoiceMayBeAvailable } from '@/lib/speech/serverVoice';
import { getVoicePrefs } from '@/lib/speech/voicePrefs';
import { voiceProfileOrDefault, voiceSpeedOrDefault, type VoiceGender } from '@/lib/speech/voices';

/**
 * Read-aloud for verified content.
 *
 * Plays a pre-recorded narration file when one is configured; otherwise the
 * server voice (Sarvam) when the server has a key for it, which sends the text
 * to Sarvam; otherwise the browser's built-in voice, where nothing leaves the
 * device. The caller passes text that has already been made
 * speakable by `@/lib/speech/mathToSpeech`.
 *
 * The server voice speaks in the profile and at the speed the child chose
 * (`@/lib/speech/voicePrefs`). A pre-recorded file is played as recorded.
 *
 * Only one thing is ever read at a time across the whole page: starting a new
 * reading stops whichever instance was reading before.
 */

interface SpeakOptions {
  /** Pre-recorded audio to try first; falls back to the browser voice if it cannot play. */
  audioSrc?: string;
  /**
   * The text is about this child (their name is in it, or it was written for
   * them just now), so its audio must not be stored where others could fetch it.
   */
  personal?: boolean;
  /** Speak in this voice profile instead of the child's chosen one (the "Listen" buttons). */
  voiceId?: string;
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

// Browsers do not say whether a device voice is male or female. Some put it in
// the name ("Google UK English Male"), and the common system voices have
// well-known first names. This is a best guess from those names and nothing
// more: a voice we cannot place is treated as unknown, and when no voice of
// the wanted kind is found the choice is made exactly as it was before.
const FEMALE_VOICE_NAMES = [
  'female', 'woman', 'heera', 'neerja', 'veena', 'lekha', 'zira', 'hazel', 'susan', 'libby', 'sonia', 'aria',
  'jenny', 'samantha', 'karen', 'moira', 'tessa', 'fiona', 'victoria', 'serena', 'kate', 'allison', 'ava',
];
const MALE_VOICE_NAMES = [
  'male', 'man', 'ravi', 'prabhat', 'rishi', 'david', 'mark', 'george', 'ryan', 'guy', 'daniel', 'oliver',
  'alex', 'fred', 'tom', 'thomas', 'arthur', 'aaron', 'gordon',
];

function nameHasWord(name: string, words: string[]): boolean {
  const parts = name.toLowerCase().split(/[^a-z]+/);
  for (let i = 0; i < parts.length; i++) {
    if (parts[i] && words.indexOf(parts[i]) !== -1) return true;
  }
  return false;
}

function voiceGender(voice: SpeechSynthesisVoice): VoiceGender | null {
  const name = voice.name || '';
  if (nameHasWord(name, FEMALE_VOICE_NAMES)) return 'female';
  if (nameHasWord(name, MALE_VOICE_NAMES)) return 'male';
  return null;
}

/**
 * The device voice to fall back on. `gender` is that of the profile the child
 * chose: a fallback that sounds like a different person is jarring, so a
 * device voice that appears (by its name) to match is preferred.
 */
function pickVoice(gender?: VoiceGender): SpeechSynthesisVoice | null {
  const voices = window.speechSynthesis.getVoices();
  const prefer = ['en-IN', 'en_IN', 'en-GB', 'en_GB', 'en-US', 'en_US'];
  if (gender) {
    for (let p = 0; p < prefer.length; p++) {
      for (let i = 0; i < voices.length; i++) {
        if (voices[i].lang === prefer[p] && voiceGender(voices[i]) === gender) return voices[i];
      }
    }
  }
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
      const prefs = getVoicePrefs();
      const profile = voiceProfileOrDefault((opts && opts.voiceId) || prefs.voiceId);
      const voice = pickVoice(profile.gender);
      if (voice) utter.voice = voice;
      utter.lang  = voice ? voice.lang : 'en-IN';
      // 0.92 at the "Normal" speed, as before; Calm and Quick move it a little.
      utter.rate  = 0.92 * voiceSpeedOrDefault(prefs.speedId).multiplier;
      utter.onstart = started;
      utter.onend   = () => finish(true);
      utter.onerror = () => finish(false);
      window.speechSynthesis.speak(utter);
    };

    setSpeaking(true);

    const playAudio = (audio: HTMLAudioElement, src: string) => {
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
      audio.src = src;
      audio.play().catch(fallBack);
    };

    // 1. A pre-recorded narration file, when the caller has one.
    if (opts && opts.audioSrc) {
      playAudio(new Audio(), opts.audioSrc);
      return;
    }

    // 2. The server voice (Sarvam), when the server has a key for it.
    if (text && serverVoiceMayBeAvailable()) {
      // Made now, inside the tap, so the browser is more willing to play it when the sound arrives.
      const audio = new Audio();
      audioRef.current = audio;
      fetchServerVoice(text, {
        personal: Boolean(opts && opts.personal),
        voiceId: opts ? opts.voiceId : undefined,
      }).then((src) => {
        if (!isCurrent()) return;
        if (src) {
          playAudio(audio, src);
        } else {
          audioRef.current = null;
          speakWithBrowserVoice();
        }
      });
      return;
    }

    // 3. The device's own voice.
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

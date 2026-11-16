/**
 * The child's choice of Sparky's voice and speaking speed.
 *
 * Kept on the device (localStorage), like the other `mathspark_` settings, so
 * it is cleared when the child logs out. Safe to import on the server: there
 * every function answers with the defaults and does nothing else.
 */

import { voiceProfileOrDefault, voiceSpeedOrDefault } from '@/lib/speech/voices';

export interface VoicePrefs {
  /** A profile id from `voices.ts`. Always a valid one. */
  voiceId: string;
  /** A speed id from `voices.ts`. Always a valid one. */
  speedId: string;
}

const VOICE_KEY = 'mathspark_voice_profile';
const SPEED_KEY = 'mathspark_voice_speed';

type Listener = (prefs: VoicePrefs) => void;
const listeners: Listener[] = [];
let listeningToStorage = false;

// Used only when the browser refuses to store anything (private mode): the
// choice then lasts for this visit.
const unsaved: { voiceId?: string; speedId?: string } = {};

function readItem(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function getVoicePrefs(): VoicePrefs {
  if (typeof window === 'undefined') {
    return { voiceId: voiceProfileOrDefault(null).id, speedId: voiceSpeedOrDefault(null).id };
  }
  return {
    voiceId: voiceProfileOrDefault(readItem(VOICE_KEY) || unsaved.voiceId).id,
    speedId: voiceSpeedOrDefault(readItem(SPEED_KEY) || unsaved.speedId).id,
  };
}

function notify(): void {
  const prefs = getVoicePrefs();
  const current = listeners.slice();
  for (let i = 0; i < current.length; i++) current[i](prefs);
}

/** Save a new choice and tell every open screen on this page. Unknown ids are ignored. */
export function setVoicePrefs(patch: { voiceId?: string; speedId?: string }): void {
  if (typeof window === 'undefined') return;
  const before = getVoicePrefs();
  const voiceId = patch.voiceId !== undefined ? voiceProfileOrDefault(patch.voiceId).id : before.voiceId;
  const speedId = patch.speedId !== undefined ? voiceSpeedOrDefault(patch.speedId).id : before.speedId;
  try {
    window.localStorage.setItem(VOICE_KEY, voiceId);
    window.localStorage.setItem(SPEED_KEY, speedId);
    delete unsaved.voiceId;
    delete unsaved.speedId;
  } catch {
    unsaved.voiceId = voiceId;
    unsaved.speedId = speedId;
  }
  notify();
}

/**
 * Be told when the choice changes, on this page or in another tab.
 * Returns the function that stops the telling.
 */
export function subscribeVoicePrefs(listener: Listener): () => void {
  if (typeof window === 'undefined') return () => undefined;
  listeners.push(listener);
  if (!listeningToStorage) {
    listeningToStorage = true;
    // Fires when another tab changes the choice (never for this tab's own writes).
    window.addEventListener('storage', (event: StorageEvent) => {
      if (event.key === null || event.key === VOICE_KEY || event.key === SPEED_KEY) notify();
    });
  }
  return () => {
    const at = listeners.indexOf(listener);
    if (at !== -1) listeners.splice(at, 1);
  };
}

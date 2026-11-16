/**
 * The server voice (Sarvam text-to-speech), for the browser.
 *
 * `fetchServerVoice(text)` resolves to an audio data URL in the voice and at
 * the speed the child has chosen, or null when the server voice cannot be used
 * for this text (not configured, signed out, too long, over a limit, offline).
 * Callers then fall back to the device's own voice.
 *
 * There are two ways to the audio:
 *
 *   GET  /api/voice/say   fixed lines (questions, hints, lessons, the tutor's
 *                         stock reactions). The answer is stored by Vercel's
 *                         CDN and by the browser, so a line is made once and
 *                         then served from storage to every child.
 *   POST /api/voice/tts   everything that must not be stored for everyone:
 *                         `{ personal: true }` lines (the child's name, live
 *                         coaching), and lines too long for an address.
 *
 * The stored line is fetched here with `fetch` and handed on as a data URL,
 * not given to the `Audio` element as an address. Two reasons: an audio
 * element asks for media with a `Range` header, and Vercel's documentation
 * lists "no Range header" among the conditions for its CDN to store an
 * answer, so a line played that way could be made afresh on every play; and
 * only `fetch` can see a 503, which is how this module learns there is no
 * server voice here.
 *
 * Sending text here sends it to Sarvam. That is why this is only reached when
 * SARVAM_API_KEY has been set on the server: until then both routes answer 503
 * and this module stops asking for the rest of the visit.
 */

import { normaliseSpeechText, sayUrl, voiceProfileOrDefault, voiceSpeedOrDefault } from '@/lib/speech/voices';
import { getVoicePrefs } from '@/lib/speech/voicePrefs';

export interface ServerVoiceOptions {
  /**
   * The text is about this child (it has their name in it, or it was written
   * for them just now). It is then never given a storable, shareable address.
   */
  personal?: boolean;
  /** Speak in this profile instead of the child's chosen one (the "Listen" buttons). */
  voiceId?: string;
  /** Speak at this speed instead of the child's chosen one. */
  speedId?: string;
}

// null: not yet known. false: the server has no voice configured, stop asking.
let available: boolean | null = null;

// A few recent readings, so tapping "read again" does not make a second request.
const CACHE_SIZE = 24;
const cacheKeys: string[] = [];
const cache: Record<string, string> = {};
// Readings being fetched now, so a prefetch and a play of the same line share one request.
const inFlight: Record<string, Promise<string | null>> = {};

// Sarvam takes about 2500 characters; leave the long ones to the device voice.
const MAX_CHARS = 2400;

export function serverVoiceMayBeAvailable(): boolean {
  return available !== false;
}

function remember(key: string, src: string): void {
  if (Object.prototype.hasOwnProperty.call(cache, key)) return;
  cache[key] = src;
  cacheKeys.push(key);
  if (cacheKeys.length > CACHE_SIZE) {
    const oldest = cacheKeys.shift();
    if (oldest !== undefined) delete cache[oldest];
  }
}

/** Audio bytes as a data URL, or null when the answer is not audio. */
function blobToDataUrl(blob: Blob): Promise<string | null> {
  return new Promise<string | null>((resolve) => {
    if (blob.size === 0 || blob.type.indexOf('audio/') !== 0 || typeof FileReader === 'undefined') {
      resolve(null);
      return;
    }
    const reader = new FileReader();
    reader.onload = () => resolve(typeof reader.result === 'string' ? reader.result : null);
    reader.onerror = () => resolve(null);
    reader.readAsDataURL(blob);
  });
}

async function load(text: string, voiceId: string, speedId: string, personal: boolean): Promise<string | null> {
  try {
    // 1. The stored line, when this text may have an address.
    const url = personal ? null : sayUrl(text, voiceId, speedId);
    if (url) {
      const res = await fetch(url);
      if (res.status === 503) {
        available = false;        // not configured on this deployment
        return null;
      }
      if (res.ok) {
        const stored = await blobToDataUrl(await res.blob());
        if (stored) available = true;
        return stored;
      }
      // Signed out, over a limit, or Sarvam is having trouble: POST would be turned down too.
      if (res.status === 401 || res.status === 429 || res.status === 502) return null;
      // Anything else (this copy of the app is older than the server, or the
      // address was refused): ask the older way below.
    }

    // 2. Made for this request only.
    const made = await fetch('/api/voice/tts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text, voice: voiceId, speed: speedId }),
    });
    if (made.status === 503 || made.status === 404) {
      available = false;          // not configured on this deployment
      return null;
    }
    if (!made.ok) return null;    // signed out, a limit, or a passing fault: try again next time
    const data = (await made.json()) as { audio?: string; mime?: string };
    if (!data.audio) return null;
    available = true;
    return `data:${data.mime || 'audio/mpeg'};base64,${data.audio}`;
  } catch {
    return null;                  // offline: the device voice still works
  }
}

export function fetchServerVoice(text: string, opts?: ServerVoiceOptions): Promise<string | null> {
  const clean = normaliseSpeechText(text);
  if (available === false || !clean || clean.length > MAX_CHARS) return Promise.resolve(null);

  const prefs = getVoicePrefs();
  const voiceId = voiceProfileOrDefault((opts && opts.voiceId) || prefs.voiceId).id;
  const speedId = voiceSpeedOrDefault((opts && opts.speedId) || prefs.speedId).id;
  const key = `${voiceId}|${speedId}|${clean}`;

  if (Object.prototype.hasOwnProperty.call(cache, key)) return Promise.resolve(cache[key]);
  if (Object.prototype.hasOwnProperty.call(inFlight, key)) return inFlight[key];

  const job = load(clean, voiceId, speedId, Boolean(opts && opts.personal)).then((src) => {
    delete inFlight[key];
    if (src) remember(key, src);
    return src;
  });
  inFlight[key] = job;
  return job;
}

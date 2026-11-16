/**
 * The voices a child can choose for Sparky, and the address of a spoken line.
 *
 * Safe to import from both the server and the browser: it holds no key, reads
 * no environment variable and touches no browser API.
 *
 * ── Changing a voice ─────────────────────────────────────────────────────────
 * Nobody who wrote this list could hear it, so the speakers are a first guess
 * and the owner should audition them on /dev/voice.
 *
 *   • To swap a speaker: change that profile's `speaker` (one line), then add 1
 *     to VOICE_CACHE_VERSION so stored audio made with the old speaker is not
 *     played again.
 *   • To change which voice a child gets before choosing: DEFAULT_VOICE_ID.
 *   • To change how fast a voice talks: its `pace` (Sarvam allows 0.5 to 2.0;
 *     1.0 is Sarvam's normal). Bump VOICE_CACHE_VERSION as well.
 *
 * ── A voice from another provider (the British-English slot) ─────────────────
 * Sarvam only has Indian-English voices. Each profile names its `provider` so
 * that one can be added later without touching the picker or the routes'
 * callers:
 *   1. add the provider's name to `VoiceProvider`;
 *   2. add a profile here, e.g.
 *        { id: 'british', label: 'British voice', blurb: '...', provider: 'newprovider',
 *          speaker: '<that provider's voice name>', pace: 1.1, temperature: 0.5, gender: 'female' }
 *   3. teach `src/lib/speech/sarvamServer.ts` (or a sibling module the two
 *      voice routes call) to send that provider's profiles to its API.
 * Until then no label here promises an accent.
 */

export type VoiceProvider = 'sarvam';

/** Used only to pick a similar-sounding device voice when the server voice cannot be used. */
export type VoiceGender = 'male' | 'female';

export interface VoiceProfile {
  /** Stored on the device and sent in requests. Never change an id once children have chosen it. */
  id: string;
  /** What the child sees. */
  label: string;
  /** One short line under the label. */
  blurb: string;
  provider: VoiceProvider;
  /** The provider's own name for the voice (for Sarvam: a bulbul:v3 speaker). */
  speaker: string;
  /** Speed at the "Normal" setting. */
  pace: number;
  /** Liveliness: lower is steadier, higher is more expressive. */
  temperature: number;
  gender: VoiceGender;
}

export const VOICE_PROFILES: VoiceProfile[] = [
  {
    id: 'teacher',
    label: 'Teacher voice',
    blurb: 'Clear and steady, like a teacher at the board.',
    provider: 'sarvam',
    speaker: 'aditya',
    pace: 1.1,
    temperature: 0.5,
    gender: 'male',
  },
  {
    id: 'warm',
    label: 'Warm voice',
    blurb: 'Gentle and friendly, like story time.',
    provider: 'sarvam',
    speaker: 'ishita',
    pace: 1.08,
    temperature: 0.7,
    gender: 'female',
  },
  {
    id: 'bright',
    label: 'Bright voice',
    blurb: 'Lively and cheerful, with lots of energy.',
    provider: 'sarvam',
    speaker: 'simran',
    pace: 1.12,
    temperature: 0.8,
    gender: 'female',
  },
];

export const DEFAULT_VOICE_ID = 'teacher';

export interface VoiceSpeed {
  id: string;
  label: string;
  /** Multiplies the profile's pace. */
  multiplier: number;
}

export const VOICE_SPEEDS: VoiceSpeed[] = [
  { id: 'calm', label: 'Calm', multiplier: 0.87 },
  { id: 'normal', label: 'Normal', multiplier: 1 },
  { id: 'quick', label: 'Quick', multiplier: 1.15 },
];

export const DEFAULT_SPEED_ID = 'normal';

/**
 * Part of every stored line's address. Add 1 to make every device and the CDN
 * fetch fresh audio (after changing a speaker, a pace, or the Sarvam settings
 * in the environment).
 */
export const VOICE_CACHE_VERSION = '1';

/** Lines longer than this are not given a storable address; they are fetched the older way (POST). */
export const SAY_MAX_CHARS = 600;
/** The longest address we will build, whatever the text encodes to. */
const SAY_MAX_URL = 2000;

/** The sentence the "Listen" buttons play. Fixed, so it is stored once per voice and speed. */
export const VOICE_SAMPLE_TEXT = 'Hello! I am Sparky. Let us work through some maths together, one step at a time.';

export function getVoiceProfile(id: string | null | undefined): VoiceProfile | null {
  if (!id) return null;
  for (let i = 0; i < VOICE_PROFILES.length; i++) {
    if (VOICE_PROFILES[i].id === id) return VOICE_PROFILES[i];
  }
  return null;
}

/** The profile with this id, or the default one when the id is missing or unknown. */
export function voiceProfileOrDefault(id: string | null | undefined): VoiceProfile {
  return getVoiceProfile(id) || getVoiceProfile(DEFAULT_VOICE_ID) || VOICE_PROFILES[0];
}

export function getVoiceSpeed(id: string | null | undefined): VoiceSpeed | null {
  if (!id) return null;
  for (let i = 0; i < VOICE_SPEEDS.length; i++) {
    if (VOICE_SPEEDS[i].id === id) return VOICE_SPEEDS[i];
  }
  return null;
}

/** The speed with this id, or "Normal" when the id is missing or unknown. */
export function voiceSpeedOrDefault(id: string | null | undefined): VoiceSpeed {
  return getVoiceSpeed(id) || getVoiceSpeed(DEFAULT_SPEED_ID) || VOICE_SPEEDS[0];
}

/**
 * The text exactly as it is sent and stored: runs of spaces, tabs and line
 * breaks become one space, and the ends are trimmed. Two readings of the same
 * line then share one address whatever the spacing was.
 */
export function normaliseSpeechText(text: string): string {
  return typeof text === 'string' ? text.replace(/\s+/g, ' ').trim() : '';
}

/**
 * The address of a spoken line: GET /api/voice/say?k=<version>&v=<voice>&s=<speed>&t=<text>.
 *
 * The parameters are always written in that order and the text is normalised,
 * so the same line in the same voice at the same speed is the same address for
 * every child. That is what lets the CDN and the browser keep the audio.
 *
 * null when the line cannot have an address (empty, or too long for a URL);
 * the caller then uses POST /api/voice/tts or the device voice.
 */
export function sayUrl(text: string, voiceId?: string | null, speedId?: string | null): string | null {
  const clean = normaliseSpeechText(text);
  if (!clean || clean.length > SAY_MAX_CHARS) return null;
  const voice = voiceProfileOrDefault(voiceId);
  const speed = voiceSpeedOrDefault(speedId);
  let encoded: string;
  try {
    encoded = encodeURIComponent(clean);
  } catch {
    return null; // half of a surrogate pair: not encodable
  }
  const url = `/api/voice/say?k=${VOICE_CACHE_VERSION}&v=${encodeURIComponent(voice.id)}&s=${encodeURIComponent(speed.id)}&t=${encoded}`;
  return url.length > SAY_MAX_URL ? null : url;
}

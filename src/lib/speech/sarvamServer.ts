/**
 * Talking to Sarvam text-to-speech. SERVER ONLY: it reads the API key's
 * neighbours in process.env and is imported by the two voice routes
 * (/api/voice/tts and /api/voice/say). Never import it from a component.
 */

import { logError } from '@/lib/logger';
import { DEFAULT_VOICE_ID, voiceProfileOrDefault, voiceSpeedOrDefault } from '@/lib/speech/voices';

export const SARVAM_URL = 'https://api.sarvam.ai/text-to-speech';
const TIMEOUT_MS = 15_000;

const MODELS = ['bulbul:v3', 'bulbul:v2', 'bulbul:v4-flash'];
const SAMPLE_RATES = [8000, 16000, 22050, 24000, 32000, 44100, 48000];
/** The model every voice profile's speaker belongs to. */
const PROFILE_MODEL = 'bulbul:v3';

/** A number from an env var or a request, kept inside the range Sarvam allows. */
function inRange(value: unknown, lo: number, hi: number, fallback: number): number {
  const n = typeof value === 'number' ? value : typeof value === 'string' && value.trim() !== '' ? Number(value) : NaN;
  if (!isFinite(n)) return fallback;
  return Math.min(hi, Math.max(lo, n));
}

/** Speaker names are lowercase words, sometimes with underscores (v4 personas). */
function speakerName(value: unknown): string | null {
  return typeof value === 'string' && /^[a-z][a-z0-9_]{1,40}$/.test(value) ? value : null;
}

export interface VoiceSettings {
  model: string;
  speaker: string;
  pace: number;
  temperature: number;
  pitch: number;
  loudness: number;
  sampleRate: number;
}

export interface VoiceRequest {
  /** A voice profile id from `voices.ts`. Missing or unknown: the default profile. */
  voice?: string | null;
  /** A speed id from `voices.ts`. Missing or unknown: "normal". */
  speed?: string | null;
  /** Raw overrides, for the voice test page only (POST /api/voice/tts). */
  model?: string;
  speaker?: string;
  pace?: number;
  temperature?: number;
}

/**
 * The exact settings sent to Sarvam for a request.
 *
 * Each voice profile in `src/lib/speech/voices.ts` fixes a speaker, a pace and
 * a temperature on bulbul:v3. On top of that:
 *
 * 1. Environment variables that override the DEFAULT profile only (the one
 *    named by DEFAULT_VOICE_ID). A child who has picked any other profile
 *    always hears that profile exactly as written in voices.ts:
 *
 *      SARVAM_TTS_MODEL        bulbul:v3 (default) | bulbul:v2 | bulbul:v4-flash
 *      SARVAM_TTS_SPEAKER      a speaker of that model (replaces the default profile's speaker)
 *      SARVAM_TTS_PACE         0.5 slow to 2.0 fast (replaces the default profile's pace;
 *                              the child's Calm/Normal/Quick choice still multiplies it)
 *      SARVAM_TTS_TEMPERATURE  v3/v4: 0.01 steady to 1.0 lively (replaces the default profile's)
 *
 *    Leave these four unset to hear the default profile as written. After
 *    changing any of them, add 1 to VOICE_CACHE_VERSION in voices.ts, because
 *    audio already stored for the default profile was made with the old values.
 *
 * 2. Environment variables that apply to every profile:
 *
 *      SARVAM_TTS_SAMPLE_RATE  audio quality in Hz (default 24000)
 *      SARVAM_TTS_DICT_ID      id of a Sarvam pronunciation dictionary (v3/v4)
 *      SARVAM_TTS_PITCH        v2 only: -0.75 to 0.75 (default 0)
 *      SARVAM_TTS_LOUDNESS     v2 only: 0.3 to 3.0 (default 1)
 *
 * 3. Raw `model`, `speaker`, `pace`, `temperature` in a POST to /api/voice/tts
 *    win over everything; the voice test page (/dev/voice) uses that to compare
 *    settings by ear. A raw `pace` is used as given: the speed choice is not
 *    applied to it. GET /api/voice/say never accepts raw values.
 */
export function voiceSettings(req: VoiceRequest): VoiceSettings {
  const env = process.env;
  const profile = voiceProfileOrDefault(req.voice);
  const speed = voiceSpeedOrDefault(req.speed);
  const isDefault = profile.id === DEFAULT_VOICE_ID;

  const envModel = isDefault ? env.SARVAM_TTS_MODEL || '' : '';
  const wantedModel = req.model || envModel;
  const model = MODELS.indexOf(wantedModel) !== -1 ? wantedModel : PROFILE_MODEL;
  // A speaker belongs to one model, so the env speaker only applies on the env model.
  const envSpeakerApplies = isDefault && (!req.model || req.model === (env.SARVAM_TTS_MODEL || PROFILE_MODEL));
  const fallbackSpeaker = model === 'bulbul:v2' ? 'anushka' : model === 'bulbul:v4-flash' ? 'shubh_enhi_ads' : profile.speaker;
  const speaker = speakerName(req.speaker) || (envSpeakerApplies ? speakerName(env.SARVAM_TTS_SPEAKER) : null) || fallbackSpeaker;

  const paceLo = model === 'bulbul:v2' ? 0.3 : 0.5;
  const paceHi = model === 'bulbul:v2' ? 3 : 2;
  let pace: number;
  if (req.pace !== undefined) {
    pace = inRange(req.pace, paceLo, paceHi, profile.pace);
  } else {
    const base = inRange(isDefault ? env.SARVAM_TTS_PACE : undefined, paceLo, paceHi, profile.pace);
    pace = inRange(base * speed.multiplier, paceLo, paceHi, profile.pace);
  }
  const temperature = inRange(
    req.temperature !== undefined ? req.temperature : isDefault ? env.SARVAM_TTS_TEMPERATURE : undefined,
    0.01,
    1,
    profile.temperature,
  );

  const rate = inRange(env.SARVAM_TTS_SAMPLE_RATE, 8000, 48000, 24000);
  return {
    model,
    speaker,
    pace: Math.round(pace * 100) / 100,
    temperature: Math.round(temperature * 100) / 100,
    pitch: inRange(env.SARVAM_TTS_PITCH, -0.75, 0.75, 0),
    loudness: inRange(env.SARVAM_TTS_LOUDNESS, 0.3, 3, 1),
    sampleRate: SAMPLE_RATES.indexOf(rate) !== -1 ? rate : 24000,
  };
}

export function sarvamBody(text: string, v: VoiceSettings, languageField: string): Record<string, unknown> {
  const body: Record<string, unknown> = {
    text,
    model: v.model,
    speaker: v.speaker,
    pace: v.pace,
    speech_sample_rate: v.sampleRate,
    output_audio_codec: 'mp3',
  };
  body[languageField] = 'en-IN';
  if (v.model === 'bulbul:v2') {
    // Pitch, loudness and the text clean-up switch exist on v2 only.
    body.pitch = v.pitch;
    body.loudness = v.loudness;
    body.enable_preprocessing = true;
  } else {
    body.temperature = v.temperature;
    if (process.env.SARVAM_TTS_DICT_ID) body.dict_id = process.env.SARVAM_TTS_DICT_ID;
  }
  return body;
}

export type SpeechResult =
  /** `audio` is base64. */
  | { ok: true; audio: string; mime: string }
  /** `detail` is Sarvam's own message when the key or a setting was turned down. */
  | { ok: false; detail?: string };

/**
 * Ask Sarvam to speak `text`. Never throws: a fault of any kind is logged
 * under `tag` and comes back as `{ ok: false }`.
 */
export async function requestSpeech(text: string, voice: VoiceSettings, apiKey: string, tag: string): Promise<SpeechResult> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const call = (languageField: string) => fetch(SARVAM_URL, {
    method: 'POST',
    headers: { 'api-subscription-key': apiKey, 'Content-Type': 'application/json' },
    body: JSON.stringify(sarvamBody(text, voice, languageField)),
    signal: controller.signal,
  });

  try {
    // Sarvam's current reference names the language field `language_code`;
    // older versions of the API called it `target_language_code`. Try the
    // current name, and the older one only if the request is rejected as invalid.
    let res = await call('language_code');
    if (res.status === 400 || res.status === 422) {
      const firstDetail = (await res.text()).slice(0, 300);
      res = await call('target_language_code');
      if (!res.ok) logError(`[${tag}] Sarvam rejected the request: ${firstDetail}`);
    }

    if (!res.ok) {
      const detail = (await res.text()).slice(0, 300);
      logError(`[${tag}] Sarvam returned ${res.status}: ${detail}`);
      // A rejected key or setting is a configuration problem, not a passing fault.
      const configProblem = res.status === 400 || res.status === 401 || res.status === 403 || res.status === 422;
      return { ok: false, detail: configProblem ? detail : undefined };
    }

    const data: unknown = await res.json();
    const audios = (data as { audios?: unknown }).audios;
    const audio = Array.isArray(audios) && typeof audios[0] === 'string' ? audios[0] : '';
    if (!audio) {
      logError(`[${tag}] Sarvam returned no audio`);
      return { ok: false };
    }

    // Sarvam may answer in WAV even when MP3 is requested: tell the browser which it is.
    // Base64 of "RIFF" (a WAV header) always starts with "UklGR".
    const mime = audio.indexOf('UklGR') === 0 ? 'audio/wav' : 'audio/mpeg';
    return { ok: true, audio, mime };
  } catch (err) {
    logError(`[${tag}] request failed`, err);
    return { ok: false };
  } finally {
    clearTimeout(timer);
  }
}

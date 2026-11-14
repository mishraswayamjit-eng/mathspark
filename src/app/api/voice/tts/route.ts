import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

const SARVAM_URL = 'https://api.sarvam.ai/text-to-speech';
// Sarvam accepts up to 2500 characters per request on bulbul:v3 (1500 on v2).
const MAX_TEXT_CHARS = 2400;
const MAX_TEXT_CHARS_V2 = 1400;
const TIMEOUT_MS = 15_000;
// Voice replies in chat plus read-aloud buttons. The counter is in memory, so
// the cap is per server instance.
const DAILY_LIMIT = 300;
const DAY_MS = 24 * 60 * 60 * 1000;

const MODELS = ['bulbul:v3', 'bulbul:v2', 'bulbul:v4-flash'];
const SAMPLE_RATES = [8000, 16000, 22050, 24000, 32000, 44100, 48000];

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

interface VoiceSettings {
  model: string;
  speaker: string;
  pace: number;
  temperature: number;
  pitch: number;
  loudness: number;
  sampleRate: number;
}

/**
 * The voice to use. Defaults live in Vercel environment variables so the voice
 * can be tuned without a code change:
 *
 *   SARVAM_TTS_MODEL        bulbul:v3 (default) | bulbul:v2 | bulbul:v4-flash
 *   SARVAM_TTS_SPEAKER      a speaker of that model (v3 default: shubh)
 *   SARVAM_TTS_PACE         speed: 0.5 slow to 2.0 fast (default 0.95)
 *   SARVAM_TTS_TEMPERATURE  v3/v4: 0.01 flat and steady to 1.0 lively (default 0.6)
 *   SARVAM_TTS_PITCH        v2 only: -0.75 to 0.75 (default 0)
 *   SARVAM_TTS_LOUDNESS     v2 only: 0.3 to 3.0 (default 1)
 *   SARVAM_TTS_SAMPLE_RATE  audio quality in Hz (default 24000)
 *   SARVAM_TTS_DICT_ID      id of a Sarvam pronunciation dictionary (v3/v4)
 *
 * A request may override model, speaker, pace and temperature; the voice test
 * page (/dev/voice) uses that to compare settings by ear.
 */
function voiceSettings(body: { model?: string; speaker?: string; pace?: number; temperature?: number }): VoiceSettings {
  const env = process.env;
  const wantedModel = body.model || env.SARVAM_TTS_MODEL || '';
  const model = MODELS.indexOf(wantedModel) !== -1 ? wantedModel : 'bulbul:v3';
  // A speaker belongs to one model, so the env default only applies to the env model.
  const sameModelAsEnv = !body.model || body.model === (env.SARVAM_TTS_MODEL || 'bulbul:v3');
  const fallbackSpeaker = model === 'bulbul:v2' ? 'anushka' : model === 'bulbul:v4-flash' ? 'shubh_enhi_ads' : 'shubh';
  const speaker = speakerName(body.speaker) || (sameModelAsEnv ? speakerName(env.SARVAM_TTS_SPEAKER) : null) || fallbackSpeaker;
  const paceLo = model === 'bulbul:v2' ? 0.3 : 0.5;
  const paceHi = model === 'bulbul:v2' ? 3 : 2;
  const rate = inRange(env.SARVAM_TTS_SAMPLE_RATE, 8000, 48000, 24000);
  return {
    model,
    speaker,
    pace: inRange(body.pace !== undefined ? body.pace : env.SARVAM_TTS_PACE, paceLo, paceHi, 0.95),
    temperature: inRange(body.temperature !== undefined ? body.temperature : env.SARVAM_TTS_TEMPERATURE, 0.01, 1, 0.6),
    pitch: inRange(env.SARVAM_TTS_PITCH, -0.75, 0.75, 0),
    loudness: inRange(env.SARVAM_TTS_LOUDNESS, 0.3, 3, 1),
    sampleRate: SAMPLE_RATES.indexOf(rate) !== -1 ? rate : 24000,
  };
}

function sarvamBody(text: string, v: VoiceSettings, languageField: string): Record<string, unknown> {
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

/**
 * POST /api/voice/tts  { text, model?, speaker?, pace?, temperature? }
 *   →  { audio: <base64>, mime, voice: { model, speaker, pace, temperature } }
 *
 * Speaks a piece of text with Sarvam text-to-speech: Sparky's replies in voice
 * mode, and the read-aloud buttons. The API key stays on the server. Returns
 * 503 when SARVAM_API_KEY is not set, and the app then uses the device's own
 * voice, so everything works with or without Sarvam.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`voice-tts:${studentId}`, 30, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }
  if (!checkRateLimit(`voice-tts-day:${studentId}`, DAILY_LIMIT, DAY_MS)) {
    return Response.json({ error: 'Voice has had a busy day. It will be back tomorrow!' }, { status: 429 });
  }

  let text: string;
  let voice: VoiceSettings;
  try {
    const parsed = validateBody<{ text: string; model?: string; speaker?: string; pace?: number; temperature?: number }>(
      await req.json(),
      { text: 'string', model: 'string?', speaker: 'string?', pace: 'number?', temperature: 'number?' },
    );
    text = parsed.text.trim();
    voice = voiceSettings(parsed);
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!text) {
    return Response.json({ error: 'text required' }, { status: 400 });
  }
  if (text.length > (voice.model === 'bulbul:v2' ? MAX_TEXT_CHARS_V2 : MAX_TEXT_CHARS)) {
    // Too long for one request: the app reads this one with the device voice.
    return Response.json({ error: 'Text too long' }, { status: 413 });
  }

  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) {
    return Response.json({ error: 'Voice is not configured.' }, { status: 503 });
  }

  const key: string = apiKey;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const call = (languageField: string) => fetch(SARVAM_URL, {
    method: 'POST',
    headers: { 'api-subscription-key': key, 'Content-Type': 'application/json' },
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
      if (!res.ok) logError(`[voice/tts] Sarvam rejected the request: ${firstDetail}`);
    }

    if (!res.ok) {
      const detail = (await res.text()).slice(0, 300);
      logError(`[voice/tts] Sarvam returned ${res.status}: ${detail}`);
      // A rejected key or setting is a configuration problem, not a passing fault.
      const configProblem = res.status === 400 || res.status === 401 || res.status === 403 || res.status === 422;
      return Response.json(
        { error: 'Voice is unavailable right now.', detail: configProblem ? detail : undefined },
        { status: 502 },
      );
    }

    const data: unknown = await res.json();
    const audios = (data as { audios?: unknown }).audios;
    const audio = Array.isArray(audios) && typeof audios[0] === 'string' ? audios[0] : '';
    if (!audio) {
      logError('[voice/tts] Sarvam returned no audio');
      return Response.json({ error: 'Voice is unavailable right now.' }, { status: 502 });
    }

    // Sarvam may answer in WAV even when MP3 is requested: tell the browser which it is.
    // Base64 of "RIFF" (a WAV header) always starts with "UklGR".
    const mime = audio.indexOf('UklGR') === 0 ? 'audio/wav' : 'audio/mpeg';
    return Response.json({
      audio,
      mime,
      voice: { model: voice.model, speaker: voice.speaker, pace: voice.pace, temperature: voice.temperature },
    });
  } catch (err) {
    logError('[voice/tts] request failed', err);
    return Response.json({ error: 'Voice is unavailable right now.' }, { status: 502 });
  } finally {
    clearTimeout(timer);
  }
}

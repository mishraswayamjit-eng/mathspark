import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { SARVAM_URL, requestSpeech, sarvamBody, voiceSettings, type VoiceSettings } from '@/lib/speech/sarvamServer';

export const dynamic = 'force-dynamic';

// Sarvam accepts up to 2500 characters per request on bulbul:v3 (1500 on v2).
const MAX_TEXT_CHARS = 2400;
const MAX_TEXT_CHARS_V2 = 1400;
// Voice replies in chat plus read-aloud buttons. The counter is in memory, so
// the cap is per server instance.
const DAILY_LIMIT = 300;
const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * POST /api/voice/tts  { text, voice?, speed?, model?, speaker?, pace?, temperature? }
 *   →  { audio: <base64>, mime, voice: { model, speaker, pace, temperature } }
 *
 * Speaks a piece of text with Sarvam text-to-speech. This is the route for
 * text that must not be stored for everyone: Sparky's chat replies, lines with
 * the child's name in them, and lines too long for an address. Fixed lesson
 * and question lines go through GET /api/voice/say, which the CDN keeps.
 *
 * `voice` and `speed` are ids from `src/lib/speech/voices.ts` (the child's
 * choice). A request with neither, as sent by copies of the app from before
 * the voice choice existed, gets the default profile at normal speed. How the
 * SARVAM_TTS_* environment variables and the raw overrides fit in is written
 * out on `voiceSettings` in `src/lib/speech/sarvamServer.ts`.
 *
 * The API key stays on the server. Returns 503 when SARVAM_API_KEY is not
 * set, and the app then uses the device's own voice, so everything works with
 * or without Sarvam.
 */
/**
 * GET /api/voice/tts  →  { available, voice: { model, speaker, pace, temperature } }
 *
 * The default profile as this deployment will speak it, for checking that a
 * change to the environment variables has taken effect. Holds no key and
 * nothing secret.
 */
export async function GET(req: Request) {
  const voice = voiceSettings({});
  const settings = { model: voice.model, speaker: voice.speaker, pace: voice.pace, temperature: voice.temperature };
  const apiKey = process.env.SARVAM_API_KEY;
  const headers = { 'Cache-Control': 'no-store' };

  // ?check=1 (signed in only): asks Sarvam for one short line with these
  // settings and reports what came back, so a voice that is set but not heard
  // can be told apart from one Sarvam is turning down.
  const wantsCheck = new URL(req.url).searchParams.get('check') === '1';
  if (!wantsCheck || !apiKey) {
    return Response.json({ available: Boolean(apiKey), voice: settings }, { headers });
  }
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401, headers });
  }
  if (!checkRateLimit(`voice-tts-check:${studentId}`, 5, 10 * 60_000)) {
    return Response.json({ error: 'Too many checks. Try again in a few minutes.' }, { status: 429, headers });
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  const started = Date.now();
  try {
    const res = await fetch(SARVAM_URL, {
      method: 'POST',
      headers: { 'api-subscription-key': apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify(sarvamBody('Hello! This is a voice check.', voice, 'language_code')),
      signal: controller.signal,
    });
    const ms = Date.now() - started;
    if (!res.ok) {
      const detail = (await res.text()).slice(0, 300);
      return Response.json({ available: true, voice: settings, check: { ok: false, status: res.status, ms, detail } }, { headers });
    }
    const data: unknown = await res.json();
    const audios = (data as { audios?: unknown }).audios;
    const audio = Array.isArray(audios) && typeof audios[0] === 'string' ? audios[0] : '';
    return Response.json(
      { available: true, voice: settings, check: { ok: audio.length > 0, status: res.status, ms, audioBytes: Math.round(audio.length * 0.75) } },
      { headers },
    );
  } catch (err) {
    logError('[voice/tts] check failed', err);
    return Response.json(
      { available: true, voice: settings, check: { ok: false, status: 0, ms: Date.now() - started, detail: 'No answer from Sarvam within 8 seconds.' } },
      { headers },
    );
  } finally {
    clearTimeout(timer);
  }
}

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
    const parsed = validateBody<{
      text: string; voice?: string; speed?: string; model?: string; speaker?: string; pace?: number; temperature?: number;
    }>(
      await req.json(),
      { text: 'string', voice: 'string?', speed: 'string?', model: 'string?', speaker: 'string?', pace: 'number?', temperature: 'number?' },
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

  const spoken = await requestSpeech(text, voice, apiKey, 'voice/tts');
  if (!spoken.ok) {
    return Response.json({ error: 'Voice is unavailable right now.', detail: spoken.detail }, { status: 502 });
  }
  return Response.json({
    audio: spoken.audio,
    mime: spoken.mime,
    voice: { model: voice.model, speaker: voice.speaker, pace: voice.pace, temperature: voice.temperature },
  });
}

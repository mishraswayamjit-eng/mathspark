import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

const SARVAM_URL = 'https://api.sarvam.ai/text-to-speech';
// Sarvam caps one request at about 2500 characters.
const MAX_TEXT_CHARS = 2400;
const TIMEOUT_MS = 15_000;
// Chat allows 100 messages a day, so a child cannot legitimately need more spoken
// replies than that. The counter is in memory, so the cap is per server instance.
const DAILY_LIMIT = 120;
const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * POST /api/voice/tts  { text }  →  { audio: <base64>, mime }
 *
 * Speaks one of Sparky's replies with Sarvam text-to-speech, for the chat's
 * voice mode. The API key stays on the server. Returns 503 when SARVAM_API_KEY
 * is not set, and the app then falls back to the device's own voice — so voice
 * mode works with or without Sarvam.
 *
 * The request fields follow Sarvam's published REST example; the model and
 * speaker can be changed with SARVAM_TTS_MODEL / SARVAM_TTS_SPEAKER.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`voice-tts:${studentId}`, 20, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }
  if (!checkRateLimit(`voice-tts-day:${studentId}`, DAILY_LIMIT, DAY_MS)) {
    return Response.json({ error: 'Voice has had a busy day. It will be back tomorrow!' }, { status: 429 });
  }

  let text: string;
  try {
    const parsed = validateBody<{ text: string }>(await req.json(), { text: 'string' });
    text = parsed.text.trim();
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!text) {
    return Response.json({ error: 'text required' }, { status: 400 });
  }
  if (text.length > MAX_TEXT_CHARS) {
    // Too long for one request: the app reads this one with the device voice.
    return Response.json({ error: 'Text too long' }, { status: 413 });
  }

  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) {
    return Response.json({ error: 'Voice is not configured.' }, { status: 503 });
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(SARVAM_URL, {
      method: 'POST',
      headers: { 'api-subscription-key': apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        target_language_code: 'en-IN',
        model: process.env.SARVAM_TTS_MODEL || 'bulbul:v3',
        speaker: process.env.SARVAM_TTS_SPEAKER || 'shubh',
        pace: 0.95,
        speech_sample_rate: 24000,
        output_audio_codec: 'mp3',
      }),
      signal: controller.signal,
    });

    if (!res.ok) {
      logError(`[voice/tts] Sarvam returned ${res.status}`);
      return Response.json({ error: 'Voice is unavailable right now.' }, { status: 502 });
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
    return Response.json({ audio, mime });
  } catch (err) {
    logError('[voice/tts] request failed', err);
    return Response.json({ error: 'Voice is unavailable right now.' }, { status: 502 });
  } finally {
    clearTimeout(timer);
  }
}

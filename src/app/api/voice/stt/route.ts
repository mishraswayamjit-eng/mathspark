import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

const SARVAM_URL = 'https://api.sarvam.ai/speech-to-text';
// One spoken turn is capped at about 25 seconds in the browser; at the bitrate
// it records, that is well under this.
const MAX_AUDIO_BYTES = 3 * 1024 * 1024;
const TIMEOUT_MS = 20_000;
const DAILY_LIMIT = 300;
const DAY_MS = 24 * 60 * 60 * 1000;

// Words a speech model is likely to mishear in a maths conversation.
const MATHS_TERMS = [
  'numerator', 'denominator', 'fraction', 'perimeter', 'area', 'HCF', 'LCM', 'BODMAS', 'quotient', 'remainder',
  'multiple', 'factor', 'prime', 'decimal', 'percentage', 'ratio', 'proportion', 'equation', 'angle', 'triangle',
  'rectangle', 'square root', 'place value', 'lakh', 'crore', 'simple interest', 'profit', 'loss', 'average', 'Sparky',
];

/**
 * Listening is switched on separately from speaking, because it sends a
 * recording of the child's voice to Sarvam, which is personal data:
 *
 *   SARVAM_API_KEY       the Sarvam key (also used for speaking)
 *   SARVAM_STT_ENABLED   must be "on" for this route to work
 *   SARVAM_STT_MODEL     saaras:v4 (default) | saaras:v3
 *   SARVAM_STT_LANGUAGE  en-IN (default), another code such as hi-IN, or "unknown" to auto-detect
 */
function sttConfigured(): boolean {
  return Boolean(process.env.SARVAM_API_KEY) && process.env.SARVAM_STT_ENABLED === 'on';
}

/** GET /api/voice/stt → { available }: lets the app decide how to listen before recording anything. */
export async function GET() {
  return Response.json({ available: sttConfigured() });
}

function fileName(mime: string): string {
  if (mime.indexOf('mp4') !== -1 || mime.indexOf('m4a') !== -1 || mime.indexOf('aac') !== -1) return 'speech.mp4';
  if (mime.indexOf('ogg') !== -1) return 'speech.ogg';
  if (mime.indexOf('wav') !== -1) return 'speech.wav';
  return 'speech.webm';
}

/**
 * POST /api/voice/stt  (multipart form, field `file`: one short recording)  →  { text }
 *
 * Turns one spoken turn into text with Sarvam speech-to-text. The recording is
 * passed straight through and is not stored by the app. Returns 503 when
 * listening through Sarvam is not switched on; the app then uses the browser's
 * own speech recognition.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  if (!sttConfigured()) {
    return Response.json({ error: 'Listening is not configured.' }, { status: 503 });
  }
  if (!checkRateLimit(`voice-stt:${studentId}`, 20, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }
  if (!checkRateLimit(`voice-stt-day:${studentId}`, DAILY_LIMIT, DAY_MS)) {
    return Response.json({ error: 'Voice has had a busy day. It will be back tomorrow!' }, { status: 429 });
  }

  let audio: Blob;
  try {
    const form = await req.formData();
    const file = form.get('file');
    if (!file || typeof file === 'string') {
      return Response.json({ error: 'file required' }, { status: 400 });
    }
    audio = file;
  } catch {
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }
  if (audio.size === 0) {
    return Response.json({ error: 'file required' }, { status: 400 });
  }
  if (audio.size > MAX_AUDIO_BYTES) {
    return Response.json({ error: 'Recording too long' }, { status: 413 });
  }

  const recording: Blob = audio;
  const key: string = process.env.SARVAM_API_KEY || '';
  const model = process.env.SARVAM_STT_MODEL === 'saaras:v3' ? 'saaras:v3' : 'saaras:v4';
  const language = /^[a-z]{2,3}-IN$|^unknown$/.test(process.env.SARVAM_STT_LANGUAGE || '') ? String(process.env.SARVAM_STT_LANGUAGE) : 'en-IN';

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const call = (withExtras: boolean) => {
    const out = new FormData();
    out.append('file', recording, fileName(recording.type || ''));
    out.append('language_code', language);
    if (withExtras) {
      out.append('model', model);
      // Key terms are supported on saaras:v4 only.
      if (model === 'saaras:v4') out.append('keyterms', JSON.stringify(MATHS_TERMS));
    }
    return fetch(SARVAM_URL, {
      method: 'POST',
      headers: { 'api-subscription-key': key },
      body: out,
      signal: controller.signal,
    });
  };

  try {
    let res = await call(true);
    if (res.status === 400 || res.status === 422) {
      // The model name or key terms may not be accepted on this account: retry with Sarvam's defaults.
      const firstDetail = (await res.text()).slice(0, 300);
      logError(`[voice/stt] Sarvam rejected the request, retrying with defaults: ${firstDetail}`);
      res = await call(false);
    }
    if (!res.ok) {
      const detail = (await res.text()).slice(0, 300);
      logError(`[voice/stt] Sarvam returned ${res.status}: ${detail}`);
      return Response.json({ error: 'Listening is unavailable right now.' }, { status: 502 });
    }
    const data: unknown = await res.json();
    const transcript = (data as { transcript?: unknown }).transcript;
    return Response.json({ text: typeof transcript === 'string' ? transcript.trim().slice(0, 2000) : '' });
  } catch (err) {
    logError('[voice/stt] request failed', err);
    return Response.json({ error: 'Listening is unavailable right now.' }, { status: 502 });
  } finally {
    clearTimeout(timer);
  }
}

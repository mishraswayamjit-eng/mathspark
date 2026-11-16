import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { requestSpeech, voiceSettings } from '@/lib/speech/sarvamServer';
import {
  SAY_MAX_CHARS,
  VOICE_CACHE_VERSION,
  getVoiceProfile,
  getVoiceSpeed,
  normaliseSpeechText,
} from '@/lib/speech/voices';

export const dynamic = 'force-dynamic';

// The same limits, under the same keys, as POST /api/voice/tts: the two routes
// share one allowance per child. Only requests that reach this function count;
// a line served from storage costs nothing.
const DAILY_LIMIT = 300;
const DAY_MS = 24 * 60 * 60 * 1000;

const ONE_YEAR = 31536000;

/** Anything that is not the audio itself must never be stored by the CDN or the browser. */
function refuse(status: number, error: string): Response {
  return Response.json({ error }, { status, headers: { 'Cache-Control': 'no-store' } });
}

/**
 * GET /api/voice/say?k=<version>&v=<voice id>&s=<speed id>&t=<text>
 *   →  the audio itself (audio/mpeg, or audio/wav when Sarvam answers in WAV)
 *
 * One fixed line, spoken once and then kept. The answer carries
 * `Cache-Control: public, max-age=31536000, s-maxage=31536000, immutable`, so
 * Vercel's CDN and the browser store it under this exact address. The function
 * (and Sarvam) then runs once per distinct line + voice + speed; later
 * requests for the same address, from any child, are answered from storage and
 * never reach this code. `src/lib/speech/voices.ts` builds the address
 * (`sayUrl`) with the parameters in a fixed order and the text normalised, so
 * the same line always has the same address.
 *
 * PRIVACY: a stored line can be fetched by anyone who has its address, signed
 * in or not, because the CDN answers before this function is reached. That is
 * acceptable only because the text is lesson content that every child sees
 * (questions, hints, lesson lines, the tutor's stock reactions). Text that is
 * about one child (their name, a chat reply, live coaching on their own
 * working) MUST NOT use this route: the client keeps those on POST
 * /api/voice/tts with `fetchServerVoice(text, { personal: true })`.
 *
 * Every request that does reach this function needs a signed-in child and
 * counts against that child's voice limits. The voice and the speed must be
 * ids from the allow-lists in voices.ts; a raw speaker name or number is never
 * accepted here. No cookie is ever set on the answer (a `Set-Cookie` would
 * stop the CDN storing it). Anything other than audio is sent with `no-store`.
 *
 * `k` is VOICE_CACHE_VERSION. Adding 1 to it in voices.ts changes every
 * address, which is how all stored audio is refreshed.
 */
export async function GET(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) return refuse(401, 'Unauthorized');

  const params = new URL(req.url).searchParams;
  // A copy of the app from before a version bump: it falls back to POST.
  if (params.get('k') !== VOICE_CACHE_VERSION) return refuse(400, 'Unknown voice version');
  const profile = getVoiceProfile(params.get('v'));
  const speed = getVoiceSpeed(params.get('s'));
  if (!profile || !speed) return refuse(400, 'Unknown voice or speed');

  const text = normaliseSpeechText(params.get('t') || '');
  if (!text) return refuse(400, 'text required');
  if (text.length > SAY_MAX_CHARS) return refuse(413, 'Text too long');

  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) return refuse(503, 'Voice is not configured.');

  if (!checkRateLimit(`voice-tts:${studentId}`, 30, 60_000)) {
    return refuse(429, 'Slow down a bit! Try again in a moment.');
  }
  if (!checkRateLimit(`voice-tts-day:${studentId}`, DAILY_LIMIT, DAY_MS)) {
    return refuse(429, 'Voice has had a busy day. It will be back tomorrow!');
  }

  const spoken = await requestSpeech(text, voiceSettings({ voice: profile.id, speed: speed.id }), apiKey, 'voice/say');
  if (!spoken.ok) return refuse(502, 'Voice is unavailable right now.');

  const decoded = Buffer.from(spoken.audio, 'base64');
  // A clip this small is not speech; storing it for a year would silence the line for everyone.
  if (decoded.length < 256) return refuse(502, 'Voice is unavailable right now.');
  const body = new ArrayBuffer(decoded.length);
  new Uint8Array(body).set(decoded);

  return new Response(body, {
    status: 200,
    headers: {
      'Content-Type': spoken.mime,
      'Content-Length': String(decoded.length),
      'Cache-Control': `public, max-age=${ONE_YEAR}, s-maxage=${ONE_YEAR}, immutable`,
      // Read by Vercel's CDN in preference to Cache-Control, and not passed on to the browser.
      'Vercel-CDN-Cache-Control': `public, max-age=${ONE_YEAR}`,
    },
  });
}

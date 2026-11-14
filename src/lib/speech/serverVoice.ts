/**
 * The server voice (Sarvam text-to-speech through /api/voice/tts), for the browser.
 *
 * `fetchServerVoice(text)` resolves to an audio data URL, or null when the
 * server voice cannot be used for this text (not configured, signed out, too
 * long, over a limit, offline). Callers then fall back to the device's own voice.
 *
 * Sending text here sends it to Sarvam. That is why this is only reached when
 * SARVAM_API_KEY has been set on the server: until then the route answers 503
 * and this module stops asking for the rest of the visit.
 */

// null: not yet known. false: the server has no voice configured, stop asking.
let available: boolean | null = null;

// A few recent readings, so tapping "read again" does not make a second request.
const CACHE_SIZE = 16;
const cacheKeys: string[] = [];
const cache: Record<string, string> = {};

// Sarvam takes about 2500 characters; leave the long ones to the device voice.
const MAX_CHARS = 2400;

export function serverVoiceMayBeAvailable(): boolean {
  return available !== false;
}

export async function fetchServerVoice(text: string): Promise<string | null> {
  if (available === false || !text || text.length > MAX_CHARS) return null;
  if (Object.prototype.hasOwnProperty.call(cache, text)) return cache[text];

  try {
    const res = await fetch('/api/voice/tts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    if (res.status === 503 || res.status === 404) {
      available = false;          // not configured on this deployment
      return null;
    }
    if (!res.ok) return null;     // signed out, a limit, or a passing fault: try again next time
    const data = (await res.json()) as { audio?: string; mime?: string };
    if (!data.audio) return null;
    available = true;
    const src = `data:${data.mime || 'audio/mpeg'};base64,${data.audio}`;
    cache[text] = src;
    cacheKeys.push(text);
    if (cacheKeys.length > CACHE_SIZE) {
      const oldest = cacheKeys.shift();
      if (oldest !== undefined) delete cache[oldest];
    }
    return src;
  } catch {
    return null;                  // offline: the device voice still works
  }
}

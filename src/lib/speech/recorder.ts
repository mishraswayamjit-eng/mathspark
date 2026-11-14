/**
 * Records one spoken turn from the microphone and stops by itself when the
 * speaker goes quiet. Used when listening goes through the server (Sarvam
 * speech-to-text) and not the browser's own speech recognition.
 *
 * The recording lives in memory only and is handed to the caller as a Blob.
 */

export interface RecordingResult {
  /** The recording, or null when nothing was said. */
  audio: Blob | null;
  /** True when the browser refused the microphone. */
  blocked: boolean;
}

export interface Recording {
  done: Promise<RecordingResult>;
  /** Stop at once and throw the recording away. */
  cancel: () => void;
}

const TICK_MS = 50;
const SPEECH_MS = 150;        // this much sound counts as "started talking"
const QUIET_AFTER_MS = 1400;  // this much quiet after talking ends the turn
const WAIT_FOR_SPEECH_MS = 8000;
const MAX_TURN_MS = 25000;

const MIME_CHOICES = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4', 'audio/ogg;codecs=opus'];

export function canRecord(): boolean {
  return typeof window !== 'undefined'
    && typeof MediaRecorder !== 'undefined'
    && Boolean(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

function pickMime(): string {
  for (let i = 0; i < MIME_CHOICES.length; i++) {
    if (MediaRecorder.isTypeSupported(MIME_CHOICES[i])) return MIME_CHOICES[i];
  }
  return '';
}

export function recordUtterance(): Recording {
  let cancelled = false;
  let finish: (() => void) | null = null;

  const done = new Promise<RecordingResult>((resolve) => {
    navigator.mediaDevices
      .getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, channelCount: 1 } })
      .then((stream) => {
        const release = () => {
          const tracks = stream.getTracks();
          for (let i = 0; i < tracks.length; i++) tracks[i].stop();
        };
        if (cancelled) {
          release();
          resolve({ audio: null, blocked: false });
          return;
        }

        // Loudness meter, to tell talking from quiet.
        const Ctx = window.AudioContext
          || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
        const ctx = Ctx ? new Ctx() : null;
        let analyser: AnalyserNode | null = null;
        if (ctx) {
          analyser = ctx.createAnalyser();
          analyser.fftSize = 1024;
          ctx.createMediaStreamSource(stream).connect(analyser);
        }
        const samples = new Uint8Array(1024);

        const mime = pickMime();
        let recorder: MediaRecorder;
        try {
          recorder = mime ? new MediaRecorder(stream, { mimeType: mime, audioBitsPerSecond: 32000 }) : new MediaRecorder(stream);
        } catch {
          release();
          if (ctx) ctx.close().catch(() => {});
          resolve({ audio: null, blocked: false });
          return;
        }

        const chunks: Blob[] = [];
        let spoke = false;
        let loudMs = 0;
        let floor = 0;          // background noise, measured over the first moments
        let floorTicks = 0;
        const startedAt = Date.now();
        let lastLoudAt = startedAt;

        const timer = setInterval(() => {
          const now = Date.now();
          if (analyser) {
            analyser.getByteTimeDomainData(samples);
            let sum = 0;
            for (let i = 0; i < samples.length; i++) {
              const v = (samples[i] - 128) / 128;
              sum += v * v;
            }
            const level = Math.sqrt(sum / samples.length);
            if (floorTicks < 6) {
              floor = Math.max(floor, level);
              floorTicks += 1;
            }
            const threshold = Math.max(0.02, floor * 2.2);
            if (level > threshold) {
              loudMs += TICK_MS;
              lastLoudAt = now;
              if (loudMs >= SPEECH_MS) spoke = true;
            } else if (!spoke) {
              loudMs = 0;
            }
          } else {
            // No meter on this device: treat the whole turn as speech and rely on the time limits.
            spoke = true;
            lastLoudAt = startedAt + 6000 > now ? now : lastLoudAt;
          }
          const quietLongEnough = spoke && now - lastLoudAt > QUIET_AFTER_MS;
          const nothingSaid = !spoke && now - startedAt > WAIT_FOR_SPEECH_MS;
          if (quietLongEnough || nothingSaid || now - startedAt > MAX_TURN_MS) stopNow();
        }, TICK_MS);

        let stopped = false;
        function stopNow() {
          if (stopped) return;
          stopped = true;
          clearInterval(timer);
          try { recorder.stop(); } catch { settle(); }
        }
        function settle() {
          release();
          if (ctx) ctx.close().catch(() => {});
          const usable = !cancelled && spoke && chunks.length > 0;
          resolve({ audio: usable ? new Blob(chunks, { type: recorder.mimeType || mime || 'audio/webm' }) : null, blocked: false });
        }

        recorder.ondataavailable = (e: BlobEvent) => { if (e.data && e.data.size > 0) chunks.push(e.data); };
        recorder.onstop = settle;
        recorder.onerror = () => stopNow();
        finish = stopNow;
        recorder.start();
      })
      .catch((err: unknown) => {
        const name = err && typeof err === 'object' && 'name' in err ? String((err as { name: unknown }).name) : '';
        resolve({ audio: null, blocked: name === 'NotAllowedError' || name === 'SecurityError' });
      });
  });

  return {
    done,
    cancel: () => {
      cancelled = true;
      if (finish) finish();
    },
  };
}

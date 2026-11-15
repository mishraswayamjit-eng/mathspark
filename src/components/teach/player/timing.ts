/**
 * Timing and small talk for the lesson player.
 *
 * Nothing here decides whether an answer is right: the lesson script says
 * which choice is the right one, and these are only the words and pauses
 * around it.
 */

/** The pause between one beat and the next, in milliseconds. */
export const GAP_MS = 450;
/** The same pause at the slower speed. */
export const SLOW_GAP_MS = 1300;
/** How much longer a caption stays up at the slower speed when the voice is off. */
export const SLOW_FACTOR = 1.35;
/** How long to wait for the voice to start before carrying on with the caption alone. */
export const START_WAIT_MS = 4000;

/** Roughly how long a sentence takes to say aloud, in milliseconds. */
export function sayMs(text: string): number {
  const parts = text.trim().split(/\s+/);
  let words = 0;
  for (let i = 0; i < parts.length; i++) {
    if (parts[i].length > 0) words += 1;
  }
  let breaths = 0;
  let stops = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text.charAt(i);
    if (ch === ',' || ch === ';' || ch === ':') breaths += 1;
    else if (ch === '.' || ch === '?' || ch === '!') stops += 1;
  }
  const ms = 500 + words * 370 + breaths * 180 + stops * 300;
  return Math.max(1400, Math.min(18000, ms));
}

const PRAISE: string[] = [
  "That's it!",
  'Yes, exactly.',
  'Spot on.',
  "You've got it.",
  "That's the one.",
  'Nicely spotted.',
];

/** A brief "that's it" for a right choice. Consecutive turns never give the same line. */
export function praiseLine(turn: number): string {
  const n = PRAISE.length;
  return PRAISE[((turn % n) + n) % n];
}

/**
 * How long a piece of audio lasts, in milliseconds, or null when the browser
 * cannot tell. Used to time the board to the real voice rather than a guess.
 */
export function audioLengthMs(src: string): Promise<number | null> {
  return new Promise<number | null>((resolve) => {
    let settled = false;
    const finish = (value: number | null) => {
      if (settled) return;
      settled = true;
      resolve(value);
    };
    if (typeof Audio === 'undefined') {
      finish(null);
      return;
    }
    try {
      const probe = new Audio();
      probe.preload = 'metadata';
      probe.onloadedmetadata = () => {
        const seconds = probe.duration;
        finish(isFinite(seconds) && seconds > 0.3 ? Math.round(seconds * 1000) : null);
      };
      probe.onerror = () => finish(null);
      probe.src = src;
    } catch {
      finish(null);
    }
    setTimeout(() => finish(null), 1500);
  });
}

/**
 * What the tutor says in reaction to something the child does.
 *
 * Outside teach mode the tutor does not lecture: it reacts. This module turns
 * an event (a right answer, a miss, a hint opened, a long pause) into one short
 * spoken line. It is deterministic: no AI model is called, so a reaction is
 * instant and can never judge an answer. Whether an answer is right is decided
 * elsewhere and passed in.
 *
 * The lines themselves live in `./lines`. This file decides which kind of line
 * fits what just happened (or that silence fits better) and picks one by
 * `ctx.turn`, so the same event and turn always give the same line.
 *
 * The exported `TutorEvent`, `TutorContext` and `tutorLine` signature are the
 * contract other screens build on, so they must not change.
 */

import { toSpeech } from '@/lib/speech/mathToSpeech';
import { LINES } from './lines';

export type TutorEvent =
  /** A question has just appeared. `first` is true for the first question of a session. */
  | { kind: 'question'; first: boolean }
  /** The child answered and the app marked it right. */
  | { kind: 'correct'; streak: number; usedHint: boolean; secondsTaken: number }
  /**
   * The child answered and the app marked it not right. `misconception` is the
   * question's own verified note on why that choice tempts, when it has one.
   */
  | { kind: 'miss'; chosenText: string; misconception?: string; missesInARow: number }
  /** The child opened a hint. `level` is 1, 2 or 3. */
  | { kind: 'hint'; level: number }
  /** The child has not done anything for a while on an open question. */
  | { kind: 'idle'; seconds: number }
  /** The child started writing on the pencil pad. */
  | { kind: 'startedWorking' }
  /** The session ended. */
  | { kind: 'sessionEnd'; correct: number; total: number };

export interface TutorContext {
  /** The child's first name, when known. Used sparingly. */
  name?: string;
  /** The topic being practised, in words a child would use. */
  topicName?: string;
  /**
   * A number that changes from one reaction to the next (a running count is
   * fine). The same event with the same turn always gives the same line; a
   * different turn gives variety.
   */
  turn: number;
}

/**
 * What the caller remembers about the session so far. Optional: `tutorLine`
 * works without it. `useTutorVoice` supplies it, which is what lets the tutor
 * notice a right answer straight after a miss and avoid repeating itself.
 */
export interface TutorMemory {
  /** The child's previous answer was a miss. */
  afterMiss?: boolean;
  /** Lines said recently, newest last. A line in this list is avoided where the pool allows. */
  recent?: string[];
}

/** A right answer faster than this (in seconds) is "quick". */
export const QUICK_SECONDS = 8;
/** A right answer slower than this (in seconds) was hard-won. */
export const HARD_WON_SECONDS = 45;
/** An idle nudge is not given before this many seconds: the child is thinking. */
export const IDLE_QUIET_SECONDS = 15;
/** The longest line built round a question's misconception note. */
export const MISS_LINE_MAX = 150;

// ── Picking a line ───────────────────────────────────────────────────────────

interface Vars {
  name: string;
  n: number;
  c: number;
  t: number;
  topic: string;
}

function swap(text: string, token: string, value: string): string {
  return text.split(token).join(value);
}

/** Fill a line's placeholders. An unknown name removes ", {name}" altogether. */
function fill(line: string, vars: Vars): string {
  let out = swap(line, ', {name}', vars.name ? `, ${vars.name}` : '');
  out = swap(out, '{n}', String(vars.n));
  out = swap(out, '{c}', String(vars.c));
  out = swap(out, '{t}', String(vars.t));
  out = swap(out, '{topic}', vars.topic);
  return out;
}

/** A first name that is safe to say, or '' when there is none. */
function firstName(name: string | undefined): string {
  if (!name) return '';
  const first = name.replace(/^\s+/, '').split(/\s+/)[0] || '';
  if (first.length < 2 || first.length > 20) return '';
  // Latin letters only: the line is spoken by an English voice.
  if (!/^[A-Za-zÀ-ɏ]+$/.test(first)) return '';
  return first;
}

/**
 * True when `line` says this child's first name. Such a line is about one
 * child, so its audio must not be stored where anyone could fetch it: the
 * voice then makes it for that child only (see `useTutorVoice`). It errs
 * towards true: a name that happens to appear inside another word counts.
 */
export function lineSaysName(line: string, name: string | undefined): boolean {
  const first = firstName(name);
  return first !== '' && line.indexOf(first) !== -1;
}

/** The topic in speakable words, or "this topic". */
function topicWords(topic: string | undefined): string {
  if (!topic) return 'this topic';
  const words = topic
    .replace(/&/g, ' and ')
    .replace(/[^A-Za-z0-9 ,']/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return words && words.length <= 40 ? words : 'this topic';
}

function wholeTurn(turn: number): number {
  if (typeof turn !== 'number' || !isFinite(turn)) return 0;
  return Math.abs(Math.floor(turn));
}

function gcd(a: number, b: number): number {
  let x = a;
  let y = b;
  while (y !== 0) {
    const r = x % y;
    x = y;
    y = r;
  }
  return x;
}

const STEPS = [7, 5, 11, 13, 3];

/**
 * Where in a pool of `size` lines turn `turn` lands. Consecutive turns jump
 * round the pool (never simply to the next line), every line is visited once
 * in each lap of `size` turns, and each lap starts somewhere new.
 */
export function pickIndex(size: number, turn: number, salt: number): number {
  if (size <= 1) return 0;
  let step = 1;
  for (let i = 0; i < STEPS.length; i++) {
    const candidate = STEPS[i] % size;
    if (candidate > 1 && candidate < size - 1 && gcd(candidate, size) === 1) {
      step = candidate;
      break;
    }
  }
  const lap = Math.floor(turn / size);
  return ((turn % size) * step + lap * 3 + salt) % size;
}

/** One line from a pool for this turn, moving on past anything said recently. */
function choose(pool: string[], turn: number, salt: number, vars: Vars, recent?: string[]): string {
  const size = pool.length;
  if (size === 0) return '';
  const start = pickIndex(size, turn, salt);
  if (recent && recent.length > 0) {
    for (let k = 0; k < size; k++) {
      const line = fill(pool[(start + k) % size], vars);
      if (recent.indexOf(line) === -1) return line;
    }
  }
  return fill(pool[start], vars);
}

// ── The question's own note on a tempting choice ─────────────────────────────

// Words a child must never hear from the tutor.
const UNSAYABLE = /\b(wrong|wrongly|incorrect|incorrectly|oops|fail|failed|failure|error|errors)\b/i;
// A sentence that could give the answer away.
const GIVES_AWAY = /\b(correct|right answer|answer is|answer was|answer should|answer would)\b/i;
// A note written about the child instead of to them cannot be said to them.
const ABOUT_THE_CHILD = /^(the\s+)?(student|students|child|children|learner|learners|pupil|pupils)\b/i;

function splitSentences(text: string): string[] {
  const out: string[] = [];
  let start = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text.charAt(i);
    const ends = ch === '.' || ch === '?' || ch === '!';
    if (ends && (i === text.length - 1 || text.charAt(i + 1) === ' ')) {
      const piece = text.slice(start, i + 1).trim();
      if (piece.length > 1) out.push(piece);
      start = i + 1;
    }
  }
  const rest = text.slice(start).trim();
  if (rest) out.push(`${rest}.`);
  return out;
}

/**
 * A question's misconception note as one or two sentences the tutor can say,
 * at most `room` characters. '' when nothing in the note can be said: it is
 * too long, it is not addressed to the child, or it might give the answer away.
 */
export function spokenMisconception(note: string | null | undefined, room: number): string {
  if (!note) return '';
  let s = String(note)
    .replace(/\bRs\.?\s*(\d[\d,]*(?:\.\d+)?)/g, '$1 rupees')
    .replace(/\be\.g\.,?/gi, 'for example,')
    .replace(/\bi\.e\.,?/gi, 'that is,')
    .replace(/&/g, ' and ');
  s = toSpeech(s);
  s = s
    .replace(/\s*[—–]\s*/g, ', ')            // em and en dashes become a breath
    .replace(/\s*\(\s*/g, ', ')
    .replace(/\s*\)/g, '')
    .replace(/[‘’]/g, "'")
    .replace(/["“”*#~|[\]]/g, '')
    .replace(/([A-Za-z])[;:]\s+/g, '$1, ')             // "Remember: ..." (not 3:45 or 2 : 3)
    .replace(/,\s*,/g, ',')
    .replace(/,\s*([.?!])/g, '$1')
    .replace(/\s+/g, ' ')
    .replace(/^[,\s]+/, '')
    .trim();
  if (!s) return '';

  const sentences = splitSentences(s);
  let out = '';
  let used = 0;
  for (let i = 0; i < sentences.length && used < 2; i++) {
    const sentence = sentences[i];
    if (UNSAYABLE.test(sentence) || GIVES_AWAY.test(sentence) || ABOUT_THE_CHILD.test(sentence)) continue;
    const next = out ? `${out} ${sentence}` : sentence;
    if (next.length > room) break;
    out = next;
    used += 1;
  }
  if (!out) return '';
  return out.charAt(0).toUpperCase() + out.slice(1);
}

// ── One function per event ───────────────────────────────────────────────────

type CorrectEvent = Extract<TutorEvent, { kind: 'correct' }>;
type MissEvent = Extract<TutorEvent, { kind: 'miss' }>;

function correctLine(event: CorrectEvent, turn: number, vars: Vars, memory?: TutorMemory): string {
  const recent = memory ? memory.recent : undefined;
  const streak = event.streak;

  // Milestones first: they are rare, and the child is counting too.
  if (streak === 3) return choose(LINES.streakThree, turn, 0, vars, recent);
  if (streak === 5) return choose(LINES.streakFive, turn, 0, vars, recent);
  if (streak >= 10 && streak % 5 === 0) return choose(LINES.streakLong, turn, 0, vars, recent);

  if (event.usedHint) return choose(LINES.correctAfterHint, turn, 0, vars, recent);
  if (memory && memory.afterMiss && streak <= 1) return choose(LINES.correctComeback, turn, 0, vars, recent);

  const seconds = event.secondsTaken;
  if (seconds >= HARD_WON_SECONDS) return choose(LINES.correctHardWon, turn, 0, vars, recent);
  if (seconds > 0 && seconds < QUICK_SECONDS) {
    if (turn % 5 === 4) return '';
    return choose(LINES.correctQuick, turn, 0, vars, recent);
  }

  // An ordinary right answer: one in three passes without comment, and on a
  // long run the tutor says less still and lets the child get on with it.
  if (turn % 3 === 2) return '';
  if (streak >= 6 && turn % 2 === 1) return '';
  return choose(LINES.correctPlain, turn, 0, vars, recent);
}

function missLine(event: MissEvent, turn: number, vars: Vars, memory?: TutorMemory): string {
  if (event.misconception) {
    let lead = choose(LINES.missFrames, turn, 0, vars);
    let note = spokenMisconception(event.misconception, MISS_LINE_MAX - lead.length - 1);
    if (!note) {
      // A long note may still fit behind the shortest lead-in.
      lead = LINES.missFrames[1];
      note = spokenMisconception(event.misconception, MISS_LINE_MAX - lead.length - 1);
    }
    if (note) {
      let line = `${lead} ${note}`;
      const tail = choose(LINES.missTails, turn, 2, vars);
      if (line.length + 1 + tail.length <= 140) line = `${line} ${tail}`;
      return line;
    }
  }
  const recent = memory ? memory.recent : undefined;
  if (event.missesInARow >= 3) return choose(LINES.missMany, turn, 0, vars, recent);
  if (event.missesInARow === 2) return choose(LINES.missSecond, turn, 0, vars, recent);
  return choose(LINES.missFirst, turn, 0, vars, recent);
}

function endLine(turn: number, vars: Vars): string {
  if (!(vars.t >= 3)) return choose(LINES.endShort, turn, 0, vars);
  if (vars.c >= vars.t) return choose(LINES.endAllRight, turn, 0, vars);
  const share = vars.c / vars.t;
  if (share >= 0.75) return choose(LINES.endMostRight, turn, 0, vars);
  if (share >= 0.4) return choose(LINES.endAboutHalf, turn, 0, vars);
  return choose(LINES.endHard, turn, 0, vars);
}

function count(value: number): number {
  return typeof value === 'number' && isFinite(value) && value > 0 ? Math.floor(value) : 0;
}

/**
 * `tutorLine` with a memory of the session. Still deterministic: the same
 * event, turn and memory always give the same line.
 */
export function tutorLineWith(event: TutorEvent, ctx: TutorContext, memory?: TutorMemory): string {
  const turn = wholeTurn(ctx.turn);
  const recent = memory ? memory.recent : undefined;
  const vars: Vars = { name: firstName(ctx.name), n: 0, c: 0, t: 0, topic: topicWords(ctx.topicName) };

  switch (event.kind) {
    case 'question':
      if (event.first) return choose(LINES.welcome, turn, 0, vars, recent);
      // Mostly quiet, so the child can read.
      return turn % 6 === 3 ? choose(LINES.nextQuestion, turn, 0, vars, recent) : '';

    case 'correct':
      vars.n = count(event.streak);
      return correctLine(event, turn, vars, memory);

    case 'miss':
      return missLine(event, turn, vars, memory);

    case 'hint':
      if (event.level >= 3) return choose(LINES.hintExample, turn, 0, vars, recent);
      if (event.level === 2) return choose(LINES.hintFirstMove, turn, 0, vars, recent);
      return choose(LINES.hintIdea, turn, 0, vars, recent);

    case 'idle':
      if (!(event.seconds >= IDLE_QUIET_SECONDS)) return '';
      if (event.seconds < 45) return choose(LINES.idleSoft, turn, 0, vars, recent);
      if (event.seconds < 90) return choose(LINES.idleHint, turn, 0, vars, recent);
      return choose(LINES.idleLong, turn, 0, vars, recent);

    case 'startedWorking':
      // Usually silent: writing needs no commentary.
      return turn % 3 === 0 ? choose(LINES.startedWorking, turn, 0, vars, recent) : '';

    case 'sessionEnd':
      vars.t = count(event.total);
      vars.c = Math.min(count(event.correct), vars.t);
      return endLine(turn, vars);

    default:
      return '';
  }
}

/** One short line for the tutor to say, in speakable words. '' means stay quiet. */
export function tutorLine(event: TutorEvent, ctx: TutorContext): string {
  return tutorLineWith(event, ctx);
}

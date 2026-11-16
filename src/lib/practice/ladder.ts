// The topic ladder: Warm-up -> Build -> Challenge -> Exam.
//
// Pure and deterministic: no database, no clock, no randomness. Given the
// questions a topic has and the child's recorded answers on that topic, it says
// which step the child is on, how far through it they are, and which questions
// to prefer next. The picker (`src/lib/adaptive.ts`) does the reading and the
// choosing; this file only holds the rules.
//
// THE RULES
//  - Every question belongs to exactly one step. A question from a real past
//    paper is an Exam question whatever its difficulty; every other question is
//    Warm-up (Easy), Build (Medium) or Challenge (Hard).
//  - A step with no questions in this topic is skipped and shown as done. The
//    Exam step always exists: where the topic has fewer than EXAM_REAL_MIN real
//    paper questions it is "Exam-style" and is topped up with the hardest other
//    questions the topic has.
//  - Only the FIRST answer to each question counts, and only answers the caller
//    passes in (the picker passes the last LADDER_WINDOW_DAYS days).
//  - A step is finished after LADDER_NEEDED right answers at that step. They
//    need not be in a row: a slip does not wipe out what the child has shown.
//    A right answer on a question from a HIGHER step also counts (it is at
//    least as good as one at this step), which keeps the ladder moving when a
//    step has run out of fresh questions and the picker has moved on.
//  - LADDER_MISSES_TO_STEP_BACK answers in a row at the current step that are
//    not right send the child back one step for a short refresher
//    (LADDER_REFRESH_NEEDED right answers). On the lowest step there is nowhere
//    to go back to, so the child simply stays.
//  - A child who is already doing well (`startHigher`) starts on the step after
//    Warm-up. Nobody starts higher than that: the later steps are always earned.
//  - Once every step is finished the topic stays complete for as long as those
//    answers are inside the window.

import type { LadderInfo, LadderStep, LadderStepId } from './ladderTypes';

/** Right answers needed to finish a step. */
export const LADDER_NEEDED = 3;
/** Right answers needed on the refresher after stepping back. */
export const LADDER_REFRESH_NEEDED = 2;
/** Answers in a row at the current step that are not right before stepping back. */
export const LADDER_MISSES_TO_STEP_BACK = 3;
/** How far back the picker reads answers for the ladder. */
export const LADDER_WINDOW_DAYS = 30;
/** Fewer real paper questions than this and the last step is "Exam-style". */
export const EXAM_REAL_MIN = 3;
/** "Already doing well": at least this many recent answers... */
export const STRONG_START_MIN_ANSWERS = 5;
/** ...of which at least this share were right (the app's "Mastered" bar). */
export const STRONG_START_RATIO = 0.8;

export const EXAM_LABEL_REAL = 'Real exam';
export const EXAM_LABEL_LIKE = 'Exam-style';

const STEP_IDS: LadderStepId[] = ['warmup', 'build', 'challenge', 'exam'];
const STEP_LABELS: string[] = ['Warm-up', 'Build', 'Challenge', EXAM_LABEL_REAL];
const EXAM = 3;

// The real past papers held in the bank, by source name. Kept in step with
// PAST in scripts/audit/topic_classification.py.
const REAL_EXAM_SOURCE = /^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)\d{4}$/;

/** What the ladder needs to know about a question. */
export interface LadderQuestionMeta {
  difficulty: string;
  source: string;
}

/** One recorded answer on the topic. Pass them oldest first. */
export interface LadderAttempt extends LadderQuestionMeta {
  questionId: string;
  isCorrect: boolean;
}

export interface LadderInput {
  /** Child-facing topic name, e.g. "HCF & LCM". */
  topicLabel: string;
  /** Every servable question of the topic (seen or not). */
  pool: LadderQuestionMeta[];
  /** The child's answers on the topic inside the window, oldest first. */
  attempts: LadderAttempt[];
  /** The child is already doing well, so Warm-up is skipped. */
  startHigher?: boolean;
}

export interface LadderPlan {
  info: LadderInfo;
  /** Exam step: the difficulty (0 Easy, 1 Medium, 2 Hard) to try first. */
  examFirstRank: number;
  /** Hardest difficulty among the topic's non-exam questions, or -1 if it has none. */
  hardestLikeRank: number;
}

/** True for a question that came from a real past paper. */
export function isRealExamSource(source: string): boolean {
  return REAL_EXAM_SOURCE.test(source);
}

function diffRank(difficulty: string): number {
  if (difficulty === 'Easy') return 0;
  if (difficulty === 'Hard') return 2;
  return 1; // Medium, and anything unexpected
}

/** 0 Warm-up, 1 Build, 2 Challenge, 3 Exam. */
function stepRank(q: LadderQuestionMeta): number {
  return isRealExamSource(q.source) ? EXAM : diffRank(q.difficulty);
}

/** The step a question belongs to. */
export function stepOfQuestion(q: LadderQuestionMeta): LadderStepId {
  return STEP_IDS[stepRank(q)];
}

/**
 * "Already doing well", from the child's most recent answers before they began
 * this topic (newest first or oldest first, the order does not matter).
 */
export function isStrongStart(recentCorrect: boolean[]): boolean {
  if (recentCorrect.length < STRONG_START_MIN_ANSWERS) return false;
  let right = 0;
  for (let i = 0; i < recentCorrect.length; i++) if (recentCorrect[i]) right++;
  return right / recentCorrect.length >= STRONG_START_RATIO;
}

/**
 * Where the child is on the ladder. Null when the topic has no questions (then
 * there is no ladder to show).
 */
export function computeLadder(input: LadderInput): LadderPlan | null {
  const pool = input.pool;
  if (pool.length === 0) return null;

  const counts = [0, 0, 0, 0];
  let hardestLike = -1;
  for (let i = 0; i < pool.length; i++) {
    const r = stepRank(pool[i]);
    counts[r]++;
    if (r < EXAM) hardestLike = Math.max(hardestLike, r);
  }
  const active = [counts[0] > 0, counts[1] > 0, counts[2] > 0, true];

  function nextActive(from: number): number {
    for (let j = from + 1; j <= EXAM; j++) if (active[j]) return j;
    return -1;
  }
  function prevActive(from: number): number {
    for (let j = from - 1; j >= 0; j--) if (active[j]) return j;
    return -1;
  }
  /** The answer was on a question at the current step's own level. */
  function atStep(cur: number, a: LadderQuestionMeta): boolean {
    const r = stepRank(a);
    if (cur < EXAM) return r === cur;
    if (r === EXAM) return true;
    // Exam-style top-up: the hardest other questions the topic has.
    return hardestLike >= 0 && r >= hardestLike;
  }

  let cur = active[0] ? 0 : nextActive(0);
  if (input.startHigher && cur === 0) {
    const after = nextActive(0);
    // Skip Warm-up only: never straight into the Exam step.
    if (after !== -1 && after < EXAM) cur = after;
  }

  let got = 0;
  let needed = LADDER_NEEDED;
  let misses = 0;
  let complete = false;

  const counted = new Set<string>();
  for (let i = 0; i < input.attempts.length && !complete; i++) {
    const a = input.attempts[i];
    if (counted.has(a.questionId)) continue; // first answer only
    counted.add(a.questionId);

    const here = atStep(cur, a);
    if (a.isCorrect) {
      const above = cur < EXAM && stepRank(a) > cur;
      if (!here && !above) continue;
      got++;
      misses = 0;
      if (got >= needed) {
        const next = nextActive(cur);
        if (next === -1) {
          complete = true;
        } else {
          cur = next;
          got = 0;
          needed = LADDER_NEEDED;
        }
      }
    } else if (here) {
      misses++;
      if (misses >= LADDER_MISSES_TO_STEP_BACK) {
        misses = 0;
        const prev = prevActive(cur);
        if (prev !== -1) {
          cur = prev;
          got = 0;
          needed = LADDER_REFRESH_NEEDED;
        }
      }
    }
  }

  const examIsReal = counts[EXAM] >= EXAM_REAL_MIN;
  const steps: LadderStep[] = [];
  for (let i = 0; i <= EXAM; i++) {
    steps.push({
      id: STEP_IDS[i],
      label: i === EXAM ? (examIsReal ? EXAM_LABEL_REAL : EXAM_LABEL_LIKE) : STEP_LABELS[i],
      done: complete || i < cur || !active[i],
    });
  }

  // Exam step: start at the level the child last worked at and get harder with
  // each right answer. A topic that is nothing but exam questions therefore
  // still goes Easy -> Medium -> Hard.
  const before = prevActive(EXAM);
  const examBase = before === -1 ? 0 : before === 2 ? 2 : 1;
  const examFirstRank = Math.min(2, examBase + (cur === EXAM ? got : 0));

  return {
    info: { topicLabel: input.topicLabel, steps: steps, current: cur, got: got, needed: needed, complete: complete },
    examFirstRank: examFirstRank,
    hardestLikeRank: hardestLike,
  };
}

/**
 * The questions to choose from next, best group first. The picker takes the
 * first group and applies its usual source ranking inside it. Pass only the
 * questions that may be served (not seen recently); empty groups are dropped,
 * so when a step has run out the next group is the one to fall forward to.
 */
export function ladderTiers<T extends LadderQuestionMeta>(plan: LadderPlan, questions: T[]): T[][] {
  const byRank: T[][] = [[], [], [], []];
  for (let i = 0; i < questions.length; i++) byRank[stepRank(questions[i])].push(questions[i]);

  const tiers: T[][] = [];
  const cur = plan.info.current;
  if (cur < EXAM) {
    // This step, then harder steps, then (last resort) easier ones, nearest first.
    for (let r = cur; r <= EXAM; r++) tiers.push(byRank[r]);
    for (let r = cur - 1; r >= 0; r--) tiers.push(byRank[r]);
  } else {
    // Real paper questions: the preferred difficulty, then harder, then easier.
    const first = plan.examFirstRank;
    const order: number[] = [first];
    for (let d = first + 1; d <= 2; d++) order.push(d);
    for (let d = first - 1; d >= 0; d--) order.push(d);
    for (let k = 0; k < order.length; k++) {
      const want = order[k];
      tiers.push(byRank[EXAM].filter((q) => diffRank(q.difficulty) === want));
    }
    // Exam-style: the hardest of the rest.
    for (let r = 2; r >= 0; r--) tiers.push(byRank[r]);
  }
  return tiers.filter((t) => t.length > 0);
}

/**
 * Make the Exam step's name honest about the question being served: it says
 * "Real exam" only while the question on screen is from a real paper.
 */
export function withServedQuestion(info: LadderInfo, servedIsRealExam: boolean): LadderInfo {
  if (info.current !== EXAM) return info;
  const label = servedIsRealExam ? EXAM_LABEL_REAL : EXAM_LABEL_LIKE;
  if (info.steps[EXAM].label === label) return info;
  const steps = info.steps.map((s, i) => (i === EXAM ? { id: s.id, label: label, done: s.done } : s));
  return { ...info, steps: steps };
}

/**
 * The ladder as it will look once the child's answer to the question on screen
 * is recorded. For the practice screen: the ladder that arrives with a question
 * was worked out BEFORE that question was answered, so the screen can call this
 * to move the strip straight away. The server remains the source of truth; the
 * next question brings the real ladder. (Stepping back is left to the server.)
 */
export function ladderAfterAnswer(info: LadderInfo, wasCorrect: boolean): LadderInfo {
  if (!wasCorrect || info.complete) return info;
  const got = info.got + 1;
  if (got < info.needed) return { ...info, got: got };

  const steps = info.steps.map((s, i) => (i === info.current ? { id: s.id, label: s.label, done: true } : s));
  let next = -1;
  for (let j = info.current + 1; j < steps.length; j++) {
    if (!steps[j].done) {
      next = j;
      break;
    }
  }
  if (next === -1) {
    return { ...info, steps: steps.map((s) => ({ id: s.id, label: s.label, done: true })), got: info.needed, complete: true };
  }
  return { ...info, steps: steps, current: next, got: 0, needed: LADDER_NEEDED };
}

// ── Questions whose topic is only in their id ────────────────────────────────
// 444 Grade 5 questions carry the sub-topic label "Auto-generated variant",
// which matches no topic key, so topic practice could never reach them. Their
// family is in the id (VAR_G5_vary_<family>_V<n>). Until the labels are
// repaired in the data, the ladder reaches them by id.
const VARIANT_FAMILIES: { [gradeAndKey: string]: string[] } = {
  '5:bodmas': ['bodmas'],
  '5:angle': ['angles'],
  '5:money': ['percentage'],
  '5:equation': ['equation'],
  '5:area': ['perimeter_area'],
  '5:hcf': ['hcf_lcm'],
  '5:interest': ['simple_interest'],
  '5:fraction': ['fraction_arithmetic'],
};

/** Id prefixes of generated questions that belong to a topic key (often none). */
export function variantIdPrefixes(grade: number, subTopicKey: string): string[] {
  const families = VARIANT_FAMILIES[grade + ':' + subTopicKey.toLowerCase()] || [];
  return families.map((f) => 'VAR_G' + grade + '_vary_' + f + '_V');
}

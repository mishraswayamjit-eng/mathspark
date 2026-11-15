/**
 * What the tutor says in reaction to something the child does.
 *
 * Outside teach mode the tutor does not lecture: it reacts. This module turns
 * an event (a right answer, a miss, a hint opened, a long pause) into one short
 * spoken line. It is deterministic: no AI model is called, so a reaction is
 * instant and can never judge an answer. Whether an answer is right is decided
 * elsewhere and passed in.
 *
 * PLACEHOLDER: the real reaction library replaces the body of `tutorLine`. The
 * exported types and the function signature are the contract other screens
 * build on, so they must not change.
 */

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

/** One short line for the tutor to say, in speakable words. '' means stay quiet. */
export function tutorLine(event: TutorEvent, ctx: TutorContext): string {
  void ctx;
  switch (event.kind) {
    case 'correct': return 'You got it!';
    case 'miss': return 'Not quite. Have another look.';
    default: return '';
  }
}

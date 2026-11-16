// The shape of "where am I in this topic", shared by the server (which works it
// out) and the practice screen (which shows it). Types only: safe to import
// from client components.

/** The four steps of a topic, in order. The last is real exam questions. */
export type LadderStepId = 'warmup' | 'build' | 'challenge' | 'exam';

export interface LadderStep {
  id: LadderStepId;
  /** Short child-facing name, e.g. "Warm-up". */
  label: string;
  /** Finished: the child has got enough right at this step. */
  done: boolean;
}

export interface LadderInfo {
  /** The topic the ladder is for, e.g. "HCF & LCM". */
  topicLabel: string;
  /** All four steps, in order. */
  steps: LadderStep[];
  /** Index into `steps` of the step the child is on now (0-3). */
  current: number;
  /** Right answers so far at the current step. */
  got: number;
  /** Right answers needed to finish the current step. */
  needed: number;
  /** True when every step is done. */
  complete: boolean;
}

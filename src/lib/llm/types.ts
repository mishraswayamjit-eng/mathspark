import type { ModelKey } from './models';

/** A single turn in a conversation sent to the model. */
export interface LlmMessage {
  role: 'user' | 'assistant';
  content: string;
}

/** Feature identifiers for per-feature usage accounting + caching. */
export type LlmFeature =
  | 'chat'
  | 'misconception'
  | 'session-narrative'
  | 'report-narrative'
  | 'lesson-reexplain'
  | 'stuck-coach'
  | 'solve'
  | 'surface'
  | 'author';

/** Options shared by both streaming and non-streaming completions. */
export interface CompletionOptions {
  model: ModelKey;
  system: string;
  messages: LlmMessage[];
  maxTokens: number;
  temperature?: number;
}

/** Result of a non-streaming completion. */
export interface CompletionResult {
  text: string;
  /** True when the model stopped for a reason other than `end_turn`. */
  truncated: boolean;
}

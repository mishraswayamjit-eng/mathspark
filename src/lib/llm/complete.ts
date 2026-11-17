import type Anthropic from '@anthropic-ai/sdk';
import { getAnthropicClient } from './client';
import { MODELS, type ModelKey } from './models';
import type { CompletionOptions, CompletionResult } from './types';

/**
 * Non-streaming completion. Returns the full text + a `truncated` flag.
 * Throws {@link LlmNotConfiguredError} if no API key, or the SDK error on
 * network/API failure — callers decide whether to fall back.
 */
export async function complete(opts: CompletionOptions): Promise<CompletionResult> {
  const anthropic = getAnthropicClient();
  const res = await anthropic.messages.create({
    model: MODELS[opts.model],
    max_tokens: opts.maxTokens,
    ...(opts.temperature !== undefined ? { temperature: opts.temperature } : {}),
    system: opts.system,
    messages: opts.messages,
  });

  const text = res.content
    .filter((b): b is Anthropic.TextBlock => b.type === 'text')
    .map((b) => b.text)
    .join('');

  return { text, truncated: res.stop_reason !== 'end_turn' };
}

/** Options for the tutor chat stream: block-based system prompt and messages (text + images). */
export interface ChatStreamOptions {
  model: ModelKey;
  /** System prompt as blocks so the stable part can carry `cache_control`. */
  system: Anthropic.TextBlockParam[];
  messages: Anthropic.MessageParam[];
  maxTokens: number;
}

export interface StreamCallbacks {
  /** Called once the full text is known (stream finished or errored). */
  onComplete?: (text: string, truncated: boolean) => void | Promise<void>;
  /** Fallback text emitted to the client if the stream errors mid-flight. */
  onErrorFallback?: string;
  /** Optional error sink (logging). */
  onError?: (err: unknown) => void;
  /** Text shown if the model declines to answer or produces no text at all. */
  onEmptyFallback?: string;
  /**
   * Chat only: a short line added to the end of a reply that stopped part-way
   * (out of room, or the call broke off after some text had streamed).
   */
  onCutOffNote?: string;
}

/**
 * How long a chat reply may take in all. Under the route's 60 second limit, so
 * what has streamed can still be saved.
 */
const CHAT_DEADLINE_MS = 50_000;

/**
 * Build a `ReadableStream<Uint8Array>` of plain-text deltas for a completion.
 * Extracted from the original `chat/route.ts` streaming loop so there is one
 * code path. `onComplete` fires after the stream closes (persist the message).
 */
export function streamCompletion(
  opts: CompletionOptions,
  callbacks: StreamCallbacks = {},
): ReadableStream<Uint8Array> {
  const encoder = new TextEncoder();

  return new ReadableStream<Uint8Array>({
    async start(controller) {
      let fullResponse = '';
      let truncated = false;
      try {
        const anthropic = getAnthropicClient();
        const stream = anthropic.messages.stream({
          model: MODELS[opts.model],
          max_tokens: opts.maxTokens,
          ...(opts.temperature !== undefined ? { temperature: opts.temperature } : {}),
          system: opts.system,
          messages: opts.messages,
        });

        for await (const event of stream) {
          if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
            fullResponse += event.delta.text;
            controller.enqueue(encoder.encode(event.delta.text));
          } else if (
            event.type === 'message_delta' &&
            event.delta.stop_reason &&
            event.delta.stop_reason !== 'end_turn'
          ) {
            truncated = true;
          }
        }

        await callbacks.onComplete?.(fullResponse, truncated);
      } catch (err) {
        callbacks.onError?.(err);
        if (callbacks.onErrorFallback) {
          controller.enqueue(encoder.encode(callbacks.onErrorFallback));
          await callbacks.onComplete?.(callbacks.onErrorFallback, true);
        }
      } finally {
        controller.close();
      }
    },
  });
}

/**
 * Streaming for the tutor chat (`/api/chat`).
 *
 * Differs from `streamCompletion` in three ways: the system prompt and the
 * messages are content blocks (so the stable prompt can be cached and a turn
 * can carry a photo), no `temperature` is sent (Claude Opus 5.5 rejects it),
 * and a reply with no text (a decline, or the token budget spent on thinking)
 * shows a friendly fallback instead of an empty bubble.
 *
 * Uses the raw event stream rather than the SDK's accumulating helper: this
 * SDK version predates thinking blocks, and the raw stream simply passes event
 * types it does not know about, of which we only read the text deltas.
 */
export function streamChat(
  opts: ChatStreamOptions,
  callbacks: StreamCallbacks = {},
): ReadableStream<Uint8Array> {
  const encoder = new TextEncoder();

  return new ReadableStream<Uint8Array>({
    async start(controller) {
      let fullResponse = '';
      let truncated = false;
      let ranOutOfRoom = false;
      // The reader may have gone (the child left the page). Carry on regardless,
      // so the reply is still saved and is there when they come back.
      const send = (text: string) => {
        try {
          controller.enqueue(encoder.encode(text));
        } catch {
          // Nobody is reading any more.
        }
      };
      // One clock for the whole reply (connecting, a retry, and the stream itself),
      // so we stop and save what we have before the platform stops us.
      const deadline = new AbortController();
      const timer = setTimeout(() => deadline.abort(), CHAT_DEADLINE_MS);
      try {
        const anthropic = getAnthropicClient();
        const stream = await anthropic.messages.create(
          {
            model: MODELS[opts.model],
            max_tokens: opts.maxTokens,
            system: opts.system,
            messages: opts.messages,
            stream: true,
          },
          { timeout: CHAT_DEADLINE_MS, maxRetries: 1, signal: deadline.signal },
        );

        for await (const event of stream) {
          if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
            fullResponse += event.delta.text;
            send(event.delta.text);
          } else if (event.type === 'message_delta' && event.delta.stop_reason) {
            // Newer stop reasons (e.g. "refusal") are not in this SDK's type union.
            const reason = String(event.delta.stop_reason);
            if (reason !== 'end_turn') truncated = true;
            if (reason === 'max_tokens') ranOutOfRoom = true;
          }
        }

        if (!fullResponse.trim() && callbacks.onEmptyFallback) {
          fullResponse = callbacks.onEmptyFallback;
          truncated = true;
          send(fullResponse);
        } else if (ranOutOfRoom && callbacks.onCutOffNote) {
          // The reply stopped mid-thought: say so, and offer to go on.
          const note = `\n\n${callbacks.onCutOffNote}`;
          fullResponse += note;
          send(note);
        }

        await callbacks.onComplete?.(fullResponse, truncated);
      } catch (err) {
        callbacks.onError?.(err);
        if (callbacks.onErrorFallback) {
          if (fullResponse.trim()) {
            // Part of a reply already streamed: close it kindly on a new line, and
            // save what the child saw (marked as cut short) so the next turn can
            // pick up from it.
            const note = `\n\n${callbacks.onCutOffNote || callbacks.onErrorFallback}`;
            send(note);
            if (callbacks.onCutOffNote) fullResponse += note;
            await callbacks.onComplete?.(fullResponse, true);
          } else {
            // Nothing came through: only then is the fallback line what gets saved.
            send(callbacks.onErrorFallback);
            await callbacks.onComplete?.(callbacks.onErrorFallback, true);
          }
        }
      } finally {
        clearTimeout(timer);
        try {
          controller.close();
        } catch {
          // Already closed by the reader going away.
        }
      }
    },
  });
}

import type Anthropic from '@anthropic-ai/sdk';
import { getAnthropicClient } from './client';
import { MODELS } from './models';
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

export interface StreamCallbacks {
  /** Called once the full text is known (stream finished or errored). */
  onComplete?: (text: string, truncated: boolean) => void | Promise<void>;
  /** Fallback text emitted to the client if the stream errors mid-flight. */
  onErrorFallback?: string;
  /** Optional error sink (logging). */
  onError?: (err: unknown) => void;
}

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

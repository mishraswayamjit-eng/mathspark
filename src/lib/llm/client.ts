import Anthropic from '@anthropic-ai/sdk';

/**
 * Typed error thrown when the LLM is called without an API key configured.
 * Callers catch this to fall back to static content / a 503 response.
 */
export class LlmNotConfiguredError extends Error {
  constructor() {
    super('ANTHROPIC_API_KEY is not set');
    this.name = 'LlmNotConfiguredError';
  }
}

let client: Anthropic | null = null;

/**
 * Lazily construct a single shared Anthropic client.
 * Throws {@link LlmNotConfiguredError} if the API key is missing.
 */
export function getAnthropicClient(): Anthropic {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new LlmNotConfiguredError();
  if (!client) client = new Anthropic({ apiKey });
  return client;
}

/** True when an API key is present (cheap pre-check before attempting a call). */
export function isLlmConfigured(): boolean {
  return Boolean(process.env.ANTHROPIC_API_KEY);
}

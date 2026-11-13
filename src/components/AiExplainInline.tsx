'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import Sparky from '@/components/Sparky';

interface AiExplainInlineProps {
  /** Streaming endpoint (POST, text/plain stream). */
  endpoint: string;
  /** JSON body sent to the endpoint. */
  body: Record<string, unknown>;
  /** Label for the trigger button. */
  buttonLabel: string;
  /** Small heading shown above the streamed text once started. */
  heading?: string;
  /** Start streaming automatically on mount (used by stuck-coach). */
  autoStart?: boolean;
  className?: string;
}

/**
 * Reusable inline streaming display for grounded AI explanations.
 * Shared by Feature 1 (stuck-coach) and Feature 3 (lesson re-explain).
 * Degrades gracefully: on any error it shows a friendly line and the trigger
 * stays available for a retry.
 */
export default function AiExplainInline({
  endpoint,
  body,
  buttonLabel,
  heading,
  autoStart = false,
  className = '',
}: AiExplainInlineProps) {
  const [text, setText] = useState('');
  const [state, setState] = useState<'idle' | 'loading' | 'done' | 'error'>('idle');
  const startedRef = useRef(false);

  const run = useCallback(async () => {
    if (startedRef.current) return;
    startedRef.current = true;
    setState('loading');
    setText('');
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok || !res.body) {
        setState('error');
        return;
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let acc = '';
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        acc += decoder.decode(value, { stream: true });
        setText(acc);
      }
      setState('done');
    } catch {
      setState('error');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endpoint]);

  useEffect(() => {
    if (autoStart) void run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoStart]);

  if (state === 'idle') {
    return (
      <button
        onClick={() => void run()}
        className={`w-full min-h-[48px] rounded-control border-2 border-ink bg-white text-ink font-extrabold text-sm shadow-hard-sm flex items-center justify-center gap-2 active:scale-[0.98] transition-transform ${className}`}
      >
        <span aria-hidden="true">💬</span> {buttonLabel}
      </button>
    );
  }

  return (
    <div className={`bg-soft border-2 border-line rounded-card px-4 py-3 ${className}`}>
      <div className="flex items-center gap-2 mb-1.5">
        <Sparky mood={state === 'loading' ? 'thinking' : 'encouraging'} size={28} />
        <p className="text-caption text-ink">
          {heading ?? 'Sparky explains'}
        </p>
      </div>

      {state === 'error' ? (
        <p className="text-sm text-ink font-semibold">
          I&apos;m having a little trouble right now! 🤔 Please try again in a moment.
        </p>
      ) : (
        <p className="text-sm text-ink font-semibold leading-snug whitespace-pre-wrap">
          {text}
          {state === 'loading' && <span className="animate-pulse">▍</span>}
        </p>
      )}
    </div>
  );
}

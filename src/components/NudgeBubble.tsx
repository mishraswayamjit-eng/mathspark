'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import type { Nudge } from '@/lib/nudges';

interface Props {
  nudge:     Nudge;
  onDismiss: () => void;
}

export default function NudgeBubble({ nudge, onDismiss }: Props) {
  const router  = useRouter();
  const [gone, setGone] = useState(false);
  const onDismissRef = useRef(onDismiss);
  onDismissRef.current = onDismiss;
  const dismissTimerRef = useRef<ReturnType<typeof setTimeout>>();

  const dismiss = useCallback(() => {
    setGone(true);
    dismissTimerRef.current = setTimeout(() => onDismissRef.current(), 280);
  }, []);

  // Auto-dismiss after 8 s
  useEffect(() => {
    const t = setTimeout(dismiss, 8000);
    return () => { clearTimeout(t); clearTimeout(dismissTimerRef.current); };
  }, [dismiss]);

  function handleAction() {
    dismiss();
    if (nudge.actionPath) router.push(nudge.actionPath);
  }

  return (
    <div
      className={`fixed top-16 left-1/2 z-40 w-[calc(100%-2rem)] max-w-lg transition-[opacity,transform] duration-280 ${
        gone
          ? 'opacity-0 -translate-y-3 pointer-events-none'
          : 'animate-slide-down opacity-100'
      }`}
      style={{ transform: `translateX(-50%) ${gone ? 'translateY(-12px)' : ''}` }}
    >
      <div className="bg-white rounded-card border-2 border-ink shadow-hard p-4 flex items-start gap-3">
        {/* Sparky mascot */}
        <div className="flex-shrink-0 animate-sparky-bounce">
          <Sparky mood={nudge.mood} size={52} />
        </div>

        {/* Message */}
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-ink text-sm leading-snug">
            {nudge.message}
          </p>
          {nudge.subtext && (
            <p className="text-xs text-ink-muted font-semibold mt-0.5">
              {nudge.subtext}
            </p>
          )}
          {nudge.actionLabel && (
            <button
              onClick={handleAction}
              className="mt-2 bg-action text-white text-xs font-extrabold rounded-full border-2 border-ink px-4 py-1.5 active:scale-95 transition-transform"
              style={{ minHeight: 0 }}
            >
              {nudge.actionLabel}
            </button>
          )}
        </div>

        {/* Dismiss */}
        <button
          onClick={dismiss}
          className="flex-shrink-0 text-ink-muted hover:text-ink font-bold leading-none text-xl"
          style={{ minHeight: 0 }}
          aria-label="Dismiss"
        >
          ×
        </button>
      </div>
    </div>
  );
}

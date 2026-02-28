'use client';

import { useEffect, useState, useCallback } from 'react';
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

  const dismiss = useCallback(() => {
    setGone(true);
    setTimeout(onDismiss, 280);
  }, [onDismiss]);

  // Auto-dismiss after 8 s
  useEffect(() => {
    const t = setTimeout(dismiss, 8000);
    return () => clearTimeout(t);
  }, [dismiss]);

  function handleAction() {
    dismiss();
    if (nudge.actionPath) router.push(nudge.actionPath);
  }

  return (
    <div
      className={`fixed top-16 left-1/2 z-40 w-[calc(100%-2rem)] max-w-lg transition-all duration-280 ${
        gone
          ? 'opacity-0 -translate-y-3 pointer-events-none'
          : 'animate-slide-down opacity-100'
      }`}
      style={{ transform: `translateX(-50%) ${gone ? 'translateY(-12px)' : ''}` }}
    >
      <div className="bg-white rounded-2xl shadow-2xl border border-gray-100 p-4 flex items-start gap-3">
        {/* Sparky mascot */}
        <div className="flex-shrink-0 animate-sparky-bounce">
          <Sparky mood={nudge.mood} size={52} />
        </div>

        {/* Message */}
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-gray-800 text-sm leading-snug">
            {nudge.message}
          </p>
          {nudge.subtext && (
            <p className="text-xs text-gray-400 font-medium mt-0.5">
              {nudge.subtext}
            </p>
          )}
          {nudge.actionLabel && (
            <button
              onClick={handleAction}
              className="mt-2 bg-[#58CC02] text-white text-xs font-extrabold rounded-full px-4 py-1.5 active:scale-95 transition-transform"
              style={{ minHeight: 0 }}
            >
              {nudge.actionLabel}
            </button>
          )}
        </div>

        {/* Dismiss */}
        <button
          onClick={dismiss}
          className="flex-shrink-0 text-gray-300 hover:text-gray-500 font-bold leading-none text-xl"
          style={{ minHeight: 0 }}
          aria-label="Dismiss"
        >
          ×
        </button>
      </div>
    </div>
  );
}

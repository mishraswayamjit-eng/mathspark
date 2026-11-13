'use client';

import { useEffect } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';

interface ReadAloudButtonProps {
  /** Speakable text (already converted with mathToSpeech). */
  text: string;
  /** Optional pre-recorded narration to play instead of the browser voice. */
  audioSrc?: string;
  /** What is being read, for screen readers: "question", "hint". */
  label?: string;
}

/** Speaker button: tap to hear the text, tap again to stop. Hidden where speech is unavailable. */
export default function ReadAloudButton({ text, audioSrc, label = 'this' }: ReadAloudButtonProps) {
  const { speak, stop, speaking, supported } = useReadAloud();

  // A new question or hint replaces the text: stop reading the old one.
  useEffect(() => {
    stop();
  }, [text, stop]);

  if (!supported || !text) return null;

  return (
    <button
      type="button"
      onClick={() => (speaking ? stop() : speak(text, { audioSrc }))}
      aria-label={speaking ? 'Stop reading' : `Read ${label} aloud`}
      aria-pressed={speaking}
      className={`w-12 h-12 flex-shrink-0 rounded-tile border-2 flex items-center justify-center text-xl transition-colors ${
        speaking ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink hover:border-ink'
      }`}
    >
      <span aria-hidden="true">{speaking ? '⏹' : '🔊'}</span>
    </button>
  );
}

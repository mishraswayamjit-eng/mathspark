'use client';

import { useCallback, useState } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';
import { tutorLine, type TutorContext, type TutorEvent } from '@/lib/tutor/reactions';

export interface TutorVoice {
  /** React to something the child did: picks a line and says it (when the voice is on). Returns the line. */
  react: (event: TutorEvent, ctx: TutorContext) => string;
  /** Say any line as the tutor. */
  say: (text: string) => void;
  stop: () => void;
  /** True while the tutor is talking. */
  speaking: boolean;
  /** Whether the tutor talks at all. Remembered on the device. */
  enabled: boolean;
  setEnabled: (on: boolean) => void;
  /** The last line the tutor said, for showing as a caption. */
  lastLine: string;
}

/**
 * The tutor's voice for a screen.
 *
 * PLACEHOLDER: the real hook replaces the body. The exported name, the
 * `TutorVoice` shape and the default behaviour (off does nothing, one line at
 * a time) are the contract other screens build on, so they must not change.
 */
export function useTutorVoice(): TutorVoice {
  const { speak, stop, speaking } = useReadAloud();
  const [enabled, setEnabled] = useState(true);
  const [lastLine, setLastLine] = useState('');

  const say = useCallback((text: string) => {
    if (!text) return;
    setLastLine(text);
    if (enabled) speak(text);
  }, [enabled, speak]);

  const react = useCallback((event: TutorEvent, ctx: TutorContext) => {
    const line = tutorLine(event, ctx);
    say(line);
    return line;
  }, [say]);

  return { react, say, stop, speaking, enabled, setEnabled, lastLine };
}

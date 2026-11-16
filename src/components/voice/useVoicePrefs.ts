'use client';

import { useCallback, useEffect, useState } from 'react';
import { DEFAULT_SPEED_ID, DEFAULT_VOICE_ID } from '@/lib/speech/voices';
import { getVoicePrefs, setVoicePrefs, subscribeVoicePrefs, type VoicePrefs } from '@/lib/speech/voicePrefs';

/**
 * The child's chosen voice and speed, kept up to date while the screen is open.
 * Starts from the defaults (so the server and the browser draw the same thing
 * first) and reads the saved choice once mounted.
 */
export function useVoicePrefs() {
  const [prefs, setPrefs] = useState<VoicePrefs>({ voiceId: DEFAULT_VOICE_ID, speedId: DEFAULT_SPEED_ID });

  useEffect(() => {
    setPrefs(getVoicePrefs());
    return subscribeVoicePrefs(setPrefs);
  }, []);

  const chooseVoice = useCallback((voiceId: string) => {
    setVoicePrefs({ voiceId });
  }, []);

  const chooseSpeed = useCallback((speedId: string) => {
    setVoicePrefs({ speedId });
  }, []);

  return { voiceId: prefs.voiceId, speedId: prefs.speedId, chooseVoice, chooseSpeed };
}

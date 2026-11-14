'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';
import { toSpeech } from '@/lib/speech/mathToSpeech';

/**
 * Voice conversation with Sparky: listen → send what was heard → speak the
 * reply → listen again, until the child taps stop.
 *
 * Listening uses the browser's speech recognition (Indian English). Speaking
 * uses Sarvam through /api/voice/tts when that is configured, otherwise the
 * device's own voice. Nothing is recorded or stored by the app.
 */

export type VoiceState = 'off' | 'listening' | 'thinking' | 'speaking';

// After this many listens in a row with nothing heard, voice mode switches itself off.
const MAX_SILENT_TURNS = 3;

export function useVoiceLoop(send: (text: string) => Promise<string | null>) {
  const { speak, stop: stopSpeaking, speaking } = useReadAloud();

  const [state,     setState]     = useState<VoiceState>('off');
  const [heard,     setHeard]     = useState('');
  const [notice,    setNotice]    = useState('');
  const [supported, setSupported] = useState(false);
  // True while the Sarvam audio for a reply is being fetched (nothing is playing yet).
  const [fetchingVoice, setFetchingVoice] = useState(false);

  const activeRef      = useRef(false);                       // is the loop switched on?
  const recRef         = useRef<SpeechRecognition | null>(null);
  const silentTurnsRef = useRef(0);
  const serverVoiceRef = useRef(true);                        // try Sarvam until it says it is unavailable
  const speakTurnRef   = useRef(0);                           // id of the reply being spoken
  const heardSoundRef  = useRef(false);                       // did the current reply actually start playing?
  const speakWordsRef  = useRef(0);                           // length of the reply being spoken, in words
  const sendRef        = useRef(send);
  sendRef.current = send;
  const listenRef      = useRef<() => void>(() => {});

  useEffect(() => {
    setSupported(typeof window !== 'undefined' && Boolean(window.SpeechRecognition || window.webkitSpeechRecognition));
  }, []);

  const stop = useCallback(() => {
    activeRef.current = false;
    speakTurnRef.current += 1;
    if (recRef.current) {
      try { recRef.current.abort(); } catch { /* already stopped */ }
      recRef.current = null;
    }
    stopSpeaking();
    setFetchingVoice(false);
    setHeard('');
    setState('off');
  }, [stopSpeaking]);

  /** Called once per spoken reply, however it ended: go back to listening. */
  const afterSpeaking = useCallback((turn: number) => {
    if (speakTurnRef.current !== turn) return;   // already handled, or the loop was stopped
    speakTurnRef.current += 1;
    if (activeRef.current) listenRef.current();
  }, []);

  const speakReply = useCallback(async (reply: string) => {
    const text = toSpeech(reply);
    if (!text) { listenRef.current(); return; }

    const turn = speakTurnRef.current;
    heardSoundRef.current = false;
    speakWordsRef.current = text.split(/\s+/).length;
    setFetchingVoice(true);
    setState('speaking');

    // Sarvam voice when the server has it; a data URL keeps the audio in memory only.
    let audioSrc: string | undefined;
    if (serverVoiceRef.current) {
      try {
        const res = await fetch('/api/voice/tts', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ text }),
        });
        if (res.ok) {
          const data = (await res.json()) as { audio?: string; mime?: string };
          if (data.audio) audioSrc = `data:${data.mime || 'audio/mpeg'};base64,${data.audio}`;
        } else if (res.status === 503 || res.status === 404) {
          serverVoiceRef.current = false;        // not configured here: stop asking
        }
      } catch {
        /* network trouble: the device voice below still works */
      }
    }
    setFetchingVoice(false);
    if (!activeRef.current || speakTurnRef.current !== turn) return;

    speak(text, {
      audioSrc,
      onStart: () => { heardSoundRef.current = true; },
      onEnd: () => afterSpeaking(turn),
    });
  }, [speak, afterSpeaking]);

  // Safety nets, so the loop never gets stuck on "speaking":
  // 1. speaking stopped without a natural end (interrupted, audio failed);
  useEffect(() => {
    if (state !== 'speaking' || fetchingVoice || speaking) return;
    const turn = speakTurnRef.current;
    const timer = setTimeout(() => afterSpeaking(turn), 500);
    return () => clearTimeout(timer);
  }, [state, fetchingVoice, speaking, afterSpeaking]);
  // 2. the browser accepted the reply but never made a sound (some block speech
  //    that does not start directly from a tap).
  useEffect(() => {
    if (state !== 'speaking' || fetchingVoice) return;
    const turn = speakTurnRef.current;
    const timer = setTimeout(() => {
      if (!heardSoundRef.current) afterSpeaking(turn);
    }, 5000);
    return () => clearTimeout(timer);
  }, [state, fetchingVoice, afterSpeaking]);
  // 3. the voice started and then died without telling us (desktop Chrome cuts
  //    long utterances this way): give up after a generous time for its length.
  useEffect(() => {
    if (state !== 'speaking' || fetchingVoice) return;
    const turn = speakTurnRef.current;
    const limitMs = Math.min(180000, 10000 + speakWordsRef.current * 700);
    const timer = setTimeout(() => {
      if (speakTurnRef.current !== turn) return;
      stopSpeaking();
      afterSpeaking(turn);
    }, limitMs);
    return () => clearTimeout(timer);
  }, [state, fetchingVoice, afterSpeaking, stopSpeaking]);

  const listen = useCallback(() => {
    if (!activeRef.current) return;
    const Ctor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Ctor) return;

    let finalText = '';
    let blocked = false;
    const rec = new Ctor();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = 'en-IN';

    rec.onresult = (event: SpeechRecognitionEvent) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) finalText += `${result[0].transcript} `;
        else interim += result[0].transcript;
      }
      setHeard(`${finalText}${interim}`.trim());
    };

    rec.onerror = (event: Event) => {
      const code = (event as Event & { error?: string }).error;
      if (code === 'not-allowed' || code === 'service-not-allowed') blocked = true;
    };

    rec.onend = () => {
      recRef.current = null;
      if (!activeRef.current) return;

      if (blocked) {
        setNotice('I need the microphone to hear you. Ask a grown-up to allow it, then tap the mic again.');
        stop();
        return;
      }

      const said = finalText.trim();
      if (!said) {
        silentTurnsRef.current += 1;
        if (silentTurnsRef.current >= MAX_SILENT_TURNS) {
          setNotice("I couldn't hear anything, so I've stopped listening. Tap the mic to talk again.");
          stop();
        } else {
          listenRef.current();
        }
        return;
      }

      silentTurnsRef.current = 0;
      setState('thinking');
      sendRef.current(said)
        .then((reply) => {
          setHeard('');
          if (!activeRef.current) return;
          if (reply) {
            speakReply(reply);
          } else {
            // No reply came back (daily limit, logged out, not set up, or a network
            // problem). Listening again would only resend into the same wall.
            setNotice("I couldn't answer just then, so I've stopped listening. Tap the mic to try again.");
            stop();
          }
        })
        .catch(() => {
          if (!activeRef.current) return;
          setNotice("I couldn't answer just then, so I've stopped listening. Tap the mic to try again.");
          stop();
        });
    };

    recRef.current = rec;
    setHeard('');
    setState('listening');
    try {
      rec.start();
    } catch {
      recRef.current = null;
      setNotice("I couldn't start listening on this device.");
      stop();
    }
  }, [speakReply, stop]);

  listenRef.current = listen;

  /** Must be called from a tap, so the browser allows the microphone and the voice. */
  const start = useCallback(() => {
    if (!supported || activeRef.current) return;
    setNotice('');
    silentTurnsRef.current = 0;
    activeRef.current = true;
    listenRef.current();
  }, [supported]);

  // Leave nothing listening or talking behind when the chat closes.
  useEffect(() => {
    return () => {
      activeRef.current = false;
      if (recRef.current) {
        try { recRef.current.abort(); } catch { /* already stopped */ }
      }
    };
  }, []);

  return { supported, state, heard, notice, start, stop };
}

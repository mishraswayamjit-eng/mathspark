'use client';

import { useCallback, useEffect, useState } from 'react';

function getAudioContext(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  try {
    return new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
  } catch {
    return null;
  }
}

function playTone(ctx: AudioContext, freq: number, startTime: number, duration: number, volume = 0.18) {
  const osc  = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.type = 'sine';
  osc.frequency.setValueAtTime(freq, startTime);
  gain.gain.setValueAtTime(volume, startTime);
  gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
  osc.start(startTime);
  osc.stop(startTime + duration + 0.01);
}

export function useSounds() {
  const [muted, setMuted] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setMuted(localStorage.getItem('mathspark_muted') === 'true');
    }
  }, []);

  const toggleMute = useCallback(() => {
    setMuted((prev) => {
      const next = !prev;
      localStorage.setItem('mathspark_muted', String(next));
      return next;
    });
  }, []);

  const playCorrect = useCallback(() => {
    if (muted) return;
    const ctx = getAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    // C5 → E5 → G5 ascending triad
    playTone(ctx, 523.25, t,        0.08);
    playTone(ctx, 659.25, t + 0.09, 0.08);
    playTone(ctx, 783.99, t + 0.18, 0.12);
  }, [muted]);

  const playWrong = useCallback(() => {
    if (muted) return;
    const ctx = getAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    // Bb4 → G4 descending minor
    playTone(ctx, 466.16, t,       0.2,  0.12);
    playTone(ctx, 392.00, t + 0.22, 0.2, 0.10);
  }, [muted]);

  const playStreak = useCallback(() => {
    if (muted) return;
    const ctx = getAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    // Rapid ascending dings ×5
    const freqs = [523.25, 587.33, 659.25, 698.46, 783.99];
    freqs.forEach((f, i) => playTone(ctx, f, t + i * 0.07, 0.06, 0.15));
  }, [muted]);

  return { playCorrect, playWrong, playStreak, muted, toggleMute };
}

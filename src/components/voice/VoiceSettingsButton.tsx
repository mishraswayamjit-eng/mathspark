'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import VoicePicker from './VoicePicker';

const FOCUSABLE = 'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

/**
 * A 48px button that opens the voice picker in a sheet at the bottom of the
 * screen. Every prop is optional, so any screen can drop it in.
 *
 * `tone="dark"` draws the button for a dark (ink) header bar. Passing
 * `voiceOn` + `onVoiceOnChange` puts a "Sparky talks" switch at the top of the
 * sheet and makes the button's icon show whether the voice is on;
 * `soundsOn` + `onSoundsOnChange` adds a "Sound effects" switch under it.
 *
 * The sheet is a modal dialog: Escape, the backdrop and the Done button close
 * it; focus moves into it when it opens, stays inside it while it is open, and
 * goes back to the button when it closes. It is drawn at the end of the page
 * body, so it sits above whatever screen the button was placed on.
 */
interface VoiceSettingsButtonProps {
  /** 'light' (default): for a white or paper surface. 'dark': for the ink header bar. */
  tone?: 'light' | 'dark';
  voiceOn?: boolean;
  onVoiceOnChange?: (on: boolean) => void;
  soundsOn?: boolean;
  onSoundsOnChange?: (on: boolean) => void;
}

export default function VoiceSettingsButton({
  tone, voiceOn, onVoiceOnChange, soundsOn, onSoundsOnChange,
}: VoiceSettingsButtonProps) {
  const [open, setOpen] = useState(false);
  // Only a screen that passes the on/off setting gets the muted icon and the longer label.
  const knowsVoice = voiceOn !== undefined;
  const voiceOff = voiceOn === false;
  const triggerLabel = !knowsVoice
    ? "Choose Sparky's voice"
    : voiceOff
      ? "Sparky's voice is off. Open voice settings"
      : "Sparky's voice is on. Open voice settings";
  const triggerCls = tone === 'dark'
    ? 'border-white/40 bg-white/10 text-white hover:border-white'
    : 'border-line bg-white text-ink hover:border-ink';
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const sheetRef = useRef<HTMLDivElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  // True only after the sheet has been open, so focus is not pulled to the button on first draw.
  const wasOpenRef = useRef(false);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    if (!open) {
      if (wasOpenRef.current) {
        wasOpenRef.current = false;
        if (triggerRef.current) triggerRef.current.focus();
      }
      return;
    }
    wasOpenRef.current = true;
    if (closeRef.current) closeRef.current.focus();

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.stopPropagation();
        setOpen(false);
        return;
      }
      const sheet = sheetRef.current;
      if (event.key !== 'Tab' || !sheet) return;
      // Keep Tab inside the sheet.
      const found = sheet.querySelectorAll<HTMLElement>(FOCUSABLE);
      if (found.length === 0) return;
      const first = found[0];
      const last = found[found.length - 1];
      const active = document.activeElement;
      const inside = active !== null && sheet.contains(active);
      if (event.shiftKey) {
        if (!inside || active === first) {
          event.preventDefault();
          last.focus();
        }
      } else if (!inside || active === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open]);

  return (
    <>
      <button
        ref={triggerRef}
        type="button"
        onClick={() => setOpen(true)}
        aria-label={triggerLabel}
        aria-haspopup="dialog"
        aria-expanded={open}
        className={`w-12 h-12 flex-shrink-0 rounded-control border-2 text-xl flex items-center justify-center transition-colors ${triggerCls}`}
      >
        <span aria-hidden="true">{voiceOff ? '🔇' : '🗣️'}</span>
      </button>

      {open && typeof document !== 'undefined' && createPortal(
        <div className="fixed inset-0 z-[110] flex items-end justify-center">
          {/* The backdrop. Not a button: Escape and "Done" are the keyboard ways out. */}
          <div className="absolute inset-0 bg-black/60" onClick={close} aria-hidden="true" />
          <div
            ref={sheetRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby="voice-sheet-title"
            className="relative w-full max-w-lg max-h-[88dvh] overflow-y-auto bg-white border-2 border-b-0 border-ink rounded-t-card px-4 pt-4 animate-slide-up"
            style={{ paddingBottom: 'calc(env(safe-area-inset-bottom, 0px) + 16px)' }}
          >
            <div className="flex items-start justify-between gap-3 mb-3">
              <div className="min-w-0">
                <h2 id="voice-sheet-title" className="text-lg font-extrabold text-ink">
                  {knowsVoice ? <>Sparky&apos;s voice</> : <>Choose Sparky&apos;s voice</>}
                </h2>
                <p className="text-sm font-medium text-ink-muted">Tap Listen to hear each one, then pick your favourite.</p>
              </div>
              <button
                ref={closeRef}
                type="button"
                onClick={close}
                className="flex-shrink-0 min-h-[48px] min-w-[72px] rounded-control border-2 border-ink bg-action px-4 text-sm font-extrabold text-white"
              >
                Done
              </button>
            </div>
            <VoicePicker
              voiceOn={voiceOn}
              onVoiceOnChange={onVoiceOnChange}
              soundsOn={soundsOn}
              onSoundsOnChange={onSoundsOnChange}
            />
          </div>
        </div>,
        document.body,
      )}
    </>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useReadAloud } from '@/hooks/useReadAloud';
import { serverVoiceMayBeAvailable } from '@/lib/speech/serverVoice';
import { VOICE_PROFILES, VOICE_SAMPLE_TEXT, VOICE_SPEEDS } from '@/lib/speech/voices';
import { useVoicePrefs } from './useVoicePrefs';

/**
 * The list of voices Sparky can speak in, and how fast.
 *
 * Tapping a voice chooses it straight away (the choice is kept on this device
 * and every open screen picks it up). "Listen" plays one fixed sentence in
 * that voice without choosing it. The voices and speeds come from
 * `src/lib/speech/voices.ts`.
 *
 * A screen that owns an on/off setting can pass it in, and a switch for it is
 * shown above the voices: "Sparky talks" (`voiceOn` + `onVoiceOnChange`) and
 * "Sound effects" (`soundsOn` + `onSoundsOnChange`). With no props the picker
 * looks and works as it always has.
 */
interface VoicePickerProps {
  /** Whether Sparky speaks his lines. Shown as a switch only when `onVoiceOnChange` is also passed. */
  voiceOn?: boolean;
  onVoiceOnChange?: (on: boolean) => void;
  /** Whether the answer sounds play. Shown as a switch only when `onSoundsOnChange` is also passed. */
  soundsOn?: boolean;
  onSoundsOnChange?: (on: boolean) => void;
}

/** One labelled on/off switch, a full-width row 56px tall. */
function SwitchRow({ label, note, on, onChange }: {
  label: string;
  note: string;
  on: boolean;
  onChange: (on: boolean) => void;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={() => onChange(!on)}
      className="w-full min-h-[56px] flex items-center justify-between gap-3 rounded-control border-2 border-line bg-white px-3 py-2 text-left transition-colors hover:border-ink"
    >
      <span className="min-w-0">
        <span className="block text-base font-extrabold text-ink">{label}</span>
        <span className="block text-sm font-medium text-ink-muted">{note}</span>
      </span>
      <span
        aria-hidden="true"
        className={`relative flex-shrink-0 w-12 h-7 rounded-full border-2 border-ink transition-colors ${on ? 'bg-action' : 'bg-soft'}`}
      >
        <span
          className={`absolute left-0 top-0.5 w-5 h-5 rounded-full bg-white border-2 border-ink transition-transform ${
            on ? 'translate-x-[22px]' : 'translate-x-0.5'
          }`}
        />
      </span>
    </button>
  );
}

export default function VoicePicker({ voiceOn, onVoiceOnChange, soundsOn, onSoundsOnChange }: VoicePickerProps = {}) {
  const { voiceId, speedId, chooseVoice, chooseSpeed } = useVoicePrefs();
  const { speak, stop, speaking } = useReadAloud();
  // Which voice's sample is playing, if any.
  const [listeningTo, setListeningTo] = useState<string | null>(null);
  // True once we know this deployment has no server voice: every sample is then the device's own voice.
  const [deviceOnly, setDeviceOnly] = useState(false);

  useEffect(() => {
    if (!speaking) setListeningTo(null);
    setDeviceOnly(!serverVoiceMayBeAvailable());
  }, [speaking]);

  function listen(id: string) {
    if (speaking && listeningTo === id) {
      stop();
      return;
    }
    setListeningTo(id);
    speak(VOICE_SAMPLE_TEXT, { voiceId: id });
  }

  const showVoiceSwitch = voiceOn !== undefined && onVoiceOnChange !== undefined;
  const showSoundsSwitch = soundsOn !== undefined && onSoundsOnChange !== undefined;
  const voiceIsOn = voiceOn === true;

  function changeVoiceOn(on: boolean) {
    if (onVoiceOnChange) onVoiceOnChange(on);
  }

  function pickSpeed(id: string) {
    // A sample still playing was made at the old speed.
    stop();
    chooseSpeed(id);
  }

  return (
    <div className="space-y-4">
      {(showVoiceSwitch || showSoundsSwitch) && (
        <div className="space-y-2">
          {showVoiceSwitch && (
            <SwitchRow
              label="Sparky talks"
              note={voiceIsOn ? 'Sparky says his lines out loud.' : 'Sparky is quiet. His lines still show on the screen.'}
              on={voiceIsOn}
              onChange={changeVoiceOn}
            />
          )}
          {showSoundsSwitch && onSoundsOnChange && (
            <SwitchRow
              label="Sound effects"
              note={soundsOn ? 'A little sound plays when you answer.' : 'No sounds when you answer.'}
              on={soundsOn === true}
              onChange={onSoundsOnChange}
            />
          )}
        </div>
      )}

      <div role="radiogroup" aria-label="Sparky's voice" className="space-y-2">
        {VOICE_PROFILES.map((profile) => {
          const selected = profile.id === voiceId;
          const playing = speaking && listeningTo === profile.id;
          return (
            <div key={profile.id} className="flex items-stretch gap-2">
              <button
                type="button"
                role="radio"
                aria-checked={selected}
                onClick={() => chooseVoice(profile.id)}
                className={`flex-1 min-w-0 min-h-[56px] flex items-center gap-3 rounded-control border-2 px-3 py-2 text-left transition-colors ${
                  selected ? 'border-ink bg-soft' : 'border-line bg-white hover:border-ink'
                }`}
              >
                <span
                  aria-hidden="true"
                  className={`w-6 h-6 flex-shrink-0 rounded-full border-2 flex items-center justify-center text-[13px] font-extrabold ${
                    selected ? 'border-ink bg-action text-white' : 'border-line bg-white text-transparent'
                  }`}
                >
                  ✓
                </span>
                <span className="min-w-0">
                  <span className="block text-base font-extrabold text-ink">{profile.label}</span>
                  <span className="block text-sm font-medium text-ink-muted">{profile.blurb}</span>
                </span>
              </button>
              <button
                type="button"
                onClick={() => listen(profile.id)}
                aria-label={playing ? `Stop the ${profile.label}` : `Listen to the ${profile.label}`}
                aria-pressed={playing}
                className={`flex-shrink-0 min-h-[56px] min-w-[84px] rounded-control border-2 px-3 text-sm font-extrabold transition-colors ${
                  playing ? 'border-ink bg-action text-white' : 'border-line bg-white text-ink hover:border-ink'
                }`}
              >
                <span aria-hidden="true">{playing ? '⏹ ' : '▶ '}</span>
                {playing ? 'Stop' : 'Listen'}
              </button>
            </div>
          );
        })}
      </div>

      <div>
        <p id="voice-speed-label" className="text-sm font-extrabold text-ink mb-2">How fast should Sparky talk?</p>
        <div role="radiogroup" aria-labelledby="voice-speed-label" className="flex gap-2">
          {VOICE_SPEEDS.map((speed) => {
            const selected = speed.id === speedId;
            return (
              <button
                key={speed.id}
                type="button"
                role="radio"
                aria-checked={selected}
                onClick={() => pickSpeed(speed.id)}
                className={`flex-1 min-h-[48px] rounded-control border-2 px-2 text-sm font-extrabold transition-colors ${
                  selected ? 'border-ink bg-action text-white' : 'border-line bg-white text-ink hover:border-ink'
                }`}
              >
                {speed.label}
              </button>
            );
          })}
        </div>
      </div>

      {deviceOnly && (
        <p className="text-sm font-medium text-ink-muted" role="status">
          Sparky is using this device&apos;s own voice right now, so the voices may sound alike.
        </p>
      )}
    </div>
  );
}

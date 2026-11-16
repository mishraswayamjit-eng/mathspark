'use client';

import { useRef, useState } from 'react';
import { toSpeech } from '@/lib/speech/mathToSpeech';
import { DEFAULT_VOICE_ID, VOICE_PROFILES, type VoiceProfile } from '@/lib/speech/voices';

/**
 * Voice test page: try Sarvam voices, speeds and liveliness by ear.
 *
 * Children choose between the voice profiles in `src/lib/speech/voices.ts`.
 * The buttons at the top load a profile into the controls so it can be heard
 * and adjusted; a setting that sounds better is then written into that file
 * (speaker, pace, temperature: one line each). The SARVAM_TTS_* environment
 * variables only override the default profile. Nothing on this page changes
 * what children hear.
 */

const V3_SPEAKERS = [
  'shubh', 'aditya', 'ritu', 'priya', 'neha', 'rahul', 'pooja', 'rohan', 'simran', 'kavya', 'amit', 'dev', 'ishita',
  'shreya', 'ratan', 'varun', 'manan', 'sumit', 'roopa', 'kabir', 'aayan', 'ashutosh', 'advait', 'anand', 'tanya',
  'tarun', 'sunny', 'mani', 'gokul', 'vijay', 'shruti', 'suhani', 'mohit', 'kavitha', 'rehan', 'soham', 'rupali',
];
const V2_SPEAKERS = ['anushka', 'manisha', 'vidya', 'arya', 'abhilash', 'karun', 'hitesh'];
// bulbul:v4-flash voices are personas named <name>_<language>_<style>. These are English ones
// from Sarvam's voice list that suit a children's tutor; any other persona name can be typed in.
const V4_SUGGESTIONS = [
  'nupur_en_kids', 'aparna_en_edtech', 'ritu_en_edtech', 'simran_en_edtech', 'shabana_en_edtech', 'payal_en_edtech',
  'ishita_en_stories', 'aditi_en_stories', 'amelia_en_conversational', 'sophia_en_conversational', 'roopa_en_conversational',
];

type Model = 'bulbul:v3' | 'bulbul:v2' | 'bulbul:v4-flash';

const SAMPLES = [
  { label: 'A question', text: 'A rectangle is 12 cm long and 7 cm wide. What is its perimeter?' },
  { label: 'A hint', text: 'Not quite yet. Think about what the bottom number of a fraction tells you. How many equal parts make the whole?' },
  { label: 'A solution step', text: 'Step 2. Half of 20 times 7 is 70, so the area of the triangle is 70 square centimetres.' },
  { label: 'Praise', text: 'You got it! That was excellent thinking. Ready for a trickier one?' },
  { label: 'Fractions and symbols', text: '3/4 + 1/8 = 7/8, and 25% of ₹480 is ₹120.' },
];

interface Heard { model: string; speaker: string; pace: number; temperature: number }

export default function VoiceTestPage() {
  const [model, setModel] = useState<Model>('bulbul:v3');
  const [speaker, setSpeaker] = useState('shubh');
  const [pace, setPace] = useState(0.95);
  const [temperature, setTemperature] = useState(0.6);
  const [text, setText] = useState(SAMPLES[0].text);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [heard, setHeard] = useState<Heard | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speakers = model === 'bulbul:v2' ? V2_SPEAKERS : V3_SPEAKERS;
  // What the app would actually send: symbols and fractions turned into words.
  const spoken = toSpeech(text);

  function chooseModel(next: Model) {
    setModel(next);
    setSpeaker(next === 'bulbul:v2' ? 'anushka' : next === 'bulbul:v4-flash' ? V4_SUGGESTIONS[0] : 'ishita');
  }

  /** Put one of the children's voice profiles into the controls, exactly as written in voices.ts. */
  function loadProfile(profile: VoiceProfile) {
    setModel('bulbul:v3');
    setSpeaker(profile.speaker);
    setPace(profile.pace);
    setTemperature(profile.temperature);
  }

  async function play() {
    if (!spoken || busy) return;
    setBusy(true);
    setMessage('');
    if (audioRef.current) audioRef.current.pause();
    try {
      const res = await fetch('/api/voice/tts', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text: spoken, model, speaker, pace, temperature }),
      });
      const data = (await res.json()) as { audio?: string; mime?: string; voice?: Heard; error?: string; detail?: string };
      if (!res.ok || !data.audio) {
        setMessage(
          res.status === 503 ? 'SARVAM_API_KEY is not set for this deployment yet.'
            : res.status === 401 ? 'Sign in as a student first, then come back to this page.'
            : `${data.error || 'The voice could not be played.'}${data.detail ? ` Sarvam said: ${data.detail}` : ''}`,
        );
        return;
      }
      const audio = new Audio(`data:${data.mime || 'audio/mpeg'};base64,${data.audio}`);
      audioRef.current = audio;
      setHeard(data.voice || null);
      await audio.play();
    } catch {
      setMessage('The request did not go through. Check the connection and try again.');
    } finally {
      setBusy(false);
    }
  }

  const field = 'w-full min-h-[48px] rounded-control border-2 border-line bg-white px-3 font-bold text-ink';

  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="max-w-xl mx-auto px-4 pt-6 space-y-5">
        <div>
          <h1 className="font-display text-display text-ink">Voice test</h1>
          <p className="text-label text-ink-muted mt-1">
            Try Sarvam voices by ear. Children choose between the profiles below; to change one, write the speaker, pace and temperature that sound right into src/lib/speech/voices.ts and add 1 to VOICE_CACHE_VERSION there.
          </p>
        </div>

        <div className="bg-white rounded-card border-2 border-line p-4 space-y-3">
          <div>
            <p className="font-display text-title text-ink">Voices children can choose</p>
            <p className="text-caption text-ink-muted mt-0.5">
              Tap one to load it into the controls, then press Play. These were chosen without anyone hearing them, so each needs a listen.
            </p>
          </div>
          <div className="flex flex-col gap-2">
            {VOICE_PROFILES.map((profile) => (
              <button
                key={profile.id}
                type="button"
                onClick={() => loadProfile(profile)}
                className="min-h-[48px] px-3 py-2 rounded-control border-2 border-line bg-white text-left hover:border-ink"
              >
                <span className="block text-ink font-extrabold">
                  {profile.label}{profile.id === DEFAULT_VOICE_ID ? ' (default)' : ''}
                </span>
                <span className="block text-caption text-ink-muted">
                  {profile.speaker} · pace {profile.pace.toFixed(2)} · temperature {profile.temperature.toFixed(2)}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-card border-2 border-line p-4 space-y-4">
          <label className="block">
            <span className="text-caption text-ink-muted">Model</span>
            <select
              className={field}
              value={model}
              onChange={(e) => chooseModel(e.target.value === 'bulbul:v2' ? 'bulbul:v2' : e.target.value === 'bulbul:v4-flash' ? 'bulbul:v4-flash' : 'bulbul:v3')}
            >
              <option value="bulbul:v3">bulbul:v3 (natural, 37 voices)</option>
              <option value="bulbul:v4-flash">bulbul:v4-flash (persona voices with a style, e.g. kids, edtech)</option>
              <option value="bulbul:v2">bulbul:v2 (older; allows pitch and loudness)</option>
            </select>
          </label>

          <label className="block">
            <span className="text-caption text-ink-muted">Speaker</span>
            {model === 'bulbul:v4-flash' ? (
              <>
                <input
                  className={field}
                  list="v4-voices"
                  value={speaker}
                  onChange={(e) => setSpeaker(e.target.value.trim().toLowerCase())}
                  spellCheck={false}
                />
                <datalist id="v4-voices">
                  {V4_SUGGESTIONS.map((s) => <option key={s} value={s} />)}
                </datalist>
                <span className="text-caption text-ink-muted">
                  Pick a suggestion or type any persona from Sarvam&apos;s voice list, as name_language_style. If Sarvam does not know the name, the message below says so.
                </span>
              </>
            ) : (
              <select className={field} value={speaker} onChange={(e) => setSpeaker(e.target.value)}>
                {speakers.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            )}
          </label>

          <label className="block">
            <span className="flex justify-between text-caption text-ink-muted">
              <span>Speed (pace)</span>
              <span className="text-ink font-extrabold">{pace.toFixed(2)}</span>
            </span>
            <input type="range" min={0.5} max={1.5} step={0.05} value={pace} onChange={(e) => setPace(Number(e.target.value))} className="w-full h-12 accent-action" />
            <span className="text-caption text-ink-muted">1.00 is Sarvam&apos;s normal. The profiles use about 1.10; children can also pick Calm or Quick.</span>
          </label>

          {model !== 'bulbul:v2' && (
            <label className="block">
              <span className="flex justify-between text-caption text-ink-muted">
                <span>Liveliness (temperature)</span>
                <span className="text-ink font-extrabold">{temperature.toFixed(2)}</span>
              </span>
              <input type="range" min={0.1} max={1} step={0.05} value={temperature} onChange={(e) => setTemperature(Number(e.target.value))} className="w-full h-12 accent-action" />
              <span className="text-caption text-ink-muted">Lower is steadier and more even. Higher is more expressive, and varies more between readings.</span>
            </label>
          )}
        </div>

        <div className="bg-white rounded-card border-2 border-line p-4 space-y-3">
          <div className="flex flex-wrap gap-2">
            {SAMPLES.map((s) => (
              <button
                key={s.label}
                type="button"
                onClick={() => setText(s.text)}
                className="min-h-[48px] px-3 rounded-full border-2 border-line bg-white text-ink text-[13px] font-bold hover:border-ink"
              >
                {s.label}
              </button>
            ))}
          </div>
          <label className="block">
            <span className="text-caption text-ink-muted">Text to speak</span>
            <textarea
              className="w-full rounded-control border-2 border-line bg-white px-3 py-2 font-semibold text-ink min-h-[110px]"
              value={text}
              maxLength={1200}
              onChange={(e) => setText(e.target.value)}
            />
          </label>
          {spoken !== text.trim() && (
            <p className="text-caption text-ink-muted">Sent as: <span className="text-ink">{spoken}</span></p>
          )}
          <button
            type="button"
            onClick={play}
            disabled={busy || !spoken}
            className="w-full min-h-[52px] rounded-control border-2 border-ink bg-action text-white font-extrabold shadow-hard-sm disabled:opacity-50"
          >
            {busy ? 'Fetching the voice…' : 'Play'}
          </button>
          {message && <p className="text-label text-ink bg-hint rounded-control px-3 py-2" role="status">{message}</p>}
        </div>

        <div className="bg-white rounded-card border-2 border-line p-4">
          <p className="font-display text-title text-ink">Settings for Vercel</p>
          <p className="text-caption text-ink-muted mt-0.5">
            {heard ? 'From the reading you just heard.' : 'These update when you play a reading.'} These override the default profile only (the other profiles always use voices.ts). Add them under Project, Settings, Environment Variables, then redeploy. If old values are set there now, the default profile is still using them.
          </p>
          <pre className="mt-3 bg-soft rounded-control px-3 py-3 text-[13px] leading-relaxed text-ink overflow-x-auto select-all">
{`SARVAM_TTS_MODEL=${heard ? heard.model : model}
SARVAM_TTS_SPEAKER=${heard ? heard.speaker : speaker}
SARVAM_TTS_PACE=${(heard ? heard.pace : pace).toFixed(2)}${(heard ? heard.model : model) !== 'bulbul:v2' ? `
SARVAM_TTS_TEMPERATURE=${(heard ? heard.temperature : temperature).toFixed(2)}` : ''}`}
          </pre>
        </div>
      </div>
    </div>
  );
}

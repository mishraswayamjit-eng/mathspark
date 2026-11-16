import { describe, it, expect } from 'vitest';
import {
  DEFAULT_SPEED_ID,
  DEFAULT_VOICE_ID,
  SAY_MAX_CHARS,
  VOICE_CACHE_VERSION,
  VOICE_PROFILES,
  VOICE_SAMPLE_TEXT,
  VOICE_SPEEDS,
  getVoiceProfile,
  getVoiceSpeed,
  normaliseSpeechText,
  sayUrl,
  voiceProfileOrDefault,
  voiceSpeedOrDefault,
} from '../speech/voices';
import { lineSaysName } from '../tutor/reactions';

describe('voice profiles', () => {
  it('has a default that exists, and unique ids', () => {
    expect(getVoiceProfile(DEFAULT_VOICE_ID)).not.toBeNull();
    expect(getVoiceSpeed(DEFAULT_SPEED_ID)).not.toBeNull();
    const ids = VOICE_PROFILES.map((p) => p.id);
    expect(ids.filter((id, i) => ids.indexOf(id) !== i)).toEqual([]);
    expect(VOICE_PROFILES.length).toBeGreaterThanOrEqual(2);
  });

  it('keeps every pace, with every speed, inside what Sarvam allows', () => {
    VOICE_PROFILES.forEach((p) => {
      expect(p.speaker).toMatch(/^[a-z][a-z0-9_]{1,40}$/);
      expect(p.temperature).toBeGreaterThanOrEqual(0.01);
      expect(p.temperature).toBeLessThanOrEqual(1);
      VOICE_SPEEDS.forEach((s) => {
        expect(p.pace * s.multiplier).toBeGreaterThanOrEqual(0.5);
        expect(p.pace * s.multiplier).toBeLessThanOrEqual(2);
      });
    });
  });

  it('is brisker than Sarvam normal by default', () => {
    expect(voiceProfileOrDefault(null).pace).toBeGreaterThan(1);
    expect(voiceSpeedOrDefault(null).multiplier).toBe(1);
  });

  it('uses child-friendly words and promises no accent', () => {
    const unsayable = /\b(wrong|incorrect|failed|error|british|american|accent)\b/i;
    VOICE_PROFILES.forEach((p) => {
      expect(unsayable.test(`${p.label} ${p.blurb}`)).toBe(false);
    });
    expect(unsayable.test(VOICE_SAMPLE_TEXT)).toBe(false);
  });

  it('falls back to the default for an unknown id', () => {
    expect(getVoiceProfile('shubh')).toBeNull();
    expect(voiceProfileOrDefault('shubh').id).toBe(DEFAULT_VOICE_ID);
    expect(voiceProfileOrDefault(undefined).id).toBe(DEFAULT_VOICE_ID);
    expect(voiceSpeedOrDefault('1.5').id).toBe(DEFAULT_SPEED_ID);
  });
});

describe('normaliseSpeechText', () => {
  it('collapses spacing and trims', () => {
    expect(normaliseSpeechText('  What is\n 3  plus\t4? ')).toBe('What is 3 plus 4?');
    expect(normaliseSpeechText('')).toBe('');
    expect(normaliseSpeechText('   ')).toBe('');
  });
});

describe('sayUrl', () => {
  it('gives the same address for the same line however it is spaced', () => {
    const a = sayUrl('What is 3 plus 4?', 'warm', 'quick');
    const b = sayUrl('  What  is 3\nplus 4? ', 'warm', 'quick');
    expect(a).not.toBeNull();
    expect(a).toBe(b);
  });

  it('writes the parameters in a fixed order', () => {
    expect(sayUrl('Half of 10 is 5.', 'warm', 'calm')).toBe(
      `/api/voice/say?k=${VOICE_CACHE_VERSION}&v=warm&s=calm&t=Half%20of%2010%20is%205.`,
    );
  });

  it('gives different addresses for different voices and speeds', () => {
    const line = 'Good, keep going.';
    expect(sayUrl(line, 'teacher', 'normal')).not.toBe(sayUrl(line, 'warm', 'normal'));
    expect(sayUrl(line, 'teacher', 'normal')).not.toBe(sayUrl(line, 'teacher', 'quick'));
  });

  it('uses the defaults for a missing or unknown voice or speed', () => {
    const line = 'Good, keep going.';
    expect(sayUrl(line)).toBe(sayUrl(line, DEFAULT_VOICE_ID, DEFAULT_SPEED_ID));
    expect(sayUrl(line, 'priya', '2.0')).toBe(sayUrl(line, DEFAULT_VOICE_ID, DEFAULT_SPEED_ID));
  });

  it('has no address for an empty line or one too long for a URL', () => {
    expect(sayUrl('   ')).toBeNull();
    let long = '';
    while (long.length <= SAY_MAX_CHARS) long += 'seven times eight ';
    expect(sayUrl(long)).toBeNull();
  });
});

describe('lineSaysName', () => {
  it('spots a line with the child\'s first name in it', () => {
    expect(lineSaysName('Good, Asha. Keep going.', 'Asha Rao')).toBe(true);
    expect(lineSaysName('Good. Keep going.', 'Asha Rao')).toBe(false);
    expect(lineSaysName('Good. Keep going.', undefined)).toBe(false);
    expect(lineSaysName('Good. Keep going.', '')).toBe(false);
  });
});

import { describe, it, expect } from 'vitest';
import {
  tutorLine,
  tutorLineWith,
  pickIndex,
  spokenMisconception,
  type TutorEvent,
} from '../tutor/reactions';
import { LINES, type LinePool } from '../tutor/lines';

const POOLS = Object.keys(LINES) as LinePool[];

/** Every line in the library, as written (placeholders still in). */
function everyLine(): string[] {
  const out: string[] = [];
  for (let p = 0; p < POOLS.length; p++) {
    const pool = LINES[POOLS[p]];
    for (let i = 0; i < pool.length; i++) out.push(pool[i]);
  }
  return out;
}

/** A line as it is said when the child's name is not known. */
function withoutName(line: string): string {
  return line.split(', {name}').join('');
}

function unnamed(pool: string[]): string[] {
  return pool.map(withoutName);
}

function correct(streak: number, secondsTaken: number, usedHint = false): TutorEvent {
  return { kind: 'correct', streak, usedHint, secondsTaken };
}

function miss(missesInARow: number, misconception?: string): TutorEvent {
  return { kind: 'miss', chosenText: '12', misconception, missesInARow };
}

/** The different lines an event produces over a run of turns (silence left out). */
function distinctLines(event: TutorEvent, turns: number): string[] {
  const seen: string[] = [];
  for (let turn = 0; turn < turns; turn++) {
    const line = tutorLine(event, { turn });
    if (line && seen.indexOf(line) === -1) seen.push(line);
  }
  return seen;
}

describe('the line library', () => {
  it('is speakable words only: no emoji, symbols or hyphens', () => {
    const lines = everyLine();
    for (let i = 0; i < lines.length; i++) {
      const said = lines[i].replace(/\{(name|n|c|t|topic)\}/g, 'x');
      expect(said).toMatch(/^[A-Za-z0-9 ,.?!']+$/);
    }
  });

  it('keeps every line short', () => {
    const lines = everyLine();
    for (let i = 0; i < lines.length; i++) {
      expect(lines[i].length).toBeLessThanOrEqual(140);
    }
  });

  it('never uses a word a child must not hear', () => {
    const lines = everyLine();
    for (let i = 0; i < lines.length; i++) {
      expect(lines[i]).not.toMatch(/\b(wrong|incorrect|oops|fail|failed|error)\b/i);
    }
  });

  it('never says "no" on a miss', () => {
    const pools = [LINES.missFirst, LINES.missSecond, LINES.missMany, LINES.missFrames, LINES.missTails];
    for (let p = 0; p < pools.length; p++) {
      for (let i = 0; i < pools[p].length; i++) {
        expect(pools[p][i]).not.toMatch(/\bno\b/i);
      }
    }
  });

  it('praises effort, never cleverness', () => {
    const lines = everyLine();
    for (let i = 0; i < lines.length; i++) {
      expect(lines[i]).not.toMatch(/\b(clever|smart|genius|brilliant|intelligent|talented)\b/i);
    }
  });

  it('has no line twice', () => {
    const lines = everyLine();
    const seen: Record<string, boolean> = {};
    for (let i = 0; i < lines.length; i++) {
      expect(seen[lines[i]]).toBeUndefined();
      seen[lines[i]] = true;
    }
  });

  it('has at least 12 lines for common situations and 6 for rare ones', () => {
    expect(LINES.correctPlain.length).toBeGreaterThanOrEqual(12);
    expect(LINES.correctQuick.length).toBeGreaterThanOrEqual(12);
    expect(LINES.correctHardWon.length).toBeGreaterThanOrEqual(12);
    expect(LINES.missFirst.length).toBeGreaterThanOrEqual(12);
    for (let p = 0; p < POOLS.length; p++) {
      if (POOLS[p] === 'missTails') continue; // a tail is the end of a line, not a line
      expect(LINES[POOLS[p]].length).toBeGreaterThanOrEqual(6);
    }
  });

  it('uses the name rarely and exclamation marks sparingly', () => {
    const lines = everyLine();
    let named = 0;
    let exclaimed = 0;
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].indexOf('{name}') !== -1) named += 1;
      if (lines[i].indexOf('!') !== -1) exclaimed += 1;
    }
    expect(named).toBeGreaterThan(0);
    expect(named / lines.length).toBeLessThanOrEqual(1 / 6);
    expect(exclaimed / lines.length).toBeLessThanOrEqual(1 / 3);
  });

  it('always writes the name with its comma, so it can be left out', () => {
    const lines = everyLine();
    for (let i = 0; i < lines.length; i++) {
      expect(withoutName(lines[i]).indexOf('{name}')).toBe(-1);
    }
  });
});

describe('pickIndex', () => {
  it('visits every line once in each lap', () => {
    const sizes = [5, 6, 7, 11, 13, 17];
    for (let s = 0; s < sizes.length; s++) {
      const size = sizes[s];
      for (let lap = 0; lap < 3; lap++) {
        const seen: Record<number, boolean> = {};
        for (let t = 0; t < size; t++) {
          const index = pickIndex(size, lap * size + t, 0);
          expect(index).toBeGreaterThanOrEqual(0);
          expect(index).toBeLessThan(size);
          expect(seen[index]).toBeUndefined();
          seen[index] = true;
        }
      }
    }
  });

  it('does not simply walk down the list', () => {
    const sizes = [7, 11, 13, 17];
    for (let s = 0; s < sizes.length; s++) {
      const size = sizes[s];
      const gap = (pickIndex(size, 1, 0) - pickIndex(size, 0, 0) + size) % size;
      expect(gap).not.toBe(1);
      expect(gap).not.toBe(size - 1);
    }
  });
});

describe('tutorLine: determinism', () => {
  it('gives the same line for the same event and turn', () => {
    const events: TutorEvent[] = [
      { kind: 'question', first: true },
      correct(1, 20),
      correct(3, 4),
      miss(1),
      miss(2, 'Check your unit conversion and formula.'),
      { kind: 'hint', level: 2 },
      { kind: 'idle', seconds: 60 },
      { kind: 'startedWorking' },
      { kind: 'sessionEnd', correct: 6, total: 10 },
    ];
    for (let e = 0; e < events.length; e++) {
      for (let turn = 0; turn < 20; turn++) {
        expect(tutorLine(events[e], { turn })).toBe(tutorLine(events[e], { turn }));
      }
    }
  });

  it('copes with a turn that is not a small whole number', () => {
    expect(tutorLine(miss(1), { turn: -3 })).not.toBe('');
    expect(tutorLine(miss(1), { turn: 2.7 })).not.toBe('');
    expect(tutorLine(miss(1), { turn: NaN })).not.toBe('');
    expect(tutorLine(miss(1), { turn: 1700000000000 })).not.toBe('');
  });
});

describe('tutorLine: a question appears', () => {
  it('welcomes the child on the first question', () => {
    for (let turn = 0; turn < 10; turn++) {
      expect(unnamed(LINES.welcome)).toContain(tutorLine({ kind: 'question', first: true }, { turn }));
    }
  });

  it('is quiet for most later questions', () => {
    let spoken = 0;
    for (let turn = 0; turn < 60; turn++) {
      if (tutorLine({ kind: 'question', first: false }, { turn })) spoken += 1;
    }
    expect(spoken).toBeGreaterThan(0);
    expect(spoken).toBeLessThanOrEqual(15);
  });
});

describe('tutorLine: a right answer', () => {
  it('marks the third and the fifth in a row', () => {
    expect(tutorLine(correct(3, 20), { turn: 0 })).toBe('Three in a row!');
    expect(tutorLine(correct(5, 20), { turn: 0 })).toBe('Five in a row!');
    for (let turn = 0; turn < 14; turn++) {
      expect(unnamed(LINES.streakThree)).toContain(tutorLine(correct(3, 20), { turn }));
      expect(unnamed(LINES.streakFive)).toContain(tutorLine(correct(5, 20), { turn }));
    }
  });

  it('counts a long run aloud', () => {
    expect(tutorLine(correct(10, 20), { turn: 0 })).toBe('10 in a row!');
    expect(tutorLine(correct(15, 20), { turn: 0 })).toBe('15 in a row!');
  });

  it('credits the hint when one was used', () => {
    for (let turn = 0; turn < 22; turn++) {
      expect(unnamed(LINES.correctAfterHint)).toContain(tutorLine(correct(1, 30, true), { turn }));
    }
  });

  it('notices a quick answer and a hard-won one', () => {
    expect(tutorLine(correct(1, 3), { turn: 0 })).toBe('That was quick!');
    expect(tutorLine(correct(1, 60), { turn: 0 })).toBe('You stuck with that one. Well done.');
    for (let turn = 0; turn < 26; turn++) {
      const quick = tutorLine(correct(2, 3), { turn });
      if (quick) expect(unnamed(LINES.correctQuick)).toContain(quick);
      expect(unnamed(LINES.correctHardWon)).toContain(tutorLine(correct(2, 60), { turn }));
    }
  });

  it('lets some ordinary right answers pass without a word', () => {
    expect(tutorLine(correct(2, 20), { turn: 0 })).toBe('Correct.');
    expect(tutorLine(correct(2, 20), { turn: 2 })).toBe('');
    let quiet = 0;
    for (let turn = 0; turn < 30; turn++) {
      if (!tutorLine(correct(2, 20), { turn })) quiet += 1;
    }
    expect(quiet).toBe(10);
  });

  it('says less on a long run', () => {
    let spoken = 0;
    for (let turn = 0; turn < 30; turn++) {
      if (tutorLine(correct(7, 20), { turn })) spoken += 1;
    }
    expect(spoken).toBeLessThan(20);
    expect(spoken).toBeGreaterThan(0);
  });

  it('treats an unknown time as an ordinary answer', () => {
    expect(unnamed(LINES.correctPlain)).toContain(tutorLine(correct(1, 0), { turn: 0 }));
  });

  it('welcomes a right answer straight after a miss, when told about the miss', () => {
    expect(tutorLineWith(correct(1, 20), { turn: 0 }, { afterMiss: true }))
      .toBe('There you go. That is how you come back.');
    expect(unnamed(LINES.correctComeback)).not.toContain(tutorLine(correct(1, 20), { turn: 0 }));
  });

  it('does not repeat itself in a session of 20 questions', () => {
    expect(distinctLines(correct(2, 20), 60).length).toBeGreaterThanOrEqual(12);
    expect(distinctLines(correct(2, 3), 60).length).toBeGreaterThanOrEqual(12);
    expect(distinctLines(correct(2, 60), 13).length).toBe(13);
  });

  it('moves on past a line said recently', () => {
    const usual = tutorLine(correct(2, 20), { turn: 0 });
    const next = tutorLineWith(correct(2, 20), { turn: 0 }, { recent: [usual] });
    expect(next).not.toBe('');
    expect(next).not.toBe(usual);
    expect(unnamed(LINES.correctPlain)).toContain(next);
  });
});

describe('tutorLine: a miss', () => {
  it('steers gently on the first miss and offers help on later ones', () => {
    for (let turn = 0; turn < 26; turn++) {
      expect(unnamed(LINES.missFirst)).toContain(tutorLine(miss(1), { turn }));
      expect(unnamed(LINES.missSecond)).toContain(tutorLine(miss(2), { turn }));
      expect(unnamed(LINES.missMany)).toContain(tutorLine(miss(3), { turn }));
      expect(unnamed(LINES.missMany)).toContain(tutorLine(miss(6), { turn }));
    }
    expect(distinctLines(miss(1), 13).length).toBe(13);
  });

  it("frames the question's own note when it has one", () => {
    expect(tutorLine(miss(1, 'Check your unit conversion and formula.'), { turn: 0 }))
      .toBe('Ah, I can see how you got there. Check your unit conversion and formula. Now try again.');
  });

  it('never says a word a child must not hear, whatever the turn', () => {
    const notes = [
      'Check your unit conversion and formula.',
      'Read the question again — are you finding the right thing?',
      'Wrong operation used.',
      'Correct! The answer is 17.',
      undefined,
    ];
    for (let n = 0; n < notes.length; n++) {
      for (let turn = 0; turn < 20; turn++) {
        for (let row = 1; row <= 4; row++) {
          const line = tutorLine(miss(row, notes[n]), { turn });
          expect(line).not.toBe('');
          expect(line).not.toMatch(/\b(wrong|incorrect|no|oops)\b/i);
          expect(line).not.toMatch(/answer is/i);
          expect(line.length).toBeLessThanOrEqual(150);
        }
      }
    }
  });

  it('falls back to a plain steer when the note cannot be said', () => {
    expect(unnamed(LINES.missFirst)).toContain(tutorLine(miss(1, 'Correct! The answer is 17.'), { turn: 0 }));
    expect(unnamed(LINES.missSecond)).toContain(tutorLine(miss(2, 'Wrong operation used.'), { turn: 0 }));
    expect(unnamed(LINES.missFirst)).toContain(tutorLine(miss(1, 'Student adds the denominators.'), { turn: 0 }));
  });
});

describe('spokenMisconception', () => {
  it('turns symbols and written punctuation into speech', () => {
    expect(spokenMisconception('Remember: place value = digit × position value.', 120))
      .toBe('Remember, place value equals digit times position value.');
    expect(spokenMisconception('Read the question again — are you finding the right thing?', 120))
      .toBe('Read the question again, are you finding the right thing?');
  });

  it('uses the first sentence when the whole note is too long to say', () => {
    const first = 'You added the tops and the bottoms.';
    const second = 'When the bottom numbers are different you must first change both fractions so that '
      + 'they share the same bottom number before you add them together.';
    expect(spokenMisconception(`${first} ${second}`, 117)).toBe(first);
  });

  it('says at most two sentences', () => {
    expect(spokenMisconception('One thing. Two things. Three things.', 120)).toBe('One thing. Two things.');
  });

  it('leaves out a sentence that could give the answer away', () => {
    expect(spokenMisconception('Correct! The answer is 17.', 120)).toBe('');
    expect(spokenMisconception('You forgot to carry. The answer is 42.', 120)).toBe('You forgot to carry.');
  });

  it('returns nothing for a missing or over-long note', () => {
    expect(spokenMisconception(undefined, 120)).toBe('');
    expect(spokenMisconception('', 120)).toBe('');
    expect(spokenMisconception('You added the tops and the bottoms.', 10)).toBe('');
  });
});

describe('tutorLine: hints, pauses and the pencil pad', () => {
  it('leads in to each hint level differently', () => {
    for (let turn = 0; turn < 14; turn++) {
      expect(LINES.hintIdea).toContain(tutorLine({ kind: 'hint', level: 1 }, { turn }));
      expect(LINES.hintFirstMove).toContain(tutorLine({ kind: 'hint', level: 2 }, { turn }));
      expect(LINES.hintExample).toContain(tutorLine({ kind: 'hint', level: 3 }, { turn }));
    }
  });

  it('stays silent while the child is thinking, then nudges once the pause is long', () => {
    expect(tutorLine({ kind: 'idle', seconds: 5 }, { turn: 0 })).toBe('');
    for (let turn = 0; turn < 14; turn++) {
      expect(LINES.idleSoft).toContain(tutorLine({ kind: 'idle', seconds: 20 }, { turn }));
      expect(unnamed(LINES.idleHint)).toContain(tutorLine({ kind: 'idle', seconds: 60 }, { turn }));
      expect(LINES.idleLong).toContain(tutorLine({ kind: 'idle', seconds: 120 }, { turn }));
    }
  });

  it('only sometimes comments on the pencil pad', () => {
    expect(unnamed(LINES.startedWorking)).toContain(tutorLine({ kind: 'startedWorking' }, { turn: 0 }));
    expect(tutorLine({ kind: 'startedWorking' }, { turn: 1 })).toBe('');
    expect(tutorLine({ kind: 'startedWorking' }, { turn: 2 })).toBe('');
  });
});

describe('tutorLine: the end of a session', () => {
  it('fits the summary to the score', () => {
    expect(tutorLine({ kind: 'sessionEnd', correct: 10, total: 10 }, { turn: 0 }))
      .toBe('All 10 right. That was careful work from start to finish.');
    expect(tutorLine({ kind: 'sessionEnd', correct: 8, total: 10 }, { turn: 0 }))
      .toBe('8 out of 10. Good session. Look again at the ones that slipped.');
    expect(tutorLine({ kind: 'sessionEnd', correct: 5, total: 10 }, { turn: 0 }))
      .toBe('5 out of 10. A fair start. We will practise this topic some more.');
    expect(tutorLine({ kind: 'sessionEnd', correct: 2, total: 10 }, { turn: 0 }))
      .toBe('That was a hard session, and you finished it. Next we go through the solutions together.');
  });

  it('names the topic when it is known', () => {
    expect(tutorLine({ kind: 'sessionEnd', correct: 5, total: 10 }, { turn: 0, topicName: 'Fractions' }))
      .toBe('5 out of 10. A fair start. We will practise Fractions some more.');
  });

  it('gives no hollow praise for a hard session', () => {
    for (let i = 0; i < LINES.endHard.length; i++) {
      expect(LINES.endHard[i]).not.toMatch(/\b(great|well done|excellent|awesome|amazing|perfect)\b/i);
    }
  });

  it('does not score a session too short to mean anything', () => {
    expect(LINES.endShort).toContain(tutorLine({ kind: 'sessionEnd', correct: 1, total: 1 }, { turn: 0 }));
    expect(LINES.endShort).toContain(tutorLine({ kind: 'sessionEnd', correct: 0, total: 0 }, { turn: 4 }));
  });
});

describe('tutorLine: the name', () => {
  it('uses the name in the lines written for it, and reads well without it', () => {
    expect(tutorLine(correct(2, 20), { turn: 16, name: 'Asha' })).toBe('Good, Asha. Keep going.');
    expect(tutorLine(correct(2, 20), { turn: 16 })).toBe('Good. Keep going.');
  });

  it('ignores a name that could not be spoken', () => {
    expect(tutorLine(correct(2, 20), { turn: 16, name: '<b>x</b>' })).toBe('Good. Keep going.');
    expect(tutorLine(correct(2, 20), { turn: 16, name: 'Asha Rao' })).toBe('Good, Asha. Keep going.');
  });
});

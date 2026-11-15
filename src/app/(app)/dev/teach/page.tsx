'use client';

import { useMemo, useState } from 'react';
import WorkingBoard from '@/components/teach/WorkingBoard';
import type { BoardOp, TeachBeat } from '@/lib/teach/types';

/**
 * Teach board preview: step through a lesson a beat at a time and watch the
 * board being written and marked. Loads a served lesson by question id, or
 * plays one of the built-in samples. Nothing here is shown to children.
 */

interface Lesson {
  title: string;
  beats: TeachBeat[];
}

// Copied from scripts/teach/example.json.
const SAMPLE_SIMPLE: Lesson = {
  title: 'Sample: 4x − 11 = 5',
  beats: [
    {
      say: 'Here is our equation. 4 x, minus 11, equals 5. Somewhere behind that x a number is hiding, and we are going to find it.',
      board: [{ op: 'write', id: 'l1', text: '4x − 11 = 5', tone: 'given' }],
    },
    {
      say: 'Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what is in the way of the 4 x?',
      ask: {
        kind: 'choose',
        choices: ['the − 11', 'the 5', 'the 4'],
        answer: 0,
        ifNot: 'Look at the left side once more. The 4 x has a minus 11 hanging on to it. That is the first thing to clear away.',
      },
    },
    {
      say: 'To undo minus 11, we add 11. And to keep the balance level, we add it to both sides.',
      board: [
        { op: 'strike', line: 'l1', target: { text: '− 11' }, note: '+ 11' },
        { op: 'both', line: 'l1', text: '+ 11' },
      ],
    },
    {
      say: 'On the left, minus 11 and plus 11 cancel each other out. On the right, 5 plus 11 makes 16.',
      board: [
        { op: 'write', id: 'l2', text: '4x = 5 + 11' },
        { op: 'write', id: 'l3', text: '4x = 16' },
      ],
    },
    {
      say: 'Nearly there. 4 x means 4 times x. What undoes times 4?',
      ask: {
        kind: 'choose',
        choices: ['divide by 4', 'subtract 4', 'multiply by 4'],
        answer: 0,
        ifNot: 'Times and divide are partners. Whatever times does, divide undoes. So to undo times 4, we divide by 4.',
      },
    },
    {
      say: 'So we divide both sides by 4.',
      board: [{ op: 'divide', line: 'l3', by: '4' }],
    },
    {
      say: '16 divided by 4 is 4. So x equals 4. There is our hidden number!',
      board: [
        { op: 'write', id: 'l4', text: 'x = 4', tone: 'answer' },
        { op: 'mark', line: 'l4', target: { text: 'x = 4' }, shape: 'circle' },
      ],
    },
    {
      say: 'Good mathematicians always check. Put 4 back in place of x. 4 times 4 is 16, and 16 minus 11 is 5. It works.',
      board: [{ op: 'write', id: 'l5', text: '4 × 4 − 11 = 5' }],
    },
    {
      say: 'So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times. Your turn next!',
    },
  ],
};

// The reference lesson (check: x = 7). Uses every kind of board op between the two samples.
const SAMPLE_BRACKETS: Lesson = {
  title: 'Sample: 4(3x − 5) − 2(x + 7) = 3x + 15',
  beats: [
    {
      say: 'Here is a big one, with two brackets. We will open the brackets, gather what is alike, and then find x.',
      board: [
        { op: 'write', id: 'p1', text: 'Open brackets, gather, undo', label: true },
        { op: 'write', id: 'l1', text: '4(3x − 5) − 2(x + 7) = 3x + 15', tone: 'given' },
      ],
    },
    {
      say: 'The 4 outside multiplies everything inside its bracket. 4 times 3 x, and 4 times minus 5.',
      board: [{ op: 'arc', line: 'l1', from: { text: '4' }, to: [{ text: '3x' }, { text: '5' }] }],
    },
    {
      say: 'Careful here: it is minus 2 that goes into the second bracket, so it multiplies the x and the 7 as well.',
      board: [
        { op: 'arc', line: 'l1', from: { text: '2' }, to: [{ text: 'x', nth: 2 }, { text: '7' }] },
        { op: 'note', line: 'l1', target: { text: '− 2' }, text: 'the minus goes in too', place: 'below' },
      ],
    },
    {
      say: 'So the brackets are gone. Now look for terms that are alike. 12 x and minus 2 x belong together.',
      board: [
        { op: 'write', id: 'l2', text: '12x − 20 − 2x − 14 = 3x + 15' },
        { op: 'group', line: 'l2', targets: [{ text: '12x' }, { text: '− 2x' }], label: '10x' },
      ],
    },
    {
      say: 'That gives 10 x, minus 34, on the left. Picture it as a balance, with both sides level.',
      board: [
        { op: 'write', id: 'l3', text: '10x − 34 = 3x + 15' },
        { op: 'figure', id: 'f1', spec: { kind: 'balance', left: '10x − 34', right: '3x + 15' } },
      ],
    },
    {
      say: 'We want every x on one side. So we take 3 x away from both sides.',
      board: [
        { op: 'strike', line: 'l3', target: { text: '3x' }, note: '− 3x' },
        { op: 'both', line: 'l3', text: '− 3x' },
      ],
    },
    {
      say: 'Now 7 x, minus 34, equals 15. To undo minus 34 we add 34, and 15 plus 34 makes 49.',
      board: [
        { op: 'write', id: 'l4', text: '7x − 34 = 15' },
        { op: 'strike', line: 'l4', target: { text: '− 34' }, note: '+ 34' },
        { op: 'write', id: 'l5', text: '7x = 15 + 34' },
        { op: 'mark', line: 'l5', target: { text: '15 + 34' }, shape: 'underline' },
        { op: 'write', id: 'l6', text: '7x = 49' },
      ],
    },
    {
      say: 'Last step. 7 x means 7 times x, so we divide both sides by 7.',
      board: [{ op: 'divide', line: 'l6', by: '7' }],
    },
    {
      say: '49 divided by 7 is 7. So x equals 7. There it is!',
      board: [
        { op: 'write', id: 'l7', text: 'x = 7', tone: 'answer' },
        { op: 'mark', line: 'l7', target: { text: 'x = 7' }, shape: 'circle' },
      ],
    },
    {
      say: 'Let us check on a clean board. With 7 in place of x, the left side comes to 36, and so does the right side.',
      board: [
        { op: 'clear' },
        { op: 'write', id: 'c0', text: 'Check with x = 7', label: true },
        { op: 'write', id: 'c1', text: '4 × 16 − 2 × 14 = 36' },
        { op: 'write', id: 'c2', text: '3 × 7 + 15 = 36' },
        { op: 'mark', line: 'c1', target: { text: '36' }, shape: 'box' },
        { op: 'mark', line: 'c2', target: { text: '36' }, shape: 'box' },
      ],
    },
  ],
};

const SAMPLES: Lesson[] = [SAMPLE_SIMPLE, SAMPLE_BRACKETS];

/** About how long a voice takes to say a sentence, so the board is paced the way it will be in a lesson. */
function speakingMs(say: string): number {
  const words = say.split(/\s+/).filter((w) => w !== '').length;
  return Math.max(1500, words * 380);
}

/** Keeps only the beats that look like beats, so a malformed reply cannot break the page. */
function readBeats(data: unknown): TeachBeat[] | null {
  if (!data || typeof data !== 'object') return null;
  const beats = (data as { beats?: unknown }).beats;
  if (!Array.isArray(beats)) return null;
  const out: TeachBeat[] = [];
  for (let i = 0; i < beats.length; i++) {
    const beat = beats[i] as TeachBeat | null;
    if (beat && typeof beat === 'object' && typeof beat.say === 'string') out.push(beat);
  }
  return out.length > 0 ? out : null;
}

export default function TeachBoardPreviewPage() {
  const [questionId, setQuestionId] = useState('');
  const [lesson, setLesson] = useState<Lesson>(SAMPLE_BRACKETS);
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');

  const beats = lesson.beats;
  const current = Math.min(step, beats.length - 1);
  const beat = beats[current];

  // Everything on the board up to and including this beat; this beat's own ops are the new ones.
  const board = useMemo(() => {
    const ops: BoardOp[] = [];
    let animateFrom = 0;
    for (let i = 0; i <= current && i < beats.length; i++) {
      if (i === current) animateFrom = ops.length;
      const add = beats[i].board;
      if (Array.isArray(add)) {
        for (let j = 0; j < add.length; j++) ops.push(add[j]);
      }
    }
    return { ops: ops, animateFrom: animateFrom };
  }, [beats, current]);

  function show(next: Lesson) {
    setLesson(next);
    setStep(0);
    setMessage('');
  }

  async function load() {
    const id = questionId.trim();
    if (!id || busy) return;
    setBusy(true);
    setMessage('');
    try {
      const res = await fetch('/api/teach/' + encodeURIComponent(id));
      if (res.status === 404) {
        setMessage('No lesson is served for ' + id + ' yet. The samples below still work.');
        return;
      }
      if (!res.ok) {
        setMessage('The lesson could not be loaded (status ' + res.status + ').');
        return;
      }
      const loaded = readBeats(await res.json());
      if (!loaded) {
        setMessage('The reply for ' + id + ' had no beats in it.');
        return;
      }
      show({ title: id, beats: loaded });
    } catch {
      setMessage('The request did not go through. Check the connection and try again.');
    } finally {
      setBusy(false);
    }
  }

  const button = 'min-h-[48px] px-4 rounded-control border-2 border-ink font-extrabold disabled:opacity-50';

  return (
    <div className="min-h-screen bg-paper pb-24">
      <div className="max-w-xl mx-auto px-4 pt-6 space-y-5">
        <div>
          <h1 className="font-display text-display text-ink">Teach board preview</h1>
          <p className="text-label text-ink-muted mt-1">
            Step through a lesson a beat at a time. Narrow the window to see the board at phone width.
          </p>
        </div>

        <div className="bg-white rounded-card border-2 border-line p-4 space-y-3">
          <label className="block">
            <span className="text-caption text-ink-muted">Question id</span>
            <input
              className="w-full min-h-[48px] rounded-control border-2 border-line bg-white px-3 font-bold text-ink"
              value={questionId}
              onChange={(e) => setQuestionId(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void load();
              }}
              placeholder="VAR_EXT_G5_WS_B7_024_04"
              spellCheck={false}
              autoComplete="off"
            />
          </label>
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={() => void load()} disabled={busy || questionId.trim() === ''} className={button + ' bg-action text-white'}>
              {busy ? 'Loading…' : 'Load'}
            </button>
            {SAMPLES.map((sample) => (
              <button key={sample.title} type="button" onClick={() => show(sample)} className={button + ' bg-white text-ink'}>
                {sample.title}
              </button>
            ))}
          </div>
          {message && <p className="text-label text-ink bg-hint rounded-control px-3 py-2" role="status">{message}</p>}
        </div>

        <div className="space-y-3">
          <p className="text-caption text-ink-muted">
            {lesson.title} · beat {current + 1} of {beats.length} · {board.ops.length - board.animateFrom} new on the board
          </p>
          <WorkingBoard
            ops={board.ops}
            animateFrom={board.animateFrom}
            beatMs={speakingMs(beat.say)}
            className="max-h-[60vh]"
          />
          <p className="text-[17px] leading-snug font-bold text-ink min-h-[72px]">{beat.say}</p>
          {beat.ask && (
            <div className="rounded-control border-2 border-line bg-white px-3 py-2 text-label text-ink">
              {beat.ask.kind === 'choose' ? (
                <>
                  <p className="text-caption text-ink-muted">The child chooses:</p>
                  <ul className="mt-1 space-y-1">
                    {beat.ask.choices.map((choice, i) => (
                      <li key={i} className={beat.ask && beat.ask.kind === 'choose' && beat.ask.answer === i ? 'font-extrabold' : ''}>
                        {choice}
                      </li>
                    ))}
                  </ul>
                  <p className="mt-2 text-caption text-ink-muted">After a miss: {beat.ask.ifNot}</p>
                </>
              ) : (
                <p className="text-caption text-ink-muted">The child takes a moment to think.</p>
              )}
            </div>
          )}
          <div className="flex gap-2">
            <button type="button" onClick={() => setStep(Math.max(0, current - 1))} disabled={current === 0} className={button + ' flex-1 bg-white text-ink'}>
              Back
            </button>
            <button type="button" onClick={() => setStep(current + 1)} disabled={current >= beats.length - 1} className={button + ' flex-1 bg-action text-white'}>
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

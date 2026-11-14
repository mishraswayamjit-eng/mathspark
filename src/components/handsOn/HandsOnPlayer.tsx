'use client';

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { useReadAloud } from '@/hooks/useReadAloud';
import { toSpeech } from '@/lib/speech/mathToSpeech';
import { publishScreenContext, clearScreenContext, requestOpenSparky } from '@/lib/sparkyContext';
import { C } from '@/components/visuals/parts';
import {
  HANDS_ON_TOPIC, getFigure, meetsTarget, colouredAmount, colouredFraction, solveTarget, nextLessonId,
  type HandsOnLesson, type LessonScreen,
} from '@/lib/handsOn/partition';
import PartitionShape, { MathText } from './PartitionShape';

const SOUND_KEY = 'mathspark_handson_sound';
export const DONE_KEY = 'mathspark_handson_done';

const PRAISE = ['Great job! ⭐', 'You got it! 🎯', 'Excellent thinking! 🧠', 'Well done! 🌟'];

type Status = 'working' | 'right' | 'shown';

type Step =
  | { type: 'screen'; screen: LessonScreen; index: number }
  | { type: 'checkIntro' }
  | { type: 'done' };

/** The lesson's screens, with a short pause before the skill check and a finish screen. */
function buildSteps(lesson: HandsOnLesson): Step[] {
  const steps: Step[] = [];
  let introduced = false;
  for (let i = 0; i < lesson.screens.length; i++) {
    const screen = lesson.screens[i];
    if (screen.kind === 'check' && !introduced) {
      steps.push({ type: 'checkIntro' });
      introduced = true;
    }
    steps.push({ type: 'screen', screen, index: i });
  }
  steps.push({ type: 'done' });
  return steps;
}

function emptyShading(count: number): boolean[] {
  const out: boolean[] = [];
  for (let i = 0; i < count; i++) out.push(false);
  return out;
}

function saveScore(lessonId: string, score: number, outOf: number) {
  try {
    const raw = localStorage.getItem(DONE_KEY);
    const done = raw ? (JSON.parse(raw) as Record<string, { score: number; outOf: number }>) : {};
    const before = done[lessonId];
    if (!before || score >= before.score) done[lessonId] = { score, outOf };
    localStorage.setItem(DONE_KEY, JSON.stringify(done));
  } catch {
    // Storage can be unavailable (private mode); the lesson still works, it is just not remembered.
  }
}

export default function HandsOnPlayer({ lesson }: { lesson: HandsOnLesson }) {
  const steps = useMemo(() => buildSteps(lesson), [lesson]);
  const teachCount = useMemo(() => lesson.screens.filter((s) => s.kind !== 'check').length, [lesson]);
  const checkCount = lesson.screens.length - teachCount;

  const [stepIndex, setStepIndex] = useState(0);
  const [shaded, setShaded] = useState<boolean[]>([]);
  const [status, setStatus] = useState<Status>('working');
  const [message, setMessage] = useState<string | null>(null);
  const [showWhy, setShowWhy] = useState(false);
  const [tries, setTries] = useState(0);
  const [checkResults, setCheckResults] = useState<boolean[]>([]);
  const [sound, setSound] = useState(true);

  const { speak, stop, supported } = useReadAloud();

  const step = steps[stepIndex];
  const screen = step.type === 'screen' ? step.screen : null;
  const task = screen && screen.kind !== 'see' ? screen : null;
  const figure = task ? getFigure(task.figure) : null;
  const isCheck = screen?.kind === 'check';
  // One colour for the lesson, another for the skill check.
  const fill = isCheck ? '#0e7490' : C.action;

  useEffect(() => {
    try { setSound(localStorage.getItem(SOUND_KEY) !== 'off'); } catch { /* keep the default */ }
  }, []);

  // Sparky says the screen's line aloud.
  const line = screen && screen.kind !== 'check' ? screen.say : '';
  useEffect(() => {
    if (!sound || !supported || !line) return;
    speak(toSpeech(line));
    return () => stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stepIndex, sound, supported]);

  // Tell the Sparky widget what is on screen, so "help me with this" works here too.
  const colouredNow = figure && task ? colouredFraction(figure, shaded, task.target[1]) : '';
  useEffect(() => {
    if (!task || !figure) {
      clearScreenContext();
      return;
    }
    publishScreenContext({
      screen: 'practice',
      topicName: HANDS_ON_TOPIC,
      questionText: `${task.prompt} (A hands-on lesson: the child taps the pieces of a shape to colour them. The shape has ${figure.pieces.length} pieces, not all the same size. So far the child has coloured ${colouredNow}.)`,
    });
  }, [task, figure, colouredNow]);
  useEffect(() => () => clearScreenContext(), []);

  const toggle = useCallback((i: number) => {
    setShaded((prev) => {
      const next = prev.slice();
      next[i] = !next[i];
      return next;
    });
    setMessage(null);
  }, []);

  function check() {
    if (!task || !figure) return;
    const n = task.target[0];
    const d = task.target[1];
    if (meetsTarget(figure, shaded, n, d)) {
      setStatus('right');
      setMessage(PRAISE[(stepIndex + tries) % PRAISE.length]);
      if (isCheck) setCheckResults((prev) => prev.concat([tries === 0]));
      return;
    }
    const amount = colouredAmount(figure, shaded);
    const tooMuch = amount.coloured * d > n * amount.whole;
    setTries(tries + 1);
    setMessage(`Not quite yet. You have coloured ${colouredFraction(figure, shaded, d)}. We want ${n}/${d}, so colour a little ${tooMuch ? 'less' : 'more'}.`);
  }

  function showMe() {
    if (!task || !figure) return;
    const answer = solveTarget(figure, task.target[0], task.target[1]);
    if (answer) setShaded(answer);
    setStatus('shown');
    setShowWhy(true);
    setMessage("That's okay. Here is one way to do it.");
    if (isCheck) setCheckResults((prev) => prev.concat([false]));
  }

  function next() {
    stop();
    const upcoming = steps[stepIndex + 1];
    if (upcoming && upcoming.type === 'done') {
      let score = 0;
      for (let i = 0; i < checkResults.length; i++) if (checkResults[i]) score += 1;
      saveScore(lesson.id, score, checkCount);
    }
    // The next screen starts clean, in the same render as the move.
    setShaded([]);
    setStatus('working');
    setMessage(null);
    setShowWhy(false);
    setTries(0);
    setStepIndex(Math.min(stepIndex + 1, steps.length - 1));
  }

  function toggleSound() {
    const on = !sound;
    setSound(on);
    if (!on) stop();
    try { localStorage.setItem(SOUND_KEY, on ? 'on' : 'off'); } catch { /* not remembered */ }
  }

  // ── Progress ────────────────────────────────────────────────────────────────
  const screensDone = step.type === 'screen' ? step.index : step.type === 'checkIntro' ? teachCount : lesson.screens.length;
  const teachDone = Math.min(screensDone, teachCount);
  const checksDone = Math.max(0, screensDone - teachCount);

  const anyColoured = shaded.some(Boolean);
  const resolved = status !== 'working';
  const primary = 'min-h-[52px] px-6 rounded-control border-2 border-ink font-extrabold text-[16px] shadow-hard-sm transition-[transform,box-shadow] active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs disabled:opacity-40 disabled:shadow-none';
  const quiet = 'min-h-[52px] px-4 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[15px] hover:border-ink transition-colors';

  return (
    <div className="min-h-screen bg-paper pb-28 animate-fade-in">
      <div className="max-w-xl mx-auto px-4 pt-4">

        {/* ── Top bar: close, progress, sound ── */}
        <div className="flex items-center gap-3 mb-4">
          <Link href="/learn/hands-on" aria-label="Close the lesson" className="w-12 h-12 flex items-center justify-center rounded-control text-ink-muted hover:text-ink text-2xl font-bold flex-shrink-0">
            <span aria-hidden="true">×</span>
          </Link>
          <div
            className="flex-1 h-3 rounded-full bg-soft border-2 border-line overflow-hidden"
            role="progressbar"
            aria-label="Lesson progress"
            aria-valuemin={0}
            aria-valuemax={lesson.screens.length}
            aria-valuenow={screensDone}
          >
            <div className="h-full bg-success rounded-full transition-[width] duration-300" style={{ width: `${(teachDone / Math.max(1, teachCount)) * 100}%` }} />
          </div>
          <div className="flex items-center gap-1.5 flex-shrink-0" aria-hidden="true">
            {emptyShading(checkCount).map((_, i) => (
              <span key={i} className={`w-3 h-3 rounded-full border-2 ${i < checksDone ? 'bg-success border-success' : 'bg-white border-line'}`} />
            ))}
          </div>
          {supported && (
            <button
              type="button"
              onClick={toggleSound}
              aria-pressed={sound}
              aria-label={sound ? 'Turn Sparky’s voice off' : 'Turn Sparky’s voice on'}
              className="w-12 h-12 flex items-center justify-center rounded-control border-2 border-line bg-white text-lg flex-shrink-0 hover:border-ink"
            >
              <span aria-hidden="true">{sound ? '🔊' : '🔇'}</span>
            </button>
          )}
        </div>

        {/* ── Skill-check pause ── */}
        {step.type === 'checkIntro' && (
          <div className="bg-white rounded-card border-2 border-line px-6 py-12 text-center">
            <div className="flex justify-center mb-4"><Sparky mood="encouraging" size={88} /></div>
            <p className="font-display text-display text-ink">Skill check</p>
            <p className="text-label text-ink-muted mt-2 max-w-[320px] mx-auto">
              {checkCount} questions on a new shape. Sparky stays quiet this time, so show what you know.
            </p>
            <button type="button" onClick={next} className={`${primary} bg-action text-white mt-6`}>Start</button>
          </div>
        )}

        {/* ── Finish ── */}
        {step.type === 'done' && (
          <LessonDone lesson={lesson} results={checkResults} outOf={checkCount} />
        )}

        {/* ── An explanation screen ── */}
        {screen && screen.kind === 'see' && (
          <div className="bg-white rounded-card border-2 border-line px-5 py-6">
            <p className="text-[18px] leading-snug font-bold text-ink"><MathText text={screen.text} /></p>
            <div className="flex flex-wrap items-end justify-center gap-x-6 gap-y-4 my-7">
              {screen.show.map((item, i) => {
                const fig = getFigure(item.figure);
                if (!fig) return null;
                const marks = emptyShading(fig.pieces.length);
                for (let k = 0; k < item.shaded.length; k++) marks[item.shaded[k]] = true;
                return (
                  <div key={i} className="flex flex-col items-center gap-2">
                    <PartitionShape figure={fig} shaded={marks} fill={fill} size={screen.show.length > 2 ? 104 : 132} label={`A shape with ${item.label} coloured`} />
                    <p className="text-[17px] font-extrabold text-ink"><MathText text={item.label} /></p>
                  </div>
                );
              })}
            </div>
            <SparkySays text={screen.say} />
            <div className="flex justify-end mt-5">
              <button type="button" onClick={next} className={`${primary} bg-ink text-white`}>Continue</button>
            </div>
          </div>
        )}

        {/* ── A task: colour the shape ── */}
        {task && figure && (
          <div
            className={`bg-white rounded-card border-2 px-5 py-6 transition-[border-color,box-shadow] duration-300 ${
              status === 'right' ? 'border-success shadow-[0_0_0_6px_#dff6ea]' : 'border-line'
            }`}
          >
            <p className="text-[19px] leading-snug font-extrabold text-ink"><MathText text={task.prompt} /></p>

            <div className="flex justify-center my-7">
              <PartitionShape
                figure={figure}
                shaded={shaded}
                fill={fill}
                onToggle={resolved ? undefined : toggle}
                label={`The shape to colour. It has ${figure.pieces.length} parts.`}
              />
            </div>

            <div className="min-h-[28px] flex justify-end">
              {!resolved && anyColoured && (
                <button type="button" onClick={() => { setShaded(emptyShading(figure.pieces.length)); setMessage(null); }} className="min-h-[48px] px-2 text-label text-ink-muted hover:text-ink">
                  <span aria-hidden="true">↺ </span>Start over
                </button>
              )}
            </div>

            <div aria-live="polite">
              {message ? (
                <SparkySays text={message} mood={status === 'right' ? 'celebrating' : 'encouraging'} />
              ) : screen && screen.kind === 'do' ? (
                <SparkySays text={screen.say} />
              ) : null}
              {showWhy && (
                <p className="mt-3 bg-soft rounded-control px-4 py-3 text-[15px] leading-relaxed font-semibold text-ink" role="note">
                  <MathText text={task.why} />
                </p>
              )}
            </div>

            <div className="flex flex-wrap items-center justify-end gap-2 mt-5">
              {!resolved && (
                <>
                  <button type="button" onClick={requestOpenSparky} className={quiet}>Ask Sparky</button>
                  <button type="button" onClick={showMe} className={quiet}>I don&apos;t know</button>
                  <button type="button" onClick={check} disabled={!anyColoured} className={`${primary} bg-ink text-white`}>Check</button>
                </>
              )}
              {resolved && (
                <>
                  {!showWhy && <button type="button" onClick={() => setShowWhy(true)} className={quiet}>Why?</button>}
                  <button type="button" onClick={next} className={`${primary} bg-success text-white`}>Continue</button>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SparkySays({ text, mood = 'happy' }: { text: string; mood?: 'happy' | 'encouraging' | 'celebrating' }) {
  return (
    <div className="flex items-end gap-2">
      <div className="flex-shrink-0"><Sparky mood={mood} size={40} /></div>
      <p className="bg-soft rounded-card rounded-bl-sm px-4 py-2.5 text-[15px] leading-relaxed font-semibold text-ink">
        <MathText text={text} />
      </p>
    </div>
  );
}

function LessonDone({ lesson, results, outOf }: { lesson: HandsOnLesson; results: boolean[]; outOf: number }) {
  let score = 0;
  for (let i = 0; i < results.length; i++) if (results[i]) score += 1;
  const nextId = nextLessonId(lesson.id);
  const all = score === outOf;
  return (
    <div className="bg-white rounded-card border-2 border-line px-6 py-10 text-center">
      <div className="flex justify-center mb-4"><Sparky mood="celebrating" size={96} /></div>
      <p className="font-display text-display text-ink">Lesson complete!</p>
      <p className="text-label text-ink-muted mt-1">{lesson.title}</p>
      <div className="inline-flex items-baseline gap-1 bg-soft rounded-tile px-6 py-4 mt-6">
        <span className="font-display text-display text-ink">{score}</span>
        <span className="font-display text-heading text-ink-muted">/ {outOf}</span>
      </div>
      <p className="text-label text-ink-muted mt-2">
        {all ? 'Every skill-check question right on the first try.' : 'Skill-check questions right on the first try. Have another go any time.'}
      </p>
      <div className="flex flex-col gap-2 mt-7 max-w-[320px] mx-auto">
        {nextId && (
          <Link href={`/learn/hands-on/${nextId}`} className="min-h-[52px] flex items-center justify-center rounded-control border-2 border-ink bg-action text-white font-extrabold shadow-hard-sm">
            Next lesson
          </Link>
        )}
        <Link href="/learn/hands-on" className="min-h-[52px] flex items-center justify-center rounded-control border-2 border-line bg-white text-ink font-extrabold hover:border-ink">
          All hands-on lessons
        </Link>
      </div>
    </div>
  );
}

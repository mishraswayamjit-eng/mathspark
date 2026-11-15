'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { C } from '@/components/visuals/parts';
import { useBoardCoach } from '@/hooks/useBoardCoach';
import { useTutorVoice } from '@/hooks/useTutorVoice';

/**
 * A small pencil pad for rough working.
 *
 * Takes a finger, a stylus (pressure makes the line thicker) or the mouse.
 * One ink colour, Undo and Clear. The pad wipes itself when `resetKey` changes
 * (a new question), and nothing drawn here is saved.
 *
 * Without `coachFor`, nothing leaves the device. With it, the live coach is
 * on: when the child pauses, a small picture of the pad is sent to
 * `/api/coach/board` and the tutor says what to do next. The child is told so
 * in a plain line, and can switch the looking off (remembered on the device).
 */

/** Device setting for the coach: 'off' switches it off; anything else is on. */
const COACH_SETTING_KEY = 'mathspark_board_coach';
/** Set once the "Sparky looks at the pad" line has been shown and a look has been sent. */
const COACH_TOLD_KEY = 'mathspark_board_coach_told';
/** Longest side, in pixels, of the picture sent to the coach. */
const COACH_IMAGE_MAX_SIDE = 1000;
const COACH_IMAGE_QUALITY = 0.7;
const JPEG_PREFIX = 'data:image/jpeg;base64,';

function readSetting(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    // Storage can be blocked (private browsing): carry on with the defaults.
    return null;
  }
}

function writeSetting(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // Not remembered on this device, and that is all: the pad still works.
  }
}

interface Point {
  x: number;
  y: number;
  w: number;
}

interface Stroke {
  points: Point[];
}

/** Line thickness in CSS pixels for a finger or the mouse. */
const PEN_WIDTH = 3;

interface ScratchPadProps {
  /** Changing this wipes the pad. Pass the question id. */
  resetKey: string;
  /**
   * Turns on the live coach for this question: when the child pauses, the
   * tutor looks at what is on the pad and says what to do next. Leave out
   * wherever help is not allowed (a test in progress).
   */
  coachFor?: { questionId: string };
  /** Extra classes for the outer element. */
  className?: string;
}

function paintStroke(ctx: CanvasRenderingContext2D, points: Point[]) {
  if (points.length === 0) return;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = C.ink;
  ctx.fillStyle = C.ink;
  if (points.length === 1) {
    const p = points[0];
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.w / 2, 0, Math.PI * 2);
    ctx.fill();
    return;
  }
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1];
    const b = points[i];
    ctx.lineWidth = b.w;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }
}

export default function ScratchPad({ resetKey, coachFor, className }: ScratchPadProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const strokesRef = useRef<Stroke[]>([]);
  const drawingRef = useRef<Stroke | null>(null);
  const [strokeCount, setStrokeCount] = useState(0);

  // ── Live coach (only when `coachFor` is given) ─────────────────────────────
  const coachQuestionId = coachFor ? coachFor.questionId : '';
  const hasCoach = coachQuestionId !== '';
  // The child's own switch. On until the device says otherwise.
  const [coachOn, setCoachOn] = useState(true);
  // Whether this device has already been told that Sparky looks at the pad.
  const [alreadyTold, setAlreadyTold] = useState(true);

  useEffect(() => {
    if (!hasCoach) return;
    setCoachOn(readSetting(COACH_SETTING_KEY) !== 'off');
    setAlreadyTold(readSetting(COACH_TOLD_KEY) === '1');
  }, [hasCoach]);

  /** The pad as a small JPEG on white, redrawn from the strokes. Null when empty or hidden. */
  const getImage = useCallback((): string | null => {
    const wrap = wrapRef.current;
    const strokes = strokesRef.current;
    if (!wrap || strokes.length === 0) return null;
    const w = wrap.clientWidth;
    const h = wrap.clientHeight;
    if (w < 1 || h < 1) return null;
    const scale = COACH_IMAGE_MAX_SIDE / Math.max(w, h);
    const out = document.createElement('canvas');
    out.width = Math.max(1, Math.round(w * scale));
    out.height = Math.max(1, Math.round(h * scale));
    const ctx = out.getContext('2d');
    if (!ctx) return null;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, out.width, out.height);
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
    for (let i = 0; i < strokes.length; i++) paintStroke(ctx, strokes[i].points);
    const url = out.toDataURL('image/jpeg', COACH_IMAGE_QUALITY);
    if (url.indexOf(JPEG_PREFIX) !== 0) return null;
    return url.slice(JPEG_PREFIX.length);
  }, []);

  const coach = useBoardCoach({ questionId: coachQuestionId, getImage, enabled: hasCoach && coachOn });
  const { say, stop: stopVoice } = useTutorVoice();
  const coachRemark = coach.remark;
  const coachPenDown = coach.penDown;
  const coachPenUp = coach.penUp;
  const coachReset = coach.reset;
  const coachHasSent = coach.hasSent;
  const coachActive = hasCoach && coachOn && coach.available;

  // Say each new remark once.
  const spokenSeqRef = useRef(0);
  useEffect(() => {
    if (!coachRemark || coachRemark.seq === spokenSeqRef.current) return;
    spokenSeqRef.current = coachRemark.seq;
    say(coachRemark.text);
  }, [coachRemark, say]);

  // Once a look has been sent, this device has been told (the line stays up for this visit).
  useEffect(() => {
    if (coachHasSent) writeSetting(COACH_TOLD_KEY, '1');
  }, [coachHasSent]);

  function toggleCoach() {
    const next = !coachOn;
    setCoachOn(next);
    writeSetting(COACH_SETTING_KEY, next ? 'on' : 'off');
    if (!next) stopVoice();
  }

  const redraw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const dpr = window.devicePixelRatio || 1;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    for (let i = 0; i < strokesRef.current.length; i++) paintStroke(ctx, strokesRef.current[i].points);
  }, []);

  // Keep the canvas the same size as its box, at the screen's pixel density.
  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas) return;
    const fit = () => {
      const dpr = window.devicePixelRatio || 1;
      const w = Math.max(1, Math.round(wrap.clientWidth * dpr));
      const h = Math.max(1, Math.round(wrap.clientHeight * dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        redraw();
      }
    };
    fit();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(fit);
    observer.observe(wrap);
    return () => observer.disconnect();
  }, [redraw]);

  // A new question: start with a clean sheet.
  useEffect(() => {
    strokesRef.current = [];
    drawingRef.current = null;
    setStrokeCount(0);
    redraw();
    coachReset();
  }, [resetKey, redraw, coachReset]);

  function pointAt(e: React.PointerEvent<HTMLCanvasElement>): Point {
    const rect = e.currentTarget.getBoundingClientRect();
    // A stylus reports pressure; fingers and mice get an even line.
    const pressure = e.pointerType === 'pen' && e.pressure > 0 ? 0.5 + e.pressure : 1;
    return { x: e.clientX - rect.left, y: e.clientY - rect.top, w: PEN_WIDTH * pressure };
  }

  function down(e: React.PointerEvent<HTMLCanvasElement>) {
    e.currentTarget.setPointerCapture(e.pointerId);
    const stroke: Stroke = { points: [pointAt(e)] };
    drawingRef.current = stroke;
    const ctx = e.currentTarget.getContext('2d');
    if (ctx) paintStroke(ctx, stroke.points);
    coachPenDown();
  }

  function move(e: React.PointerEvent<HTMLCanvasElement>) {
    const stroke = drawingRef.current;
    if (!stroke) return;
    stroke.points.push(pointAt(e));
    const ctx = e.currentTarget.getContext('2d');
    // Draw only the newest segment.
    if (ctx) paintStroke(ctx, stroke.points.slice(-2));
  }

  function up() {
    const stroke = drawingRef.current;
    if (!stroke) return;
    drawingRef.current = null;
    strokesRef.current.push(stroke);
    setStrokeCount(strokesRef.current.length);
    coachPenUp();
  }

  function undo() {
    strokesRef.current.pop();
    setStrokeCount(strokesRef.current.length);
    redraw();
  }

  function clear() {
    strokesRef.current = [];
    setStrokeCount(0);
    redraw();
    // A clean sheet: the tutor forgets what it said about the old working.
    coachReset();
  }

  const tool = 'min-h-[48px] px-4 rounded-control border-2 border-line bg-white text-ink font-extrabold text-[14px] flex items-center gap-2 hover:border-ink transition-colors disabled:opacity-40 disabled:hover:border-line';

  return (
    <div className={className ?? ''}>
      <div
        ref={wrapRef}
        className="relative h-56 rounded-control border-2 border-line bg-white overflow-hidden"
      >
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full"
          style={{ touchAction: 'none', cursor: 'crosshair' }}
          onPointerDown={down}
          onPointerMove={move}
          onPointerUp={up}
          onPointerCancel={up}
          role="img"
          aria-label="Pencil pad for rough working"
        />
        {strokeCount === 0 && (
          <p className="absolute inset-0 flex items-center justify-center text-ink-muted text-[15px] font-bold pointer-events-none px-4 text-center">
            Draw or work it out here
          </p>
        )}
        {coachActive && coach.thinking && (
          <p
            role="status"
            className="absolute top-2 right-2 rounded-control border-2 border-line bg-soft px-3 py-1 text-[14px] font-bold text-ink-muted pointer-events-none"
          >
            <span aria-hidden="true">👀 </span>Sparky is having a look
          </p>
        )}
      </div>
      {coachActive && coachRemark && (
        <p
          role="status"
          className="mt-2 rounded-control border-2 border-line bg-hint px-4 py-3 text-[15px] leading-relaxed font-semibold text-ink"
        >
          <span aria-hidden="true">💬 </span>{coachRemark.text}
        </p>
      )}
      <div className="flex flex-wrap items-center gap-2 mt-2">
        <button type="button" onClick={undo} disabled={strokeCount === 0} className={tool}>
          <span aria-hidden="true">↩</span> Undo
        </button>
        <button type="button" onClick={clear} disabled={strokeCount === 0} className={tool}>
          <span aria-hidden="true">🗑</span> Clear
        </button>
        {coachActive && (
          <button
            type="button"
            onClick={coach.askNow}
            disabled={strokeCount === 0 || coach.thinking || coach.looksLeft <= 0}
            className={tool}
          >
            <span aria-hidden="true">🔎</span> Check my working
          </button>
        )}
      </div>
      {hasCoach && coach.available && (
        <div className="mt-2">
          <button
            type="button"
            role="switch"
            aria-checked={coachOn}
            onClick={toggleCoach}
            className="w-full min-h-[48px] px-4 rounded-control border-2 border-line bg-white text-ink font-bold text-[14px] flex items-center justify-between gap-2 hover:border-ink transition-colors"
          >
            <span>Sparky looks at my working</span>
            <span className={coachOn ? 'text-success font-extrabold' : 'text-ink-muted font-extrabold'}>
              {coachOn ? 'On' : 'Off'}
            </span>
          </button>
          {coachOn && !alreadyTold && (
            <p className="mt-2 text-[14px] leading-relaxed font-semibold text-ink-muted">
              When you pause, a picture of what is written on this pad is sent to Sparky&apos;s AI helper, so Sparky can say what to try next. MathSpark does not keep the picture. You can turn this off with the switch above.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

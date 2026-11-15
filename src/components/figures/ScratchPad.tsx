'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { C } from '@/components/visuals/parts';

/**
 * A small pencil pad for rough working.
 *
 * Takes a finger, a stylus (pressure makes the line thicker) or the mouse.
 * One ink colour, Undo and Clear. Nothing drawn here is saved or sent anywhere,
 * and the pad wipes itself when `resetKey` changes (a new question).
 */

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

export default function ScratchPad({ resetKey, className }: ScratchPadProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const strokesRef = useRef<Stroke[]>([]);
  const drawingRef = useRef<Stroke | null>(null);
  const [strokeCount, setStrokeCount] = useState(0);

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
  }, [resetKey, redraw]);

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
      </div>
      <div className="flex items-center gap-2 mt-2">
        <button type="button" onClick={undo} disabled={strokeCount === 0} className={tool}>
          <span aria-hidden="true">↩</span> Undo
        </button>
        <button type="button" onClick={clear} disabled={strokeCount === 0} className={tool}>
          <span aria-hidden="true">🗑</span> Clear
        </button>
      </div>
    </div>
  );
}

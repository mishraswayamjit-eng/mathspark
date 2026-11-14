'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { C } from './parts';

/**
 * A pencil layer over the whiteboard.
 *
 * When the pencil is on, a transparent canvas sits over whatever is on the
 * board and takes the pointer: a finger, a stylus (pressure makes the line
 * thicker) or the mouse. Strokes can be undone, rubbed out and cleared, and
 * the sketch can be handed to the chat as a picture so Sparky can look at it.
 * Nothing is uploaded until the child sends it.
 */

interface Stroke {
  color: string;
  width: number;
  erase: boolean;
  points: Array<{ x: number; y: number; w: number }>;
}

const INKS = [
  { name: 'Dark blue', value: C.ink },
  { name: 'Purple', value: C.action },
  { name: 'Green', value: C.success },
  { name: 'Orange', value: C.star },
];

interface SketchPadProps {
  /** Pencil on: the canvas takes the pointer. Off: the board underneath is used as normal. */
  active: boolean;
  /** Changing this wipes the sketch (a new picture has arrived on the board). */
  resetKey: string;
  /** Hands the finished sketch over as an image file. */
  onSend: (file: File) => void;
  children: ReactNode;
}

export default function SketchPad({ active, resetKey, onSend, children }: SketchPadProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const strokesRef = useRef<Stroke[]>([]);
  const drawingRef = useRef<Stroke | null>(null);

  const [ink, setInk] = useState(C.ink);
  const [erasing, setErasing] = useState(false);
  const [strokeCount, setStrokeCount] = useState(0);

  const paint = useCallback((ctx: CanvasRenderingContext2D, s: Stroke) => {
    if (s.points.length === 0) return;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = s.erase ? 'destination-out' : 'source-over';
    ctx.strokeStyle = s.color;
    ctx.fillStyle = s.color;
    if (s.points.length === 1) {
      const p = s.points[0];
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.w / 2, 0, Math.PI * 2);
      ctx.fill();
      return;
    }
    for (let i = 1; i < s.points.length; i++) {
      const a = s.points[i - 1];
      const b = s.points[i];
      ctx.lineWidth = b.w;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }
  }, []);

  const redraw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const dpr = window.devicePixelRatio || 1;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < strokesRef.current.length; i++) paint(ctx, strokesRef.current[i]);
  }, [paint]);

  // Keep the canvas the same size as the board, at the screen's pixel density.
  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas || typeof ResizeObserver === 'undefined') return;
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
    const observer = new ResizeObserver(fit);
    observer.observe(wrap);
    return () => observer.disconnect();
  }, [redraw]);

  // A new picture on the board: start with a clean sheet.
  useEffect(() => {
    strokesRef.current = [];
    drawingRef.current = null;
    setStrokeCount(0);
    redraw();
  }, [resetKey, redraw]);

  function pointAt(e: React.PointerEvent<HTMLCanvasElement>, base: number) {
    const rect = e.currentTarget.getBoundingClientRect();
    // A stylus reports pressure; fingers and mice get an even line.
    const pressure = e.pointerType === 'pen' && e.pressure > 0 ? 0.5 + e.pressure : 1;
    return { x: e.clientX - rect.left, y: e.clientY - rect.top, w: base * pressure };
  }

  function down(e: React.PointerEvent<HTMLCanvasElement>) {
    if (!active) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    const base = erasing ? 26 : 4;
    const stroke: Stroke = { color: ink, width: base, erase: erasing, points: [pointAt(e, base)] };
    drawingRef.current = stroke;
    const ctx = e.currentTarget.getContext('2d');
    if (ctx) paint(ctx, stroke);
  }

  function move(e: React.PointerEvent<HTMLCanvasElement>) {
    const stroke = drawingRef.current;
    if (!stroke) return;
    stroke.points.push(pointAt(e, stroke.width));
    const ctx = e.currentTarget.getContext('2d');
    if (!ctx) return;
    // Draw only the newest segment.
    paint(ctx, { color: stroke.color, width: stroke.width, erase: stroke.erase, points: stroke.points.slice(-2) });
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

  function send() {
    const canvas = canvasRef.current;
    if (!canvas || strokesRef.current.length === 0) return;
    // Flatten onto white so the picture reads well as a photo.
    const flat = document.createElement('canvas');
    flat.width = canvas.width;
    flat.height = canvas.height;
    const ctx = flat.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, flat.width, flat.height);
    ctx.drawImage(canvas, 0, 0);
    flat.toBlob((blob) => {
      if (blob) onSend(new File([blob], 'whiteboard-sketch.jpg', { type: 'image/jpeg' }));
    }, 'image/jpeg', 0.9);
  }

  const tool = 'w-12 h-12 flex-shrink-0 rounded-tile border-2 flex items-center justify-center text-lg transition-colors disabled:opacity-40';

  return (
    <div className="flex flex-col h-full min-h-0">
      {active && (
        <div className="flex items-center gap-2 px-4 py-2 border-b-2 border-line bg-soft flex-shrink-0 overflow-x-auto">
          {INKS.map((c) => (
            <button
              key={c.value}
              type="button"
              onClick={() => { setInk(c.value); setErasing(false); }}
              aria-label={`${c.name} pencil`}
              aria-pressed={!erasing && ink === c.value}
              className={`${tool} bg-white ${!erasing && ink === c.value ? 'border-ink shadow-hard-xs' : 'border-line'}`}
            >
              <span className="w-6 h-6 rounded-full border-2 border-ink" style={{ backgroundColor: c.value }} aria-hidden="true" />
            </button>
          ))}
          <button
            type="button"
            onClick={() => setErasing(!erasing)}
            aria-label="Rubber"
            aria-pressed={erasing}
            className={`${tool} ${erasing ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink'}`}
          >
            <span aria-hidden="true">🧽</span>
          </button>
          <button type="button" onClick={undo} disabled={strokeCount === 0} aria-label="Undo the last line" className={`${tool} bg-white border-line text-ink`}>
            <span aria-hidden="true">↩</span>
          </button>
          <button type="button" onClick={clear} disabled={strokeCount === 0} aria-label="Clear the sketch" className={`${tool} bg-white border-line text-ink`}>
            <span aria-hidden="true">🗑</span>
          </button>
          <button
            type="button"
            onClick={send}
            disabled={strokeCount === 0}
            className="ml-auto flex-shrink-0 min-h-[48px] px-4 rounded-control border-2 border-ink bg-action text-white font-extrabold text-[14px] shadow-hard-sm disabled:opacity-40 disabled:shadow-none"
          >
            Show Sparky
          </button>
        </div>
      )}

      <div className="flex-1 min-h-0 overflow-y-auto">
        <div ref={wrapRef} className="relative min-h-full">
          {children}
          <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full"
            style={{ pointerEvents: active ? 'auto' : 'none', touchAction: active ? 'none' : 'auto', cursor: active ? 'crosshair' : 'default' }}
            onPointerDown={down}
            onPointerMove={move}
            onPointerUp={up}
            onPointerCancel={up}
            aria-label="Sketch layer"
          />
        </div>
      </div>
    </div>
  );
}

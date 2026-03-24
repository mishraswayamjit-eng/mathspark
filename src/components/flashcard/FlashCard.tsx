'use client';

import React, { useState, useRef, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { getTopicColor } from '@/data/topicColors';
import type { FlashCard as FlashCardType } from '@/types';

const KatexRenderer = dynamic(() => import('@/components/KatexRenderer'), { ssr: false });

// ── Types ────────────────────────────────────────────────────────────────────

interface FlashCardProps {
  card: FlashCardType;
  /** Called when swiped right ("Nailed it") */
  onSwipeRight?: () => void;
  /** Called when swiped left ("Still learning") */
  onSwipeLeft?: () => void;
  /** Number of remaining cards behind this one (for stacked deck visual) */
  deckSize?: number;
  /** Whether confidence buttons are rendered externally (back face bottom left empty) */
  showConfidenceSlot?: boolean;
}

// ── Difficulty dots ──────────────────────────────────────────────────────────

const DifficultyDots = React.memo(function DifficultyDots({ level }: { level: number }) {
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className={`w-2 h-2 rounded-full ${
            i <= level ? 'bg-white/70' : 'bg-white/20'
          }`}
        />
      ))}
    </div>
  );
});

// ── Main component ───────────────────────────────────────────────────────────

export default function FlashCard({
  card,
  onSwipeRight,
  onSwipeLeft,
  deckSize = 0,
  showConfidenceSlot = false,
}: FlashCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const [dragX, setDragX] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [flyOff, setFlyOff] = useState<'left' | 'right' | null>(null);

  const touchStartRef = useRef<{ x: number; y: number; t: number } | null>(null);
  const cardRef = useRef<HTMLDivElement>(null);

  // Refs for stable callbacks (avoid recreating handlers on every drag pixel)
  const dragXRef = useRef(0);
  const isDraggingRef = useRef(false);
  const flyOffRef = useRef<'left' | 'right' | null>(null);
  const onSwipeRightRef = useRef(onSwipeRight);
  const onSwipeLeftRef = useRef(onSwipeLeft);
  onSwipeRightRef.current = onSwipeRight;
  onSwipeLeftRef.current = onSwipeLeft;

  const topicColor = getTopicColor(card.topicName);
  const SWIPE_THRESHOLD = 60;

  // ── Flip handler ─────────────────────────────────────────────────────────

  const handleFlip = useCallback(() => {
    if (isDraggingRef.current) return;
    setIsFlipped((prev) => !prev);
  }, []);

  // ── Touch / swipe handlers ───────────────────────────────────────────────

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    const touch = e.touches[0];
    touchStartRef.current = { x: touch.clientX, y: touch.clientY, t: Date.now() };
    isDraggingRef.current = false;
    setIsDragging(false);
  }, []);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (!touchStartRef.current) return;
    const touch = e.touches[0];
    const dx = touch.clientX - touchStartRef.current.x;
    const dy = touch.clientY - touchStartRef.current.y;
    // Only horizontal drags
    if (Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy)) {
      isDraggingRef.current = true;
      dragXRef.current = dx;
      setIsDragging(true);
      setDragX(dx);
    }
  }, []);

  const handleTouchEnd = useCallback(() => {
    if (!touchStartRef.current) return;
    const wasDragging = isDraggingRef.current;
    const dx = dragXRef.current;
    const wasShortTap = !wasDragging && Date.now() - touchStartRef.current.t < 300;

    if (wasDragging && Math.abs(dx) >= SWIPE_THRESHOLD) {
      const direction = dx > 0 ? 'right' : 'left';
      flyOffRef.current = direction;
      setFlyOff(direction);
      setTimeout(() => {
        if (direction === 'right') onSwipeRightRef.current?.();
        else onSwipeLeftRef.current?.();
        // Reset after callback
        flyOffRef.current = null;
        dragXRef.current = 0;
        setFlyOff(null);
        setDragX(0);
        setIsFlipped(false);
      }, 300);
    } else if (wasShortTap) {
      handleFlip();
    }

    if (!flyOffRef.current) { dragXRef.current = 0; setDragX(0); }
    isDraggingRef.current = false;
    setIsDragging(false);
    touchStartRef.current = null;
  }, [handleFlip]);

  // ── Mouse drag (desktop) ─────────────────────────────────────────────────

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    touchStartRef.current = { x: e.clientX, y: e.clientY, t: Date.now() };
    isDraggingRef.current = false;
    setIsDragging(false);
  }, []);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (!touchStartRef.current || e.buttons !== 1) return;
    const dx = e.clientX - touchStartRef.current.x;
    const dy = e.clientY - touchStartRef.current.y;
    if (Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy)) {
      isDraggingRef.current = true;
      dragXRef.current = dx;
      setIsDragging(true);
      setDragX(dx);
    }
  }, []);

  const handleMouseUp = useCallback(() => {
    handleTouchEnd();
  }, [handleTouchEnd]);

  // ── Computed styles ──────────────────────────────────────────────────────

  const dragRotation = isDragging ? Math.min(Math.max(dragX * 0.05, -15), 15) : 0;

  const cardStyle: React.CSSProperties = flyOff
    ? {
        transform: `translateX(${flyOff === 'right' ? '120vw' : '-120vw'}) rotate(${flyOff === 'right' ? 30 : -30}deg)`,
        transition: 'transform 300ms ease-out',
      }
    : isDragging
    ? {
        transform: `translateX(${dragX}px) rotate(${dragRotation}deg)`,
        transition: 'none',
      }
    : {
        transform: 'translateX(0) rotate(0deg)',
        transition: 'transform 200ms ease-out',
      };

  const swipeIndicatorOpacity = Math.min(Math.abs(dragX) / SWIPE_THRESHOLD, 1);

  return (
    <div className="relative w-full flex justify-center" style={{ perspective: '1000px' }}>
      {/* ── Stacked deck cards behind ──────────────────────────────────────── */}
      {deckSize >= 2 && (
        <div
          className="absolute rounded-[20px] bg-[#1E293B]/80 border border-white/[0.04]"
          style={{
            width: '85%',
            maxWidth: 400,
            aspectRatio: '3/4',
            transform: 'scale(0.9) translateY(16px)',
            zIndex: 0,
          }}
        />
      )}
      {deckSize >= 1 && (
        <div
          className="absolute rounded-[20px] bg-[#1E293B]/90 border border-white/[0.05]"
          style={{
            width: '85%',
            maxWidth: 400,
            aspectRatio: '3/4',
            transform: 'scale(0.95) translateY(8px)',
            zIndex: 1,
          }}
        />
      )}

      {/* ── Swipe indicators ──────────────────────────────────────────────── */}
      {isDragging && dragX > 20 && (
        <div
          className="absolute top-8 left-8 z-50 px-4 py-2 rounded-xl bg-duo-green/90 text-white font-bold text-lg rotate-[-12deg]"
          style={{ opacity: swipeIndicatorOpacity }}
        >
          Nailed it! 🎯
        </div>
      )}
      {isDragging && dragX < -20 && (
        <div
          className="absolute top-8 right-8 z-50 px-4 py-2 rounded-xl bg-blue-500/90 text-white font-bold text-lg rotate-[12deg]"
          style={{ opacity: swipeIndicatorOpacity }}
        >
          Still learning 📚
        </div>
      )}

      {/* ── Main card container ───────────────────────────────────────────── */}
      <div
        ref={cardRef}
        className="relative z-10 w-[85%] max-w-[400px] cursor-pointer select-none"
        style={{
          aspectRatio: '3/4',
          ...cardStyle,
        }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {/* ── Flip container ────────────────────────────────────────────── */}
        <div
          className="w-full h-full relative"
          style={{
            transformStyle: 'preserve-3d',
            transform: isFlipped
              ? 'rotateY(180deg) translateZ(40px)'
              : 'rotateY(0deg)',
            transition: 'transform 500ms cubic-bezier(0.4, 0.0, 0.2, 1)',
          }}
        >
          {/* ── FRONT FACE ──────────────────────────────────────────────── */}
          <div
            className="absolute inset-0 rounded-[20px] flex flex-col overflow-hidden flashcard-breathe"
            style={{
              backfaceVisibility: 'hidden',
              WebkitBackfaceVisibility: 'hidden',
              background: '#1E293B',
              borderLeft: `4px solid ${topicColor}`,
              border: `1px solid rgba(255,255,255,0.06)`,
              borderLeftWidth: '4px',
              borderLeftColor: topicColor,
              boxShadow: '0 4px 24px rgba(52,211,153,0.08), 0 1px 4px rgba(0,0,0,0.3)',
            }}
          >
            {/* Top bar */}
            <div className="flex items-center justify-between px-4 pt-4 pb-2">
              <span
                className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"
                style={{ backgroundColor: topicColor + '22', color: topicColor }}
              >
                {card.topicName}
              </span>
              <DifficultyDots level={card.difficulty} />
            </div>

            {/* Center — question */}
            <div className="flex-1 flex flex-col items-center justify-center px-6 text-center gap-3">
              <p className="text-[#F1F5F9] text-xl sm:text-2xl font-bold leading-snug">
                {card.front}
              </p>
              {card.formula && (
                <div className="mt-2">
                  <KatexRenderer
                    latex={card.formula}
                    displayMode
                    className="text-[#F1F5F9] text-2xl"
                  />
                </div>
              )}
            </div>

            {/* Bottom — tap hint */}
            <div className="pb-5 text-center">
              <p className="text-sm text-[#94A3B8] animate-pulse">
                Tap to reveal ✨
              </p>
            </div>
          </div>

          {/* ── BACK FACE ───────────────────────────────────────────────── */}
          <div
            className="absolute inset-0 rounded-[20px] flex flex-col overflow-hidden"
            style={{
              backfaceVisibility: 'hidden',
              WebkitBackfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
              background: 'linear-gradient(135deg, #1E293B 0%, #1a2332 100%)',
              borderLeft: `4px solid ${topicColor}`,
              border: `1px solid rgba(255,255,255,0.06)`,
              borderLeftWidth: '4px',
              borderLeftColor: topicColor,
              boxShadow: '0 4px 24px rgba(52,211,153,0.08), 0 1px 4px rgba(0,0,0,0.3)',
            }}
          >
            {/* Top — Answer label */}
            <div className="px-4 pt-4 pb-2">
              <span className="text-xs font-bold uppercase tracking-[1.5px] text-[#34D399]">
                Answer
              </span>
            </div>

            {/* Center — answer text */}
            <div className="flex-1 flex flex-col items-center justify-center px-6 text-center gap-3">
              <p className="text-[#F1F5F9] text-lg sm:text-xl font-bold leading-snug">
                {card.back}
              </p>
              {card.formula && (
                <div className="mt-2">
                  <KatexRenderer
                    latex={card.formula}
                    displayMode
                    className="text-[#F1F5F9] text-2xl"
                  />
                </div>
              )}
            </div>

            {/* Bottom — confidence buttons slot or empty */}
            <div className="pb-5 px-4">
              {showConfidenceSlot ? (
                <div className="h-14" /> // Placeholder for external confidence buttons
              ) : (
                <p className="text-center text-xs text-[#64748B]">
                  Swipe right = Got it · Swipe left = Review again
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

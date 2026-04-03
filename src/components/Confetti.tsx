'use client';

import { useEffect, useRef, useState } from 'react';

const COLORS = ['#58CC02', '#1CB0F6', '#FF9600', '#FF4B4B', '#FFC800', '#CE82FF'];

interface Particle {
  id: number;
  x: number;
  size: number;
  delay: number;
  color: string;
  borderRadius: string;
  duration: number;
}

const VARIANT_CONFIG = {
  full: { count: 30, minSize: 6, maxSize: 12, duration: 1800, baseDur: 1.2, durRange: 0.6, delayRange: 0.4 },
  mini: { count: 12, minSize: 4, maxSize: 8,  duration: 1000, baseDur: 0.7, durRange: 0.3, delayRange: 0.2 },
} as const;

function makeParticles(variant: 'full' | 'mini'): Particle[] {
  const cfg = VARIANT_CONFIG[variant];
  return Array.from({ length: cfg.count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    size: cfg.minSize + Math.random() * (cfg.maxSize - cfg.minSize),
    delay: Math.random() * cfg.delayRange,
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
    borderRadius: ['50%', '0%', '4px'][Math.floor(Math.random() * 3)],
    duration: cfg.baseDur + Math.random() * cfg.durRange,
  }));
}

interface ConfettiProps {
  variant?: 'full' | 'mini';
  onDone?: () => void;
}

export default function Confetti({ variant = 'full', onDone }: ConfettiProps) {
  const cfg = VARIANT_CONFIG[variant];
  const [particles] = useState(() => makeParticles(variant));
  const [visible, setVisible] = useState(true);
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      onDoneRef.current?.();
    }, cfg.duration);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!visible) return null;

  return (
    <div
      className="fixed inset-0 pointer-events-none z-50 overflow-hidden"
      aria-hidden="true"
    >
      {particles.map((p) => (
        <div
          key={p.id}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: '-20px',
            width:  p.size,
            height: p.size,
            background: p.color,
            borderRadius: p.borderRadius,
            animation: `confetti-fall ${p.duration}s ease-in ${p.delay}s forwards`,
          }}
        />
      ))}
    </div>
  );
}

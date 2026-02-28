'use client';

import { useEffect, useState } from 'react';

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

function makeParticles(count: number): Particle[] {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    size: 6 + Math.random() * 6,
    delay: Math.random() * 0.4,
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
    borderRadius: ['50%', '0%', '4px'][Math.floor(Math.random() * 3)],
    duration: 1.2 + Math.random() * 0.6,
  }));
}

interface ConfettiProps {
  onDone?: () => void;
}

export default function Confetti({ onDone }: ConfettiProps) {
  const [particles] = useState(() => makeParticles(30));
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      onDone?.();
    }, 1800);
    return () => clearTimeout(t);
  }, [onDone]);

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

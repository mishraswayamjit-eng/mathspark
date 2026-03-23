'use client';

interface TimerCircleProps {
  totalMs: number;
  remainingMs: number;
  size?: number;
}

export default function TimerCircle({ totalMs, remainingMs, size = 56 }: TimerCircleProps) {
  const pct = totalMs > 0 ? Math.max(0, remainingMs / totalMs) : 0;
  const seconds = Math.ceil(remainingMs / 1000);

  const r = (size - 8) / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - pct);

  // Color shifts: green → amber → red
  let color = '#34D399'; // green
  if (pct < 0.3) color = '#EF4444'; // red
  else if (pct < 0.6) color = '#F59E0B'; // amber

  // Pulse when under 3 seconds
  const pulse = seconds <= 3 && seconds > 0;

  return (
    <div className={`relative flex-shrink-0 ${pulse ? 'animate-pulse' : ''}`}>
      <svg width={size} height={size}>
        {/* Background ring */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth={5}
        />
        {/* Progress ring */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={5}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          className="transition-[stroke-dashoffset] duration-200"
        />
        {/* Seconds text */}
        <text
          x={size / 2}
          y={size / 2}
          textAnchor="middle"
          dominantBaseline="central"
          fill={color}
          fontSize={size * 0.36}
          fontWeight="900"
          className="tabular-nums"
        >
          {seconds}
        </text>
      </svg>
    </div>
  );
}

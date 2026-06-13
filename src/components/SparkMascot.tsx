'use client';

/**
 * Spark — MathSpark's mascot. A friendly glowing star.
 *
 * Deliberately RESTRAINED (per design direction): two expressions only,
 * used in celebrations and the chat companion — not plastered on every screen.
 */

interface SparkMascotProps {
  /** 'idle' = calm smile · 'cheer' = happy, eyes-closed grin */
  expression?: 'idle' | 'cheer';
  /** pixel size (square) */
  size?: number;
  /** soft pulsing glow */
  glow?: boolean;
  className?: string;
}

// Rounded 5-point star outline (computed for a 100×100 viewBox).
const STAR_POINTS =
  '50,6 60.58,35.44 91.85,36.4 67.12,55.56 75.86,85.6 50,68 24.14,85.6 32.88,55.56 8.15,36.4 39.42,35.44';

export default function SparkMascot({
  expression = 'idle',
  size = 48,
  glow = false,
  className = '',
}: SparkMascotProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      role="img"
      aria-label="Spark, your math buddy"
      className={`${glow ? 'animate-spark-glow' : ''} ${className}`}
    >
      {/* Star body */}
      <polygon
        points={STAR_POINTS}
        fill="#FFC53D"
        stroke="#FFC53D"
        strokeWidth="8"
        strokeLinejoin="round"
      />
      {/* Inner highlight for a soft 3D pop */}
      <polygon
        points={STAR_POINTS}
        fill="#FFD874"
        opacity="0.55"
        transform="translate(50 47) scale(0.62) translate(-50 -50)"
      />

      {expression === 'cheer' ? (
        <>
          {/* Happy closed eyes */}
          <path d="M37 46 q4 -5 8 0" stroke="#3D3DAA" strokeWidth="3.5" strokeLinecap="round" fill="none" />
          <path d="M55 46 q4 -5 8 0" stroke="#3D3DAA" strokeWidth="3.5" strokeLinecap="round" fill="none" />
          {/* Big grin */}
          <path d="M40 53 q10 12 20 0" stroke="#3D3DAA" strokeWidth="3.5" strokeLinecap="round" fill="none" />
          {/* Cheeks */}
          <circle cx="35" cy="53" r="3" fill="#FF7A59" opacity="0.55" />
          <circle cx="65" cy="53" r="3" fill="#FF7A59" opacity="0.55" />
        </>
      ) : (
        <>
          {/* Calm round eyes */}
          <circle cx="42" cy="47" r="3.6" fill="#3D3DAA" />
          <circle cx="58" cy="47" r="3.6" fill="#3D3DAA" />
          {/* Gentle smile */}
          <path d="M43 55 q7 7 14 0" stroke="#3D3DAA" strokeWidth="3.2" strokeLinecap="round" fill="none" />
        </>
      )}
    </svg>
  );
}

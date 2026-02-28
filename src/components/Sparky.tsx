// Sparky — inline SVG calculator mascot with 4 moods

export type SparkyMood = 'happy' | 'thinking' | 'encouraging' | 'celebrating';

interface SparkyProps {
  mood?: SparkyMood;
  size?: number;
  className?: string;
}

export default function Sparky({ mood = 'happy', size = 120, className = '' }: SparkyProps) {
  // Mouth path per mood
  const mouth = {
    happy:       <path d="M 38 72 Q 50 84 62 72" stroke="#1a1a1a" strokeWidth="3" fill="none" strokeLinecap="round" />,
    thinking:    <path d="M 38 74 Q 45 70 50 74 Q 55 78 62 74" stroke="#1a1a1a" strokeWidth="3" fill="none" strokeLinecap="round" />,
    encouraging: <path d="M 40 72 Q 50 82 60 72" stroke="#1a1a1a" strokeWidth="3" fill="none" strokeLinecap="round" />,
    celebrating: <path d="M 34 70 Q 50 86 66 70" stroke="#1a1a1a" strokeWidth="3" fill="none" strokeLinecap="round" />,
  }[mood];

  // Brow overrides for thinking
  const leftBrow  = mood === 'thinking'
    ? <path d="M 33 45 Q 40 40 47 44" stroke="#1a1a1a" strokeWidth="2.5" fill="none" strokeLinecap="round" />
    : <path d="M 33 46 Q 40 43 47 46" stroke="#1a1a1a" strokeWidth="2"   fill="none" strokeLinecap="round" />;
  const rightBrow = mood === 'thinking'
    ? <path d="M 53 44 Q 60 42 67 46" stroke="#1a1a1a" strokeWidth="2.5" fill="none" strokeLinecap="round" />
    : <path d="M 53 46 Q 60 43 67 46" stroke="#1a1a1a" strokeWidth="2"   fill="none" strokeLinecap="round" />;

  // Extras per mood
  const extras = {
    happy: null,
    thinking: (
      <text x="66" y="30" fontSize="14" textAnchor="middle">💭</text>
    ),
    encouraging: (
      <text x="68" y="28" fontSize="12" textAnchor="middle">❤️</text>
    ),
    celebrating: (
      <>
        {/* Arms up */}
        <path d="M 18 60 Q 8 40 15 30"  stroke="#FF9600" strokeWidth="4" fill="none" strokeLinecap="round" />
        <path d="M 82 60 Q 92 40 85 30" stroke="#FF9600" strokeWidth="4" fill="none" strokeLinecap="round" />
        {/* Stars */}
        <text x="8"  y="28" fontSize="11">⭐</text>
        <text x="80" y="26" fontSize="11">⭐</text>
      </>
    ),
  }[mood];

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      className={className}
      role="img"
      aria-label={`Sparky ${mood}`}
    >
      {/* Body — rounded calculator */}
      <rect x="12" y="20" width="76" height="72" rx="16" ry="16" fill="#58CC02" />
      {/* Screen area */}
      <rect x="20" y="28" width="60" height="26" rx="8" ry="8" fill="#1e7a00" />
      {/* Screen shine */}
      <rect x="24" y="31" width="18" height="5" rx="3" ry="3" fill="rgba(255,255,255,0.25)" />
      {/* Buttons row */}
      {[0,1,2].map((col) => [0,1,2].map((row) => (
        <rect
          key={`${col}-${row}`}
          x={22 + col * 20}
          y={62 + row * 8}
          width="14"
          height="5"
          rx="2"
          fill="rgba(255,255,255,0.35)"
        />
      )))}
      {/* Eyes */}
      <circle cx="40" cy="52" r="6" fill="white" />
      <circle cx="60" cy="52" r="6" fill="white" />
      <circle cx="41" cy="53" r="3" fill="#1a1a1a" />
      <circle cx="61" cy="53" r="3" fill="#1a1a1a" />
      {/* Eye shine */}
      <circle cx="42.5" cy="51.5" r="1.2" fill="white" />
      <circle cx="62.5" cy="51.5" r="1.2" fill="white" />
      {/* Brows */}
      {leftBrow}
      {rightBrow}
      {/* Mouth */}
      {mouth}
      {/* Extras */}
      {extras}
    </svg>
  );
}

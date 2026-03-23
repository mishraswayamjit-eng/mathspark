'use client';

export default function ScrollButton({ targetId, children, className }: {
  targetId: string; children: React.ReactNode; className?: string;
}) {
  return (
    <button
      onClick={() => document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' })}
      className={className}
    >
      {children}
    </button>
  );
}

'use client';

// DuoButton — Duolingo-style pill button with 3D press-sink effect
import type { ReactNode } from 'react';

export type DuoVariant = 'green' | 'blue' | 'orange' | 'red' | 'white';

interface DuoButtonProps {
  variant?: DuoVariant;
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  onClick?: () => void;
  children: ReactNode;
  type?: 'button' | 'submit';
}

const VARIANT_STYLES: Record<DuoVariant, { bg: string; border: string; text: string }> = {
  green:  { bg: 'bg-[#58CC02] hover:bg-[#5bd800]', border: 'border-b-[4px] border-[#46a302]', text: 'text-white' },
  blue:   { bg: 'bg-[#1CB0F6] hover:bg-[#22bfff]', border: 'border-b-[4px] border-[#0a98dc]', text: 'text-white' },
  orange: { bg: 'bg-[#FF9600] hover:bg-[#ffaa2a]', border: 'border-b-[4px] border-[#cc7800]', text: 'text-white' },
  red:    { bg: 'bg-[#FF4B4B] hover:bg-[#ff6060]', border: 'border-b-[4px] border-[#cc3333]', text: 'text-white' },
  white:  { bg: 'bg-white hover:bg-gray-50',         border: 'border-b-[4px] border-gray-300',  text: 'text-gray-700' },
};

export default function DuoButton({
  variant = 'green',
  disabled = false,
  loading = false,
  fullWidth = false,
  onClick,
  children,
  type = 'button',
}: DuoButtonProps) {
  const { bg, border, text } = VARIANT_STYLES[variant];

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        ${fullWidth ? 'w-full' : ''}
        ${bg} ${border} ${text}
        rounded-[9999px]
        min-h-[56px]
        px-6
        font-extrabold
        text-base
        uppercase
        tracking-wide
        transition-all
        duration-75
        select-none
        active:translate-y-[4px]
        active:border-b-0
        disabled:opacity-50
        disabled:cursor-not-allowed
        flex items-center justify-center gap-2
      `}
    >
      {loading ? (
        <span
          className="inline-block w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
          aria-hidden="true"
        />
      ) : children}
    </button>
  );
}

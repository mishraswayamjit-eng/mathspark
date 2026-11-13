'use client';

// DuoButton — IPM-style outlined button: ink border, hard offset shadow, sinks on press.
// Variant names are historical: `green` is the primary action (indigo), `blue` is a
// secondary button (white, same as `white`), `orange` is a reward, `red` is not-quite.
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
  green:  { bg: 'bg-action hover:bg-action-dark', border: 'border-2 border-ink', text: 'text-white' },
  blue:   { bg: 'bg-white hover:bg-soft',           border: 'border-2 border-ink', text: 'text-ink' },
  orange: { bg: 'bg-star hover:brightness-95',      border: 'border-2 border-ink', text: 'text-ink' },
  red:    { bg: 'bg-retry hover:brightness-95',      border: 'border-2 border-ink', text: 'text-white' },
  white:  { bg: 'bg-white hover:bg-soft',           border: 'border-2 border-ink', text: 'text-ink' },
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
        rounded-control
        min-h-[52px]
        px-5
        font-extrabold
        text-base
        shadow-hard-sm
        transition-[colors,transform,box-shadow]
        duration-75
        select-none
        active:translate-x-[2px]
        active:translate-y-[2px]
        active:shadow-hard-xs
        disabled:opacity-50
        disabled:cursor-not-allowed
        disabled:pointer-events-none
        flex items-center justify-center gap-2
      `}
    >
      {loading ? (
        <span
          className="inline-block w-5 h-5 border-2 border-transparent border-t-current border-r-current rounded-full animate-spin"
          aria-hidden="true"
        />
      ) : children}
    </button>
  );
}

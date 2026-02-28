'use client';

import { useEffect, useRef } from 'react';

interface KatexRendererProps {
  latex: string;
  displayMode?: boolean;
  className?: string;
}

export default function KatexRenderer({
  latex,
  displayMode = false,
  className = '',
}: KatexRendererProps) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!ref.current || !latex) return;
    Promise.all([
      import('katex'),
      import('katex/dist/katex.min.css' as string),
    ]).then(([{ default: katex }]) => {
      try {
        katex.render(latex, ref.current!, {
          displayMode,
          throwOnError: false,
          strict: false,
          trust: false,
        });
      } catch {
        if (ref.current) ref.current.textContent = latex;
      }
    });
  }, [latex, displayMode]);

  if (!latex) return null;
  return <span ref={ref} className={className} />;
}

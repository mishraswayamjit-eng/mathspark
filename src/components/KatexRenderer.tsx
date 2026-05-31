'use client';

import { useEffect, useRef } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

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
    let html = '';
    try {
      html = katex.renderToString(latex, {
        displayMode,
        throwOnError: false,
        strict: false,
        trust: false,
      });
    } catch {
      html = `<span style="color:#888">${latex}</span>`;
    }
    if (ref.current) ref.current.innerHTML = html;
  }, [latex, displayMode]);

  if (!latex) return null;
  return <span ref={ref} className={className} />;
}

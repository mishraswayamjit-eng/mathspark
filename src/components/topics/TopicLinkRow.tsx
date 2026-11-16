import Link from 'next/link';

// One tappable row: emoji tile, title, one line of help, chevron. Used for the
// content on a topic page and for the "More ways to learn" links on Learn.
// No hooks, so server and client components can both render it.

export interface TopicLinkRowProps {
  href: string;
  emoji: string;
  title: string;
  sub: string;
}

export default function TopicLinkRow({ href, emoji, title, sub }: TopicLinkRowProps) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 bg-white rounded-card border-2 border-line hover:border-ink px-4 py-3 min-h-[76px] transition-colors active:scale-[0.98]"
    >
      <span
        className="w-11 h-11 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-2xl shrink-0"
        aria-hidden="true"
      >
        {emoji}
      </span>
      <span className="flex-1 min-w-0">
        <span className="block font-display text-title text-ink">{title}</span>
        <span className="block text-label text-ink-muted">{sub}</span>
      </span>
      <span className="text-2xl leading-none text-ink-muted shrink-0" aria-hidden="true">›</span>
    </Link>
  );
}

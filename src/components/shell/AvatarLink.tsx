'use client';

import Link from 'next/link';
import { useStudent } from '@/components/shell/StudentProvider';

/**
 * Round 48px avatar that opens the child's profile. Takes no props: the initial
 * and colour come from the shared student payload (see StudentProvider).
 * The white edge plus ink ring keeps it visible on both dark and light headers.
 */
export default function AvatarLink() {
  const { student } = useStudent();
  const initial = student && student.name ? student.name.charAt(0).toUpperCase() : '';

  return (
    <Link
      href="/profile"
      aria-label="Your profile"
      className={`shrink-0 w-12 h-12 rounded-full border-2 border-white ring-2 ring-ink flex items-center justify-center text-white text-lg font-extrabold active:scale-95 transition-transform ${
        student ? '' : 'bg-ink-muted'
      }`}
      style={student ? { backgroundColor: student.avatarColor } : undefined}
    >
      <span aria-hidden="true">{initial || '🙂'}</span>
    </Link>
  );
}

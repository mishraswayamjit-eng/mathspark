// Types shared by the server loaders and the client shell.
// This file has no imports on purpose, so client components can use it freely.

/** The small student payload the app shell needs on every page. */
export interface StudentBootstrap {
  id: string;
  name: string;
  grade: number;
  /** Hex colour for the avatar circle, e.g. "#3B82F6". */
  avatarColor: string;
  /** Lifetime XP (Student.totalLifetimeXP). */
  totalXP: number;
  /** Current league tier, 1 (Bronze) to 5. */
  leagueTier: number;
}

/**
 * localStorage flag set while a parent (NextAuth) session is known to exist on
 * this device. The landing page uses it to decide whether it may send a child
 * straight to /home without waiting for the NextAuth session check.
 */
export const PARENT_SESSION_FLAG = 'mathspark_parent_session';

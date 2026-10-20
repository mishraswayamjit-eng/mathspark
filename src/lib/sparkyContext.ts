/**
 * Module-level store for the "what's on screen right now" context that the
 * Sparky widget uses to give page-aware help.
 *
 * Implemented as a tiny external store consumed via `useSyncExternalStore` so
 * that the `(app)` layout can stay a Server Component (no React Context
 * provider). Pages publish their current screen; the widget subscribes and
 * forwards the context to `/api/chat`.
 *
 * SAFETY: the context type deliberately has NO answer field. On a live graded
 * practice question we pass the question text only — never the correct answer —
 * so the LLM can guide without ever being handed (or able to reveal) the answer.
 */

import { useSyncExternalStore } from 'react';

export type ScreenKind =
  | 'practice'
  | 'lesson'
  | 'learn'
  | 'home'
  | 'progress'
  | 'flashcards'
  | 'other';

export interface ScreenContext {
  /** Which kind of screen the student is on — drives suggestion chips + prompt. */
  screen: ScreenKind;
  /** Human-readable topic name, if the screen has one. */
  topicName?: string;
  /** The question / problem text currently shown. NEVER the answer. */
  questionText?: string;
}

let current: ScreenContext | null = null;
const listeners = new Set<() => void>();

function emit() {
  for (const l of listeners) l();
}

/** Publish the current screen context (replaces any previous value). */
export function publishScreenContext(ctx: ScreenContext): void {
  current = ctx;
  emit();
}

/** Clear the screen context (e.g. on page unmount). */
export function clearScreenContext(): void {
  if (current === null) return;
  current = null;
  emit();
}

function subscribe(cb: () => void): () => void {
  listeners.add(cb);
  return () => listeners.delete(cb);
}

// ── Open-request channel — lets any page ask the floating widget to open ───────

const openListeners = new Set<() => void>();

/** Ask the floating Sparky widget to open (no-op if the widget isn't mounted). */
export function requestOpenSparky(): void {
  for (const l of openListeners) l();
}

/** Subscribe to open requests. Returns an unsubscribe fn. */
export function subscribeOpenSparky(cb: () => void): () => void {
  openListeners.add(cb);
  return () => openListeners.delete(cb);
}

function getSnapshot(): ScreenContext | null {
  return current;
}

/** Server snapshot — always null (context is a client-only concern). */
function getServerSnapshot(): ScreenContext | null {
  return null;
}

/** Subscribe to the current screen context from a client component. */
export function useScreenContext(): ScreenContext | null {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

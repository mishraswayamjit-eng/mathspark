'use client';

import { useCallback, useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { usePathname } from 'next/navigation';
import Sparky from '@/components/Sparky';
import { subscribeOpenSparky } from '@/lib/sparkyContext';
import { isAppChromeHidden, isPracticeSessionPath } from '@/lib/navVisibility';
import { useStudent } from '@/components/shell/StudentProvider';

// Only this button is in the app shell's eager bundle. The chat panel (and with
// it the message list, VisualBoard, SketchPad and voice) is a separate chunk,
// fetched when the child first reaches for Sparky.

/** What shows for the moment between the tap and the panel's code arriving. */
function PanelLoading() {
  return (
    <div
      className="fixed z-[70] flex flex-col items-center justify-center gap-3 bg-paper border-ink bottom-0 left-0 right-0 max-w-lg mx-auto rounded-t-card border-t-2 border-x-2 h-[56dvh] min-[1360px]:left-auto min-[1360px]:right-4 min-[1360px]:bottom-[84px] min-[1360px]:mx-0 min-[1360px]:w-[400px] min-[1360px]:max-w-none min-[1360px]:h-[min(78dvh,700px)] min-[1360px]:rounded-card min-[1360px]:border-2 min-[1360px]:shadow-hard"
      role="dialog"
      aria-label="Sparky chat"
      aria-busy="true"
    >
      <Sparky mood="thinking" size={64} />
      <p className="text-ink-muted font-semibold text-sm">Loading…</p>
    </div>
  );
}

const SparkyPanel = dynamic(() => import('@/components/shell/SparkyPanel'), {
  ssr: false,
  loading: () => <PanelLoading />,
});

/** Start fetching the panel's code early (finger down / pointer over the button). */
function preloadPanel() {
  import('@/components/shell/SparkyPanel').catch(() => {
    // Offline: the real open will try again and show the loading sheet meanwhile.
  });
}

export default function SparkyWidget() {
  const pathname = usePathname();
  // The signed-in child comes with the page from the server (see StudentProvider),
  // so the button is in the first paint: no waiting for an effect, and the same
  // on server and client.
  const { student } = useStudent();

  const [open, setOpen] = useState(false);
  // True once the child has opened the panel: from then on it stays mounted
  // (hidden while closed) so the conversation is kept. Until then nothing of the
  // chat runs, so no chat history is fetched on ordinary page loads.
  const [activated, setActivated] = useState(false);

  // Hide on the same routes as the bottom nav, plus the full /chat page itself,
  // and whenever no child is signed in.
  const hidden =
    !student ||
    isAppChromeHidden(pathname) ||
    pathname === '/chat' ||
    pathname.startsWith('/chat/');

  // A practice session keeps the screen clear: no floating button there. The
  // widget itself stays, so the session's own "Ask Sparky" buttons still open the chat.
  const noFloatingButton = isPracticeSessionPath(pathname);

  // Auto-close the sheet whenever the student navigates to another page.
  useEffect(() => { setOpen(false); }, [pathname]);

  // Leaving for a screen without the widget drops the panel entirely, as before.
  useEffect(() => {
    if (hidden) {
      setOpen(false);
      setActivated(false);
    }
  }, [hidden]);

  const openPanel = useCallback(() => {
    setActivated(true);
    setOpen(true);
  }, []);

  const closePanel = useCallback(() => setOpen(false), []);

  // Let pages (e.g. the practice result bubble) open the widget.
  useEffect(() => {
    if (hidden) return undefined;
    return subscribeOpenSparky(openPanel);
  }, [hidden, openPanel]);

  if (hidden) return null;

  return (
    <>
      {/* ── Floating action button ── */}
      {!open && !noFloatingButton && (
        <button
          type="button"
          onClick={openPanel}
          onPointerEnter={preloadPanel}
          onTouchStart={preloadPanel}
          onFocus={preloadPanel}
          aria-label="Ask Sparky"
          className="fixed right-4 z-[55] bg-white border-2 border-ink rounded-full p-1.5 shadow-hard-sm active:scale-95 transition-transform"
          style={{ bottom: 'calc(64px + env(safe-area-inset-bottom, 0px) + 12px)' }}
        >
          <Sparky mood="happy" size={44} />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-action rounded-full border-2 border-white flex items-center justify-center">
            <span className="text-white text-[9px] font-extrabold" aria-hidden="true">?</span>
          </span>
        </button>
      )}

      {/* ── Chat panel (separate chunk) ──
          The wrapper also hides the loading sheet if the child moves on before
          the panel's code has arrived. */}
      {activated && (
        <div hidden={!open}>
          <SparkyPanel open={open} onClose={closePanel} />
        </div>
      )}
    </>
  );
}

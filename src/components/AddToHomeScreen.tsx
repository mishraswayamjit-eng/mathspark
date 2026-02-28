'use client';

import { useEffect, useState } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export default function AddToHomeScreen() {
  const [show,   setShow]   = useState(false);
  const [isIOS,  setIsIOS]  = useState(false);
  const [prompt, setPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    if (localStorage.getItem('mathspark_a2hs_dismissed')) return;
    if (window.matchMedia('(display-mode: standalone)').matches) return;

    const count = parseInt(localStorage.getItem('mathspark_visit_count') ?? '0') + 1;
    localStorage.setItem('mathspark_visit_count', String(count));
    if (count < 3) return;

    const iOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    setIsIOS(iOS);
    if (iOS) { setShow(true); return; }

    const handler = (e: BeforeInstallPromptEvent) => {
      e.preventDefault();
      setPrompt(e);
      setShow(true);
    };
    window.addEventListener('beforeinstallprompt', handler as EventListener);
    return () => window.removeEventListener('beforeinstallprompt', handler as EventListener);
  }, []);

  if (!show) return null;

  function dismiss() {
    localStorage.setItem('mathspark_a2hs_dismissed', 'true');
    setShow(false);
  }

  function install() {
    prompt?.prompt();
    dismiss();
  }

  return (
    <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-50 w-[calc(100%-2rem)] max-w-lg">
      <div className="bg-[#131F24] rounded-2xl px-4 py-3 flex items-center gap-3 shadow-2xl">
        <span className="text-2xl">🧮</span>
        <p className="flex-1 text-white text-xs font-bold">
          {isIOS
            ? 'Tap Share → Add to Home Screen 📱'
            : 'Install MathSpark for quick access! 📱'}
        </p>
        {!isIOS && (
          <button
            onClick={install}
            style={{ minHeight: 0 }}
            className="bg-[#58CC02] text-white text-xs font-extrabold rounded-full px-3 py-1"
          >
            Install
          </button>
        )}
        <button
          onClick={dismiss}
          style={{ minHeight: 0 }}
          className="text-white/50 text-lg leading-none"
          aria-label="Dismiss"
        >
          ×
        </button>
      </div>
    </div>
  );
}

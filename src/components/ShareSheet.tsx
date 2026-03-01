'use client';

import { useRef, useState } from 'react';
import { track } from '@vercel/analytics';
import { ShareCard } from './ShareCard';
import type { ShareCardData } from './ShareCard';

// ── WhatsApp message templates ────────────────────────────────────────────────

function buildWhatsAppMessage(card: ShareCardData): string {
  if (card.type === 'lesson') {
    const { studentName, topicName, correct, total, xp } = card.data;
    return (
      `🌟 ${studentName} just completed a math lesson on MathSpark!\n` +
      `📐 Topic: ${topicName}\n` +
      `🎯 Score: ${correct}/${total} correct\n` +
      `⭐ Earned ${xp} XP\n` +
      `Keep encouraging them! 💪`
    );
  }
  if (card.type === 'mocktest') {
    const { studentName, score, totalQ, pct, strongTopic, weakTopic } = card.data;
    return (
      `📝 ${studentName} just took an IPM Mock Test on MathSpark!\n` +
      `🎯 Score: ${score}/${totalQ} (${pct}%)\n` +
      `💪 Strongest: ${strongTopic}\n` +
      `📚 Focus on: ${weakTopic}\n` +
      `They're preparing for the IPM exam! 🏆`
    );
  }
  if (card.type === 'badge') {
    const { studentName, badgeName, badgeDesc } = card.data;
    return (
      `🏅 ${studentName} just earned the ${badgeName} badge on MathSpark!\n` +
      `${badgeDesc}\n` +
      `So proud of their math journey! 🌟`
    );
  }
  if (card.type === 'streak') {
    const { studentName, streakDays } = card.data;
    return (
      `🔥 ${studentName} has practiced math for ${streakDays} days in a row on MathSpark!\n` +
      `That's incredible dedication! Keep cheering them on 💪`
    );
  }
  if (card.type === 'mastered') {
    const { studentName, topicName } = card.data;
    return (
      `🏆 ${studentName} just MASTERED ${topicName} on MathSpark!\n` +
      `So proud of their hard work and dedication! 🌟`
    );
  }
  return '';
}

// ── Props ─────────────────────────────────────────────────────────────────────

interface ShareSheetProps {
  card:            ShareCardData;
  studentId:       string;
  parentEmail?:    string;
  parentWhatsApp?: string;
  onClose:         () => void;
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function ShareSheet({
  card, studentId, parentEmail, parentWhatsApp, onClose,
}: ShareSheetProps) {
  const [sharing, setSharing] = useState<'whatsapp' | 'email' | 'gallery' | null>(null);
  const [toast,   setToast]   = useState<string | null>(null);
  const exportRef = useRef<HTMLDivElement>(null);

  function showToast(msg: string) {
    setToast(msg);
    setTimeout(() => setToast(null), 4500);
  }

  async function captureImage(): Promise<Blob | null> {
    if (!exportRef.current) return null;
    try {
      const { generateShareImage } = await import('@/lib/shareImage');
      return generateShareImage(exportRef.current);
    } catch {
      return null;
    }
  }

  function saveBlob(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a   = document.createElement('a');
    a.href     = url;
    a.download = filename;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  }

  // ── WhatsApp ───────────────────────────────────────────────────────────────
  async function handleWhatsApp() {
    setSharing('whatsapp');
    track('share_initiated', { cardType: card.type, method: 'whatsapp' });

    const message = buildWhatsAppMessage(card);

    try {
      const blob = await captureImage();

      // Try Web Share API with file (works on mobile Chrome/Safari)
      if (blob && typeof navigator.canShare === 'function') {
        const file = new File([blob], 'mathspark-achievement.png', { type: 'image/png' });
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({ title: 'MathSpark Achievement', text: message, files: [file] });
          track('share_completed', { cardType: card.type, method: 'whatsapp_native' });
          setSharing(null);
          onClose();
          return;
        }
      }

      // Fallback: save image + open WhatsApp URL with text
      if (blob) saveBlob(blob, 'mathspark-achievement.png');
      const cleanNumber = (parentWhatsApp ?? '').replace(/\D/g, '');
      if (cleanNumber) {
        window.open(`https://wa.me/${cleanNumber}?text=${encodeURIComponent(message)}`, '_blank');
        showToast('Image saved! Open WhatsApp and attach it 📎');
      } else {
        showToast('Image saved! Open WhatsApp and share it 📱');
      }
      track('share_completed', { cardType: card.type, method: 'whatsapp_fallback' });

    } catch (err) {
      // AbortError = user cancelled the native share sheet — that's fine
      if ((err as Error).name !== 'AbortError') {
        showToast('Could not share. Try "Save to Gallery" instead.');
      }
    } finally {
      setSharing(null);
    }
  }

  // ── Email ──────────────────────────────────────────────────────────────────
  async function handleEmail() {
    if (!parentEmail) {
      showToast("Add a parent email in Profile settings first! ⚙️");
      return;
    }
    setSharing('email');
    track('share_initiated', { cardType: card.type, method: 'email' });

    try {
      const res  = await fetch('/api/share/email', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body:    JSON.stringify({ studentId, cardType: card.type, cardData: card.data }),
      });
      const json = await res.json() as { success?: boolean; sentTo?: string; error?: string };
      if (res.ok && json.success) {
        showToast(`Sent to ${json.sentTo}! ✉️`);
        track('share_email_sent', { cardType: card.type });
        setTimeout(onClose, 2500);
      } else {
        showToast(json.error ?? 'Could not send. Try again.');
      }
    } catch {
      showToast('Network error. Try again.');
    } finally {
      setSharing(null);
    }
  }

  // ── Gallery ────────────────────────────────────────────────────────────────
  async function handleGallery() {
    setSharing('gallery');
    track('share_initiated', { cardType: card.type, method: 'gallery' });

    const blob = await captureImage();
    if (blob) {
      saveBlob(blob, 'mathspark-achievement.png');
      showToast('Saved! Share it anywhere you like 📸');
      track('share_completed', { cardType: card.type, method: 'gallery' });
    } else {
      showToast('Could not generate image. Please try again.');
    }
    setSharing(null);
  }

  return (
    <div className="fixed inset-0 z-[90] flex flex-col justify-end">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70" onClick={onClose} />

      {/* Toast */}
      {toast && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[100] bg-gray-800 text-white px-5 py-3 rounded-full text-sm font-bold animate-pop-in pointer-events-none shadow-xl max-w-xs text-center">
          {toast}
        </div>
      )}

      {/* Sheet */}
      <div className="relative bg-white rounded-t-3xl max-w-lg mx-auto w-full animate-slide-up shadow-2xl">

        {/* Header */}
        <div className="flex items-center justify-between px-5 pt-5 pb-3">
          <div>
            <p className="font-extrabold text-gray-800 text-base">Share with Parents 📤</p>
            <p className="text-xs text-gray-400 font-medium">Choose how to share this achievement</p>
          </div>
          <button
            onClick={onClose}
            style={{ minHeight: 0 }}
            className="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 font-bold text-lg"
          >
            ✕
          </button>
        </div>

        {/* Card preview (scaled to fit) */}
        <div className="mx-5 mb-4 overflow-hidden rounded-2xl bg-[#0A0E17]"
          style={{ height: 200, position: 'relative' }}>
          <div style={{
            position: 'absolute', top: 0, left: '50%',
            transform: 'translateX(-50%) scale(0.37)',
            transformOrigin: 'top center',
            width: 540,
          }}>
            <ShareCard card={card} />
          </div>
        </div>

        {/* Hidden full-size card used for PNG export */}
        <div style={{ position: 'fixed', left: -9999, top: 0, pointerEvents: 'none', zIndex: -1 }}>
          <ShareCard ref={exportRef} card={card} />
        </div>

        {/* Share options */}
        <div className="px-5 pb-8 space-y-3">
          <ShareOption
            emoji="📱"
            title="Send via WhatsApp"
            subtitle={parentWhatsApp
              ? `To ${parentWhatsApp}`
              : 'Shares image + message to parent'}
            color="#25D366"
            loading={sharing === 'whatsapp'}
            onClick={handleWhatsApp}
          />
          <ShareOption
            emoji="📧"
            title="Send via Email"
            subtitle={parentEmail
              ? `To ${parentEmail}`
              : 'Add parent email in Profile first'}
            color="#1CB0F6"
            loading={sharing === 'email'}
            onClick={handleEmail}
          />
          <ShareOption
            emoji="📸"
            title="Save to Gallery"
            subtitle="Download as image · share anywhere"
            color="#FF9600"
            loading={sharing === 'gallery'}
            onClick={handleGallery}
          />
        </div>
      </div>
    </div>
  );
}

// ── ShareOption button ────────────────────────────────────────────────────────

function ShareOption({
  emoji, title, subtitle, color, loading, onClick,
}: {
  emoji: string; title: string; subtitle: string;
  color: string; loading: boolean; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="w-full flex items-center gap-4 px-4 py-3.5 rounded-2xl border-2 border-gray-100 hover:bg-gray-50 active:bg-gray-100 transition-colors disabled:opacity-60"
    >
      <div
        className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0"
        style={{ backgroundColor: `${color}20`, border: `2px solid ${color}40` }}
      >
        {loading
          ? <span className="animate-spin-refresh text-base font-bold">↻</span>
          : emoji}
      </div>
      <div className="text-left flex-1">
        <p className="font-extrabold text-gray-800 text-sm">{title}</p>
        <p className="text-xs text-gray-400 font-medium">{subtitle}</p>
      </div>
      <span className="text-gray-300 text-xl">›</span>
    </button>
  );
}

'use client';

import { MS_PER_DAY } from '@/lib/timeConstants';
import { logError } from '@/lib/logger';
import { useCallback, useEffect, useRef, useState } from 'react';
import type { ScreenContext } from '@/lib/sparkyContext';
import { PHOTO_NOTE } from '@/lib/chatPhotoNote';
import { extractVisual } from '@/lib/visuals/spec';
import { useStudent } from '@/components/shell/StudentProvider';

// Shared across the full /chat page AND the floating Sparky widget so both
// surfaces drive one conversation (persisted session id below).
const SESSION_KEY = 'mathspark_chat_session_id';

export interface ChatUiMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  /** Preview of a photo the child sent with this message (this session only). */
  imageUrl?: string;
}

/** A photo waiting to be sent with the next message. */
export interface ChatAttachment {
  /** data: URL for the on-screen preview. */
  previewUrl: string;
  /** The same image as bare base64, for the server. */
  base64: string;
  mediaType: 'image/jpeg';
}

// Photos are shrunk in the browser before upload: plenty for handwriting, small
// enough to send quickly on a phone connection.
const MAX_PHOTO_EDGE = 1600;

function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const el = new Image();
    el.onload = () => resolve(el);
    el.onerror = () => reject(new Error('unreadable image'));
    el.src = url;
  });
}

/** Shrink a picked photo to a JPEG no larger than MAX_PHOTO_EDGE on its long side. */
async function toAttachment(file: File): Promise<ChatAttachment> {
  const objectUrl = URL.createObjectURL(file);
  try {
    const img = await loadImage(objectUrl);
    const longest = Math.max(img.naturalWidth, img.naturalHeight) || 1;
    const scale = Math.min(1, MAX_PHOTO_EDGE / longest);
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('no canvas');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const previewUrl = canvas.toDataURL('image/jpeg', 0.85);
    return { previewUrl, base64: previewUrl.slice(previewUrl.indexOf(',') + 1), mediaType: 'image/jpeg' };
  } finally {
    URL.revokeObjectURL(objectUrl);
  }
}

// ── Quick reply chips — grade-aware ───────────────────────────────────────────

export const QUICK_REPLIES_BASE = [
  { label: 'Quiz me! 🎯',                message: 'Quiz me on something from my recent topics!' },
  { label: 'Help with homework 📝',       message: "I'm stuck on my homework. Can you help me?" },
  { label: 'What should I practice? 🤔', message: 'What topic should I practice next?' },
];

export const QUICK_REPLIES_BY_GRADE: Record<number, Array<{ label: string; message: string }>> = {
  2: [{ label: 'Counting 🔢', message: 'Help me understand counting and numbers!' }, { label: 'Addition ➕', message: 'Can you explain addition with examples?' }],
  3: [{ label: 'Multiplication ✖️', message: 'Help me with multiplication tables!' }, { label: 'Fractions 🍕', message: 'Help me understand fractions!' }],
  4: [{ label: 'Decimals 📊', message: 'Can you explain decimals to me in a simple way?' }, { label: 'BODMAS 🧮', message: 'Can you explain BODMAS with an example?' }],
  5: [{ label: 'Percentages %', message: 'Help me understand percentages!' }, { label: 'Algebra 🔤', message: 'Can you explain algebra basics?' }],
  6: [{ label: 'Ratios ⚖️', message: 'Help me understand ratios and proportions!' }, { label: 'Geometry 📐', message: 'Can you explain geometry concepts?' }],
  7: [{ label: 'Linear equations 📝', message: 'Help me solve linear equations!' }, { label: 'Integers 🔢', message: 'Can you explain integers?' }],
  8: [{ label: 'Quadratics ²', message: 'Help me understand quadratic equations!' }, { label: 'Statistics 📊', message: 'Can you explain statistics?' }],
  9: [{ label: 'Trigonometry 📐', message: 'Help me understand trigonometry!' }, { label: 'Polynomials 🔤', message: 'Can you explain polynomials?' }],
};

export function getQuickReplies(grade: number) {
  return [...QUICK_REPLIES_BASE, ...(QUICK_REPLIES_BY_GRADE[grade] ?? QUICK_REPLIES_BY_GRADE[4])];
}

// ── Proactive nudge logic ─────────────────────────────────────────────────────

function getOpeningMessage(name: string, grade: number, lastPracticeDate: string | null, streakDays: number): string {
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - MS_PER_DAY).toDateString();

  if (!lastPracticeDate) {
    return `Hi ${name}! 🌟 I'm Sparky, your math buddy! I love helping with Grade ${grade} math. What would you like to explore today?`;
  }
  if (lastPracticeDate !== today && lastPracticeDate !== yesterday) {
    return `Hey ${name}! I missed you! 🔥 Want to keep your streak going? Let's solve some math together!`;
  }
  if (streakDays >= 3) {
    return `Hi ${name}! 🔥 You're on a ${streakDays}-day streak — amazing! Ready for some more math magic?`;
  }
  return `Hi ${name}! 🌟 Ready for some math magic today? Ask me anything or I can quiz you!`;
}

/** The current streak, from the object the streak tracker keeps in localStorage. */
function readStreakDays(): number {
  try {
    const raw = localStorage.getItem('mathspark_streak');
    if (!raw) return 0;
    const parsed = JSON.parse(raw) as { currentStreak?: unknown } | null;
    const days = parsed ? parsed.currentStreak : 0;
    return typeof days === 'number' && isFinite(days) ? days : 0;
  } catch {
    return 0;
  }
}

// ── Reading saved history ─────────────────────────────────────────────────────

interface StoredChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  /** ISO time the message was saved. */
  createdAt?: string;
}

function toUiMessages(stored: StoredChatMessage[]): ChatUiMessage[] {
  return stored.map((m) => ({
    id: m.id,
    role: m.role,
    // Photos are not kept: show a camera in place of the internal note.
    content: m.role === 'user' && m.content.indexOf(PHOTO_NOTE) === 0
      ? `📷 ${m.content.slice(PHOTO_NOTE.length).trim()}`
      : m.content,
  }));
}

// A reply that was still being written when this view opened (the child came
// from the other chat view mid-reply): how long to wait before looking again.
const PENDING_REPLY_RECHECK_MS = 6000;
const PENDING_REPLY_WINDOW_MS = 2 * 60_000;

// Added when the connection drops part-way through a reply: what arrived is kept.
const CUT_OFF_NOTE = 'Oh, I got cut off there! 🙈 Ask me to carry on and I will finish.';

// The longest message the server accepts (see /api/chat).
export const MAX_CHAT_MESSAGE_CHARS = 6000;

// ── Hook ──────────────────────────────────────────────────────────────────────

interface UseSparkyChatOptions {
  /** Called when there is no logged-in student (e.g. redirect to onboarding). */
  onNoStudent?: () => void;
}

export function useSparkyChat(opts: UseSparkyChatOptions = {}) {
  const { onNoStudent } = opts;

  // The signed-in child comes from the app shell (server truth). localStorage is
  // only a fallback for the moment before the shell knows who is signed in.
  const { student } = useStudent();
  const [storedId,    setStudentId]    = useState<string | null>(null);
  const [storedName,  setStudentName]  = useState('');
  const [storedGrade, setStudentGrade] = useState(4);
  const studentId    = student ? student.id : storedId;
  const studentName  = student ? student.name : storedName;
  const studentGrade = student ? student.grade : storedGrade;
  const [sessionId,    setSessionId]    = useState<string | null>(null);
  const [messages,     setMessages]     = useState<ChatUiMessage[]>([]);
  const [input,        setInput]        = useState('');
  const [isLoading,    setIsLoading]    = useState(false);
  const [streamingMsg, setStreamingMsg] = useState('');
  const [rateLimited,  setRateLimited]  = useState(false);
  const [initialized,  setInitialized]  = useState(false);
  const [remaining,    setRemaining]    = useState<number | null>(null);
  const [attachment,   setAttachment]   = useState<ChatAttachment | null>(null);
  const [attachmentNotice, setAttachmentNotice] = useState('');

  const inputRef = useRef<HTMLInputElement>(null);

  // Keep the persisted session id in sync so a new conversation on /chat and the
  // widget (or vice-versa) continue the same thread.
  const persistSession = useCallback((id: string | null) => {
    try {
      if (id) localStorage.setItem(SESSION_KEY, id);
      else localStorage.removeItem(SESSION_KEY);
    } catch { /* ignore */ }
  }, []);

  // Boot: load student + rehydrate the shared session (persisted id first, else
  // most recent) + proactive opening nudge.
  useEffect(() => {
    const storedGradeNum = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    const sid   = student ? student.id : localStorage.getItem('mathspark_student_id');
    const name  = student ? student.name : (localStorage.getItem('mathspark_student_name') ?? '');
    const grade = student ? student.grade : (isNaN(storedGradeNum) ? 4 : storedGradeNum);
    if (!sid) { onNoStudent?.(); setInitialized(true); return; }
    setStudentId(sid);
    setStudentName(name);
    setStudentGrade(grade);

    const persisted = (() => { try { return localStorage.getItem(SESSION_KEY); } catch { return null; } })();
    const url = persisted ? `/api/chat/history?sessionId=${encodeURIComponent(persisted)}` : '/api/chat/history';

    const showOpening = () => {
      // Written by the practice screens (a `toDateString()` value) and the streak tracker.
      const lastPractice = localStorage.getItem('mathspark_last_practice_date') ?? null;
      const opening = getOpeningMessage(name || 'friend', grade, lastPractice, readStreakDays());
      setMessages([{ id: 'opening', role: 'assistant', content: opening }]);
    };

    let alive = true;
    let recheckTimer: ReturnType<typeof setTimeout> | null = null;

    fetch(url)
      .then((r) => { if (!r.ok) throw new Error('Fetch failed'); return r.json(); })
      .then((session: { id: string; messages?: StoredChatMessage[] } | null) => {
        if (!alive) return;
        const stored = session && session.messages ? session.messages : [];
        if (session && stored.length > 0) {
          const loadedId = session.id;
          setSessionId(loadedId);
          persistSession(loadedId);
          setMessages(toUiMessages(stored));

          // The last word is the child's: Sparky's reply is probably still being
          // written (they moved here from the other chat view mid-reply). Show
          // the waiting state and look once more after a short while.
          // Only for a message sent in the last couple of minutes: an old
          // unanswered one is not going to get its reply now.
          const last = stored[stored.length - 1];
          const sentAt = last.createdAt ? new Date(last.createdAt).getTime() : NaN;
          if (last.role === 'user' && !isNaN(sentAt) && Math.abs(Date.now() - sentAt) < PENDING_REPLY_WINDOW_MS) {
            setIsLoading(true);
            recheckTimer = setTimeout(() => {
              recheckTimer = null;
              fetch(`/api/chat/history?sessionId=${encodeURIComponent(loadedId)}`)
                .then((r) => (r.ok ? r.json() : null))
                .then((again: { messages?: StoredChatMessage[] } | null) => {
                  if (!alive) return;
                  if (again && again.messages && again.messages.length > 0
                    && again.messages[again.messages.length - 1].id !== last.id) {
                    setMessages(toUiMessages(again.messages));
                  }
                })
                .catch((err) => logError('[sparky] recheck session history', err))
                .then(() => { if (alive) setIsLoading(false); });
            }, PENDING_REPLY_RECHECK_MS);
          }
        } else {
          showOpening();
        }
        setInitialized(true);
      })
      .catch((err) => {
        if (!alive) return;
        logError('[sparky] fetch session history', err);
        showOpening();
        setInitialized(true);
      });

    return () => {
      alive = false;
      if (recheckTimer !== null) clearTimeout(recheckTimer);
    };
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  // ── Photo of working ──────────────────────────────────────────────────────

  const attachImage = useCallback(async (file: File) => {
    setAttachmentNotice('');
    if (file.type.indexOf('image/') !== 0) {
      setAttachmentNotice('That file is not a picture. Try a photo of your working.');
      return;
    }
    try {
      setAttachment(await toAttachment(file));
    } catch {
      setAttachmentNotice("I couldn't open that photo. Try taking it again.");
    }
  }, []);

  const clearAttachment = useCallback(() => {
    setAttachment(null);
    setAttachmentNotice('');
  }, []);

  // ── Send message ──────────────────────────────────────────────────────────
  // Resolves with Sparky's full reply (or null if nothing was sent or it did
  // not come through), so voice mode can read the reply aloud.

  // `usePhoto: false` is for canned requests (suggestion chips, the help button,
  // voice): a photo the child has picked but not sent stays waiting in the composer.
  const sendMessage = useCallback(async (
    text: string,
    context?: ScreenContext | null,
    opts?: { usePhoto?: boolean },
  ): Promise<string | null> => {
    const photo = opts && opts.usePhoto === false ? null : attachment;
    // With a photo and no words, say the obvious thing on the child's behalf.
    const trimmed = text.trim() || (photo ? 'Here is my working. Can you check it? 📷' : '');
    if (!trimmed || isLoading || !studentId) return null;

    setInput('');
    if (photo) {
      setAttachment(null);
      setAttachmentNotice('');
    }
    setIsLoading(true);
    setStreamingMsg('');

    const userMsgId = `user-${Date.now()}`;
    setMessages((prev) => [...prev, {
      id: userMsgId, role: 'user', content: trimmed,
      ...(photo ? { imageUrl: photo.previewUrl } : {}),
    }]);

    // A message typed in the composer that did not get through goes back into
    // the composer (words and photo), so the child can send it again without
    // retyping. Canned requests (chips, the help button, voice) are left alone.
    const fromComposer = !(opts && opts.usePhoto === false);
    const putDraftBack = () => {
      if (!fromComposer) return;
      setMessages((prev) => prev.filter((m) => m.id !== userMsgId));
      setInput(text);
      if (photo) setAttachment(photo);
    };

    // What has arrived of the reply so far. Kept outside the `try` so a dropped
    // connection does not throw away what the child was already reading.
    let fullText = '';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          message: trimmed,
          ...(context ? { context } : {}),
          ...(photo ? { imageBase64: photo.base64, imageType: photo.mediaType } : {}),
        }),
      });

      if (res.status === 429) {
        // Two distinct 429 reasons: the per-minute rate limit ("rate", passes in a
        // moment) and the daily budget ("daily", lasts until tomorrow). Only the
        // daily one takes the composer away.
        let content = '';
        let reason = '';
        try {
          const body = await res.clone().json();
          if (typeof body?.error === 'string' && body.error) content = body.error;
          if (typeof body?.reason === 'string') reason = body.reason;
        } catch { /* keep defaults */ }
        if (reason === 'daily') {
          setRateLimited(true);
          if (!content) content = "You've been chatting a lot today — great work! 🌟 Come back tomorrow for more math adventures!";
        } else {
          putDraftBack();
          if (!content) content = "Let's slow down a little! 🐢 Try again in a moment.";
        }
        setMessages((prev) => [...prev, { id: `limit-${Date.now()}`, role: 'assistant', content }]);
        return null;
      }

      // Sparky is not switched on in this environment (no API key on the server).
      // Say so plainly instead of the generic retry message, which would never work.
      if (res.status === 503) {
        setMessages((prev) => [...prev, {
          id: `off-${Date.now()}`,
          role: 'assistant',
          content: "I'm not switched on here yet! 🔌 Ask a grown-up to check Sparky's settings, then try again.",
        }]);
        return null;
      }
      // Session expired: retrying will not help until the child logs in again.
      if (res.status === 401) {
        setMessages((prev) => [...prev, {
          id: `auth-${Date.now()}`,
          role: 'assistant',
          content: "I've lost track of who I'm talking to! 🙈 Please log in again and I'll be right here.",
        }]);
        return null;
      }

      if (!res.ok || !res.body) {
        logError(`[chat] /api/chat returned ${res.status}`);
        throw new Error('API error');
      }

      const remainingHeader = res.headers.get('X-Remaining');
      if (remainingHeader !== null) {
        const n = parseInt(remainingHeader, 10);
        if (!isNaN(n)) setRemaining(n);
      }

      // Reconcile sessionId from the server header. The server is the source of
      // truth: it may start a fresh session (we had none) OR hand back a
      // different id than we sent (e.g. ours expired / belonged to another
      // student). Always adopt the server's id so the widget and /chat page
      // keep driving the same persisted thread.
      const newSessionId = res.headers.get('X-Session-Id');
      if (newSessionId && newSessionId !== sessionId) {
        setSessionId(newSessionId);
        persistSession(newSessionId);
      }

      const reader  = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        fullText += decoder.decode(value, { stream: true });
        setStreamingMsg(fullText);
      }

      if (fullText) {
        setMessages((prev) => [...prev, { id: `asst-${Date.now()}`, role: 'assistant', content: fullText }]);
      }
      // Callers (voice mode) get the words only, without the whiteboard tag.
      return extractVisual(fullText).text || null;
    } catch {
      if (fullText.trim()) {
        // The connection dropped part-way: keep what arrived, and say it was cut off.
        const kept = `${fullText}\n\n${CUT_OFF_NOTE}`;
        setMessages((prev) => [...prev, { id: `asst-${Date.now()}`, role: 'assistant', content: kept }]);
        return null;
      }
      putDraftBack();
      setMessages((prev) => [...prev, {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: "Oops! I had a little brain freeze 🤔 Can you try sending that again?",
      }]);
      return null;
    } finally {
      setIsLoading(false);
      setStreamingMsg('');
      inputRef.current?.focus();
    }
  }, [studentId, sessionId, isLoading, persistSession, attachment]);

  // ── New conversation ──────────────────────────────────────────────────────

  const startNewChat = useCallback(() => {
    // Not while a reply is arriving: it would land in the new conversation.
    if (isLoading) return;
    setSessionId(null);
    persistSession(null);
    setRateLimited(false);
    setMessages([{
      id: `new-${Date.now()}`,
      role: 'assistant',
      content: `Starting fresh! 🌟 What math topic shall we explore today, ${studentName || 'friend'}?`,
    }]);
  }, [studentName, persistSession, isLoading]);

  const studentInitial = studentName ? studentName[0].toUpperCase() : '?';

  return {
    studentId, studentName, studentGrade,
    messages, input, setInput,
    isLoading, streamingMsg, rateLimited, initialized, remaining,
    sendMessage, startNewChat,
    studentInitial, inputRef,
    attachment, attachmentNotice, attachImage, clearAttachment,
  };
}

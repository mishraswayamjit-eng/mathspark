'use client';

import { MS_PER_DAY } from '@/lib/timeConstants';
import { useEffect, useState, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DuoButton from '@/components/DuoButton';
import VoicePicker from '@/components/voice/VoicePicker';
import { getTopicsForGrade } from '@/data/topicTree';
import { logError } from '@/lib/logger';
import { useStudent } from '@/components/shell/StudentProvider';
import { MONETIZATION_ENABLED } from '@/lib/monetization';

// ── Sub-components ────────────────────────────────────────────────────────────

function Toggle({ on, onToggle, label }: { on: boolean; onToggle: () => void; label: string }) {
  return (
    <button onClick={onToggle}
      type="button"
      role="switch"
      aria-checked={on}
      aria-label={label}
      className="relative min-w-[48px] min-h-[48px] flex items-center justify-center flex-shrink-0"
    >
      <div className={`relative w-12 h-6 rounded-full transition-colors ${on ? 'bg-action' : 'bg-line'}`}>
        <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${on ? 'translate-x-7' : 'translate-x-1'}`} />
      </div>
    </button>
  );
}

function SettingRow({ icon, label, sublabel, control }: {
  icon: string; label: string; sublabel?: string; control: ReactNode;
}) {
  return (
    <div className="flex items-center justify-between py-3.5 border-b border-line">
      <div className="flex items-center gap-3">
        <span className="text-xl" aria-hidden="true">{icon}</span>
        <div>
          <p className="font-bold text-ink text-sm">{label}</p>
          {sublabel && <p className="text-xs text-ink-muted font-medium">{sublabel}</p>}
        </div>
      </div>
      {control}
    </div>
  );
}

function PillSelector<T extends string | number>({
  options, value, onChange, label,
}: { options: T[]; value: T; onChange: (v: T) => void; label: (v: T) => string }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {options.map((opt) => (
        <button
          key={String(opt)}
          onClick={() => onChange(opt)}
          aria-pressed={value === opt}
          className={`px-4 min-h-[48px] rounded-full border-2 text-xs font-extrabold transition-[colors,transform] active:scale-95 ${
            value === opt
              ? 'bg-action border-action text-white'
              : 'bg-soft border-line text-ink-muted hover:border-ink'
          }`}
        >
          {label(opt)}
        </button>
      ))}
    </div>
  );
}

function Card({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <div className="bg-white px-4 py-4 mt-2 border-y-2 border-line">
      {title && <h2 className="text-title text-ink mb-3">{title}</h2>}
      {children}
    </div>
  );
}

const LEAGUE_TIER_NAMES = ['', 'Bronze', 'Silver', 'Gold', 'Diamond', 'Champion'];
const LEAGUE_TIER_EMOJIS = ['', '🥉', '🥈', '🥇', '💎', '👑'];

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ProfilePage() {
  const router = useRouter();

  // Student meta — starts from the child the app shell loaded on the server, so
  // the first render is the same on the server and in the browser (reading
  // localStorage here made the two differ) and the header paints with real data.
  const { student: shellStudent, refresh: refreshShell } = useStudent();
  const [studentId,   setStudentId]   = useState(shellStudent ? shellStudent.id : '');
  const [name,        setName]        = useState(shellStudent ? shellStudent.name : '');
  const [grade,       setGrade]       = useState<number>(
    shellStudent && shellStudent.grade >= 2 && shellStudent.grade <= 9 ? shellStudent.grade : 4,
  );
  const [avatarColor, setAvatarColor] = useState(
    shellStudent && shellStudent.avatarColor ? shellStudent.avatarColor : '#3B82F6',
  );
  const [createdAt,   setCreatedAt]   = useState('');
  const [streakDays,  setStreakDays]  = useState(0);
  const [leagueTier,  setLeagueTier]  = useState(1);

  // Identity
  const [editingName,    setEditingName]    = useState(false);
  const [newName,        setNewName]        = useState('');
  const [newDisplayName, setNewDisplayName] = useState('');
  // The leaderboard name the server holds ('' when none has been set).
  const [savedDisplayName, setSavedDisplayName] = useState('');
  // The grade a child tapped, waiting for "Yes, change" (null when not asking).
  const [pendingGrade,   setPendingGrade]   = useState<number | null>(null);
  const [savingGrade,    setSavingGrade]    = useState(false);
  const [city,           setCity]           = useState('');

  // Exam goals
  const [examName,    setExamName]    = useState('IPM 2027');
  const [examDate,    setExamDate]    = useState('');
  const [targetScore, setTargetScore] = useState<number | null>(null);
  const [savingExam,  setSavingExam]  = useState(false);

  // Preferences
  const [dailyGoalMins,          setDailyGoalMins]          = useState(20);
  const [sessionLengthMins,      setSessionLengthMins]      = useState(15);
  const [preferredPracticeTime,  setPreferredPracticeTime]  = useState('');
  const [muted,                  setMuted]                  = useState(false);
  const [notifications,          setNotifications]          = useState(false);
  const [hiddenFromLeaderboard,  setHiddenFromLeaderboard]  = useState(false);

  // Focus areas
  const [focusTopics,     setFocusTopics]     = useState<string[]>([]);
  const [confidentTopics, setConfidentTopics] = useState<string[]>([]);

  // Parent settings
  const [parentEmail,    setParentEmail]    = useState('');
  const [parentWhatsApp, setParentWhatsApp] = useState('');
  const [savingContact,  setSavingContact]  = useState(false);

  // UI
  const [loading,    setLoading]    = useState(true);
  const [fetchError, setFetchError] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const [toast,   setToast]     = useState<{ msg: string; ok: boolean } | null>(null);

  function showToast(msg: string, ok: boolean) {
    setToast({ msg, ok });
    setTimeout(() => setToast(null), 3500);
  }

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);

    // Restore local prefs
    setMuted(localStorage.getItem('mathspark_muted') === 'true');
    setNotifications(localStorage.getItem('mathspark_notifications') === 'true');

    // Fetch student data
    fetch('/api/profile')
      .then((r) => {
        // Signed out (the session ran out): go and sign in again.
        if (r.status === 401) { router.replace('/student/login'); return null; }
        if (!r.ok) throw new Error("Fetch failed");
        return r.json();
      })
      .then((d) => {
        if (!d) return;
        const s = d.student ?? d;
        setName(s.name ?? '');
        setNewName(s.name ?? '');
        setNewDisplayName(s.displayName ?? '');
        setSavedDisplayName(s.displayName ?? '');
        setGrade(s.grade ?? 4);
        setAvatarColor(s.avatarColor ?? '#3B82F6');
        setCreatedAt(s.createdAt ?? '');
        setStreakDays(d.stats?.streakDays ?? 0);
        setLeagueTier(s.currentLeagueTier ?? 1);
        setCity(s.city ?? '');
        setExamName(s.examName ?? 'IPM 2027');
        setExamDate(s.examDate ? s.examDate.split('T')[0] : '');
        setTargetScore(s.targetScore ?? null);
        setDailyGoalMins(s.dailyGoalMins ?? 20);
        setSessionLengthMins(s.sessionLengthMins ?? 15);
        setPreferredPracticeTime(s.preferredPracticeTime ?? '');
        setHiddenFromLeaderboard(s.hiddenFromLeaderboard ?? false);
        try { setFocusTopics(JSON.parse(s.focusTopics ?? '[]')); } catch { setFocusTopics([]); }
        try { setConfidentTopics(JSON.parse(s.confidentTopics ?? '[]')); } catch { setConfidentTopics([]); }
        setParentEmail(s.parentEmail ?? '');
        setParentWhatsApp(s.parentWhatsApp ?? '');
        setLoading(false);
      })
      .catch((err) => { logError('[profile] fetch student settings', err); setFetchError(true); setLoading(false); });
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const NOT_SAVED = "That didn't save. Please try again.";

  // Saves fields and says whether the server kept them, so no screen claims a
  // save that did not happen. `error` is the server's own message when it sent one.
  async function patchStudent(fields: Record<string, unknown>): Promise<{ ok: boolean; status: number; error: string }> {
    if (!studentId) return { ok: false, status: 0, error: NOT_SAVED };
    try {
      const res = await fetch('/api/student', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...fields }),
      });
      if (res.ok) return { ok: true, status: res.status, error: '' };
      const body = await res.json().catch(() => null);
      const message = body && typeof body.error === 'string' && res.status < 500 && res.status !== 401
        ? body.error
        : NOT_SAVED;
      return { ok: false, status: res.status, error: message };
    } catch (err) {
      logError('[profile] save settings', err);
      return { ok: false, status: 0, error: NOT_SAVED };
    }
  }

  async function saveName() {
    const t = newName.trim();
    if (!t) return;
    // The name and the leaderboard name are saved apart: a leaderboard name
    // that is already taken must not stop the real name from changing.
    if (t !== name) {
      const saved = await patchStudent({ name: t });
      if (!saved.ok) { showToast(saved.error, false); return; }
      localStorage.setItem('mathspark_student_name', t);
      setName(t);
      refreshShell();
    }
    // An empty box leaves the leaderboard name as it is (league-mates then see the first name).
    const dn = newDisplayName.trim().slice(0, 20);
    if (dn && dn !== savedDisplayName) {
      const saved = await patchStudent({ displayName: dn });
      if (!saved.ok) {
        // Keep the box open so the child can pick another leaderboard name.
        showToast(saved.error, false);
        return;
      }
      setSavedDisplayName(dn);
    }
    setEditingName(false);
    showToast('Name updated ✓', true);
  }

  async function saveExam() {
    setSavingExam(true);
    // An empty date is sent as '' so the server clears it.
    const saved = await patchStudent({ examName, examDate, targetScore });
    setSavingExam(false);
    showToast(saved.ok ? 'Exam goal saved ✓' : saved.error, saved.ok);
  }

  async function saveParentContact() {
    setSavingContact(true);
    const saved = await patchStudent({ parentEmail: parentEmail.trim(), parentWhatsApp: parentWhatsApp.trim() });
    if (saved.ok) {
      localStorage.setItem('mathspark_parent_email', parentEmail.trim());
      localStorage.setItem('mathspark_parent_whatsapp', parentWhatsApp.trim());
    }
    setSavingContact(false);
    showToast(saved.ok ? 'Contact saved ✓' : saved.error, saved.ok);
  }

  async function toggleHidden() {
    const next = !hiddenFromLeaderboard;
    setHiddenFromLeaderboard(next);
    const saved = await patchStudent({ hiddenFromLeaderboard: next });
    if (!saved.ok) { setHiddenFromLeaderboard(!next); showToast(saved.error, false); }
  }

  function toggleMuted() {
    const next = !muted;
    setMuted(next);
    localStorage.setItem('mathspark_muted', String(next));
  }

  function toggleNotifications() {
    const next = !notifications;
    setNotifications(next);
    localStorage.setItem('mathspark_notifications', String(next));
  }

  // The choices below show at once and go back to what they were if the save does not go through.
  async function updateDailyGoal(mins: number) {
    const before = dailyGoalMins;
    setDailyGoalMins(mins);
    const saved = await patchStudent({ dailyGoalMins: mins });
    if (!saved.ok) { setDailyGoalMins(before); showToast(saved.error, false); }
  }

  async function updateSessionLength(mins: number) {
    const before = sessionLengthMins;
    setSessionLengthMins(mins);
    const saved = await patchStudent({ sessionLengthMins: mins });
    if (!saved.ok) { setSessionLengthMins(before); showToast(saved.error, false); }
  }

  async function updatePracticeTime(t: string) {
    const before = preferredPracticeTime;
    setPreferredPracticeTime(t);
    const saved = await patchStudent({ preferredPracticeTime: t });
    if (!saved.ok) { setPreferredPracticeTime(before); showToast(saved.error, false); }
  }

  async function toggleFocus(topicId: string) {
    const before = focusTopics;
    const next = focusTopics.includes(topicId)
      ? focusTopics.filter((t) => t !== topicId)
      : [...focusTopics, topicId];
    setFocusTopics(next);
    const saved = await patchStudent({ focusTopics: next });
    if (!saved.ok) { setFocusTopics(before); showToast(saved.error, false); }
  }

  async function toggleConfident(topicId: string) {
    const before = confidentTopics;
    const next = confidentTopics.includes(topicId)
      ? confidentTopics.filter((t) => t !== topicId)
      : [...confidentTopics, topicId];
    setConfidentTopics(next);
    const saved = await patchStudent({ confidentTopics: next });
    if (!saved.ok) { setConfidentTopics(before); showToast(saved.error, false); }
  }

  // Runs only after the child has said "Yes, change" (see the Account card).
  async function changeGrade(g: number) {
    setSavingGrade(true);
    const saved = await patchStudent({ grade: g, focusTopics: [], confidentTopics: [] });
    setSavingGrade(false);
    setPendingGrade(null);
    if (!saved.ok) { showToast(saved.error, false); return; }

    setGrade(g);
    setFocusTopics([]);
    setConfidentTopics([]);
    localStorage.setItem('mathspark_student_grade', String(g));
    // The topic list keeps a short-lived copy of the old grade on this device;
    // left alone it would put the old grade back.
    localStorage.removeItem(`mathspark_dashboard_${studentId}`);
    // Tell the rest of the app (Learn, the header) about the new grade now,
    // not after the next full page load.
    refreshShell();
    showToast(`Grade changed to ${g} ✓`, true);
    // Invalidate brain analytics so the new grade's topics are recomputed
    fetch('/api/brain/recompute', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({}),
    }).catch((err) => logError('[fetch]', err));
  }

  // Profile has no tab of its own; it opens from the avatar in a page header,
  // so "back" returns to wherever the child came from.
  function goBack() {
    if (window.history.length > 1) router.back();
    else router.push('/home');
  }

  async function logout() {
    if (loggingOut) return;
    setLoggingOut(true);
    // End the session on the server first: clearing this device's storage alone
    // left the child signed in (the cookie lasts 30 days).
    let ended = false;
    try {
      const res = await fetch('/api/student/session', { method: 'DELETE' });
      ended = res.ok;
    } catch (err) {
      logError('[profile] log out', err);
    }
    if (!ended) {
      // Offline or a hiccup: stay signed in and say so, never half logged out.
      setLoggingOut(false);
      showToast("We couldn't log you out just now. Please try again.", false);
      return;
    }
    Object.keys(localStorage).filter((k) => k.startsWith('mathspark_')).forEach((k) => localStorage.removeItem(k));
    // A full page load, so nothing of this child stays in memory for the next person.
    window.location.href = '/start';
  }

  // ── Error state ─────────────────────────────────────────────────────────
  if (fetchError) {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-4 pb-24">
        <p className="text-ink font-extrabold text-lg">Oops! Sparky tripped over a number</p>
        <p className="text-ink-muted text-sm">Could not load your profile. Check your connection.</p>
        <button onClick={() => window.location.reload()} className="min-h-[48px] bg-action text-white border-2 border-ink shadow-hard-sm font-extrabold px-6 py-2.5 rounded-control text-sm active:scale-95 transition-transform">
          Retry
        </button>
      </div>
    );
  }

  // ── Loading skeleton ──────────────────────────────────────────────────────
  if (loading) {
    const skeletonInitial = name ? name[0].toUpperCase() : '?';
    return (
      <div className="min-h-screen bg-paper pb-24">
        {/* Identity header — real data from localStorage, no pulse */}
        <div className="bg-ink pt-2 pb-6 px-4">
          <button
            onClick={goBack}
            aria-label="Back"
            className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-start"
          >
            &larr;
          </button>
          <div className="flex items-center gap-4">
            <div
              className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white border-4 border-white shrink-0"
              style={{ backgroundColor: avatarColor }}
            >
              {skeletonInitial}
            </div>
            <div className="flex-1 min-w-0">
              {name ? (
                <>
                  <h1 className="text-heading text-white truncate">{name}</h1>
                  <p className="text-white/70 text-sm font-semibold">Grade {grade}</p>
                </>
              ) : (
                <div className="space-y-2">
                  <div className="h-6 bg-white/20 rounded-xl w-36 animate-pulse" />
                  <div className="h-4 bg-white/10 rounded-xl w-48 animate-pulse" />
                </div>
              )}
            </div>
          </div>
        </div>
        {/* Card skeletons */}
        {[0,1,2,3].map((i) => (
          <div key={i} className="bg-white mt-2 px-4 py-6 border-y-2 border-line">
            <div className="h-3 bg-gray-100 rounded w-24 mb-4 animate-pulse" />
            <div className="h-12 bg-gray-100 rounded-control animate-pulse" />
          </div>
        ))}
      </div>
    );
  }

  const initial    = name ? name[0].toUpperCase() : '?';
  const tierName   = LEAGUE_TIER_NAMES[leagueTier] ?? 'Bronze';
  const tierEmoji  = LEAGUE_TIER_EMOJIS[leagueTier] ?? '🥉';
  const memberSince = createdAt
    ? new Date(createdAt).toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })
    : '';

  // Every exam chapter of the child's grade (the "extra practice" pools are left out).
  const gradeTopics = getTopicsForGrade(grade).filter((t) => !t.extra);

  const examDaysLeft = examDate
    ? Math.max(0, Math.ceil((new Date(examDate).getTime() - Date.now()) / MS_PER_DAY))
    : null;

  return (
    <div className="min-h-screen bg-paper pb-24">

      {/* ── Toast ─────────────────────────────────────────────────────────── */}
      {toast && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 z-[80] px-5 py-3 rounded-full border-2 border-ink shadow-hard-sm font-bold text-sm text-white animate-pop-in pointer-events-none ${toast.ok ? 'bg-success' : 'bg-retry'}`}>
          {toast.msg}
        </div>
      )}

      {/* ── Edit name modal ────────────────────────────────────────────────── */}
      {editingName && (
        <div className="fixed inset-0 bg-black/60 z-[70] flex items-center justify-center p-4">
          <div className="bg-white rounded-card border-2 border-ink p-6 w-full max-w-xs shadow-hard-lg animate-pop-in space-y-4">
            <h3 className="text-title text-ink">Change your name</h3>
            <div className="space-y-2">
              <label htmlFor="profile-name" className="text-xs font-extrabold text-ink-muted">Your name</label>
              <input
                id="profile-name"
                type="text" autoFocus value={newName}
                onChange={(e) => setNewName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && saveName()}
                placeholder="First name"
                className="w-full border-2 border-line rounded-control px-4 py-3 text-base font-bold text-ink outline-none focus:border-action"
                maxLength={30}
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="profile-leaderboard-name" className="text-xs font-extrabold text-ink-muted">Leaderboard name</label>
              <input
                id="profile-leaderboard-name"
                type="text" value={newDisplayName}
                onChange={(e) => setNewDisplayName(e.target.value)}
                placeholder="Max 20 chars"
                className="w-full border-2 border-line rounded-control px-4 py-3 text-base font-bold text-ink outline-none focus:border-action"
                maxLength={20}
              />
            </div>
            <div className="flex gap-2">
              <DuoButton variant="white" onClick={() => setEditingName(false)}>Cancel</DuoButton>
              <DuoButton variant="green" fullWidth onClick={saveName}>Save ✓</DuoButton>
            </div>
          </div>
        </div>
      )}

      {/* ── 1. Identity Header ─────────────────────────────────────────────── */}
      <div className="bg-ink pt-2 pb-6 px-4">
        <button
          onClick={goBack}
          aria-label="Back"
          className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-start"
        >
          &larr;
        </button>
        <div className="flex items-center gap-4">
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white border-4 border-white shrink-0"
            style={{ backgroundColor: avatarColor }}
          >
            {initial}
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-heading text-white truncate">{name}</h1>
            <p className="text-white/70 text-sm font-semibold">
              Grade {grade}{city ? ` · ${city}` : ''}
            </p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-white/70 text-xs font-medium">
                {tierEmoji} {tierName} League
              </span>
              {streakDays > 0 && (
                <span className="text-star text-xs font-extrabold"><span aria-hidden="true">🔥 </span>{streakDays}-day streak</span>
              )}
            </div>
            {memberSince && (
              <p className="text-white/70 text-xs font-medium mt-0.5">Member since {memberSince}</p>
            )}
          </div>
        </div>
        <button
          onClick={() => setEditingName(true)}
          className="mt-4 min-h-[48px] bg-white hover:bg-soft text-ink border-2 border-white text-sm font-bold rounded-full px-4 py-2 transition-colors"
        >
          <span aria-hidden="true">✏️ </span>Edit name
        </button>
      </div>

      {/* ── 2. My Exam ─────────────────────────────────────────────────────── */}
      <Card title="My Exam">
        <div className="space-y-3">
          <div>
            <label htmlFor="profile-exam-name" className="text-xs font-extrabold text-ink-muted">Exam name</label>
            <input
              id="profile-exam-name"
              type="text" value={examName}
              onChange={(e) => setExamName(e.target.value)}
              placeholder="e.g. IPM 2027"
              className="w-full mt-1.5 border-2 border-line rounded-control px-3 py-2.5 text-sm font-medium text-ink outline-none focus:border-action"
            />
          </div>
          <div>
            <label htmlFor="profile-exam-date" className="text-xs font-extrabold text-ink-muted">Exam date</label>
            <input
              id="profile-exam-date"
              type="date" value={examDate}
              onChange={(e) => setExamDate(e.target.value)}
              className="w-full mt-1.5 border-2 border-line rounded-control px-3 py-2.5 text-sm font-medium text-ink outline-none focus:border-action"
            />
            {examDaysLeft !== null && (
              <p className="text-xs text-ink-muted font-semibold mt-1">
                📅 {examDaysLeft} days to exam
              </p>
            )}
          </div>
          <div>
            <label className="text-xs font-extrabold text-ink-muted mb-1.5 block">Target score (out of 40)</label>
            <div className="flex gap-2">
              {[25, 30, 35, 38].map((s) => (
                <button
                  key={s}
                  onClick={() => setTargetScore(s)}
                  aria-pressed={targetScore === s}
                  className={`flex-1 min-h-[48px] rounded-control border-2 text-sm font-extrabold transition-colors ${
                    targetScore === s
                      ? 'bg-action border-action text-white'
                      : 'bg-soft border-line text-ink-muted hover:border-ink'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
          <button
            onClick={saveExam}
            disabled={savingExam}
            className="px-4 min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm text-white text-xs font-extrabold disabled:opacity-60"
          >
            {savingExam ? 'Saving…' : 'Save goals ✓'}
          </button>
        </div>
      </Card>

      {/* ── 3. My Goals ────────────────────────────────────────────────────── */}
      <Card title="My Goals">
        <div className="space-y-4">
          <div>
            <p className="text-sm font-bold text-gray-700 mb-2">Daily practice</p>
            <PillSelector
              options={[10, 20, 30, 45]}
              value={dailyGoalMins}
              onChange={updateDailyGoal}
              label={(v) => `${v} min`}
            />
          </div>
          <div>
            <p className="text-sm font-bold text-gray-700 mb-2">Session length</p>
            <PillSelector
              options={[5, 10, 15, 25]}
              value={sessionLengthMins}
              onChange={updateSessionLength}
              label={(v) => `${v} min`}
            />
          </div>
        </div>
      </Card>

      {/* ── 4. My Preferences ─────────────────────────────────────────────── */}
      <Card title="My Preferences">
        <div>
          <p className="text-sm font-bold text-gray-700 mb-2">Best time to practice</p>
          <div className="flex gap-2 mb-4">
            {[['morning', 'Morning 🌅'], ['afternoon', 'Afternoon ☀️'], ['evening', 'Evening 🌙']].map(([v, l]) => (
              <button
                key={v}
                onClick={() => updatePracticeTime(v)}
                aria-pressed={preferredPracticeTime === v}
                className={`flex-1 min-h-[48px] rounded-control border-2 text-xs font-extrabold transition-colors ${
                  preferredPracticeTime === v
                    ? 'bg-action border-action text-white'
                    : 'bg-soft border-line text-ink-muted hover:border-ink'
                }`}
              >
                {l}
              </button>
            ))}
          </div>
          <SettingRow
            icon="🔊" label="Sound effects"
            sublabel={muted ? 'Sounds are off' : 'Sounds are on'}
            control={<Toggle on={!muted} onToggle={toggleMuted} label="Sound effects" />}
          />
          <SettingRow
            icon="🔔" label="Daily reminders"
            sublabel="Coming soon"
            control={<Toggle on={notifications} onToggle={toggleNotifications} label="Daily reminders" />}
          />
          <SettingRow
            icon="🙈" label="Hide from leaderboard"
            sublabel={hiddenFromLeaderboard ? 'Your profile is hidden' : 'Others can see your rank'}
            control={<Toggle on={hiddenFromLeaderboard} onToggle={toggleHidden} label="Hide from leaderboard" />}
          />
        </div>
      </Card>

      {/* ── Sparky's voice (kept on this device, like the sound setting) ──── */}
      <Card title="Sparky's Voice">
        <p className="text-xs text-ink-muted font-medium mb-3">Tap Listen to hear each one, then pick your favourite.</p>
        <VoicePicker />
      </Card>

      {/* ── 5. Focus Areas ────────────────────────────────────────────────── */}
      <Card title="Focus Areas">
        <p className="text-xs text-gray-500 font-medium mb-3">These help Sparky prioritise your practice 🧠</p>

        <div className="mb-4">
          <p className="text-sm font-bold text-gray-700 mb-2"><span aria-hidden="true">📌 </span>Topics I Find Hard</p>
          <div className="flex flex-wrap gap-1.5">
            {gradeTopics.map((t) => (
              <button
                key={t.id}
                onClick={() => toggleFocus(t.id)}
                aria-pressed={focusTopics.includes(t.id)}
                className={`flex items-center gap-1 px-3 min-h-[48px] rounded-full border-2 text-xs font-extrabold text-left transition-colors ${
                  focusTopics.includes(t.id)
                    ? 'bg-retry-soft border-retry text-retry'
                    : 'bg-soft border-line text-ink-muted hover:border-ink'
                }`}
              >
                <span aria-hidden="true">{t.emoji}</span>
                <span>{t.name}</span>
                {focusTopics.includes(t.id) && <span aria-hidden="true">×</span>}
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="text-sm font-bold text-gray-700 mb-2"><span aria-hidden="true">💪 </span>Topics I&apos;m Confident In</p>
          <div className="flex flex-wrap gap-1.5">
            {gradeTopics.map((t) => (
              <button
                key={t.id}
                onClick={() => toggleConfident(t.id)}
                aria-pressed={confidentTopics.includes(t.id)}
                className={`flex items-center gap-1 px-3 min-h-[48px] rounded-full border-2 text-xs font-extrabold text-left transition-colors ${
                  confidentTopics.includes(t.id)
                    ? 'bg-success-soft border-success text-ink'
                    : 'bg-soft border-line text-ink-muted hover:border-ink'
                }`}
              >
                <span aria-hidden="true">{t.emoji}</span>
                <span>{t.name}</span>
                {confidentTopics.includes(t.id) && <span aria-hidden="true">×</span>}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* ── 6. Parent Settings ────────────────────────────────────────────── */}
      <Card title="Parent Settings">
        <div className="space-y-3">
          <div>
            <label htmlFor="profile-parent-email" className="text-xs font-extrabold text-ink-muted">Parent email</label>
            <input
              id="profile-parent-email"
              type="email" value={parentEmail}
              onChange={(e) => setParentEmail(e.target.value)}
              placeholder="parent@email.com"
              className="w-full mt-1.5 border-2 border-line rounded-control px-3 py-2.5 text-sm font-medium text-ink outline-none focus:border-action"
            />
          </div>
          <div>
            <label htmlFor="profile-parent-whatsapp" className="text-xs font-extrabold text-ink-muted">WhatsApp number</label>
            <input
              id="profile-parent-whatsapp"
              type="tel" value={parentWhatsApp}
              onChange={(e) => setParentWhatsApp(e.target.value)}
              placeholder="+91 98XXX XXXXX"
              className="w-full mt-1.5 border-2 border-line rounded-control px-3 py-2.5 text-sm font-medium text-ink outline-none focus:border-action"
            />
          </div>
          <button
            onClick={saveParentContact}
            disabled={savingContact}
            className="px-4 min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm text-white text-xs font-extrabold disabled:opacity-60"
          >
            {savingContact ? 'Saving…' : 'Save contact ✓'}
          </button>
        </div>
      </Card>

      {/* ── 7. Account ────────────────────────────────────────────────────── */}
      <Card title="Account">
        <div className="space-y-3">
          {/* Change Grade */}
          <div>
            <p className="text-sm font-bold text-gray-700 mb-2">Change Grade</p>
            <div className="grid grid-cols-4 gap-2">
              {[2,3,4,5,6,7,8,9].map((g) => (
                <button
                  key={g}
                  onClick={() => { if (g !== grade) setPendingGrade(g); }}
                  aria-pressed={grade === g}
                  disabled={savingGrade}
                  className={`min-h-[48px] rounded-control border-2 text-xs font-extrabold transition-colors disabled:opacity-60 ${
                    grade === g
                      ? 'bg-action border-action text-white'
                      : 'bg-soft border-line text-ink-muted hover:border-ink'
                  }`}
                >
                  Gr {g}
                </button>
              ))}
            </div>
            {/* One tap must not switch the whole app to another grade: ask first. */}
            {pendingGrade !== null && (
              <div className="mt-3 rounded-control border-2 border-ink bg-soft p-3" role="alertdialog" aria-label="Change grade">
                <p className="text-sm font-bold text-ink">Change to Grade {pendingGrade}?</p>
                <p className="text-xs text-ink-muted font-medium mt-0.5">
                  Your topics and practice will switch to Grade {pendingGrade}. Everything you have done so far is kept.
                </p>
                <div className="flex gap-2 mt-3">
                  <button
                    onClick={() => changeGrade(pendingGrade)}
                    disabled={savingGrade}
                    className="flex-1 min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm text-white text-sm font-extrabold disabled:opacity-60"
                  >
                    {savingGrade ? 'Changing…' : 'Yes, change'}
                  </button>
                  <button
                    onClick={() => setPendingGrade(null)}
                    disabled={savingGrade}
                    className="flex-1 min-h-[48px] rounded-control bg-white border-2 border-line text-ink text-sm font-extrabold disabled:opacity-60"
                  >
                    Keep Grade {grade}
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Subscription (only while payments are switched on) */}
          {MONETIZATION_ENABLED && (
            <div className="flex items-center justify-between py-2">
              <div>
                <p className="text-sm font-bold text-gray-700">Subscription</p>
                <p className="text-xs text-gray-500 font-medium">Current plan</p>
              </div>
              <Link href="/pricing" className="min-h-[48px] inline-flex items-center text-xs font-extrabold text-action bg-soft border-2 border-line rounded-full px-3">
                Upgrade →
              </Link>
            </div>
          )}

          {/* Sparky Chat */}
          <div className="flex items-center justify-between py-2 border-t border-line">
            <div className="flex items-center gap-2">
              <span className="text-lg" aria-hidden="true">💬</span>
              <p className="text-sm font-bold text-gray-700">Sparky Chat</p>
            </div>
            <Link href="/chat" className="min-h-[48px] inline-flex items-center text-xs font-extrabold text-action bg-soft border-2 border-line rounded-full px-3">
              → Open
            </Link>
          </div>

          <div className="pt-2">
            <DuoButton variant="red" fullWidth onClick={logout} loading={loggingOut}>
              Log out
            </DuoButton>
          </div>
        </div>
      </Card>

      <p className="text-center text-xs text-ink-muted font-medium py-4">MathSpark · Grade {grade} Math · v1.0</p>
    </div>
  );
}

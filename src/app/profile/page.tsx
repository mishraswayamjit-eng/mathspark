'use client';

import { useEffect, useState, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import DuoButton from '@/components/DuoButton';
import { getTopicsForGrade } from '@/data/topicTree';

// ── Sub-components ────────────────────────────────────────────────────────────

function Toggle({ on, onToggle }: { on: boolean; onToggle: () => void }) {
  return (
    <button onClick={onToggle} style={{ minHeight: 0 }}
      className={`relative w-12 h-6 rounded-full transition-colors flex-shrink-0 ${on ? 'bg-[#58CC02]' : 'bg-gray-200'}`}
      aria-label="toggle"
    >
      <div className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${on ? 'translate-x-7' : 'translate-x-1'}`} />
    </button>
  );
}

function SettingRow({ icon, label, sublabel, control }: {
  icon: string; label: string; sublabel?: string; control: ReactNode;
}) {
  return (
    <div className="flex items-center justify-between py-3.5 border-b border-gray-100">
      <div className="flex items-center gap-3">
        <span className="text-xl">{icon}</span>
        <div>
          <p className="font-bold text-gray-700 text-sm">{label}</p>
          {sublabel && <p className="text-xs text-gray-400 font-medium">{sublabel}</p>}
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
          style={{ minHeight: 0 }}
          className={`px-3 py-1.5 rounded-full text-xs font-extrabold transition-all active:scale-95 ${
            value === opt
              ? 'bg-[#58CC02] text-white shadow-sm'
              : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
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
    <div className="bg-white px-4 py-4 mt-2 border-b border-gray-100">
      {title && <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">{title}</h2>}
      {children}
    </div>
  );
}

const LEAGUE_TIER_NAMES = ['', 'Bronze', 'Silver', 'Gold', 'Diamond', 'Champion'];
const LEAGUE_TIER_EMOJIS = ['', '🥉', '🥈', '🥇', '💎', '👑'];

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ProfilePage() {
  const router = useRouter();

  // Student meta
  const [studentId,   setStudentId]   = useState('');
  const [name,        setName]        = useState('');
  const [grade,       setGrade]       = useState(4);
  const [avatarColor, setAvatarColor] = useState('#3B82F6');
  const [createdAt,   setCreatedAt]   = useState('');
  const [streakDays,  setStreakDays]  = useState(0);
  const [leagueTier,  setLeagueTier]  = useState(1);

  // Identity
  const [editingName,    setEditingName]    = useState(false);
  const [newName,        setNewName]        = useState('');
  const [newDisplayName, setNewDisplayName] = useState('');
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
  const [loading, setLoading]   = useState(true);
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
    fetch(`/api/profile?studentId=${id}`)
      .then((r) => r.json())
      .then((d) => {
        const s = d.student ?? d;
        setName(s.name ?? '');
        setNewName(s.name ?? '');
        setNewDisplayName(s.displayName ?? s.name ?? '');
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
        setFocusTopics(JSON.parse(s.focusTopics ?? '[]'));
        setConfidentTopics(JSON.parse(s.confidentTopics ?? '[]'));
        setParentEmail(s.parentEmail ?? '');
        setParentWhatsApp(s.parentWhatsApp ?? '');
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [router]);

  async function patchStudent(fields: Record<string, unknown>) {
    if (!studentId) return;
    await fetch('/api/student', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ studentId, ...fields }),
    }).catch(() => {});
  }

  async function saveName() {
    const t = newName.trim();
    if (!t) return;
    localStorage.setItem('mathspark_student_name', t);
    setName(t);
    setEditingName(false);
    await patchStudent({ name: t, displayName: newDisplayName.trim().slice(0, 20) || t });
    showToast('Name updated ✓', true);
  }

  async function saveExam() {
    setSavingExam(true);
    await patchStudent({ examName, examDate: examDate || undefined, targetScore });
    setSavingExam(false);
    showToast('Exam goal saved ✓', true);
  }

  async function saveParentContact() {
    setSavingContact(true);
    localStorage.setItem('mathspark_parent_email', parentEmail.trim());
    localStorage.setItem('mathspark_parent_whatsapp', parentWhatsApp.trim());
    try {
      await patchStudent({ parentEmail: parentEmail.trim(), parentWhatsApp: parentWhatsApp.trim() });
      showToast('Contact saved ✓', true);
    } catch {
      showToast('Could not save. Try again.', false);
    } finally {
      setSavingContact(false);
    }
  }

  async function toggleHidden() {
    const next = !hiddenFromLeaderboard;
    setHiddenFromLeaderboard(next);
    await patchStudent({ hiddenFromLeaderboard: next });
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

  async function updateDailyGoal(mins: number) {
    setDailyGoalMins(mins);
    await patchStudent({ dailyGoalMins: mins });
  }

  async function updateSessionLength(mins: number) {
    setSessionLengthMins(mins);
    await patchStudent({ sessionLengthMins: mins });
  }

  async function updatePracticeTime(t: string) {
    setPreferredPracticeTime(t);
    await patchStudent({ preferredPracticeTime: t });
  }

  async function toggleFocus(topicId: string) {
    const next = focusTopics.includes(topicId)
      ? focusTopics.filter((t) => t !== topicId)
      : [...focusTopics, topicId];
    setFocusTopics(next);
    await patchStudent({ focusTopics: next });
  }

  async function toggleConfident(topicId: string) {
    const next = confidentTopics.includes(topicId)
      ? confidentTopics.filter((t) => t !== topicId)
      : [...confidentTopics, topicId];
    setConfidentTopics(next);
    await patchStudent({ confidentTopics: next });
  }

  async function changeGrade(g: number) {
    setGrade(g);
    localStorage.setItem('mathspark_student_grade', String(g));
    await patchStudent({ grade: g });
    showToast(`Grade changed to ${g} ✓`, true);
  }

  function logout() {
    Object.keys(localStorage).filter((k) => k.startsWith('mathspark_')).forEach((k) => localStorage.removeItem(k));
    router.replace('/start');
  }

  // ── Loading skeleton ──────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 animate-pulse pb-24">
        <div className="bg-[#131F24] pt-10 pb-6 px-4">
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 rounded-full bg-white/20" />
            <div className="space-y-2 flex-1">
              <div className="h-6 bg-white/20 rounded-xl w-36" />
              <div className="h-4 bg-white/10 rounded-xl w-48" />
            </div>
          </div>
        </div>
        {[0,1,2,3].map((i) => (
          <div key={i} className="bg-white mt-2 px-4 py-6 border-b border-gray-100">
            <div className="h-3 bg-gray-100 rounded w-24 mb-4" />
            <div className="h-12 bg-gray-100 rounded-2xl" />
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

  const gradeTopics = getTopicsForGrade(grade);

  const examDaysLeft = examDate
    ? Math.max(0, Math.ceil((new Date(examDate).getTime() - Date.now()) / 86400000))
    : null;

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">

      {/* ── Toast ─────────────────────────────────────────────────────────── */}
      {toast && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 z-[80] px-5 py-3 rounded-full shadow-xl font-bold text-sm text-white animate-pop-in pointer-events-none ${toast.ok ? 'bg-[#58CC02]' : 'bg-[#FF4B4B]'}`}>
          {toast.msg}
        </div>
      )}

      {/* ── Edit name modal ────────────────────────────────────────────────── */}
      {editingName && (
        <div className="fixed inset-0 bg-black/60 z-[70] flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 w-full max-w-xs shadow-2xl animate-pop-in space-y-4">
            <h3 className="font-extrabold text-gray-800 text-lg">Change your name</h3>
            <div className="space-y-2">
              <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Your name</label>
              <input
                type="text" autoFocus value={newName}
                onChange={(e) => setNewName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && saveName()}
                placeholder="First name"
                className="w-full border-2 border-blue-200 rounded-2xl px-4 py-3 text-base font-bold text-gray-800 outline-none focus:border-[#1CB0F6]"
                maxLength={30}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Leaderboard name</label>
              <input
                type="text" value={newDisplayName}
                onChange={(e) => setNewDisplayName(e.target.value)}
                placeholder="Max 20 chars"
                className="w-full border-2 border-gray-200 rounded-2xl px-4 py-3 text-base font-bold text-gray-800 outline-none focus:border-[#1CB0F6]"
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
      <div className="bg-[#131F24] pt-10 pb-6 px-4">
        <div className="flex items-center gap-4">
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white border-4 border-white/30 shadow-lg shrink-0"
            style={{ backgroundColor: avatarColor }}
          >
            {initial}
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-extrabold text-white truncate">{name}</h1>
            <p className="text-white/60 text-sm font-semibold">
              Grade {grade}{city ? ` · ${city}` : ''}
            </p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-white/50 text-xs font-medium">
                {tierEmoji} {tierName} League
              </span>
              {streakDays > 0 && (
                <span className="text-orange-400 text-xs font-extrabold">🔥 {streakDays}-day streak</span>
              )}
            </div>
            {memberSince && (
              <p className="text-white/30 text-xs font-medium mt-0.5">Member since {memberSince}</p>
            )}
          </div>
        </div>
        <button
          onClick={() => setEditingName(true)}
          style={{ minHeight: 0 }}
          className="mt-4 bg-white/15 hover:bg-white/25 text-white text-sm font-bold rounded-full px-4 py-2 transition-colors"
        >
          ✏️ Edit name
        </button>
      </div>

      {/* ── 2. My Exam ─────────────────────────────────────────────────────── */}
      <Card title="My Exam">
        <div className="space-y-3">
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Exam name</label>
            <input
              type="text" value={examName}
              onChange={(e) => setExamName(e.target.value)}
              placeholder="e.g. IPM 2027"
              className="w-full mt-1.5 border-2 border-gray-200 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-800 outline-none focus:border-[#1CB0F6]"
            />
          </div>
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Exam date</label>
            <input
              type="date" value={examDate}
              onChange={(e) => setExamDate(e.target.value)}
              className="w-full mt-1.5 border-2 border-gray-200 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-800 outline-none focus:border-[#1CB0F6]"
            />
            {examDaysLeft !== null && (
              <p className="text-xs text-[#1CB0F6] font-semibold mt-1">
                📅 {examDaysLeft} days to exam
              </p>
            )}
          </div>
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide mb-1.5 block">Target score (out of 40)</label>
            <div className="flex gap-2">
              {[25, 30, 35, 38].map((s) => (
                <button
                  key={s}
                  onClick={() => setTargetScore(s)}
                  style={{ minHeight: 0 }}
                  className={`flex-1 py-2 rounded-xl text-sm font-extrabold transition-all ${
                    targetScore === s
                      ? 'bg-[#58CC02] text-white shadow-sm'
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
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
            style={{ minHeight: 0 }}
            className="px-4 py-2 rounded-xl bg-[#58CC02] text-white text-xs font-extrabold disabled:opacity-60"
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
                style={{ minHeight: 0 }}
                className={`flex-1 py-2 rounded-xl text-xs font-extrabold transition-all ${
                  preferredPracticeTime === v
                    ? 'bg-[#1CB0F6] text-white shadow-sm'
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                }`}
              >
                {l}
              </button>
            ))}
          </div>
          <SettingRow
            icon="🔊" label="Sound effects"
            sublabel={muted ? 'Sounds are off' : 'Sounds are on'}
            control={<Toggle on={!muted} onToggle={toggleMuted} />}
          />
          <SettingRow
            icon="🔔" label="Daily reminders"
            sublabel="Practice notifications"
            control={<Toggle on={notifications} onToggle={toggleNotifications} />}
          />
          <SettingRow
            icon="🙈" label="Hide from leaderboard"
            sublabel={hiddenFromLeaderboard ? 'Your profile is hidden' : 'Others can see your rank'}
            control={<Toggle on={hiddenFromLeaderboard} onToggle={toggleHidden} />}
          />
        </div>
      </Card>

      {/* ── 5. Focus Areas ────────────────────────────────────────────────── */}
      <Card title="Focus Areas">
        <p className="text-xs text-gray-400 font-medium mb-3">These help Sparky prioritise your practice 🧠</p>

        <div className="mb-4">
          <p className="text-sm font-bold text-gray-700 mb-2">📌 Topics I Find Hard</p>
          <div className="flex flex-wrap gap-1.5">
            {gradeTopics.slice(0, 10).map((t) => (
              <button
                key={t.id}
                onClick={() => toggleFocus(t.id)}
                style={{ minHeight: 0 }}
                className={`flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-extrabold transition-all ${
                  focusTopics.includes(t.id)
                    ? 'bg-[#FF4B4B] text-white'
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                }`}
              >
                <span>{t.emoji}</span>
                <span>{t.name.split(' ')[0]}</span>
                {focusTopics.includes(t.id) && <span>×</span>}
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="text-sm font-bold text-gray-700 mb-2">💪 Topics I&apos;m Confident In</p>
          <div className="flex flex-wrap gap-1.5">
            {gradeTopics.slice(0, 10).map((t) => (
              <button
                key={t.id}
                onClick={() => toggleConfident(t.id)}
                style={{ minHeight: 0 }}
                className={`flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-extrabold transition-all ${
                  confidentTopics.includes(t.id)
                    ? 'bg-[#58CC02] text-white'
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                }`}
              >
                <span>{t.emoji}</span>
                <span>{t.name.split(' ')[0]}</span>
                {confidentTopics.includes(t.id) && <span>×</span>}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* ── 6. Parent Settings ────────────────────────────────────────────── */}
      <Card title="Parent Settings">
        <div className="space-y-3">
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Parent email</label>
            <input
              type="email" value={parentEmail}
              onChange={(e) => setParentEmail(e.target.value)}
              placeholder="parent@email.com"
              className="w-full mt-1.5 border-2 border-gray-200 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-800 outline-none focus:border-[#1CB0F6]"
            />
          </div>
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">WhatsApp number</label>
            <input
              type="tel" value={parentWhatsApp}
              onChange={(e) => setParentWhatsApp(e.target.value)}
              placeholder="+91 98XXX XXXXX"
              className="w-full mt-1.5 border-2 border-gray-200 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-800 outline-none focus:border-[#25D366]"
            />
          </div>
          <button
            onClick={saveParentContact}
            disabled={savingContact}
            style={{ minHeight: 0 }}
            className="px-4 py-2 rounded-xl bg-[#58CC02] text-white text-xs font-extrabold disabled:opacity-60"
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
                  onClick={() => changeGrade(g)}
                  style={{ minHeight: 0 }}
                  className={`py-2 rounded-xl text-xs font-extrabold transition-all ${
                    grade === g
                      ? 'bg-[#1CB0F6] text-white shadow-sm'
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}
                >
                  Gr {g}
                </button>
              ))}
            </div>
          </div>

          {/* Subscription */}
          <div className="flex items-center justify-between py-2">
            <div>
              <p className="text-sm font-bold text-gray-700">Subscription</p>
              <p className="text-xs text-gray-400 font-medium">Current plan</p>
            </div>
            <Link href="/pricing" className="text-xs font-extrabold text-[#1CB0F6] bg-blue-50 rounded-full px-3 py-1.5">
              Upgrade →
            </Link>
          </div>

          {/* Sparky Chat */}
          <div className="flex items-center justify-between py-2 border-t border-gray-100">
            <div className="flex items-center gap-2">
              <span className="text-lg">💬</span>
              <p className="text-sm font-bold text-gray-700">Sparky Chat</p>
            </div>
            <Link href="/chat" className="text-xs font-extrabold text-[#1CB0F6] bg-blue-50 rounded-full px-3 py-1.5">
              → Open
            </Link>
          </div>

          <div className="pt-2">
            <DuoButton variant="red" fullWidth onClick={logout}>
              Log out
            </DuoButton>
          </div>
        </div>
      </Card>

      <p className="text-center text-xs text-gray-300 font-medium py-4">MathSpark · Grade {grade} Math · v1.0</p>
    </div>
  );
}

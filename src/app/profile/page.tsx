'use client';

import { useEffect, useState, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import type { ProfileData } from '@/types';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

// ─── Constants ─────────────────────────────────────────────────────────────────

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

const TOPIC_SHORT: Record<string, string> = {
  'ch01-05': 'Numbers',   'ch06': 'Factors',    'ch07-08': 'Fractions', 'ch09-10': 'Operations',
  'ch11': 'Decimals',     'ch12': 'Measures',    'ch13': 'Algebra',      'ch14': 'Equations',
  'ch15': 'Puzzles',      'ch16': 'Sequences',   'ch17': 'Time',         'ch18': 'Angles',
  'ch19': 'Triangles',    'ch20': 'Quadrilaterals', 'ch21': 'Circle',    'dh': 'Data',
};

const AVATAR_COLORS = [
  '#FF9600','#58CC02','#1CB0F6','#FF4B4B',
  '#9B59B6','#00BCD4','#FFC800','#FF69B4',
];

// ─── Badge definitions ─────────────────────────────────────────────────────────

interface Badge {
  id: string;
  emoji: string;
  name: string;
  desc: string;
  color: string;
  earned: boolean;
}

function computeBadges(data: ProfileData): Badge[] {
  const { stats, topics } = data;

  const geoMastered   = ['ch18','ch19','ch20','ch21'].every(
    (id) => topics.find((t) => t.id === id)?.mastery === 'Mastered',
  );
  const puzzleMastered = ['ch15','ch16'].every(
    (id) => topics.find((t) => t.id === id)?.mastery === 'Mastered',
  );
  const allGoldPlus = stats.topicsMastered >= 16 && topics.every((t) => {
    const pct = t.attempted > 0 ? t.correct / t.attempted : 0;
    return pct >= 0.8 || t.mastery === 'Mastered';
  });

  return [
    { id: 'first_steps',    emoji: '🌱', name: 'First Steps',    color: '#58CC02', desc: 'Started your learning journey',       earned: stats.totalAttempted > 0                     },
    { id: 'sharp_shooter',  emoji: '🎯', name: 'Sharp Shooter',  color: '#1CB0F6', desc: '10 correct answers in a row',          earned: stats.maxConsecutiveCorrect >= 10             },
    { id: 'week_warrior',   emoji: '🔥', name: 'Week Warrior',   color: '#FF9600', desc: '7-day learning streak',                earned: stats.streakDays >= 7                        },
    { id: 'century_club',   emoji: '💯', name: 'Century Club',   color: '#FFC800', desc: '100 questions answered correctly',      earned: stats.totalSolved >= 100                     },
    { id: 'champion',       emoji: '🏆', name: 'Champion',       color: '#FFC800', desc: '5 topics mastered',                   earned: stats.topicsMastered >= 5                    },
    { id: 'superstar',      emoji: '⭐', name: 'Superstar',      color: '#9B59B6', desc: 'All 16 topics mastered',               earned: stats.topicsMastered >= 16                   },
    { id: 'speed_demon',    emoji: '⚡', name: 'Speed Demon',    color: '#FFC800', desc: '5 correct answers under 10 seconds',   earned: stats.fastCorrects >= 5                      },
    { id: 'geometry_guru',  emoji: '📐', name: 'Geometry Guru',  color: '#1CB0F6', desc: 'All geometry topics mastered',         earned: geoMastered                                  },
    { id: 'puzzle_master',  emoji: '🧩', name: 'Puzzle Master',  color: '#FF9600', desc: 'Mastered Puzzles & Sequences',         earned: puzzleMastered                               },
    { id: 'ipm_ready',      emoji: '🎓', name: 'IPM Ready',      color: '#58CC02', desc: 'All topics at gold+ level',            earned: allGoldPlus                                  },
  ];
}

// ─── Sub-components ────────────────────────────────────────────────────────────

function StatCard({ emoji, label, value, sub, color, animated = false }: {
  emoji: string; label: string; value: string; sub?: string; color: string; animated?: boolean;
}) {
  return (
    <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100">
      <div className="flex items-center gap-1.5 mb-1">
        <span className={`text-lg ${animated ? 'animate-sparky-bounce' : ''}`}>{emoji}</span>
        <span className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide leading-tight">{label}</span>
      </div>
      <p className="text-2xl font-extrabold leading-none" style={{ color }}>{value}</p>
      {sub && <p className="text-[11px] text-gray-400 font-medium mt-1">{sub}</p>}
    </div>
  );
}

function BadgeTile({ badge }: { badge: Badge }) {
  return (
    <div className="flex flex-col items-center gap-1" title={badge.desc}>
      <div
        className="w-14 h-14 rounded-full flex items-center justify-center text-2xl relative border-2 transition-all"
        style={badge.earned ? {
          backgroundColor: `${badge.color}18`,
          borderColor: badge.color,
          boxShadow: `0 0 12px ${badge.color}55`,
        } : {
          backgroundColor: '#f3f4f6',
          borderColor: '#e5e7eb',
        }}
      >
        <span className={badge.earned ? '' : 'opacity-15'}>{badge.emoji}</span>
        {!badge.earned && (
          <span className="absolute inset-0 flex items-center justify-center text-gray-400 text-base font-extrabold">?</span>
        )}
        {badge.earned && (
          <div
            className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full flex items-center justify-center border border-white"
            style={{ backgroundColor: badge.color }}
          >
            <span className="text-white text-[8px] font-extrabold">✓</span>
          </div>
        )}
      </div>
      <span className={`text-[9px] font-bold text-center leading-tight px-0.5 ${badge.earned ? 'text-gray-700' : 'text-gray-400'}`}>
        {badge.name}
      </span>
    </div>
  );
}

function Toggle({ on, onToggle }: { on: boolean; onToggle: () => void }) {
  return (
    <button
      onClick={onToggle}
      style={{ minHeight: 0 }}
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

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'long', year: 'numeric',
  });
}

// ─── Page ──────────────────────────────────────────────────────────────────────

export default function ProfilePage() {
  const router = useRouter();

  const [data,          setData]          = useState<ProfileData | null>(null);
  const [loading,       setLoading]       = useState(true);
  const [studentName,   setStudentName]   = useState('');

  // settings
  const [muted,         setMuted]         = useState(false);
  const [dailyGoal,     setDailyGoal]     = useState('2');
  const [notifications, setNotifications] = useState(false);

  // UI
  const [editingName,   setEditingName]   = useState(false);
  const [newName,       setNewName]       = useState('');
  const [shareOpen,     setShareOpen]     = useState(false);
  const [parentEmail,   setParentEmail]   = useState('');
  const [sending,       setSending]       = useState(false);
  const [toast,         setToast]         = useState<{ msg: string; ok: boolean } | null>(null);
  const [studentId,     setStudentId]     = useState('');

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);

    const name = localStorage.getItem('mathspark_student_name') ?? '';
    setStudentName(name);
    setNewName(name);
    setMuted(localStorage.getItem('mathspark_muted') === 'true');
    setDailyGoal(localStorage.getItem('mathspark_daily_goal') ?? '2');
    setNotifications(localStorage.getItem('mathspark_notifications') === 'true');
    setParentEmail(localStorage.getItem('mathspark_parent_email') ?? '');

    fetch(`/api/profile?studentId=${id}`)
      .then((r) => r.json())
      .then((d: ProfileData) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [router]);

  function saveName() {
    const trimmed = newName.trim();
    if (!trimmed) return;
    localStorage.setItem('mathspark_student_name', trimmed);
    setStudentName(trimmed);
    setEditingName(false);
  }

  function toggleMuted() {
    const next = !muted;
    setMuted(next);
    localStorage.setItem('mathspark_muted', String(next));
  }

  function updateDailyGoal(val: string) {
    setDailyGoal(val);
    localStorage.setItem('mathspark_daily_goal', val);
  }

  function toggleNotifications() {
    const next = !notifications;
    setNotifications(next);
    localStorage.setItem('mathspark_notifications', String(next));
  }

  function logout() {
    Object.keys(localStorage)
      .filter((k) => k.startsWith('mathspark_'))
      .forEach((k) => localStorage.removeItem(k));
    router.replace('/start');
  }

  function showToast(msg: string, ok: boolean) {
    setToast({ msg, ok });
    setTimeout(() => setToast(null), 4000);
  }

  async function saveParentEmail(email: string) {
    const trimmed = email.trim();
    localStorage.setItem('mathspark_parent_email', trimmed);
    setParentEmail(trimmed);
    if (studentId) {
      await fetch('/api/student', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentId, parentEmail: trimmed }),
      });
    }
  }

  async function sendReport() {
    if (!studentId) return;
    setSending(true);
    setShareOpen(false);
    try {
      const res = await fetch('/api/reports/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentId }),
      });
      const json = await res.json() as { success?: boolean; sentTo?: string; error?: string };
      if (json.success) {
        showToast(`Report sent to ${json.sentTo}! ✉️`, true);
      } else {
        showToast(json.error ?? 'Failed to send. Try again.', false);
      }
    } catch {
      showToast('Network error. Please try again.', false);
    } finally {
      setSending(false);
    }
  }

  function handleSendClick() {
    if (!parentEmail.trim()) {
      setShareOpen(true); // open email setup modal first
    } else {
      sendReport();
    }
  }

  // ── Loading ──────────────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white gap-4">
        <div className="animate-sparky-bounce"><Sparky mood="thinking" size={100} /></div>
        <p className="text-gray-400 font-bold text-sm">Loading your profile…</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white gap-4 p-8">
        <Sparky mood="encouraging" size={80} />
        <p className="text-gray-500 font-bold text-center">Couldn't load your profile. Please try again.</p>
        <DuoButton variant="blue" onClick={() => router.refresh()}>Retry</DuoButton>
      </div>
    );
  }

  const { student, stats, topics, weeklyData } = data;
  const displayName = studentName || student.name;
  const initial     = displayName ? displayName[0].toUpperCase() : '?';
  const avatarColor = AVATAR_COLORS[initial.charCodeAt(0) % AVATAR_COLORS.length];
  const xp          = stats.totalSolved * 10;
  const accuracy    = stats.totalAttempted > 0
    ? Math.round((stats.totalSolved / stats.totalAttempted) * 100) : 0;
  const badges      = computeBadges(data);
  const maxBar      = Math.max(...weeklyData.map((d) => d.count), 1);
  const earned      = badges.filter((b) => b.earned).length;

  const strongest = [...topics]
    .filter((t) => t.attempted > 0)
    .sort((a, b) => (b.correct / (b.attempted || 1)) - (a.correct / (a.attempted || 1)))[0];
  const weakest = [...topics]
    .filter((t) => t.attempted > 0 && t.mastery !== 'Mastered')
    .sort((a, b) => (a.correct / (a.attempted || 1)) - (b.correct / (b.attempted || 1)))[0];

  const sortedTopics = [...topics].sort(
    (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
  );

  return (
    <div className="min-h-screen bg-gray-50 pb-8">

      {/* ── Toast notification ──────────────────────────────────────────── */}
      {toast && (
        <div className={`fixed top-4 left-1/2 -translate-x-1/2 z-[80] px-5 py-3 rounded-full shadow-xl font-bold text-sm text-white animate-pop-in pointer-events-none ${toast.ok ? 'bg-[#58CC02]' : 'bg-[#FF4B4B]'}`}>
          {toast.msg}
        </div>
      )}

      {/* ── Edit name modal ──────────────────────────────────────────────── */}
      {editingName && (
        <div className="fixed inset-0 bg-black/60 z-[70] flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 w-full max-w-xs shadow-2xl animate-pop-in">
            <h3 className="font-extrabold text-gray-800 text-lg mb-1">Change your name</h3>
            <p className="text-gray-400 text-sm mb-4">What should Sparky call you?</p>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && saveName()}
              className="w-full border-2 border-blue-200 rounded-2xl px-4 py-3 text-base font-bold text-gray-800 outline-none focus:border-[#1CB0F6] mb-4 transition-colors"
              placeholder="Your first name"
              autoFocus
              maxLength={30}
            />
            <div className="flex gap-2">
              <DuoButton variant="white" onClick={() => setEditingName(false)}>Cancel</DuoButton>
              <DuoButton variant="green" onClick={saveName} fullWidth>Save ✓</DuoButton>
            </div>
          </div>
        </div>
      )}

      {/* ── Share modal ─────────────────────────────────────────────────── */}
      {shareOpen && (
        <div className="fixed inset-0 bg-black/60 z-[70] flex items-end justify-center">
          <div className="bg-white rounded-t-3xl p-6 w-full max-w-lg animate-slide-up shadow-2xl">
            <div className="flex items-center gap-3 mb-1">
              <Sparky mood="happy" size={40} />
              <div>
                <h3 className="font-extrabold text-gray-800 text-lg">Send Report to Parent</h3>
                <p className="text-gray-400 text-sm">A beautiful HTML email will be sent instantly</p>
              </div>
            </div>
            <input
              type="email"
              value={parentEmail}
              onChange={(e) => setParentEmail(e.target.value)}
              className="w-full border-2 border-gray-200 rounded-2xl px-4 py-3 text-base font-medium text-gray-800 outline-none focus:border-[#1CB0F6] mt-4 mb-4 transition-colors"
              placeholder="parent@email.com"
            />
            <div className="flex gap-2">
              <DuoButton variant="white" onClick={() => setShareOpen(false)}>Cancel</DuoButton>
              <DuoButton
                variant="green"
                fullWidth
                loading={sending}
                onClick={async () => {
                  await saveParentEmail(parentEmail);
                  sendReport();
                }}
              >
                Send Report 📧
              </DuoButton>
            </div>
          </div>
        </div>
      )}

      {/* ── 1. Profile Header ────────────────────────────────────────────── */}
      <div className="bg-[#131F24] pt-10 pb-6 px-4">
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white border-4 border-white/30 shadow-lg flex-shrink-0"
            style={{ backgroundColor: avatarColor }}
          >
            {initial}
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-extrabold text-white truncate">{displayName}</h1>
            <p className="text-white/60 text-sm font-semibold">Grade {student.grade} · Math Explorer</p>
            <p className="text-white/35 text-xs font-medium mt-0.5">
              Member since {formatDate(student.createdAt)}
            </p>
          </div>
        </div>
        <button
          onClick={() => setEditingName(true)}
          style={{ minHeight: 0 }}
          className="mt-4 bg-white/15 hover:bg-white/25 active:bg-white/10 text-white text-sm font-bold rounded-full px-4 py-2 transition-colors"
        >
          ✏️ Edit name
        </button>
      </div>

      {/* ── 2. Stats Section ─────────────────────────────────────────────── */}
      <div className="bg-white px-4 py-5 border-b border-gray-100">
        <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-4">Your Stats</h2>

        {/* Big XP */}
        <div className="flex items-center gap-3 mb-5 p-4 bg-[#FFF9E6] rounded-2xl border border-yellow-200">
          <div
            className="text-5xl font-extrabold tabular-nums"
            style={{ color: '#FFC800', textShadow: '0 2px 10px rgba(255,200,0,0.35)' }}
          >
            {xp.toLocaleString()}
          </div>
          <div className="flex-1">
            <p className="text-sm font-extrabold text-gray-700">Total XP 💎</p>
            <p className="text-xs text-gray-400 font-medium">{stats.totalSolved} correct × 10 pts each</p>
          </div>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-3">
          <StatCard
            emoji={stats.streakDays >= 3 ? '🔥' : '📅'}
            label="Day Streak"
            value={`${stats.streakDays}`}
            sub={stats.streakDays >= 7 ? 'Week Warrior! 🏅' : stats.streakDays >= 3 ? 'On fire! Keep going!' : 'Start a streak today!'}
            color={stats.streakDays >= 3 ? '#FF9600' : '#1CB0F6'}
            animated={stats.streakDays >= 3}
          />
          <StatCard
            emoji="⭐"
            label="Topics Mastered"
            value={`${stats.topicsMastered}/16`}
            sub={stats.topicsMastered === 16 ? 'Complete! 🎓' : `${16 - stats.topicsMastered} left to master`}
            color="#58CC02"
          />
          <StatCard
            emoji="✅"
            label="Questions Solved"
            value={`${stats.totalSolved}`}
            sub={stats.totalSolved >= 100 ? 'Century Club! 💯' : `${Math.max(0, 100 - stats.totalSolved)} to join 💯`}
            color="#1CB0F6"
          />
          <StatCard
            emoji="🎯"
            label="Accuracy"
            value={`${accuracy}%`}
            sub={accuracy >= 80 ? 'Excellent! 🌟' : accuracy >= 60 ? 'Good work!' : 'Keep practicing!'}
            color={accuracy >= 80 ? '#58CC02' : accuracy >= 60 ? '#FF9600' : '#FF4B4B'}
          />
        </div>
      </div>

      {/* ── 3. Badge Case ────────────────────────────────────────────────── */}
      <div className="bg-white px-4 py-5 mt-2 border-b border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest">Badge Case</h2>
          <div className="flex items-center gap-1.5">
            <div className="h-2 w-2 rounded-full bg-[#58CC02]" />
            <span className="text-xs font-bold text-gray-500">{earned} / {badges.length} earned</span>
          </div>
        </div>
        <div className="grid grid-cols-5 gap-3">
          {badges.map((badge) => (
            <BadgeTile key={badge.id} badge={badge} />
          ))}
        </div>

        {/* Next badge hint */}
        {(() => {
          const next = badges.find((b) => !b.earned);
          return next ? (
            <div className="mt-4 bg-gray-50 rounded-xl px-3 py-2.5 flex items-center gap-2">
              <span className="text-base opacity-40">{next.emoji}</span>
              <div>
                <p className="text-xs font-extrabold text-gray-600">Next: {next.name}</p>
                <p className="text-[11px] text-gray-400 font-medium">{next.desc}</p>
              </div>
            </div>
          ) : null;
        })()}
      </div>

      {/* ── 4. Weekly Report ─────────────────────────────────────────────── */}
      <div className="bg-white px-4 py-5 mt-2 border-b border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest">Weekly Report</h2>
          <button
            onClick={handleSendClick}
            disabled={sending}
            style={{ minHeight: 0 }}
            className="text-xs font-bold text-[#1CB0F6] bg-blue-50 rounded-full px-3 py-1.5 hover:bg-blue-100 transition-colors disabled:opacity-50"
          >
            {sending ? '⏳ Sending…' : '📧 Send to parent'}
          </button>
        </div>

        {/* Activity chart */}
        <div className="bg-gray-50 rounded-2xl p-4 mb-4">
          <div className="flex items-end gap-1.5 h-20 mb-1">
            {weeklyData.map(({ date, count }) => (
              <div key={date} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t-sm transition-all duration-700"
                  style={{
                    background: count > 0
                      ? 'linear-gradient(to top, #46a302, #58CC02)'
                      : 'transparent',
                    height: `${(count / maxBar) * 64}px`,
                    minHeight: count > 0 ? '4px' : '0',
                  }}
                />
                <span className="text-[10px] text-gray-400 font-semibold">{date}</span>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-gray-400 text-center font-medium">Correct answers per day</p>
        </div>

        {/* Strongest & weakest */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          {strongest ? (
            <div className="bg-green-50 border border-green-200 rounded-2xl p-3">
              <p className="text-[10px] text-green-600 font-extrabold uppercase tracking-wide">💪 Strongest</p>
              <p className="text-sm font-extrabold text-gray-800 mt-1 truncate">
                {TOPIC_SHORT[strongest.id] ?? strongest.name}
              </p>
              <p className="text-xs text-green-600 font-bold mt-0.5">
                {strongest.attempted > 0 ? Math.round(strongest.correct / strongest.attempted * 100) : 0}% accurate
              </p>
            </div>
          ) : (
            <div className="bg-gray-50 border border-gray-200 rounded-2xl p-3 flex items-center justify-center">
              <p className="text-xs text-gray-400 text-center font-medium">Start practicing!</p>
            </div>
          )}
          {weakest ? (
            <div className="bg-orange-50 border border-orange-200 rounded-2xl p-3">
              <p className="text-[10px] text-orange-600 font-extrabold uppercase tracking-wide">📈 Needs Work</p>
              <p className="text-sm font-extrabold text-gray-800 mt-1 truncate">
                {TOPIC_SHORT[weakest.id] ?? weakest.name}
              </p>
              <p className="text-xs text-orange-600 font-bold mt-0.5">
                {weakest.attempted > 0 ? Math.round(weakest.correct / weakest.attempted * 100) : 0}% accurate
              </p>
            </div>
          ) : strongest ? (
            <div className="bg-green-50 border border-green-200 rounded-2xl p-3 flex items-center justify-center">
              <p className="text-xs text-green-600 text-center font-bold">All mastered! 🎉</p>
            </div>
          ) : null}
        </div>

        {/* Topics practiced this week */}
        {sortedTopics.filter((t) => t.attempted > 0).length > 0 && (
          <div>
            <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-2">Topics practiced</p>
            <div className="flex flex-wrap gap-1.5">
              {sortedTopics.filter((t) => t.attempted > 0).map((t) => {
                const pct = t.attempted > 0 ? Math.round(t.correct / t.attempted * 100) : 0;
                const color = t.mastery === 'Mastered' ? '#58CC02' : t.attempted > 0 ? '#FF9600' : '#9CA3AF';
                return (
                  <div
                    key={t.id}
                    className="flex items-center gap-1 rounded-full px-2.5 py-1 text-[11px] font-bold"
                    style={{ backgroundColor: `${color}18`, color, border: `1px solid ${color}40` }}
                  >
                    <span>{TOPIC_SHORT[t.id] ?? t.name}</span>
                    <span className="opacity-70">· {pct}%</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* ── 5. Settings ──────────────────────────────────────────────────── */}
      <div className="bg-white px-4 py-5 mt-2">
        <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-2">Settings</h2>

        <div>
          <SettingRow
            icon="🔊"
            label="Sound effects"
            sublabel={muted ? 'Sounds are off' : 'Sounds are on'}
            control={<Toggle on={!muted} onToggle={toggleMuted} />}
          />

          {/* Daily goal selector */}
          <div className="flex items-center justify-between py-3.5 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <span className="text-xl">🎯</span>
              <div>
                <p className="font-bold text-gray-700 text-sm">Daily goal</p>
                <p className="text-xs text-gray-400 font-medium">Lessons per day</p>
              </div>
            </div>
            <div className="flex gap-1.5">
              {(['1','2','3','5'] as const).map((n) => (
                <button
                  key={n}
                  onClick={() => updateDailyGoal(n)}
                  style={{ minHeight: 0 }}
                  className={`w-9 h-9 rounded-full text-xs font-extrabold transition-all ${
                    dailyGoal === n
                      ? 'bg-[#58CC02] text-white shadow-md scale-110'
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          <SettingRow
            icon="👨‍👩‍👧"
            label="Parent's email"
            sublabel={parentEmail || 'Not set — tap to add'}
            control={
              <button
                onClick={() => setShareOpen(true)}
                style={{ minHeight: 0 }}
                className="text-xs font-bold text-[#1CB0F6] bg-blue-50 px-3 py-1.5 rounded-full"
              >
                {parentEmail ? 'Change' : 'Set up'}
              </button>
            }
          />
          <SettingRow
            icon="🔔"
            label="Daily reminders"
            sublabel="Practice notifications"
            control={<Toggle on={notifications} onToggle={toggleNotifications} />}
          />
        </div>

        {/* Logout */}
        <div className="mt-6 mb-2">
          <DuoButton variant="red" fullWidth onClick={logout}>
            Log out
          </DuoButton>
        </div>
        <p className="text-center text-xs text-gray-300 font-medium">MathSpark · Grade 4 Math · v1.0</p>
      </div>

    </div>
  );
}

'use client';

import { useRouter } from 'next/navigation';

// ── Test student registry ─────────────────────────────────────────────────────

interface TestStudent {
  id:    string;
  name:  string;
  grade: number;
  tier:  number;
  color: string;
  emoji: string;
  note:  string;
}

const TIER_LABEL: Record<number, string> = {
  0: 'Free',
  1: 'Starter',
  2: 'Advanced',
  3: 'Unlimited',
};

const TIER_COLOR: Record<number, string> = {
  0: 'bg-gray-100 text-gray-600',
  1: 'bg-blue-100 text-blue-700',
  2: 'bg-purple-100 text-purple-700',
  3: 'bg-green-100 text-green-700',
};

// Multi-grade test students (student_test_grN)
const GRADE_STUDENTS: TestStudent[] = [
  { id: 'student_test_gr2', name: 'Aarav',  grade: 2, tier: 0, color: '#EF4444', emoji: '🌱', note: 'Grade 2 pool only' },
  { id: 'student_test_gr3', name: 'Priya',  grade: 3, tier: 1, color: '#F97316', emoji: '🌿', note: 'Gr3 + Gr4 sample' },
  { id: 'student_test_gr4', name: 'Rahul',  grade: 4, tier: 2, color: '#EAB308', emoji: '🌳', note: 'Ch-series + Gr4–6 full' },
  { id: 'student_test_gr5', name: 'Sneha',  grade: 5, tier: 3, color: '#22C55E', emoji: '🍀', note: 'Gr5 mastered → grade-up CTA' },
  { id: 'student_test_gr6', name: 'Arjun',  grade: 6, tier: 0, color: '#06B6D4', emoji: '⭐', note: 'Gr6 only, Gr7+ locked' },
  { id: 'student_test_gr7', name: 'Kavya',  grade: 7, tier: 1, color: '#8B5CF6', emoji: '🌟', note: 'Gr6 mastered, Gr8 sample' },
  { id: 'student_test_gr8', name: 'Dhruv',  grade: 8, tier: 2, color: '#EC4899', emoji: '🏆', note: 'Gr7+8 mastered, Gr9 full' },
  { id: 'student_test_gr9', name: 'Ananya', grade: 9, tier: 3, color: '#14B8A6', emoji: '🎯', note: 'All grades mastered, no grade-up' },
];

// Original Grade 4 test students (student_001 – student_010)
const GRADE4_STUDENTS: TestStudent[] = [
  { id: 'student_001', name: 'Aarav Sharma',  grade: 4, tier: 3, color: '#3B82F6', emoji: '🏆', note: '12/16 topics mastered, 7-day streak' },
  { id: 'student_002', name: 'Ananya Sharma', grade: 4, tier: 3, color: '#8B5CF6', emoji: '🌟', note: '6 topics mastered, steady learner' },
  { id: 'student_003', name: 'Vivaan Mehta',  grade: 4, tier: 2, color: '#F97316', emoji: '⚡', note: '4 topics mastered, loves puzzles' },
  { id: 'student_004', name: 'Ishika Mehta',  grade: 4, tier: 2, color: '#EC4899', emoji: '🌱', note: 'New user, 5 days, decimal strength' },
  { id: 'student_005', name: 'Arjun Patel',   grade: 4, tier: 1, color: '#22C55E', emoji: '⏰', note: 'Hits daily limit, 2 mastered' },
  { id: 'student_006', name: 'Saanvi Iyer',   grade: 4, tier: 3, color: '#14B8A6', emoji: '🔥', note: 'Power user, 23-day streak, 14 mastered' },
  { id: 'student_007', name: 'Dhruv Iyer',    grade: 4, tier: 1, color: '#EAB308', emoji: '🌱', note: 'Just started, 2 days practice' },
  { id: 'student_008', name: 'Meera Reddy',   grade: 4, tier: 2, color: '#EF4444', emoji: '📈', note: '15-day streak, 8 mastered' },
  { id: 'student_009', name: 'Kabir Reddy',   grade: 4, tier: 2, color: '#06B6D4', emoji: '🧠', note: '7 mastered, weak in geometry' },
  { id: 'student_010', name: 'Tara Reddy',    grade: 4, tier: 1, color: '#84CC16', emoji: '🌸', note: 'Brand new, 3 days' },
];

// ── Component ─────────────────────────────────────────────────────────────────

function StudentCard({ s }: { s: TestStudent }) {
  const router = useRouter();

  function loginAs() {
    localStorage.setItem('mathspark_student_id',        s.id);
    localStorage.setItem('mathspark_student_name',      s.name);
    localStorage.setItem('mathspark_student_grade',     String(s.grade));
    localStorage.setItem('mathspark_subscription_tier', String(s.tier));
    router.push('/chapters');
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-4 flex items-center gap-3 shadow-sm hover:shadow-md transition-shadow">
      {/* Avatar */}
      <div
        className="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold text-sm"
        style={{ backgroundColor: s.color }}
      >
        {s.name[0]}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold text-gray-800 text-sm">{s.name}</span>
          <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded-full">Gr {s.grade}</span>
          <span className={`text-xs px-1.5 py-0.5 rounded-full ${TIER_COLOR[s.tier]}`}>{TIER_LABEL[s.tier]}</span>
        </div>
        <p className="text-xs text-gray-400 mt-0.5 truncate">{s.note}</p>
      </div>

      {/* CTA */}
      <button
        onClick={loginAs}
        className="flex-shrink-0 bg-indigo-500 hover:bg-indigo-600 text-white text-xs font-bold px-3 py-2 rounded-xl transition-colors"
      >
        Log in →
      </button>
    </div>
  );
}

export default function DevPage() {
  return (
    <div className="min-h-screen bg-gray-50 px-4 py-8 max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-2xl">🔧</span>
          <h1 className="text-xl font-bold text-gray-800">Dev Quick-Login</h1>
          <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded-full font-semibold">DEV ONLY</span>
        </div>
        <p className="text-sm text-gray-500">Sets localStorage and navigates to /chapters. No password needed.</p>
      </div>

      {/* Multi-grade students */}
      <section className="mb-6">
        <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
          Multi-Grade Students (Gr 2–9)
        </h2>
        <div className="space-y-2">
          {GRADE_STUDENTS.map((s) => <StudentCard key={s.id} s={s} />)}
        </div>
      </section>

      {/* Grade 4 original students */}
      <section className="mb-8">
        <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
          Original Grade 4 Students
        </h2>
        <div className="space-y-2">
          {GRADE4_STUDENTS.map((s) => <StudentCard key={s.id} s={s} />)}
        </div>
      </section>

      {/* Footer links */}
      <div className="flex gap-4 text-sm text-center justify-center text-gray-400">
        <a href="/seed" className="underline hover:text-gray-600">Seed page</a>
        <span>·</span>
        <a href="/chapters" className="underline hover:text-gray-600">Chapters</a>
        <span>·</span>
        <a href="/start" className="underline hover:text-gray-600">Onboarding</a>
        <span>·</span>
        <a href="/leaderboard" className="underline hover:text-gray-600">Leaderboard</a>
      </div>
    </div>
  );
}

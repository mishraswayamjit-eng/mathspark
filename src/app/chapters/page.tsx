'use client';

import { useEffect, useState, type ReactElement } from 'react';
import { useRouter } from 'next/navigation';
import type { DashboardData, TopicWithProgress, TopicNode, CrownLevel, NodeState } from '@/types';
import Sparky from '@/components/Sparky';

// ─── Topic metadata ────────────────────────────────────────────────────────────

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06': '🔍', 'ch07-08': '🍕', 'ch09-10': '🧮',
  'ch11': '🔟', 'ch12': '📏', 'ch13': '🔡', 'ch14': '⚖️',
  'ch15': '🧩', 'ch16': '📈', 'ch17': '🕐', 'ch18': '📐',
  'ch19': '🔺', 'ch20': '🟦', 'ch21': '⭕', 'dh': '📊',
};

const TOPIC_SHORT: Record<string, string> = {
  'ch01-05': 'Numbers', 'ch06': 'Factors', 'ch07-08': 'Fractions', 'ch09-10': 'Operations',
  'ch11': 'Decimals', 'ch12': 'Measures', 'ch13': 'Algebra', 'ch14': 'Equations',
  'ch15': 'Puzzles', 'ch16': 'Sequences', 'ch17': 'Time', 'ch18': 'Angles',
  'ch19': 'Triangles', 'ch20': 'Quadrilaterals', 'ch21': 'Circle', 'dh': 'Data',
};

// S-curve: L=22%, C=50%, R=78%
// Pattern: L→C→R→R→C→L→L→C→R→R→C→L→L→C→R→C
const NODE_X_PCT = [22, 50, 78, 78, 50, 22, 22, 50, 78, 78, 50, 22, 22, 50, 78, 50];

const NODE_SPACING    = 130;
const NODE_TOP_OFFSET = 20;
const NODE_NORMAL     = 72;
const NODE_CURRENT    = 88;
const DAILY_GOAL      = 10;

const CROWN_COLORS = ['', '#CD7F32', '#C0C0C0', '#FFD700', '#9B59B6', '#00BCD4'];

const PREREQS: Record<string, string[] | '__any3__'> = {
  'ch01-05': [],
  'ch06': ['ch01-05'], 'ch07-08': ['ch06'], 'ch09-10': ['ch07-08'],
  'ch11': ['ch09-10'], 'ch12': ['ch11'], 'ch13': ['ch12'], 'ch14': ['ch13'],
  'ch15': '__any3__', 'ch16': '__any3__', 'ch17': '__any3__',
  'ch18': ['ch14'], 'ch19': ['ch18'], 'ch20': ['ch19'], 'ch21': ['ch20'],
  'dh': '__any3__',
};

// ─── Pure helpers ──────────────────────────────────────────────────────────────

function getCrownLevel(t: TopicWithProgress): CrownLevel {
  if (t.mastery === 'Mastered') return 5;
  if (t.attempted === 0) return 0;
  const pct = t.correct / t.attempted;
  if (pct >= 0.8) return 4;
  if (pct >= 0.6) return 3;
  if (pct >= 0.4) return 2;
  return 1;
}

function isUnlocked(id: string, byId: Map<string, TopicWithProgress>): boolean {
  const prereq = PREREQS[id];
  if (!prereq) return true;
  if (prereq === '__any3__') {
    let count = 0;
    byId.forEach((t) => { if (t.attempted > 0) count++; });
    return count >= 3;
  }
  return prereq.every((pid) => (byId.get(pid)?.attempted ?? 0) > 0);
}

function buildTopicNodes(topics: TopicWithProgress[]): TopicNode[] {
  const byId = new Map<string, TopicWithProgress>();
  topics.forEach((t) => byId.set(t.id, t));

  let currentSet = false;
  const nodes: TopicNode[] = [];

  for (const id of TOPIC_ORDER) {
    const topic = byId.get(id);
    if (!topic) continue;

    const unlocked = isUnlocked(id, byId);
    const crown    = getCrownLevel(topic);

    let state: NodeState;
    let prereqLabel = '';

    if (!unlocked) {
      state = 'locked';
      const prereq = PREREQS[id];
      if (prereq === '__any3__') {
        prereqLabel = 'Complete 3 topics first';
      } else if (Array.isArray(prereq) && prereq.length > 0) {
        const prereqName = TOPIC_SHORT[prereq[prereq.length - 1]] ?? 'previous topic';
        prereqLabel = `Finish ${prereqName} first`;
      }
    } else if (topic.mastery === 'Mastered') {
      state = 'completed';
    } else if (topic.attempted > 0) {
      state = 'practicing';
    } else {
      state = 'not_started';
    }

    if (!currentSet && state !== 'locked' && state !== 'completed') {
      state = 'current';
      currentSet = true;
    }

    nodes.push({ topic, state, crownLevel: crown, prerequisiteLabel: prereqLabel });
  }

  return nodes;
}

function getHearts(): number {
  if (typeof window === 'undefined') return 5;
  const today     = new Date().toDateString();
  const savedDate = localStorage.getItem('mathspark_hearts_date');
  if (savedDate !== today) {
    localStorage.setItem('mathspark_hearts', '5');
    localStorage.setItem('mathspark_hearts_date', today);
    return 5;
  }
  return parseInt(localStorage.getItem('mathspark_hearts') ?? '5', 10);
}

// ─── Component ─────────────────────────────────────────────────────────────────

export default function ChaptersPage() {
  const router = useRouter();
  const [data,        setData]        = useState<DashboardData | null>(null);
  const [loading,     setLoading]     = useState(true);
  const [hearts,      setHearts]      = useState(5);
  const [studentName, setStudentName] = useState('');
  const [lockedMsg,   setLockedMsg]   = useState<string | null>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentName(localStorage.getItem('mathspark_student_name') ?? '');
    setHearts(getHearts());
    fetch(`/api/dashboard?studentId=${id}`)
      .then((r) => r.json())
      .then((d: DashboardData) => { setData(d); setLoading(false); });
  }, [router]);

  // Computed values
  const nodes        = data ? buildTopicNodes(data.topics) : [];
  const xp           = (data?.stats.totalSolved ?? 0) * 10;
  const todayCorrect = data?.weeklyData?.[data.weeklyData.length - 1]?.count ?? 0;
  const goalMet      = todayCorrect >= DAILY_GOAL;
  const streakDays   = data?.stats.streakDays ?? 0;
  const pathHeight   = TOPIC_ORDER.length * NODE_SPACING + NODE_TOP_OFFSET + 120;

  // ── Loading skeleton ─────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#131F24] to-[#1a3040]">
        <div className="sticky top-0 z-50 h-14 bg-[#131F24]/90 backdrop-blur-sm flex items-center justify-between px-4">
          <div className="h-6 w-28 rounded-full bg-white/20 animate-pulse" />
          <div className="flex gap-3">
            {[1,2,3,4].map((n) => (
              <div key={n} className="h-6 w-12 rounded-full bg-white/20 animate-pulse" />
            ))}
          </div>
        </div>
        <div className="mx-4 mt-3 h-16 rounded-2xl bg-white/10 animate-pulse" />
        <div className="relative mx-2 mt-4" style={{ height: 5 * NODE_SPACING }}>
          {[22, 50, 78, 50, 22].map((x, i) => (
            <div
              key={i}
              className="absolute animate-pulse"
              style={{
                left: `${x}%`,
                top:  NODE_TOP_OFFSET + i * NODE_SPACING,
                transform: 'translateX(-50%)',
                width: NODE_NORMAL, height: NODE_NORMAL,
                borderRadius: '50%',
                background: 'rgba(255,255,255,0.15)',
              }}
            />
          ))}
        </div>
      </div>
    );
  }

  // ── TopBar ───────────────────────────────────────────────────────────────────
  function TopBar() {
    const initial = studentName ? studentName[0].toUpperCase() : '?';
    return (
      <div className="sticky top-0 z-50 h-14 bg-[#131F24]/95 backdrop-blur-sm flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="animate-sparky-bounce">
            <Sparky mood="happy" size={30} />
          </div>
          <span className="font-extrabold text-white text-base tracking-tight">MathSpark</span>
        </div>
        <div className="flex items-center gap-3">
          {/* Streak */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm">🔥</span>
            <span className="text-white text-xs font-extrabold">{streakDays}</span>
          </div>
          {/* XP */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm">💎</span>
            <span className="text-white text-xs font-extrabold">{xp}</span>
          </div>
          {/* Hearts */}
          <div className="flex items-center gap-0.5">
            {[1,2,3,4,5].map((h) => (
              <span
                key={h}
                className="text-sm transition-opacity duration-300"
                style={{ opacity: h <= hearts ? 1 : 0.2 }}
              >❤️</span>
            ))}
          </div>
          {/* Avatar */}
          <div className="w-8 h-8 rounded-full bg-[#FFC800] flex items-center justify-center font-extrabold text-sm text-yellow-900 border-2 border-white">
            {initial}
          </div>
        </div>
      </div>
    );
  }

  // ── DailyGoalBanner ──────────────────────────────────────────────────────────
  function DailyGoalBanner() {
    const r          = 20;
    const circ       = 2 * Math.PI * r; // ≈125.7
    const progress   = Math.min(todayCorrect / DAILY_GOAL, 1);
    const dashOffset = circ * (1 - progress);

    return (
      <div className="mx-4 mt-3 bg-[#1e2d38] rounded-2xl px-4 py-2 flex items-center gap-3 shadow-sm">
        <svg width="52" height="52" viewBox="0 0 52 52">
          <circle cx="26" cy="26" r={r} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="5" />
          <circle
            cx="26" cy="26" r={r} fill="none"
            stroke={goalMet ? '#58CC02' : '#FFC800'}
            strokeWidth="5"
            strokeLinecap="round"
            strokeDasharray={circ}
            strokeDashoffset={dashOffset}
            transform="rotate(-90 26 26)"
            style={{ transition: 'stroke-dashoffset 0.6s ease' }}
          />
          <text x="26" y="30" textAnchor="middle" fontSize="11" fontWeight="bold" fill={goalMet ? '#58CC02' : '#FFC800'}>
            {goalMet ? '✓' : todayCorrect}
          </text>
        </svg>
        <div>
          <p className="text-sm font-extrabold text-white">
            {goalMet ? 'Daily goal met! 🎯' : `${todayCorrect} / ${DAILY_GOAL} correct today`}
          </p>
          <p className="text-xs text-white/50 font-medium">
            {goalMet ? 'Amazing work, keep it up!' : 'Complete 2 lessons to reach your goal!'}
          </p>
        </div>
      </div>
    );
  }

  // ── ConnectingPath ────────────────────────────────────────────────────────────
  function ConnectingPath() {
    const segments: ReactElement[] = [];
    for (let i = 0; i < nodes.length - 1; i++) {
      const x1   = NODE_X_PCT[i];
      const x2   = NODE_X_PCT[i + 1];
      const r1   = nodes[i].state     === 'current' ? NODE_CURRENT / 2 : NODE_NORMAL / 2;
      const r2   = nodes[i + 1].state === 'current' ? NODE_CURRENT / 2 : NODE_NORMAL / 2;
      const y1   = NODE_TOP_OFFSET + i       * NODE_SPACING + r1;
      const y2   = NODE_TOP_OFFSET + (i + 1) * NODE_SPACING + r2;
      const midY = (y1 + y2) / 2;
      const cx   = (x1 + x2) / 2;
      segments.push(
        <path
          key={i}
          d={`M ${x1} ${y1} Q ${cx} ${midY} ${x2} ${y2}`}
          fill="none"
          stroke="rgba(255,255,255,0.3)"
          strokeWidth="0.8"
          strokeDasharray="3 4"
        />
      );
    }
    return (
      <svg
        className="absolute inset-0 w-full"
        style={{ height: pathHeight }}
        viewBox={`0 0 100 ${pathHeight}`}
        preserveAspectRatio="none"
      >
        {segments}
      </svg>
    );
  }

  // ── TopicNodeButton ───────────────────────────────────────────────────────────
  function TopicNodeButton({ node, index }: { node: TopicNode; index: number }) {
    const { topic, state, crownLevel } = node;
    const isCurrent = state === 'current';
    const size      = isCurrent ? NODE_CURRENT : NODE_NORMAL;

    const bgClass = {
      completed:   'bg-[#58CC02] border-[#46a302]',
      current:     'bg-[#FFC800] border-[#CC9900] ring-4 ring-yellow-200 animate-pulse',
      practicing:  'bg-[#1CB0F6] border-[#0a98dc]',
      not_started: 'bg-white border-blue-200',
      locked:      'bg-gray-700 border-gray-600 opacity-60',
    }[state];

    const top  = NODE_TOP_OFFSET + index * NODE_SPACING;
    const left = NODE_X_PCT[index];

    function handleClick() {
      if (state === 'locked') {
        setLockedMsg(node.prerequisiteLabel || 'Complete earlier topics first');
        setTimeout(() => setLockedMsg(null), 2500);
      } else {
        router.push(`/practice/${topic.id}`);
      }
    }

    const innerEmoji = state === 'locked'
      ? '🔒'
      : state === 'completed'
      ? '✓'
      : TOPIC_EMOJI[topic.id] ?? '📚';

    const innerColor =
      state === 'current'                                           ? 'text-gray-800' :
      state === 'completed' || state === 'practicing' || state === 'locked' ? 'text-white' :
      'text-gray-600';

    return (
      <div
        className="absolute flex flex-col items-center"
        style={{ left: `${left}%`, top, transform: 'translateX(-50%)' }}
      >
        <button
          onClick={handleClick}
          className={`flex items-center justify-center border-4 rounded-full font-bold text-2xl transition-transform active:scale-95 ${bgClass} ${innerColor}`}
          style={{ width: size, height: size, minHeight: 48 }}
          aria-label={topic.name}
        >
          {innerEmoji}
        </button>

        {/* Crown stars */}
        <div className="flex gap-0.5 mt-1">
          {[1,2,3,4,5].map((level) => (
            <span
              key={level}
              className="text-[11px] leading-none select-none"
              style={{
                color: level <= crownLevel ? CROWN_COLORS[crownLevel] : 'rgba(255,255,255,0.18)',
                textShadow: level <= crownLevel ? `0 0 6px ${CROWN_COLORS[crownLevel]}` : 'none',
                filter: level <= crownLevel ? 'drop-shadow(0 0 2px rgba(0,0,0,0.3))' : 'none',
              }}
            >★</span>
          ))}
        </div>

        {/* Short label */}
        <span
          className={`mt-1 text-xs text-white drop-shadow leading-tight text-center max-w-[80px] ${isCurrent ? 'font-extrabold' : 'font-semibold'}`}
        >
          {TOPIC_SHORT[topic.id] ?? topic.name}
        </span>

        {/* START HERE badge */}
        {isCurrent && (
          <span className="mt-1 bg-[#FFC800] text-gray-800 text-[10px] font-extrabold rounded-full px-2 py-0.5 shadow-md">
            START HERE
          </span>
        )}
      </div>
    );
  }

  // ── Locked tooltip ────────────────────────────────────────────────────────────
  function LockedTooltip({ msg }: { msg: string }) {
    return (
      <div className="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 pointer-events-none">
        <div className="bg-gray-800 text-white rounded-full px-4 py-2 shadow-lg text-sm font-bold whitespace-nowrap animate-pop-in">
          🔒 {msg}
        </div>
      </div>
    );
  }

  // ── Main render ───────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#131F24] to-[#1a3040]">
      <TopBar />
      <DailyGoalBanner />

      {/* Crown legend */}
      <div className="mx-4 mt-3 flex items-center justify-between">
        <span className="text-white/70 text-xs font-bold uppercase tracking-widest">Learning Path</span>
        <div className="flex items-center gap-2">
          {([
            ['#CD7F32','Bronze'],['#C0C0C0','Silver'],['#FFD700','Gold'],
            ['#9B59B6','Purple'],['#00BCD4','Diamond'],
          ] as [string,string][]).map(([color, label]) => (
            <div key={label} className="flex items-center gap-0.5">
              <span className="text-[10px]" style={{ color, textShadow: `0 0 4px ${color}` }}>★</span>
              <span className="text-[9px] text-white/40 font-semibold">{label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="relative mx-2 mt-4" style={{ height: pathHeight }}>
        <ConnectingPath />
        {nodes.map((node, i) => (
          <TopicNodeButton key={node.topic.id} node={node} index={i} />
        ))}
      </div>
      {/* Bottom padding so last node isn't clipped behind nav */}
      <div className="h-8" />
      {lockedMsg && <LockedTooltip msg={lockedMsg} />}
    </div>
  );
}

'use client';

import { useEffect, useState, useRef, useCallback, type Ref } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Confetti from '@/components/Confetti';
import type { LeagueData, LeagueMember, LastWeekResult } from '@/types';

// ── Tier metadata ─────────────────────────────────────────────────────────────

const TIER_COLORS: Record<number, { bg: string; text: string; border: string; badge: string }> = {
  1: { bg: '#CD7F32', text: '#7B4D1E', border: '#CD7F32', badge: '🥉' },
  2: { bg: '#C0C0C0', text: '#4a4a4a', border: '#C0C0C0', badge: '🥈' },
  3: { bg: '#FFD700', text: '#7B5800', border: '#FFD700', badge: '🥇' },
  4: { bg: '#b9f2ff', text: '#005f7a', border: '#00BCD4', badge: '💎' },
  5: { bg: '#e8d5ff', text: '#5B00A0', border: '#9B59B6', badge: '👑' },
};

// ── Avatar ────────────────────────────────────────────────────────────────────

function Avatar({ name, color, size = 40 }: { name: string; color: string; size?: number }) {
  const initial = name ? name[0].toUpperCase() : '?';
  return (
    <div
      className="rounded-full flex items-center justify-center font-extrabold text-white flex-shrink-0"
      style={{ width: size, height: size, backgroundColor: color, fontSize: size * 0.4 }}
    >
      {initial}
    </div>
  );
}

// ── Tier status card ──────────────────────────────────────────────────────────

function StatusCard({
  league,
  isLoading,
}: {
  league: LeagueData | null;
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <div className="mx-4 rounded-3xl bg-gray-100 animate-pulse h-28" />
    );
  }
  if (!league) return null;

  const tier    = league.tier;
  const colors  = TIER_COLORS[tier] ?? TIER_COLORS[1];
  const total   = league.totalMembers;
  const promo   = league.promoteCount;
  const demote  = league.demoteCount;
  const myRank  = league.myRank;

  const zoneMsg =
    myRank <= promo                ? '⬆️ Promotion zone! Keep it up!' :
    myRank > total - demote        ? '⚠️ Danger zone — practice more!' :
    myRank <= Math.ceil(total / 2) ? '👍 Mid-table — push for promotion!' :
                                     '💪 You can climb higher!';

  return (
    <div
      className="mx-4 rounded-3xl p-4 border-2"
      style={{ borderColor: colors.border, background: `${colors.bg}22` }}
    >
      <div className="flex items-center gap-3">
        <div className="text-4xl">{colors.badge}</div>
        <div className="flex-1">
          <p className="font-extrabold text-lg text-gray-800">{league.leagueName} League</p>
          <p className="text-sm font-semibold text-gray-500">
            #{myRank} of {total} · {league.myWeeklyXP.toLocaleString()} XP this week
          </p>
        </div>
        <div
          className="rounded-2xl px-3 py-1 text-xs font-extrabold"
          style={{ backgroundColor: `${colors.border}33`, color: colors.text }}
        >
          Tier {tier}/5
        </div>
      </div>
      <p className="mt-2 text-sm font-semibold text-gray-600">{zoneMsg}</p>
    </div>
  );
}

// ── Member row ────────────────────────────────────────────────────────────────

function MemberRow({
  member,
  rank,
  total,
  promoteCount,
  demoteCount,
  isFree,
  onClick,
  rowRef,
}: {
  member: LeagueMember;
  rank: number;
  total: number;
  promoteCount: number;
  demoteCount: number;
  isFree: boolean;
  onClick: () => void;
  rowRef?: Ref<HTMLDivElement>;
}) {
  const isTop3      = rank <= 3;
  const isPromoZone = rank <= promoteCount;
  const isDangerZone = rank > total - demoteCount;
  const blurred     = !isFree && rank > 5;

  const medals = ['🥇', '🥈', '🥉'];
  const bg     = isTop3 ? `${['#FFD70020','#C0C0C020','#CD7F3220'][rank - 1]}` :
                 isPromoZone ? '#f0fdf4' :
                 isDangerZone ? '#fffbeb' : 'white';

  return (
    <div
      ref={rowRef}
      className={`relative flex items-center gap-3 px-4 py-3 border-b border-gray-50 cursor-pointer transition-colors hover:bg-gray-50 ${
        member.isMe ? 'ring-2 ring-inset ring-duo-blue' : ''
      } ${blurred ? 'select-none' : ''}`}
      style={{
        minHeight: isTop3 ? 72 : 56,
        backgroundColor: bg,
        filter: blurred ? 'blur(4px)' : undefined,
        pointerEvents: blurred ? 'none' : undefined,
      }}
      onClick={onClick}
    >
      {/* Rank / medal */}
      <div className="w-8 text-center flex-shrink-0">
        {isTop3 ? (
          <span className="text-xl">{medals[rank - 1]}</span>
        ) : (
          <span className="text-sm font-extrabold text-gray-400">#{rank}</span>
        )}
      </div>

      {/* Avatar */}
      <Avatar name={member.displayName} color={member.avatarColor} size={isTop3 ? 44 : 36} />

      {/* Name + zone indicator */}
      <div className="flex-1 min-w-0">
        <p className={`font-extrabold truncate ${member.isMe ? 'text-duo-blue' : 'text-gray-800'} ${isTop3 ? 'text-base' : 'text-sm'}`}>
          {member.displayName} {member.isMe && <span className="text-xs font-bold">(you)</span>}
        </p>
        <p className="text-xs text-gray-400 font-semibold">
          {isPromoZone && !isTop3 && '⬆️ Promotion zone ·'}
          {isDangerZone && '⚠️ Danger zone ·'}{' '}
          {member.weeklyXP.toLocaleString()} XP
        </p>
      </div>

      {/* XP badge for top 3 */}
      {isTop3 && (
        <div className="bg-yellow-100 text-yellow-700 rounded-full px-2 py-0.5 text-xs font-extrabold flex-shrink-0">
          {member.weeklyXP.toLocaleString()} XP
        </div>
      )}
    </div>
  );
}

// ── Free gate overlay ─────────────────────────────────────────────────────────

function FreeGate({ rank }: { rank: number }) {
  return (
    <div className="mx-4 my-2 rounded-2xl border-2 border-duo-gold bg-[#FFF9E6] p-4 text-center">
      <p className="text-2xl mb-1">🔒</p>
      <p className="font-extrabold text-gray-800 text-sm">You&apos;re #{rank} — see your full rank!</p>
      <p className="text-xs text-gray-500 font-medium mt-1 mb-3">
        Upgrade to see all {rank > 5 ? rank - 5 : 0}+ members below you and track your league position.
      </p>
      <Link
        href="/pricing"
        className="inline-block bg-duo-gold text-[#7B5800] font-extrabold text-sm rounded-full px-5 py-2 active:scale-95 transition-transform"
      >
        Upgrade to Pro 🚀
      </Link>
    </div>
  );
}

// ── Sticky my-rank bar ────────────────────────────────────────────────────────

function StickyMyRankBar({ member, visible }: { member: LeagueMember | null; visible: boolean }) {
  if (!member || !visible) return null;
  return (
    <div className="fixed bottom-[72px] left-0 right-0 z-40 px-4">
      <div className="max-w-lg mx-auto">
        <div
          className="flex items-center gap-3 bg-white rounded-2xl shadow-xl border-2 border-duo-blue px-4 py-2.5"
        >
          <Avatar name={member.displayName} color={member.avatarColor} size={32} />
          <div className="flex-1">
            <p className="text-sm font-extrabold text-duo-blue">{member.displayName} (you)</p>
            <p className="text-xs text-gray-400 font-semibold">#{member.rank} · {member.weeklyXP.toLocaleString()} XP</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Promotion overlay ─────────────────────────────────────────────────────────

function PromotionOverlay({
  from, to, myRank, onDismiss,
}: {
  from: string; to: string; myRank: number | null; onDismiss: () => void;
}) {
  const [showConfetti, setShowConfetti] = useState(true);

  const tierColors: Record<string, string> = {
    Silver: '#C0C0C0', Gold: '#FFD700', Diamond: '#00BCD4', Champion: '#9B59B6',
  };
  const color = tierColors[to] ?? '#58CC02';

  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center bg-black/70 px-6">
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}
      <div className="bg-white rounded-3xl p-8 w-full max-w-sm text-center shadow-2xl animate-pop-in">
        <div className="text-6xl mb-3">🎉</div>
        <h2 className="text-2xl font-extrabold text-gray-800 mb-1">You&apos;ve been promoted!</h2>
        {myRank && (
          <p className="text-gray-500 font-semibold text-sm mb-2">Finished #{myRank} in {from} League</p>
        )}
        <div
          className="inline-flex items-center gap-2 rounded-2xl px-5 py-3 mb-5 font-extrabold text-lg"
          style={{ backgroundColor: `${color}22`, color }}
        >
          Welcome to {to} League!
        </div>
        <button
          onClick={onDismiss}
          className="w-full bg-duo-green text-white font-extrabold rounded-2xl py-3.5 text-base active:scale-95 transition-transform"
          style={{ minHeight: 56 }}
        >
          Continue →
        </button>
      </div>
    </div>
  );
}

// ── Demotion banner ───────────────────────────────────────────────────────────

function DemotionBanner({ tier, onDismiss }: { tier: number; onDismiss: () => void }) {
  const tierName = { 1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Diamond', 5: 'Champion' }[tier] ?? 'Bronze';
  return (
    <div className="bg-amber-100 border-b-2 border-amber-300 px-4 py-3 flex items-center gap-3">
      <span className="text-lg">⬇️</span>
      <p className="flex-1 text-sm font-bold text-amber-800">
        You were demoted to {tierName} League this week. Practice more to climb back up!
      </p>
      <button onClick={onDismiss} className="text-amber-500 font-extrabold text-lg leading-none" style={{ minHeight: 0 }}>
        ✕
      </button>
    </div>
  );
}

// ── Last-week tab ─────────────────────────────────────────────────────────────

function LastWeekTab({ data }: { data: LastWeekResult | null }) {
  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center py-20 gap-3 text-center px-8">
        <p className="text-5xl">📊</p>
        <p className="font-extrabold text-gray-700">No last-week data yet</p>
        <p className="text-sm text-gray-400 font-medium">Keep playing and check back after Sunday!</p>
      </div>
    );
  }

  const { league, awards } = data;

  return (
    <div className="pb-6">
      {awards.length > 0 && (
        <div className="mx-4 mt-4 mb-2">
          <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-2">Your Awards</p>
          <div className="space-y-2">
            {awards.map((a, i) => {
              const icons: Record<string, string> = {
                most_improved: '📈', speed_demon: '⚡', accuracy_king: '🎯', explorer: '🗺️',
              };
              const names: Record<string, string> = {
                most_improved: 'Most Improved', speed_demon: 'Speed Demon',
                accuracy_king: 'Accuracy King', explorer: 'Explorer',
              };
              return (
                <div key={i} className="bg-yellow-50 border border-yellow-200 rounded-2xl px-4 py-3 flex items-center gap-3">
                  <span className="text-2xl">{icons[a.awardType] ?? '🏅'}</span>
                  <div>
                    <p className="font-extrabold text-gray-800 text-sm">{names[a.awardType] ?? a.awardType}</p>
                    <p className="text-xs text-gray-500 font-medium">{a.value}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {league ? (
        <div className="mt-4">
          <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mx-4 mb-2">
            Last Week — {league.leagueName} League
          </p>
          {league.members.map((m, i) => (
            <div
              key={m.studentId}
              className={`flex items-center gap-3 px-4 py-3 border-b border-gray-50 ${m.isMe ? 'ring-2 ring-inset ring-duo-blue' : ''}`}
              style={{ minHeight: 56 }}
            >
              <div className="w-8 text-center">
                {m.rank && m.rank <= 3 ? (
                  <span className="text-xl">{['🥇', '🥈', '🥉'][m.rank - 1]}</span>
                ) : (
                  <span className="text-sm font-extrabold text-gray-400">#{m.rank ?? i + 1}</span>
                )}
              </div>
              <Avatar name={m.displayName} color={m.avatarColor} size={36} />
              <div className="flex-1 min-w-0">
                <p className={`font-extrabold text-sm truncate ${m.isMe ? 'text-duo-blue' : 'text-gray-800'}`}>
                  {m.displayName} {m.isMe && '(you)'}
                  {m.promoted && <span className="ml-1 text-green-500 text-xs">⬆️ Promoted</span>}
                  {m.demoted  && <span className="ml-1 text-amber-500 text-xs">⬇️ Demoted</span>}
                </p>
                <p className="text-xs text-gray-400 font-semibold">{m.weeklyXP.toLocaleString()} XP</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-400 text-sm font-medium py-8 px-4">
          You weren&apos;t in a league last week. Keep playing this week!
        </p>
      )}
    </div>
  );
}

// ── All-time tab ──────────────────────────────────────────────────────────────

interface AllTimeMember {
  studentId: string;
  displayName: string;
  avatarColor: string;
  totalXP: number;
  tier: number;
  rank: number;
  isMe: boolean;
}

function AllTimeTab({
  data,
  isFree,
  myRank,
}: {
  data: { members: AllTimeMember[]; myEntry: AllTimeMember | null } | null;
  isFree: boolean;
  myRank: number;
}) {
  if (!data) {
    return <div className="flex items-center justify-center py-20 text-gray-400 font-semibold">Loading…</div>;
  }

  const { members, myEntry } = data;

  return (
    <div className="pb-6">
      {members.map((m) => {
        const blurred = isFree && m.rank > 5;
        const tierBadge = TIER_COLORS[m.tier]?.badge ?? '🥉';
        return (
          <div
            key={m.studentId}
            className={`flex items-center gap-3 px-4 py-3 border-b border-gray-50 ${m.isMe ? 'ring-2 ring-inset ring-duo-blue' : ''}`}
            style={{ minHeight: 56, filter: blurred ? 'blur(4px)' : undefined }}
          >
            <div className="w-8 text-center">
              {m.rank <= 3 ? (
                <span className="text-xl">{['🥇', '🥈', '🥉'][m.rank - 1]}</span>
              ) : (
                <span className="text-sm font-extrabold text-gray-400">#{m.rank}</span>
              )}
            </div>
            <Avatar name={m.displayName} color={m.avatarColor} size={36} />
            <div className="flex-1 min-w-0">
              <p className={`font-extrabold text-sm truncate ${m.isMe ? 'text-duo-blue' : 'text-gray-800'}`}>
                {m.displayName} {m.isMe && '(you)'} <span className="opacity-60">{tierBadge}</span>
              </p>
              <p className="text-xs text-gray-400 font-semibold">{m.totalXP.toLocaleString()} lifetime XP</p>
            </div>
          </div>
        );
      })}

      {isFree && myRank > 5 && (
        <FreeGate rank={myRank} />
      )}

      {myEntry && !members.find((m) => m.isMe) && (
        <div className="mx-4 mt-4">
          <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-2">Your Position</p>
          <div className="flex items-center gap-3 px-4 py-3 rounded-2xl ring-2 ring-duo-blue bg-blue-50">
            <div className="w-8 text-center">
              <span className="text-sm font-extrabold text-duo-blue">#{myEntry.rank}</span>
            </div>
            <Avatar name={myEntry.displayName} color={myEntry.avatarColor} size={36} />
            <div className="flex-1">
              <p className="font-extrabold text-sm text-duo-blue">{myEntry.displayName} (you)</p>
              <p className="text-xs text-gray-400 font-semibold">{myEntry.totalXP.toLocaleString()} lifetime XP</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function LeaderboardPage() {
  const router = useRouter();

  const [studentId, setStudentId] = useState<string | null>(null);
  const [tab,       setTab]       = useState<'week' | 'last' | 'all'>('week');

  // This-week data
  const [leagueData,  setLeagueData]  = useState<LeagueData | null>(null);
  const [weekLoading, setWeekLoading] = useState(true);

  // Last-week data
  const [lastWeekData,    setLastWeekData]    = useState<LastWeekResult | null>(null);
  const [lastWeekLoaded,  setLastWeekLoaded]  = useState(false);

  // All-time data
  const [allTimeData,   setAllTimeData]   = useState<{ members: AllTimeMember[]; myEntry: AllTimeMember | null } | null>(null);
  const [allTimeLoaded, setAllTimeLoaded] = useState(false);

  // Promotion / demotion
  const [showPromo,  setShowPromo]  = useState(false);
  const [showDemote, setShowDemote] = useState(false);
  const [promoInfo,  setPromoInfo]  = useState<{ from: string; to: string; myRank: number | null } | null>(null);

  // Sticky my-rank bar
  const [myRowVisible, setMyRowVisible] = useState(true);
  const myRowRef = useRef<HTMLDivElement | null>(null);

  // Is the student on free plan (simplified: check localStorage flag, default true)
  const [isFree, setIsFree] = useState(true);

  // ── Load student + this-week league ─────────────────────────────────────
  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setStudentId(id);

    // Check subscription (simplified: if subscription stored, not free)
    const sub = localStorage.getItem('mathspark_subscription_tier');
    setIsFree(!sub || sub === 'free');

    fetch(`/api/leaderboard?studentId=${id}`)
      .then((r) => r.json())
      .then((d: LeagueData) => { setLeagueData(d); setWeekLoading(false); })
      .catch(() => setWeekLoading(false));
  }, [router]);

  // ── Check for promotion / demotion from last week ────────────────────────
  useEffect(() => {
    if (!studentId) return;

    fetch(`/api/leaderboard/last-week?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d: LastWeekResult) => {
        setLastWeekData(d);
        setLastWeekLoaded(true);

        if (d.promoted && d.myPromotion) {
          const key = `leaderboard_promo_seen_${d.league?.weekStart ?? 'prev'}`;
          if (!localStorage.getItem(key)) {
            setPromoInfo({ from: d.myPromotion.from, to: d.myPromotion.to, myRank: d.myRank });
            setShowPromo(true);
          }
        } else if (d.demoted) {
          const key = `leaderboard_demote_seen_${d.league?.weekStart ?? 'prev'}`;
          if (!localStorage.getItem(key)) {
            setShowDemote(true);
          }
        }
      })
      .catch(() => setLastWeekLoaded(true));
  }, [studentId]);

  // ── Load all-time on first tap ────────────────────────────────────────────
  const loadAllTime = useCallback(() => {
    if (!studentId || allTimeLoaded) return;
    fetch(`/api/leaderboard/all-time?studentId=${studentId}`)
      .then((r) => r.json())
      .then((d) => { setAllTimeData(d); setAllTimeLoaded(true); })
      .catch(() => setAllTimeLoaded(true));
  }, [studentId, allTimeLoaded]);

  // ── IntersectionObserver for my-rank row ──────────────────────────────────
  useEffect(() => {
    if (!myRowRef.current) return;
    const obs = new IntersectionObserver(
      ([entry]) => setMyRowVisible(entry.isIntersecting),
      { threshold: 0.5 },
    );
    obs.observe(myRowRef.current);
    return () => obs.disconnect();
  }, [leagueData]); // re-run when leagueData loads

  function dismissPromo() {
    const key = `leaderboard_promo_seen_${lastWeekData?.league?.weekStart ?? 'prev'}`;
    localStorage.setItem(key, '1');
    setShowPromo(false);
  }

  function dismissDemote() {
    const key = `leaderboard_demote_seen_${lastWeekData?.league?.weekStart ?? 'prev'}`;
    localStorage.setItem(key, '1');
    setShowDemote(false);
  }

  const myMember = leagueData?.members.find((m) => m.isMe) ?? null;

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">

      {/* ── Promotion overlay ──────────────────────────────────────────── */}
      {showPromo && promoInfo && (
        <PromotionOverlay
          from={promoInfo.from}
          to={promoInfo.to}
          myRank={promoInfo.myRank}
          onDismiss={dismissPromo}
        />
      )}

      {/* ── Demotion banner ────────────────────────────────────────────── */}
      {showDemote && leagueData && (
        <DemotionBanner tier={leagueData.tier} onDismiss={dismissDemote} />
      )}

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="bg-duo-dark pt-10 pb-4 px-4">
        <h1 className="text-2xl font-extrabold text-white">🏆 League</h1>
        <p className="text-white/60 text-sm font-semibold mt-0.5">
          Compete with students around you — earn XP, get promoted!
        </p>
      </div>

      {/* ── Status card ────────────────────────────────────────────────── */}
      <div className="mt-4 mb-4">
        <StatusCard league={leagueData} isLoading={weekLoading} />
      </div>

      {/* ── Tab bar ────────────────────────────────────────────────────── */}
      <div className="flex mx-4 gap-1 bg-gray-100 rounded-2xl p-1 mb-2">
        {([
          { id: 'week', label: 'This Week' },
          { id: 'last', label: 'Last Week' },
          { id: 'all',  label: 'All Time'  },
        ] as const).map(({ id, label }) => (
          <button
            key={id}
            onClick={() => {
              setTab(id);
              if (id === 'all') loadAllTime();
            }}
            style={{ minHeight: 0 }}
            className={`flex-1 rounded-xl py-2 text-xs font-extrabold transition-colors ${
              tab === id
                ? 'bg-white text-gray-800 shadow-sm'
                : 'text-gray-400 hover:text-gray-600'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* ── Tab content ────────────────────────────────────────────────── */}
      <div className="bg-white rounded-t-3xl overflow-hidden shadow-sm">

        {/* This Week */}
        {tab === 'week' && (
          <>
            {weekLoading ? (
              <div className="py-20 flex flex-col items-center gap-3">
                <div className="w-10 h-10 rounded-full border-4 border-duo-green border-t-transparent animate-spin" />
                <p className="text-gray-400 font-semibold text-sm">Loading your league…</p>
              </div>
            ) : !leagueData ? (
              <div className="py-20 text-center px-8">
                <p className="text-4xl mb-3">😕</p>
                <p className="font-extrabold text-gray-700">Couldn&apos;t load league</p>
                <p className="text-sm text-gray-400 mt-1">Try refreshing the page.</p>
              </div>
            ) : (
              <>
                {leagueData.members.map((m, idx) => (
                  <MemberRow
                    key={m.studentId}
                    member={m}
                    rank={m.rank}
                    total={leagueData.totalMembers}
                    promoteCount={leagueData.promoteCount}
                    demoteCount={leagueData.demoteCount}
                    isFree={isFree}
                    onClick={() => router.push(`/profile/${m.studentId}`)}
                    rowRef={m.isMe ? ((el) => { myRowRef.current = el; }) : undefined}
                  />
                ))}
                {isFree && leagueData.myRank > 5 && (
                  <FreeGate rank={leagueData.myRank} />
                )}
              </>
            )}
          </>
        )}

        {/* Last Week */}
        {tab === 'last' && (
          !lastWeekLoaded
            ? <div className="py-20 flex items-center justify-center"><div className="w-8 h-8 rounded-full border-4 border-duo-green border-t-transparent animate-spin" /></div>
            : <LastWeekTab data={lastWeekData} />
        )}

        {/* All Time */}
        {tab === 'all' && (
          <AllTimeTab data={allTimeData} isFree={isFree} myRank={leagueData?.myRank ?? 99} />
        )}
      </div>

      {/* ── Sticky my-rank bar ─────────────────────────────────────────── */}
      {tab === 'week' && (
        <StickyMyRankBar member={myMember} visible={!myRowVisible} />
      )}
    </div>
  );
}

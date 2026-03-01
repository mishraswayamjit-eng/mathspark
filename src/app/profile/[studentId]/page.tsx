'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import type { PublicProfile, WeeklyAwardData } from '@/types';

// ── Tier metadata ─────────────────────────────────────────────────────────────

const TIER_NAMES: Record<number, string> = {
  1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Diamond', 5: 'Champion',
};

const TIER_BADGE: Record<number, string> = {
  1: '🥉', 2: '🥈', 3: '🥇', 4: '💎', 5: '👑',
};

// ── Award icons + names ───────────────────────────────────────────────────────

const AWARD_META: Record<string, { icon: string; name: string }> = {
  most_improved: { icon: '📈', name: 'Most Improved' },
  speed_demon:   { icon: '⚡', name: 'Speed Demon'   },
  accuracy_king: { icon: '🎯', name: 'Accuracy King' },
  explorer:      { icon: '🗺️', name: 'Explorer'      },
};

// ── Stat tile ─────────────────────────────────────────────────────────────────

function StatTile({ emoji, label, value, color }: {
  emoji: string; label: string; value: string | number; color: string;
}) {
  return (
    <div className="bg-gray-50 rounded-2xl p-3 border border-gray-100 text-center">
      <span className="text-2xl">{emoji}</span>
      <p className="text-xl font-extrabold mt-1" style={{ color }}>{value}</p>
      <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-0.5">{label}</p>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PublicProfilePage() {
  const params    = useParams();
  const router    = useRouter();
  const targetId  = params?.studentId as string;

  const [profile,  setProfile]  = useState<PublicProfile | null>(null);
  const [loading,  setLoading]  = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [isMe,     setIsMe]     = useState(false);

  useEffect(() => {
    const myId = localStorage.getItem('mathspark_student_id');
    setIsMe(myId === targetId);

    if (!targetId) { setNotFound(true); setLoading(false); return; }

    fetch(`/api/profile/${targetId}`)
      .then((r) => {
        if (r.status === 404) { setNotFound(true); setLoading(false); return null; }
        return r.json();
      })
      .then((d: PublicProfile | null) => {
        if (d) setProfile(d);
        setLoading(false);
      })
      .catch(() => { setNotFound(true); setLoading(false); });
  }, [targetId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 animate-pulse">
        <div className="bg-[#131F24] pt-10 pb-8 px-4">
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 rounded-full bg-white/20" />
            <div className="flex-1 space-y-2">
              <div className="h-6 bg-white/20 rounded-xl w-32" />
              <div className="h-4 bg-white/10 rounded-xl w-24" />
            </div>
          </div>
        </div>
        <div className="m-4 grid grid-cols-2 gap-3">
          {[0,1,2,3].map((i) => <div key={i} className="h-24 bg-gray-200 rounded-2xl" />)}
        </div>
      </div>
    );
  }

  if (notFound || !profile) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center gap-4 px-8 text-center">
        <p className="text-5xl">🔒</p>
        <h2 className="font-extrabold text-gray-800 text-lg">Profile not found</h2>
        <p className="text-gray-400 text-sm font-medium">
          This student has hidden their profile or it doesn&apos;t exist.
        </p>
        <button
          onClick={() => router.back()}
          className="mt-2 bg-[#1CB0F6] text-white font-extrabold rounded-2xl px-6 py-3 active:scale-95 transition-transform"
          style={{ minHeight: 48 }}
        >
          ← Go back
        </button>
      </div>
    );
  }

  const { displayName, avatarColor, currentLeagueTier, totalLifetimeXP, totalSolved, topicsMastered, currentStreak, joinedAt, awards } = profile;
  const initial = displayName ? displayName[0].toUpperCase() : '?';
  const tierName  = TIER_NAMES[currentLeagueTier] ?? 'Bronze';
  const tierBadge = TIER_BADGE[currentLeagueTier] ?? '🥉';
  const joined    = new Date(joinedAt).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });

  return (
    <div className="min-h-screen bg-gray-50 pb-8 animate-fade-in">

      {/* ── Back button ─────────────────────────────────────────────────── */}
      <div className="absolute top-4 left-4 z-10">
        <button
          onClick={() => router.back()}
          className="bg-white/90 backdrop-blur rounded-full px-3 py-2 font-bold text-sm text-gray-600 shadow active:scale-95 transition-transform"
          style={{ minHeight: 0 }}
        >
          ← Back
        </button>
      </div>

      {/* ── Profile header ──────────────────────────────────────────────── */}
      <div className="bg-[#131F24] pt-16 pb-8 px-4 text-center">
        <div
          className="w-24 h-24 rounded-full flex items-center justify-center text-3xl font-extrabold text-white border-4 border-white/30 shadow-xl mx-auto mb-3"
          style={{ backgroundColor: avatarColor }}
        >
          {initial}
        </div>
        <h1 className="text-2xl font-extrabold text-white">{displayName}</h1>
        <div className="flex items-center justify-center gap-2 mt-1">
          <span className="text-lg">{tierBadge}</span>
          <span className="text-white/70 font-semibold text-sm">{tierName} League</span>
        </div>
        <p className="text-white/40 text-xs font-medium mt-1">Member since {joined}</p>
        {isMe && (
          <Link
            href="/profile"
            className="mt-3 inline-block bg-white/15 hover:bg-white/25 text-white text-xs font-bold rounded-full px-4 py-1.5 transition-colors"
          >
            ✏️ Edit your profile
          </Link>
        )}
      </div>

      {/* ── Stats grid ──────────────────────────────────────────────────── */}
      <div className="bg-white px-4 py-5 border-b border-gray-100">
        <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">Stats</h2>
        <div className="grid grid-cols-2 gap-3">
          <StatTile emoji="💎"  label="Lifetime XP"     value={totalLifetimeXP.toLocaleString()} color="#9B59B6" />
          <StatTile emoji="✅"  label="Questions Solved" value={totalSolved}                      color="#58CC02" />
          <StatTile emoji="⭐"  label="Topics Mastered"  value={topicsMastered}                   color="#FFC800" />
          <StatTile emoji="🔥"  label="Day Streak"       value={currentStreak}                    color="#FF9600" />
        </div>
      </div>

      {/* ── Awards ──────────────────────────────────────────────────────── */}
      {awards.length > 0 && (
        <div className="bg-white px-4 py-5 mt-2 border-b border-gray-100">
          <h2 className="text-[10px] font-extrabold text-gray-400 uppercase tracking-widest mb-3">Recent Awards</h2>
          <div className="space-y-2">
            {awards.map((a: WeeklyAwardData, i: number) => {
              const meta = AWARD_META[a.awardType] ?? { icon: '🏅', name: a.awardType };
              return (
                <div key={i} className="flex items-center gap-3 bg-yellow-50 border border-yellow-100 rounded-2xl px-3 py-2.5">
                  <span className="text-2xl">{meta.icon}</span>
                  <div>
                    <p className="font-extrabold text-gray-800 text-sm">{meta.name}</p>
                    <p className="text-xs text-gray-400 font-medium">{a.value}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Report / flag section ────────────────────────────────────────── */}
      {!isMe && (
        <div className="px-4 pt-6 text-center">
          <a
            href={`mailto:admin@mathspark.in?subject=Report profile ${targetId}&body=I want to report this profile for the following reason:`}
            className="text-xs text-gray-400 font-medium underline"
          >
            🚩 Report this profile
          </a>
        </div>
      )}
    </div>
  );
}

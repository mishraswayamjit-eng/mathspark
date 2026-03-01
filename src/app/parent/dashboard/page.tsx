'use client';

import { useEffect, useState } from 'react';
import { useSession, signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { isUnlimitedPlan } from '@/lib/usageLimits';

interface Child {
  id:                      string;
  name:                    string;
  grade:                   number;
  subscriptionId:          string | null;
  dailyUsageMinutes:       number;
  lastActiveDate:          string | null;
  aiChatMessagesUsedToday: number;
  subscription:            { name: string; tier: number; dailyLimitMinutes: number; aiChatDailyLimit: number } | null;
}

function PlanBadge({ sub }: { sub: Child['subscription'] }) {
  if (!sub) return <span className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full font-semibold">No plan</span>;
  const colors = ['', 'bg-green-100 text-green-700', 'bg-blue-100 text-blue-700', 'bg-purple-100 text-purple-700'];
  return <span className={`text-xs ${colors[sub.tier] ?? colors[1]} px-2 py-0.5 rounded-full font-semibold`}>{sub.name}</span>;
}

export default function ParentDashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [children, setChildren] = useState<Child[]>([]);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    if (status === 'unauthenticated') router.replace('/auth/login');
  }, [status, router]);

  useEffect(() => {
    if (status !== 'authenticated') return;
    fetch('/api/parent/children')
      .then((r) => r.json())
      .then((d) => { setChildren(d.children ?? []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [status]);

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-[#131F24] flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-[#58CC02] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  function loginAsChild(childId: string, childName: string) {
    localStorage.setItem('mathspark_student_id',   childId);
    localStorage.setItem('mathspark_student_name', childName);
    router.push('/chapters');
  }

  return (
    <div className="min-h-screen bg-[#131F24] pb-16">
      {/* Header */}
      <div className="px-4 pt-10 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-white/50 text-xs font-semibold uppercase tracking-widest">Parent Dashboard</p>
            <h1 className="text-2xl font-extrabold text-white mt-0.5">
              Hi, {session?.user?.name?.split(' ')[0]} 👋
            </h1>
          </div>
          <button
            onClick={() => signOut({ callbackUrl: '/auth/login' })}
            className="text-white/40 text-xs font-semibold hover:text-white/70 transition-colors border border-white/10 rounded-xl px-3 py-2"
          >
            Sign out
          </button>
        </div>
      </div>

      {/* Children */}
      <div className="px-4 mt-2">
        <div className="flex items-center justify-between mb-3">
          <p className="text-xs font-extrabold text-white/40 uppercase tracking-widest">Your children</p>
          <Link
            href="/parent/add-child"
            className="text-[#58CC02] text-sm font-extrabold hover:text-[#46a302] transition-colors"
          >
            + Add child
          </Link>
        </div>

        {children.length === 0 ? (
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 text-center">
            <div className="text-4xl mb-3">👦</div>
            <p className="text-white font-semibold">No children yet</p>
            <p className="text-white/40 text-sm mt-1 mb-4">Add your child to get started</p>
            <Link
              href="/parent/add-child"
              className="inline-block bg-[#58CC02] hover:bg-[#46a302] text-white font-extrabold px-6 py-3 rounded-2xl transition-colors"
            >
              Add a child →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {children.map((child) => {
              const limit      = child.subscription?.dailyLimitMinutes ?? 60;
              const unlimited  = isUnlimitedPlan(limit);
              const usedPct    = unlimited ? 100 : Math.min(100, Math.round((child.dailyUsageMinutes / limit) * 100));
              const lastActive = child.lastActiveDate
                ? new Date(child.lastActiveDate).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
                : 'Never';

              return (
                <div key={child.id} className="bg-white/5 border border-white/10 rounded-2xl p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-white font-extrabold text-base">{child.name}</span>
                        <PlanBadge sub={child.subscription} />
                      </div>
                      <p className="text-white/40 text-xs">Grade {child.grade} · Last active: {lastActive}</p>

                      {/* Daily usage bar */}
                      <div className="mt-3">
                        <div className="flex justify-between text-xs text-white/40 mb-1">
                          <span>Today&apos;s usage</span>
                          {unlimited
                            ? <span className="text-[#58CC02] font-extrabold">Unlimited ♾️</span>
                            : <span>{child.dailyUsageMinutes} / {limit} min</span>
                          }
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-1.5">
                          <div
                            className={`h-1.5 rounded-full transition-all ${unlimited ? 'bg-[#58CC02]' : usedPct >= 100 ? 'bg-[#FF4B4B]' : usedPct >= 75 ? 'bg-[#FF9600]' : 'bg-[#58CC02]'}`}
                            style={{ width: unlimited ? '100%' : `${usedPct}%` }}
                          />
                        </div>
                      </div>

                      <p className="text-white/40 text-xs mt-2">
                        AI chats today: {child.aiChatMessagesUsedToday} / {child.subscription?.aiChatDailyLimit ?? 5}
                      </p>
                    </div>

                    <button
                      onClick={() => loginAsChild(child.id, child.name)}
                      className="bg-[#58CC02] hover:bg-[#46a302] text-white text-xs font-extrabold px-3 py-2 rounded-xl transition-colors whitespace-nowrap"
                    >
                      Practice →
                    </button>
                  </div>

                  {!child.subscriptionId && (
                    <div className="mt-3 border-t border-white/10 pt-3">
                      <Link
                        href="/pricing"
                        className="block w-full text-center bg-[#FF9600]/20 border border-[#FF9600]/40 text-[#FF9600] text-xs font-extrabold py-2 rounded-xl hover:bg-[#FF9600]/30 transition-colors"
                      >
                        ⚡ Subscribe to unlock full access →
                      </Link>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Quick links */}
      <div className="px-4 mt-6 space-y-2">
        <Link
          href="/pricing"
          className="block w-full bg-white/5 border border-white/10 rounded-2xl p-4 flex items-center gap-3 hover:bg-white/10 transition-colors"
        >
          <span className="text-2xl">💳</span>
          <div>
            <p className="text-white font-extrabold text-sm">View Plans & Pricing</p>
            <p className="text-white/40 text-xs">Starter ₹500/mo · Advanced ₹1,500/mo · Unlimited ₹5,000/mo</p>
          </div>
          <span className="text-white/40 ml-auto">→</span>
        </Link>
      </div>
    </div>
  );
}

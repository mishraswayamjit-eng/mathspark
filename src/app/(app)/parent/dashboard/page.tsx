'use client';

import { useEffect, useState } from 'react';
import { logError } from '@/lib/logger';
import { useSession, signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { isUnlimitedPlan } from '@/lib/usageLimits';
import { MONETIZATION_ENABLED } from '@/lib/monetization';

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
  if (!sub) return <span className="text-xs bg-soft text-ink-muted border-2 border-line px-2 py-0.5 rounded-full font-semibold">No plan</span>;
  const colors: Record<number, string> = {
    1: 'bg-soft text-ink',
    2: 'bg-soft text-ink',
    3: 'bg-soft text-ink',
    4: 'bg-soft text-ink',
    5: 'bg-soft text-ink',
  };
  return <span className={`text-xs ${colors[sub.tier] ?? 'bg-soft text-ink-muted'} border-2 border-line px-2 py-0.5 rounded-full font-semibold`}>{sub.name}</span>;
}

export default function ParentDashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [children, setChildren] = useState<Child[]>([]);
  const [loading,  setLoading]  = useState(true);
  const [confirmId, setConfirmId] = useState<string | null>(null);
  const [busyId,    setBusyId]    = useState<string | null>(null);
  const [removeError, setRemoveError] = useState<string | null>(null);

  useEffect(() => {
    if (status === 'unauthenticated') router.replace('/auth/login');
  }, [status, router]);

  useEffect(() => {
    if (status !== 'authenticated') return;
    fetch('/api/parent/children')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d) => { setChildren(d.children ?? []); setLoading(false); })
      .catch((err) => { logError('[parent/dashboard] fetch children', err); setLoading(false); });
  }, [status]);

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-paper flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-action border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  async function removeChild(childId: string) {
    setBusyId(childId);
    setRemoveError(null);
    try {
      const res = await fetch(`/api/parent/children/${childId}`, { method: 'DELETE' });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.error ?? 'Could not remove child. Please try again.');
      }
      setChildren((prev) => prev.filter((c) => c.id !== childId));
      setConfirmId(null);
    } catch (err) {
      logError('[parent/dashboard] remove child', err);
      setRemoveError(err instanceof Error ? err.message : 'Could not remove child. Please try again.');
    } finally {
      setBusyId(null);
    }
  }

  async function loginAsChild(childId: string, childName: string, childGrade: number) {
    // Set httpOnly cookie for API auth
    await fetch('/api/student/session', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ studentId: childId }),
    });
    // Keep localStorage for UI display only
    localStorage.setItem('mathspark_student_id',    childId);
    localStorage.setItem('mathspark_student_name',  childName);
    localStorage.setItem('mathspark_student_grade', String(childGrade));
    router.push('/home');
  }

  return (
    <div className="min-h-screen bg-paper pb-16">
      {/* Header */}
      <div className="px-4 pt-10 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-ink-muted text-xs font-semibold">Parent Dashboard</p>
            <h1 className="text-2xl font-extrabold text-ink mt-0.5">
              Hi, {session?.user?.name?.split(' ')[0]} 👋
            </h1>
          </div>
          <button
            onClick={() => signOut({ callbackUrl: '/auth/login' })}
            className="bg-white text-ink text-xs font-semibold hover:bg-soft transition-colors border-2 border-ink shadow-hard-sm rounded-control px-3 py-2"
          >
            Sign out
          </button>
        </div>
      </div>

      {/* Children */}
      <div className="px-4 mt-2">
        <div className="flex items-center justify-between mb-3">
          <p className="text-xs font-extrabold text-ink-muted">Your children</p>
          <Link
            href="/parent/add-child"
            className="text-action text-sm font-extrabold hover:text-action-dark transition-colors"
          >
            + Add child
          </Link>
        </div>

        {children.length === 0 ? (
          <div className="bg-white border-2 border-line rounded-card p-6 text-center">
            <div className="text-4xl mb-3">👦</div>
            <p className="text-ink font-semibold">No children yet</p>
            <p className="text-ink-muted text-sm mt-1 mb-4">Add your child to get started</p>
            <Link
              href="/parent/add-child"
              className="inline-block bg-action hover:bg-action-dark text-white font-extrabold px-6 py-3 rounded-control border-2 border-ink shadow-hard-sm transition-colors"
            >
              Add a child →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {children.map((child) => {
              const limit      = child.subscription?.dailyLimitMinutes ?? 60;
              const unlimited  = !MONETIZATION_ENABLED || isUnlimitedPlan(limit);
              const usedPct    = unlimited ? 100 : Math.min(100, Math.round((child.dailyUsageMinutes / limit) * 100));
              const lastActive = child.lastActiveDate
                ? new Date(child.lastActiveDate).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
                : 'Never';

              return (
                <div key={child.id} className="bg-white border-2 border-line rounded-card p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-ink font-extrabold text-base">{child.name}</span>
                        {MONETIZATION_ENABLED && <PlanBadge sub={child.subscription} />}
                      </div>
                      <p className="text-ink-muted text-xs">Grade {child.grade} · Last active: {lastActive}</p>

                      {/* Daily usage bar */}
                      <div className="mt-3">
                        <div className="flex justify-between text-xs text-ink-muted mb-1">
                          <span>Today&apos;s usage</span>
                          {unlimited
                            ? <span className="text-success font-extrabold">Unlimited ♾️</span>
                            : <span>{child.dailyUsageMinutes} / {limit} min</span>
                          }
                        </div>
                        <div className="w-full bg-soft rounded-full h-1.5">
                          <div
                            className={`h-1.5 rounded-full transition-[width] ${unlimited ? 'bg-action' : usedPct >= 100 ? 'bg-retry' : usedPct >= 75 ? 'bg-star' : 'bg-action'}`}
                            style={{ width: unlimited ? '100%' : `${usedPct}%` }}
                          />
                        </div>
                      </div>

                      {MONETIZATION_ENABLED && (
                        <p className="text-ink-muted text-xs mt-2">
                          AI chats today: {child.aiChatMessagesUsedToday} / {child.subscription?.aiChatDailyLimit ?? 5}
                        </p>
                      )}
                    </div>

                    <button
                      onClick={() => loginAsChild(child.id, child.name, child.grade)}
                      disabled={busyId === child.id}
                      className="bg-action hover:bg-action-dark text-white text-xs font-extrabold px-3 py-2 rounded-control border-2 border-ink shadow-hard-sm transition-colors whitespace-nowrap disabled:opacity-50"
                    >
                      Practice →
                    </button>
                  </div>

                  {MONETIZATION_ENABLED && !child.subscriptionId && (
                    <div className="mt-3 border-t-2 border-line pt-3">
                      <Link
                        href="/pricing"
                        className="block w-full text-center bg-hint border-2 border-hint-ink text-hint-ink text-xs font-extrabold py-2 rounded-control hover:border-ink transition-colors"
                      >
                        ⚡ Subscribe to unlock full access →
                      </Link>
                    </div>
                  )}

                  <div className="mt-3 flex flex-col items-end gap-1">
                    {confirmId === child.id ? (
                      <div className="flex items-center gap-2">
                        <span className="text-ink-muted text-xs">Remove {child.name}?</span>
                        <button
                          onClick={() => removeChild(child.id)}
                          disabled={busyId === child.id}
                          aria-label={`Confirm remove ${child.name}`}
                          className="text-retry text-xs font-extrabold px-3 min-h-[48px] rounded-control hover:bg-retry-soft transition-colors disabled:opacity-50"
                        >
                          {busyId === child.id ? 'Removing…' : 'Yes, remove'}
                        </button>
                        <button
                          onClick={() => { setConfirmId(null); setRemoveError(null); }}
                          disabled={busyId === child.id}
                          className="text-ink-muted text-xs font-semibold px-3 min-h-[48px] rounded-control hover:text-ink transition-colors disabled:opacity-50"
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => { setConfirmId(child.id); setRemoveError(null); }}
                        aria-label={`Remove ${child.name}`}
                        className="text-ink-muted text-xs font-semibold min-h-[48px] px-2 hover:text-retry transition-colors"
                      >
                        Remove
                      </button>
                    )}
                    {confirmId === child.id && removeError && (
                      <p className="text-retry text-xs font-semibold">{removeError}</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Quick links */}
      {MONETIZATION_ENABLED && (
        <div className="px-4 mt-6 space-y-2">
          <Link
            href="/pricing"
            className="block w-full bg-white border-2 border-line rounded-card p-4 flex items-center gap-3 hover:border-ink transition-colors"
          >
            <span className="text-2xl">💳</span>
            <div>
              <p className="text-ink font-extrabold text-sm">View Plans & Pricing</p>
              <p className="text-ink-muted text-xs">Starter ₹500/mo · Advanced ₹1,500/mo · Unlimited ₹5,000/mo</p>
            </div>
            <span className="text-ink-muted ml-auto">→</span>
          </Link>
        </div>
      )}
    </div>
  );
}

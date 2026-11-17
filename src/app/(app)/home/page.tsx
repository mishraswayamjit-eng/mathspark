import Link from 'next/link';
import Sparky from '@/components/Sparky';
import AvatarLink from '@/components/shell/AvatarLink';
import TodayPlan from '@/components/home/TodayPlan';
import type { PlanRow } from '@/components/home/TodayPlan';
import MilestoneCard from '@/components/home/MilestoneCard';
import HomeSignedOut from '@/components/home/HomeSignedOut';
import HomeRetry from '@/components/home/HomeRetry';
import NextActionCard from '@/components/home/NextActionCard';
import NudgeStrip from '@/components/home/NudgeStrip';
import HomeRefresher from '@/components/home/HomeRefresher';
import { getNextActions } from '@/lib/brain/nextAction';
import type { NextAction } from '@/lib/brain/nextAction';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { loadHomeData } from '@/lib/student/homeData';
import type { HomeData } from '@/lib/student/homeData';
import {
  greetingForIndia,
  isAppPath,
  isRecentWin,
  pickContinueTopic,
  pickDisplayTopics,
  reframePlanReason,
} from '@/lib/student/homeView';
import type { ContinueTopic } from '@/lib/student/homeView';
import { STREAK_MILESTONES } from '@/lib/flashcardXP';
import { logError } from '@/lib/logger';
import type { TopicMasteryEntry } from '@/lib/brain/engine';

// Home ("Today") is rendered on the server with the child's data in the first
// response. It reads the session cookie, so it is per request and the response
// is private and never stored (Next sends `private, no-cache, no-store` for it).
export const dynamic = 'force-dynamic';
// NOTE: maxDuration is ignored on Vercel Hobby (10s hard limit). Only effective on Pro+.
export const maxDuration = 30;

const LEAGUE_EMOJI: Record<number, string> = { 1: '🥉', 2: '🥈', 3: '🥇', 4: '💎', 5: '👑' };

// Runs before first paint on a full page load. Plan ticks and the "milestone
// put away" choice live in localStorage, which the server cannot see; this
// applies them to the server-rendered HTML so nothing visibly swaps when React
// starts. On in-app navigation the client components do the same in a layout
// effect. Keys match TodayPlan.tsx and MilestoneCard.tsx.
const RESTORE_SCRIPT = `(function(){try{
var d=new Date().toDateString();
var done=JSON.parse(localStorage.getItem('mathspark_plan_done_'+d)||'[]');
if(!(done instanceof Array)){done=[];}
var rows=document.querySelectorAll('[data-plan-id]');
var n=0;
for(var i=0;i<rows.length;i++){
if(done.indexOf(rows[i].getAttribute('data-plan-id'))!==-1){rows[i].setAttribute('data-done','true');n++;}
}
var c=document.querySelector('[data-plan-count]');
if(c&&rows.length){c.textContent=n+'/'+rows.length+' done';}
var a=document.querySelector('[data-plan-alldone]');
if(a&&rows.length&&n>=rows.length){a.removeAttribute('hidden');}
if(localStorage.getItem('mathspark_milestone_'+d)==='true'){
var m=document.querySelector('[data-milestone]');
if(m){m.setAttribute('hidden','');}
}
}catch(e){}})();`;

// ── Server-rendered pieces ────────────────────────────────────────────────────

function StatsBar({ data }: { data: HomeData }) {
  const leagueEmoji = LEAGUE_EMOJI[data.leagueTier] ?? '🥉';
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <div className="flex items-center gap-1.5 bg-card rounded-tile px-3 py-1.5 border-2 border-line">
        <span className="text-sm" aria-hidden="true">🔥</span>
        {data.streak > 0 ? (
          <span className="text-sm font-extrabold text-ink">
            {data.streak}
            <span className="sr-only">{data.streak === 1 ? ' day streak' : ' days streak'}</span>
          </span>
        ) : (
          <span className="text-sm font-extrabold text-ink">
            <span aria-hidden="true">—</span>
            <span className="sr-only">No streak yet</span>
          </span>
        )}
      </div>
      <div className="flex items-center gap-1.5 bg-card rounded-tile px-3 py-1.5 border-2 border-line">
        <span className="text-sm" aria-hidden="true">⭐</span>
        <span className="text-sm font-extrabold text-ink">{`${data.todayXP} XP`}</span>
      </div>
      <Link
        href="/leaderboard"
        className="flex items-center gap-1.5 bg-card rounded-tile px-3 py-1.5 border-2 border-line"
      >
        <span className="text-sm" aria-hidden="true">{leagueEmoji}</span>
        <span className="text-sm font-extrabold text-ink">
          {`${data.leagueName}${data.leagueRank ? ` #${data.leagueRank}` : ''}`}
        </span>
      </Link>
    </div>
  );
}

function HeroCard({ continueTopic }: { continueTopic: ContinueTopic | null }) {
  if (continueTopic) {
    return (
      <Link href={continueTopic.url} className="block ui-card ui-card-pop border-l-[10px] border-l-action">
        <div className="flex items-center gap-3 min-h-[48px]">
          <span className="text-2xl shrink-0" aria-hidden="true">{continueTopic.emoji}</span>
          <div className="flex-1 min-w-0">
            <p className="font-extrabold text-ink text-[15px] truncate">Continue: {continueTopic.topicName}</p>
            <p className="text-xs text-ink-muted font-medium truncate">{continueTopic.reason}</p>
          </div>
          <span className="text-action font-extrabold text-sm shrink-0">Go →</span>
        </div>
      </Link>
    );
  }

  // Nothing practised yet: welcome.
  return (
    <Link href="/chapters" className="block ui-card ui-card-pop border-l-[10px] border-l-action">
      <div className="flex items-center gap-3 min-h-[48px]">
        <div className="shrink-0">
          <Sparky mood="happy" size={48} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-ink text-[15px]">Welcome to MathSpark!</p>
          <p className="text-xs text-ink-muted font-medium">Start your math journey today</p>
        </div>
        <span className="text-action font-extrabold text-sm shrink-0">Start →</span>
      </div>
    </Link>
  );
}

function TopicBar({ entry }: { entry: TopicMasteryEntry }) {
  const pct = Math.round(entry.mastery * 100);
  const barColor = pct >= 70 ? '#12805c' : pct >= 40 ? '#f5a400' : pct > 0 ? '#c62f3d' : '#d3deee';
  // Amber and the empty-state grey are too pale to read as text; use ink tones there.
  const textColor = pct >= 70 ? '#12805c' : pct >= 40 ? '#5a4300' : pct > 0 ? '#c62f3d' : '#47557a';
  return (
    <div className="flex items-center gap-3 py-1.5">
      <span className="text-base shrink-0 w-6 text-center" aria-hidden="true">{entry.emoji}</span>
      <span className="text-xs font-semibold text-ink w-28 truncate">{entry.topicName}</span>
      <div className="flex-1 h-2 bg-soft rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: barColor }} />
      </div>
      <span className="text-xs font-extrabold w-9 text-right" style={{ color: textColor }}>
        {`${pct}%`}
      </span>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default async function HomePage() {
  // No child session on the server. A tiny client component decides between
  // /student/login (this device has been signed in before) and /start (new
  // visitor), because only the browser can tell those apart.
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) return <HomeSignedOut />;

  let data: HomeData | null = null;
  let actions: NextAction[] = [];
  let loadFailed = false;
  try {
    // One after the other, on purpose. `loadHomeData` brings the stored
    // analytics up to date (the child may just have practised); the suggestion
    // reads those analytics, so it must not start before they are written.
    // Side by side, the card was always one visit behind Today's Plan.
    data = await loadHomeData(studentId);
    if (data) {
      // The suggestion is an extra: if it cannot be worked out, Home still shows.
      actions = await getNextActions(studentId, { limit: 3 }).catch((err) => {
        logError('[home] could not work out the next action', err);
        return [] as NextAction[];
      });
    }
  } catch (err) {
    logError('[home] could not load home data', err);
    loadFailed = true;
  }
  if (loadFailed) return <HomeRetry />;
  // A valid cookie for a student who no longer exists: treat as signed out.
  if (!data) return <HomeSignedOut />;

  const { student, streak, todayCorrect } = data;
  const recentActivity = Array.isArray(data.recentActivity) ? data.recentActivity : [];
  const greeting = greetingForIndia(new Date());
  const surfaceNarration =
    data.surfacePlan && typeof data.surfacePlan.narration === 'string' && data.surfacePlan.narration.trim()
      ? data.surfacePlan.narration.trim()
      : null;

  const continueTopic = pickContinueTopic(data);
  const displayTopics = pickDisplayTopics(data);

  // Only on the day the milestone is reached: the streak now carries over to the
  // next morning, and yesterday's milestone must not be cheered a second time.
  const milestone = data.practisedToday
    ? STREAK_MILESTONES.find((m) => m.days === streak) ?? null
    : null;

  const recentWin = recentActivity[0];
  const showRecentWin = !!recentWin && recentWin.pct >= 85 && isRecentWin(recentWin.timeAgo);

  // Today's plan: at most three items, with links that stay inside the app.
  const planRows: PlanRow[] = (Array.isArray(data.dailyPlan) ? data.dailyPlan : [])
    .slice(0, 3)
    .map((item) => ({
      // What the row is ABOUT, not its place in the list: after practice the
      // plan is worked out again, and a tick must not move on to a new topic
      // that happens to take the same place.
      id: typeof item.topicId === 'string' && item.topicId
        ? `${String(item.type ?? 'practice')}:${item.topicId}`
        : String(item.id),
      action: String(item.action ?? ''),
      type: String(item.type ?? 'practice'),
      targetUrl: isAppPath(item.targetUrl) ? item.targetUrl : '/chapters',
      reason: reframePlanReason(String(item.reason ?? '')),
      estimatedMins: Number(item.estimatedMins) || 0,
    }));

  return (
    <div className="min-h-screen bg-paper pb-24">

      {/* ── STICKY HEADER: greeting + avatar ──────────────────────────── */}
      <header className="sticky top-0 z-40 bg-ink px-4 py-2 flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-white font-display text-title leading-tight truncate">
            {greeting}, {student.name}! <span aria-hidden="true">🌟</span>
          </h1>
          <p className="text-white/70 text-xs font-bold truncate">
            {`Grade ${student.grade}`}
            {streak > 0 && (
              <>
                {' · '}
                <span aria-hidden="true">🔥 </span>
                {`${streak} day streak`}
              </>
            )}
          </p>
        </div>
        <AvatarLink />
      </header>

      <div className="px-4 pt-4 space-y-4">

        {/* ── The one thing to do next, picked from the child's own practice ── */}
        <NextActionCard actions={actions} surface="home" />

        {/* ── Narration + stats ───────────────────────────────────────── */}
        <section className="space-y-2.5">
          <p className="text-ink-muted text-[15px] font-semibold">
            {surfaceNarration
              ?? `${todayCorrect > 0 ? `${todayCorrect} correct today · ` : ''}Ready to practice?`}
          </p>
          <StatsBar data={data} />
        </section>

        {/* ── Trial banner (if active) ────────────────────────────────── */}
        {student.trialActive && student.trialDaysLeft !== null && (
          <div className="bg-hint border-2 border-hint-ink rounded-card px-4 py-2.5 flex items-center justify-between">
            <div>
              <p className="text-hint-ink font-extrabold text-sm"><span aria-hidden="true">🎉 </span>Pro Trial Active</p>
              <p className="text-hint-ink text-xs font-medium">
                {`${student.trialDaysLeft} ${student.trialDaysLeft === 1 ? 'day' : 'days'} left`}
              </p>
            </div>
            <Link
              href="/pricing"
              className="text-xs font-extrabold text-ink bg-card border-2 border-ink rounded-full px-3 min-h-[48px] flex items-center"
            >
              Upgrade →
            </Link>
          </div>
        )}

        {/* ── Streak milestone (only on the day it is reached) ────────── */}
        {milestone && (
          <MilestoneCard
            emoji={milestone.emoji}
            title={milestone.title}
            description={milestone.description}
            streak={streak}
          />
        )}

        {/* ── Hero: continue where the child left off ─────────────────── */}
        {/* Only when there is no suggestion above, so the child is never offered the same thing twice. */}
        {actions.length === 0 && <HeroCard continueTopic={continueTopic} />}

        {/* ── Recent win (85%+ in the last 12 hours) ──────────────────── */}
        {showRecentWin && (
          <div className="ui-card border-l-[10px] border-l-success">
            <div className="flex items-center gap-3">
              <div className="shrink-0">
                <Sparky mood="happy" size={44} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-extrabold text-ink">
                  You aced {recentWin.topicName}! <span aria-hidden="true">🎉</span>
                </p>
                <p className="text-xs text-ink-muted font-medium">
                  {`${recentWin.correct}/${recentWin.attempted} correct · ${recentWin.pct}%`}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ── Today's Plan (max 3) + Daily Challenge ──────────────────── */}
        <TodayPlan items={planRows} />

        {/* ── One gentle nudge at most ────────────────────────────────── */}
        <NudgeStrip nudges={Array.isArray(data.nudges) ? data.nudges : []} />

        {/* ── Your Topics (3 bars + summary) ──────────────────────────── */}
        <section className="bg-card rounded-card p-4 border-2 border-line">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-title text-ink">Your Topics</h2>
            <Link href="/chapters" className="text-sm font-extrabold text-action min-h-[48px] flex items-center">
              See all →
            </Link>
          </div>

          {displayTopics.length === 0 ? (
            <p className="py-2 text-ink-muted text-sm font-medium">No practice yet. Start learning!</p>
          ) : (
            <>
              {displayTopics.map((entry) => (
                <TopicBar key={entry.topicId} entry={entry} />
              ))}
              <p className="text-xs font-medium text-ink-muted mt-2">
                {`${data.topicsExploredCount} of ${data.totalTopics} topics explored`}
                {data.topicsMasteredCount > 0 ? ` · ${data.topicsMasteredCount} mastered` : ''}
              </p>
            </>
          )}
        </section>

        {/* ── Recent Activity (3 items) ───────────────────────────────── */}
        {recentActivity.length > 0 && (
          <section className="bg-card rounded-card p-4 border-2 border-line">
            <h2 className="text-title text-ink mb-3">Recent Activity</h2>
            <div className="space-y-2.5">
              {recentActivity.slice(0, 3).map((act, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-tile bg-soft flex items-center justify-center text-sm shrink-0" aria-hidden="true">
                    📚
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-ink truncate">{act.topicName}</p>
                    <p className="text-xs text-ink-muted font-medium">{`${act.correct}/${act.attempted} correct`}</p>
                  </div>
                  <div className="text-right">
                    <p
                      className="text-sm font-extrabold"
                      style={{ color: act.pct >= 70 ? '#12805c' : act.pct >= 40 ? '#5a4300' : '#c62f3d' }}
                    >
                      {`${act.pct}%`}
                    </p>
                    <p className="text-xs text-ink-muted font-medium">{act.timeAgo}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

      </div>

      {/* Asks the server for this page again when the child comes back to an old copy of it. */}
      <HomeRefresher token={String(Date.now())} />

      {/* Restores localStorage-only state (plan ticks, milestone) before first paint. */}
      <script dangerouslySetInnerHTML={{ __html: RESTORE_SCRIPT }} />
    </div>
  );
}

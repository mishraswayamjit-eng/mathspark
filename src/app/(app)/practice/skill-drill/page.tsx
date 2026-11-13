'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

// ── Types ─────────────────────────────────────────────────────────────────────

interface LevelInfo {
  levelId: string;
  name: string;
  label: string;
  color: string;
  gradeRange: number[];
  sessionsAvailable: number;
}

interface TopicInfo {
  topicId: string;
  displayName: string;
  icon: string;
  description: string;
  levels: Record<string, LevelInfo>;
}

interface LevelMeta {
  label: string;
  emoji: string;
  description: string;
}

interface Meta {
  levelLabels: Record<string, LevelMeta>;
}

// ── Progress helpers ──────────────────────────────────────────────────────────

interface LevelProgress {
  bestScore: number;
  sessions: Record<string, number>; // sessionNumber → best score
  unlocked: boolean;
}

type DrillProgress = Record<string, Record<string, LevelProgress>>;

const STORAGE_KEY = 'mathspark_drill_progress';

function loadProgress(): DrillProgress {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw) as DrillProgress;
  } catch { /* ignore */ }
  return {};
}

function getTopicProgress(progress: DrillProgress, topicId: string): Record<string, LevelProgress> {
  return progress[topicId] ?? {};
}

function getHighestUnlockedLevel(topicLevels: Record<string, LevelProgress>): string {
  const levels = ['L1', 'L2', 'L3', 'L4', 'L5'];
  let highest = 'L1';
  for (const lvl of levels) {
    const lp = topicLevels[lvl];
    if (lp && lp.unlocked) highest = lvl;
  }
  return highest;
}

function getLevelStatus(topicLevels: Record<string, LevelProgress>, levelId: string): 'locked' | 'available' | 'started' | 'passed' | 'mastered' {
  const lp = topicLevels[levelId];
  if (!lp || !lp.unlocked) {
    // L1 is always unlocked
    if (levelId === 'L1') return 'available';
    return 'locked';
  }
  if (lp.bestScore >= 9) return 'mastered';
  if (lp.bestScore >= 7) return 'passed';
  if (Object.keys(lp.sessions).length > 0) return 'started';
  return 'available';
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SkillDrillTopicsPage() {
  const [topics, setTopics] = useState<Record<string, TopicInfo> | null>(null);
  const [meta, setMeta] = useState<Meta | null>(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState<DrillProgress>({});

  useEffect(() => {
    setProgress(loadProgress());

    const grade = localStorage.getItem('mathspark_student_grade') || '4';
    fetch(`/api/skill-drills?grade=${grade}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: { meta: Meta; topics: Record<string, TopicInfo> }) => {
        setMeta(d.meta);
        setTopics(d.topics);
      })
      .catch((err) => logError('[fetch]', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-paper pb-24">
        <div className="bg-ink px-4 py-4 flex items-center gap-3">
          <Link href="/home" className="text-white/70 hover:text-white text-sm">&larr;</Link>
          <h1 className="text-white text-title">Skill Drills</h1>
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-3">
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-24" />
          ))}
        </div>
      </div>
    );
  }

  if (!topics || !meta) {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center gap-4 px-6">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-ink-muted">Skill drills not available yet.</p>
        <Link href="/home" className="text-sm font-bold text-action underline">Go Home</Link>
      </div>
    );
  }

  const topicList = Object.values(topics);
  const levelLabels = meta.levelLabels;

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/home" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Skill Drills</h1>
          <p className="text-white/70 text-xs font-medium">{topicList.length} topics &middot; master step by step</p>
        </div>
        <span className="text-2xl">🎯</span>
      </div>

      {/* Intro */}
      <div className="max-w-lg mx-auto px-4 pt-5">
        <div className="bg-soft rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Master any topic, step by step!</p>
            <p className="text-xs font-semibold text-ink-muted mt-0.5">
              Each topic has 5 levels. Score 8/10 to unlock the next level. Score 9/10 for mastery!
            </p>
          </div>
        </div>

        {/* Level legend */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
          {['L1', 'L2', 'L3', 'L4', 'L5'].map((lvl) => {
            const ll = levelLabels[lvl];
            return (
              <div key={lvl} className="flex items-center gap-1 bg-white rounded-full px-2.5 py-1 border-2 border-line shrink-0">
                <span className="text-xs">{ll?.emoji}</span>
                <span className="text-xs font-bold text-ink-muted">{ll?.label}</span>
              </div>
            );
          })}
        </div>

        {/* Topic cards */}
        <div className="space-y-3">
          {topicList.map((topic) => {
            const tp = getTopicProgress(progress, topic.topicId);
            const highestLevel = getHighestUnlockedLevel(tp);
            const levels = ['L1', 'L2', 'L3', 'L4', 'L5'];

            // Count mastered and started levels
            const masteredCount = levels.filter((l) => getLevelStatus(tp, l) === 'mastered').length;
            const passedCount = levels.filter((l) => {
              const s = getLevelStatus(tp, l);
              return s === 'passed' || s === 'mastered';
            }).length;

            return (
              <Link
                key={topic.topicId}
                href={`/practice/skill-drill/${topic.topicId}/${highestLevel}`}
                className="block bg-white rounded-card p-4 border-2 border-line hover:border-ink transition-[border-color,transform] active:scale-[0.98]"
              >
                <div className="flex items-start gap-3">
                  {/* Icon */}
                  <div className="text-3xl shrink-0 mt-0.5">{topic.icon}</div>

                  <div className="flex-1 min-w-0">
                    {/* Title + description */}
                    <h3 className="font-extrabold text-ink text-sm leading-tight">{topic.displayName}</h3>
                    <p className="text-xs text-ink-muted font-medium mt-0.5 line-clamp-1">{topic.description}</p>

                    {/* Level dots */}
                    <div className="flex items-center gap-1.5 mt-2.5">
                      {levels.map((lvl) => {
                        const levelInfo = topic.levels[lvl];
                        if (!levelInfo || levelInfo.sessionsAvailable === 0) {
                          return (
                            <div key={lvl} className="w-6 h-6 rounded-full bg-soft border-2 border-line flex items-center justify-center">
                              <span className="text-xs text-gray-300">-</span>
                            </div>
                          );
                        }

                        const status = getLevelStatus(tp, lvl);
                        const ll = levelLabels[lvl];

                        let dotCls = 'w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border-2 ';
                        if (status === 'mastered') {
                          dotCls += 'bg-star border-ink text-ink';
                        } else if (status === 'passed') {
                          dotCls += 'bg-success-soft border-success text-success';
                        } else if (status === 'started') {
                          dotCls += 'bg-hint border-hint-ink/40 text-hint-ink';
                        } else if (status === 'available') {
                          dotCls += 'bg-white border-line text-ink-muted';
                        } else {
                          dotCls += 'bg-soft border-line text-gray-300';
                        }

                        return (
                          <div key={lvl} className={dotCls} title={`${ll?.label}: ${status}`}>
                            {status === 'mastered' ? '★' : status === 'passed' ? '✓' : ll?.emoji?.slice(0, 2) ?? lvl.slice(1)}
                          </div>
                        );
                      })}

                      {/* Progress summary */}
                      <span className="ml-auto text-xs font-bold text-ink-muted shrink-0">
                        {masteredCount > 0 && <span className="text-hint-ink">{masteredCount}★</span>}
                        {passedCount > masteredCount && <span className="text-success ml-1">{passedCount - masteredCount}✓</span>}
                        {passedCount === 0 && masteredCount === 0 && 'Start →'}
                      </span>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

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

    fetch('/api/skill-drills')
      .then((r) => r.json())
      .then((d: { meta: Meta; topics: Record<string, TopicInfo> }) => {
        setMeta(d.meta);
        setTopics(d.topics);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        <div className="bg-duo-dark px-4 py-4 flex items-center gap-3">
          <Link href="/home" className="text-white/60 hover:text-white text-sm">&larr;</Link>
          <h1 className="text-white font-extrabold text-lg">Skill Drills</h1>
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-3">
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-24" />
          ))}
        </div>
      </div>
    );
  }

  if (!topics || !meta) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-6">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-gray-500">Skill drills not available yet.</p>
        <Link href="/home" className="text-sm text-blue-500 underline">Go Home</Link>
      </div>
    );
  }

  const topicList = Object.values(topics);
  const levelLabels = meta.levelLabels;

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/home" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Skill Drills</h1>
          <p className="text-white/50 text-xs font-medium">16 topics &middot; 5 mastery levels each</p>
        </div>
        <span className="text-2xl">🎯</span>
      </div>

      {/* Intro */}
      <div className="max-w-lg mx-auto px-4 pt-5">
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl px-4 py-3 border border-indigo-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-indigo-800">Master any topic, step by step!</p>
            <p className="text-xs text-indigo-600 mt-0.5">
              Each topic has 5 levels. Score 8/10 to unlock the next level. Score 9/10 for mastery!
            </p>
          </div>
        </div>

        {/* Level legend */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
          {['L1', 'L2', 'L3', 'L4', 'L5'].map((lvl) => {
            const ll = levelLabels[lvl];
            return (
              <div key={lvl} className="flex items-center gap-1 bg-white rounded-full px-2.5 py-1 border border-gray-200 shrink-0">
                <span className="text-xs">{ll?.emoji}</span>
                <span className="text-[10px] font-bold text-gray-600">{ll?.label}</span>
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
                className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-[box-shadow,transform] active:scale-[0.98]"
              >
                <div className="flex items-start gap-3">
                  {/* Icon */}
                  <div className="text-3xl shrink-0 mt-0.5">{topic.icon}</div>

                  <div className="flex-1 min-w-0">
                    {/* Title + description */}
                    <h3 className="font-extrabold text-gray-800 text-sm leading-tight">{topic.displayName}</h3>
                    <p className="text-xs text-gray-400 font-medium mt-0.5 line-clamp-1">{topic.description}</p>

                    {/* Level dots */}
                    <div className="flex items-center gap-1.5 mt-2.5">
                      {levels.map((lvl) => {
                        const levelInfo = topic.levels[lvl];
                        if (!levelInfo || levelInfo.sessionsAvailable === 0) {
                          return (
                            <div key={lvl} className="w-6 h-6 rounded-full bg-gray-100 border border-gray-200 flex items-center justify-center">
                              <span className="text-[8px] text-gray-300">-</span>
                            </div>
                          );
                        }

                        const status = getLevelStatus(tp, lvl);
                        const ll = levelLabels[lvl];

                        let dotCls = 'w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border-2 ';
                        if (status === 'mastered') {
                          dotCls += 'bg-gradient-to-br from-yellow-300 to-orange-400 border-yellow-400 text-white';
                        } else if (status === 'passed') {
                          dotCls += 'bg-duo-green border-duo-green-dark text-white';
                        } else if (status === 'started') {
                          dotCls += 'bg-blue-100 border-blue-300 text-blue-600';
                        } else if (status === 'available') {
                          dotCls += 'bg-white border-gray-300 text-gray-500';
                        } else {
                          dotCls += 'bg-gray-100 border-gray-200 text-gray-300';
                        }

                        return (
                          <div key={lvl} className={dotCls} title={`${ll?.label}: ${status}`}>
                            {status === 'mastered' ? '★' : status === 'passed' ? '✓' : ll?.emoji?.slice(0, 2) ?? lvl.slice(1)}
                          </div>
                        );
                      })}

                      {/* Progress summary */}
                      <span className="ml-auto text-[10px] font-bold text-gray-400 shrink-0">
                        {masteredCount > 0 && <span className="text-yellow-500">{masteredCount}★</span>}
                        {passedCount > masteredCount && <span className="text-duo-green ml-1">{passedCount - masteredCount}✓</span>}
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

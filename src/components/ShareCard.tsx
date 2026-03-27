'use client';

import React from 'react';

// ── Types ──────────────────────────────────────────────────────────────────────

export interface LessonCardData {
  studentName: string;
  topicName:   string;
  topicEmoji:  string;
  correct:     number;
  total:       number;
  xp:          number;
  date:        string;
}

export interface MockTestCardData {
  studentName:  string;
  score:        number;
  totalQ:       number;
  pct:          number;
  gradeLabel:   string;
  strongTopic:  string;
  weakTopic:    string;
  timeUsedMs:   number;
  timeLimitMs:  number;
}

export interface BadgeCardData {
  studentName: string;
  badgeEmoji:  string;
  badgeName:   string;
  badgeDesc:   string;
  date:        string;
}

export interface StreakCardData {
  studentName: string;
  streakDays:  number;
  date:        string;
}

export interface MasteredCardData {
  studentName:    string;
  topicName:      string;
  topicEmoji:     string;
  questionsTotal: number;
  accuracy:       number;
  daysPracticed:  number;
  date:           string;
}

export type ShareCardData =
  | { type: 'lesson';   data: LessonCardData   }
  | { type: 'mocktest'; data: MockTestCardData  }
  | { type: 'badge';    data: BadgeCardData     }
  | { type: 'streak';   data: StreakCardData    }
  | { type: 'mastered'; data: MasteredCardData  };

// ── Design tokens (inline styles — required for reliable PNG export) ───────────

const GREEN   = '#58CC02';
const BLUE    = '#1CB0F6';
const ORANGE  = '#FF9600';
const GOLD    = '#FBBF24';
const RED     = '#EF4444';
const PRIMARY = '#1F2937';
const SECONDARY = '#6B7280';
const CARD_FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif';

const CARD: React.CSSProperties = {
  width: 540, height: 540,
  background: '#FFFFFF',
  borderRadius: 24,
  padding: 0,
  display: 'flex',
  flexDirection: 'column',
  position: 'relative',
  overflow: 'hidden',
  fontFamily: CARD_FONT,
  boxSizing: 'border-box',
};

// ── Shared sub-components ─────────────────────────────────────────────────────

function GreenStrip() {
  return (
    <div style={{
      width: '100%', height: 8,
      background: 'linear-gradient(90deg, #58CC02 0%, #46A302 100%)',
      flexShrink: 0,
    }} />
  );
}

function OrangeStrip() {
  return (
    <div style={{
      width: '100%', height: 8,
      background: 'linear-gradient(90deg, #FF9600 0%, #E08600 100%)',
      flexShrink: 0,
    }} />
  );
}

function Watermark() {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
      paddingBottom: 20, paddingTop: 8,
    }}>
      <span style={{ fontSize: 13, color: SECONDARY }}>✨</span>
      <span style={{ fontSize: 12, color: SECONDARY, fontWeight: 700, letterSpacing: 0.5 }}>
        MathSpark · mathspark.in
      </span>
    </div>
  );
}

function Label({ text, color }: { text: string; color: string }) {
  return (
    <div style={{
      fontSize: 11, color, fontWeight: 800, letterSpacing: 1.5,
      textTransform: 'uppercase', marginBottom: 4,
    }}>{text}</div>
  );
}

function ScoreRing({ pct, topLabel, bottomLabel, size = 140 }: {
  pct: number; topLabel: string; bottomLabel: string; size?: number;
}) {
  const r    = (size - 14) / 2;
  const cx   = size / 2;
  const circ = 2 * Math.PI * r;
  const dash = circ * Math.min(pct, 100) / 100;
  const color = pct >= 70 ? GREEN : pct >= 50 ? GOLD : RED;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#F3F4F6" strokeWidth="12" />
      <circle cx={cx} cy={cx} r={r} fill="none" stroke={color} strokeWidth="12"
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`} />
      <text x={cx} y={cx - 6} textAnchor="middle" fontSize="26" fontWeight="900" fill={PRIMARY}>{topLabel}</text>
      <text x={cx} y={cx + 16} textAnchor="middle" fontSize="13" fill={SECONDARY} fontWeight="600">{bottomLabel}</text>
    </svg>
  );
}

// ── Card A: Lesson Complete ────────────────────────────────────────────────────

function LessonCard({ data }: { data: LessonCardData }) {
  const pct = Math.round((data.correct / data.total) * 100);
  return (
    <div style={CARD}>
      <GreenStrip />
      <div style={{ padding: '28px 36px 0', flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 10 }}>
          <div>
            <Label text="MathSpark Achievement" color={GREEN} />
            <div style={{ fontSize: 24, color: PRIMARY, fontWeight: 900, lineHeight: 1.2 }}>
              Lesson Complete! 🏆
            </div>
          </div>
          <span style={{ fontSize: 36 }}>✨</span>
        </div>

        {/* Student name */}
        <div style={{ fontSize: 15, color: SECONDARY, fontWeight: 600, marginBottom: 16 }}>
          {data.studentName} just completed
        </div>

        {/* Topic pill */}
        <div style={{
          background: '#F0FDF4', border: '1.5px solid #BBF7D0',
          borderRadius: 14, padding: '10px 16px', marginBottom: 20,
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <span style={{ fontSize: 26 }}>{data.topicEmoji}</span>
          <span style={{ fontSize: 17, color: PRIMARY, fontWeight: 800 }}>{data.topicName}</span>
        </div>

        {/* Score ring + stats */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 28, flex: 1 }}>
          <ScoreRing pct={pct} topLabel={`${data.correct}/${data.total}`} bottomLabel={`${pct}%`} />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <Label text="Accuracy" color={SECONDARY} />
              <div style={{ fontSize: 30, color: GREEN, fontWeight: 900 }}>{pct}%</div>
            </div>
            <div>
              <Label text="XP Earned" color={SECONDARY} />
              <div style={{ fontSize: 26, color: GOLD, fontWeight: 900 }}>+{data.xp} ⭐</div>
            </div>
          </div>
        </div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card B: Mock Test Score ───────────────────────────────────────────────────

function MockTestCard({ data }: { data: MockTestCardData }) {
  const timeMin  = Math.round(data.timeUsedMs  / 60_000);
  const limitMin = Math.round(data.timeLimitMs / 60_000);
  return (
    <div style={CARD}>
      <GreenStrip />
      <div style={{ padding: '24px 36px 0', flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Label row */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
          <Label text="MathSpark · IPM Mock Test" color={BLUE} />
          <span style={{ fontSize: 24 }}>📝</span>
        </div>

        {/* Student name */}
        <div style={{ fontSize: 22, color: PRIMARY, fontWeight: 900, marginBottom: 20 }}>
          {data.studentName}
        </div>

        {/* Score ring + grade + time */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 24, marginBottom: 24 }}>
          <ScoreRing pct={data.pct} topLabel={`${data.score}/${data.totalQ}`} bottomLabel={`${data.pct}%`} size={140} />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 22, color: PRIMARY, fontWeight: 900, marginBottom: 6 }}>
              {data.gradeLabel} {data.pct >= 70 ? '⭐' : data.pct >= 50 ? '👍' : '💪'}
            </div>
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              background: '#F9FAFB', borderRadius: 8, padding: '5px 12px',
            }}>
              <span style={{ fontSize: 14 }}>⏱</span>
              <span style={{ fontSize: 14, color: SECONDARY, fontWeight: 600 }}>
                {timeMin} / {limitMin} min
              </span>
            </div>
          </div>
        </div>

        {/* Two stat cards */}
        <div style={{ display: 'flex', gap: 12, flex: 1 }}>
          <div style={{
            flex: 1, background: '#F0FDF4', border: '1.5px solid #BBF7D0',
            borderRadius: 14, padding: '12px 14px',
            display: 'flex', flexDirection: 'column', justifyContent: 'center',
          }}>
            <div style={{ fontSize: 10, color: GREEN, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>
              ✅ Strongest
            </div>
            <div style={{ fontSize: 15, color: PRIMARY, fontWeight: 700, lineHeight: 1.3 }}>
              {data.strongTopic}
            </div>
          </div>
          <div style={{
            flex: 1, background: '#FFFBEB', border: '1.5px solid #FDE68A',
            borderRadius: 14, padding: '12px 14px',
            display: 'flex', flexDirection: 'column', justifyContent: 'center',
          }}>
            <div style={{ fontSize: 10, color: '#D97706', fontWeight: 800, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>
              🎯 Focus on
            </div>
            <div style={{ fontSize: 15, color: PRIMARY, fontWeight: 700, lineHeight: 1.3 }}>
              {data.weakTopic}
            </div>
          </div>
        </div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card C: Badge Earned ──────────────────────────────────────────────────────

function BadgeCard({ data }: { data: BadgeCardData }) {
  return (
    <div style={CARD}>
      <GreenStrip />
      <div style={{
        padding: '0 36px', flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 12,
      }}>
        <Label text="Badge Earned!" color={GOLD} />
        <div style={{ fontSize: 88, lineHeight: 1.1, filter: 'drop-shadow(0 4px 12px rgba(251,191,36,0.3))' }}>
          {data.badgeEmoji}
        </div>
        <div style={{ fontSize: 28, color: PRIMARY, fontWeight: 900, textAlign: 'center' }}>
          {data.badgeName}
        </div>
        <div style={{ fontSize: 15, color: SECONDARY, fontWeight: 600, textAlign: 'center', maxWidth: 360, lineHeight: 1.5 }}>
          {data.badgeDesc}
        </div>
        <div style={{
          marginTop: 8, background: '#F9FAFB', borderRadius: 10, padding: '8px 20px',
        }}>
          <span style={{ fontSize: 14, color: PRIMARY, fontWeight: 700 }}>
            {data.studentName}
          </span>
        </div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card D: Streak Milestone ──────────────────────────────────────────────────

function StreakCard({ data }: { data: StreakCardData }) {
  return (
    <div style={CARD}>
      <OrangeStrip />
      <div style={{
        padding: '0 36px', flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 14,
      }}>
        <div style={{ fontSize: 80, fontWeight: 900, color: ORANGE, display: 'flex', alignItems: 'center', gap: 8, lineHeight: 1 }}>
          🔥 {data.streakDays}
        </div>
        <div style={{ fontSize: 28, color: PRIMARY, fontWeight: 900 }}>
          {data.streakDays}-Day Streak!
        </div>
        <div style={{ fontSize: 15, color: SECONDARY, fontWeight: 600, textAlign: 'center', maxWidth: 380, lineHeight: 1.6 }}>
          {data.studentName} has practiced math every day for{' '}
          <span style={{ color: ORANGE, fontWeight: 800 }}>{data.streakDays} days</span> in a row!
        </div>
        <div style={{
          marginTop: 4, background: '#FFF7ED', border: '1.5px solid #FED7AA',
          borderRadius: 10, padding: '8px 20px',
        }}>
          <span style={{ fontSize: 14, color: '#C2410C', fontWeight: 700 }}>
            Incredible dedication 💪
          </span>
        </div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card E: Topic Mastered ────────────────────────────────────────────────────

function MasteredCard({ data }: { data: MasteredCardData }) {
  return (
    <div style={CARD}>
      <GreenStrip />
      <div style={{ padding: '24px 36px 0', flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
          <div style={{ fontSize: 22, color: PRIMARY, fontWeight: 900 }}>Topic Mastered 🏆</div>
        </div>

        {/* Centered content */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 12 }}>
          <div style={{ fontSize: 64, filter: 'drop-shadow(0 4px 12px rgba(88,204,2,0.25))' }}>
            {data.topicEmoji}
          </div>
          <div style={{ fontSize: 26, color: PRIMARY, fontWeight: 900, textAlign: 'center' }}>
            {data.topicName}
          </div>
          <div style={{ fontSize: 14, color: SECONDARY, fontWeight: 600 }}>
            {data.studentName} has fully mastered this topic!
          </div>

          {/* 3 stat columns */}
          <div style={{
            display: 'flex', justifyContent: 'center', gap: 24, marginTop: 8,
            background: '#F9FAFB', borderRadius: 16, padding: '16px 32px',
          }}>
            {[
              { val: String(data.questionsTotal), label: 'Questions', color: PRIMARY },
              { val: `${data.accuracy}%`,         label: 'Accuracy',  color: GREEN },
              { val: String(data.daysPracticed),  label: 'Days',      color: BLUE },
            ].map(({ val, label, color }) => (
              <div key={label} style={{ textAlign: 'center', minWidth: 70 }}>
                <div style={{ fontSize: 26, color, fontWeight: 900 }}>{val}</div>
                <div style={{ fontSize: 11, color: SECONDARY, fontWeight: 600, marginTop: 2 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Main ShareCard (forwarded ref for PNG capture) ────────────────────────────

export const ShareCard = React.forwardRef<HTMLDivElement, { card: ShareCardData }>(
  function ShareCard({ card }, ref) {
    return (
      <div ref={ref} style={{ display: 'inline-block', lineHeight: 0 }}>
        {card.type === 'lesson'   && <LessonCard   data={card.data} />}
        {card.type === 'mocktest' && <MockTestCard  data={card.data} />}
        {card.type === 'badge'    && <BadgeCard     data={card.data} />}
        {card.type === 'streak'   && <StreakCard     data={card.data} />}
        {card.type === 'mastered' && <MasteredCard  data={card.data} />}
      </div>
    );
  }
);

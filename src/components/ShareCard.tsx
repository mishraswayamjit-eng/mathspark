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

const BG   = 'linear-gradient(140deg, #0A0E17 0%, #0D1620 60%, #0A1118 100%)';
const GREEN = '#34D399';
const BLUE  = '#60A5FA';
const GOLD  = '#FBBF24';
const WHITE = '#F9FAFB';
const MUTED = '#9CA3AF';
const DIM   = '#6B7280';
const DARK2 = '#0F2035';
const CARD_FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif';

const CARD: React.CSSProperties = {
  width: 540, height: 540,
  background: BG,
  borderRadius: 24,
  padding: 36,
  display: 'flex',
  flexDirection: 'column',
  position: 'relative',
  overflow: 'hidden',
  fontFamily: CARD_FONT,
  boxSizing: 'border-box',
};

// ── Shared sub-components ─────────────────────────────────────────────────────

function Watermark() {
  return (
    <div style={{
      position: 'absolute', bottom: 18, left: 0, right: 0,
      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
    }}>
      <span style={{ fontSize: 13, color: '#374151', fontWeight: 700 }}>✨</span>
      <span style={{ fontSize: 12, color: '#374151', fontWeight: 700, letterSpacing: 0.5 }}>
        MathSpark · mathspark.in
      </span>
    </div>
  );
}

function Label({ text, color }: { text: string; color: string }) {
  return (
    <div style={{
      fontSize: 10, color, fontWeight: 800, letterSpacing: 2,
      textTransform: 'uppercase', marginBottom: 6,
    }}>{text}</div>
  );
}

function ScoreRing({ pct, topLabel, bottomLabel }: { pct: number; topLabel: string; bottomLabel: string }) {
  const r    = 50;
  const circ = 2 * Math.PI * r;
  const dash = circ * Math.min(pct, 100) / 100;
  const color = pct >= 70 ? GREEN : pct >= 50 ? GOLD : '#FF4B4B';
  return (
    <svg width="126" height="126" viewBox="0 0 126 126">
      <circle cx="63" cy="63" r={r} fill="none" stroke="#1a2f3a" strokeWidth="10" />
      <circle cx="63" cy="63" r={r} fill="none" stroke={color} strokeWidth="10"
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 63 63)" />
      <text x="63" y="57" textAnchor="middle" fontSize="22" fontWeight="900" fill={WHITE}>{topLabel}</text>
      <text x="63" y="78" textAnchor="middle" fontSize="11" fill={MUTED} fontWeight="600">{bottomLabel}</text>
    </svg>
  );
}

// ── Card A: Lesson Complete ────────────────────────────────────────────────────

function LessonCard({ data }: { data: LessonCardData }) {
  const pct = Math.round((data.correct / data.total) * 100);
  return (
    <div style={CARD}>
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 16 }}>
        <div>
          <Label text="MathSpark Achievement" color={GREEN} />
          <div style={{ fontSize: 22, color: WHITE, fontWeight: 900, lineHeight: 1.2 }}>
            Lesson Complete! 🏆
          </div>
        </div>
        <span style={{ fontSize: 38 }}>✨</span>
      </div>

      <div style={{ fontSize: 14, color: MUTED, fontWeight: 600, marginBottom: 18 }}>
        {data.studentName} just completed
      </div>

      <div style={{
        background: DARK2, border: '1px solid #1a3a50',
        borderRadius: 16, padding: '12px 16px', marginBottom: 22,
        display: 'flex', alignItems: 'center', gap: 12,
      }}>
        <span style={{ fontSize: 28 }}>{data.topicEmoji}</span>
        <span style={{ fontSize: 17, color: WHITE, fontWeight: 800 }}>{data.topicName}</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 24, flex: 1 }}>
        <ScoreRing pct={pct} topLabel={`${data.correct}/${data.total}`} bottomLabel={`${pct}%`} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <Label text="Accuracy" color={DIM} />
            <div style={{ fontSize: 30, color: GREEN, fontWeight: 900 }}>{pct}%</div>
          </div>
          <div>
            <Label text="XP Earned" color={DIM} />
            <div style={{ fontSize: 26, color: GOLD, fontWeight: 900 }}>+{data.xp} ⭐</div>
          </div>
        </div>
      </div>

      <div style={{ fontSize: 11, color: DIM, fontWeight: 600, marginBottom: 30 }}>{data.date}</div>
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
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 14 }}>
        <div>
          <Label text="MathSpark IPM Prep" color={BLUE} />
          <div style={{ fontSize: 20, color: WHITE, fontWeight: 900 }}>📝 Mock Test Results</div>
        </div>
        <span style={{ fontSize: 36 }}>📋</span>
      </div>

      <div style={{ fontSize: 13, color: MUTED, fontWeight: 600, marginBottom: 18 }}>{data.studentName}</div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 24, marginBottom: 22 }}>
        <ScoreRing pct={data.pct} topLabel={`${data.score}/${data.totalQ}`} bottomLabel={`${data.pct}%`} />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 18, color: WHITE, fontWeight: 900, marginBottom: 10 }}>{data.gradeLabel}</div>
          <div style={{ fontSize: 12, color: MUTED, fontWeight: 600 }}>
            ⏱ {timeMin} min / {limitMin} min
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 30 }}>
        <div style={{ flex: 1, background: DARK2, border: '1px solid #1a3a50', borderRadius: 14, padding: '10px 14px' }}>
          <div style={{ fontSize: 9, color: GREEN, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 4 }}>✅ Strongest</div>
          <div style={{ fontSize: 13, color: WHITE, fontWeight: 700, lineHeight: 1.3 }}>{data.strongTopic}</div>
        </div>
        <div style={{ flex: 1, background: '#1a1005', border: '1px solid #3a2a05', borderRadius: 14, padding: '10px 14px' }}>
          <div style={{ fontSize: 9, color: GOLD, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 4 }}>🟡 Focus on</div>
          <div style={{ fontSize: 13, color: WHITE, fontWeight: 700, lineHeight: 1.3 }}>{data.weakTopic}</div>
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
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 14,
      }}>
        <Label text="🏅 Badge Earned!" color={GOLD} />
        <div style={{ fontSize: 90, lineHeight: 1.1, filter: 'drop-shadow(0 0 24px rgba(251,191,36,0.45))' }}>
          {data.badgeEmoji}
        </div>
        <div style={{ fontSize: 28, color: WHITE, fontWeight: 900, textAlign: 'center' }}>{data.badgeName}</div>
        <div style={{ fontSize: 15, color: MUTED, fontWeight: 600, textAlign: 'center', maxWidth: 340, lineHeight: 1.5 }}>
          {data.badgeDesc}
        </div>
        <div style={{ fontSize: 13, color: DIM, fontWeight: 600, marginTop: 4 }}>
          {data.studentName} earned this on MathSpark
        </div>
        <div style={{ fontSize: 11, color: DIM, fontWeight: 500 }}>{data.date}</div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card D: Streak Milestone ──────────────────────────────────────────────────

function StreakCard({ data }: { data: StreakCardData }) {
  return (
    <div style={CARD}>
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 18,
      }}>
        <Label text="Streak Milestone 🔥" color="#FF9600" />
        <div style={{ fontSize: 80, fontWeight: 900, color: '#FF9600', display: 'flex', alignItems: 'center', gap: 10, lineHeight: 1 }}>
          🔥 {data.streakDays}
        </div>
        <div style={{ fontSize: 26, color: WHITE, fontWeight: 900 }}>
          {data.streakDays}-Day Streak!
        </div>
        <div style={{ fontSize: 15, color: MUTED, fontWeight: 600, textAlign: 'center', maxWidth: 360, lineHeight: 1.5 }}>
          {data.studentName} has practiced math every day for{' '}
          <span style={{ color: '#FF9600', fontWeight: 800 }}>{data.streakDays} days</span> in a row!
        </div>
        <div style={{ fontSize: 15, color: GOLD, fontWeight: 700 }}>That&apos;s incredible dedication 💪</div>
        <div style={{ fontSize: 11, color: DIM, fontWeight: 500 }}>{data.date}</div>
      </div>
      <Watermark />
    </div>
  );
}

// ── Card E: Topic Mastered ────────────────────────────────────────────────────

function MasteredCard({ data }: { data: MasteredCardData }) {
  return (
    <div style={CARD}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
        <Label text="MathSpark Mastery" color={GREEN} />
        <span style={{ fontSize: 30 }}>🏆</span>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 16 }}>
        <div style={{ fontSize: 68, filter: 'drop-shadow(0 0 20px rgba(52,211,153,0.4))' }}>✅</div>
        <div style={{ textAlign: 'center' }}>
          <Label text="Mastered" color={GREEN} />
          <div style={{ fontSize: 26, color: WHITE, fontWeight: 900 }}>{data.topicEmoji} {data.topicName}</div>
          <div style={{ fontSize: 14, color: MUTED, fontWeight: 600, marginTop: 6 }}>
            {data.studentName} has fully mastered this topic!
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', gap: 32, marginTop: 4 }}>
          {[
            { val: String(data.questionsTotal), label: 'Questions' },
            { val: `${data.accuracy}%`,         label: 'Accuracy', color: GREEN },
            { val: String(data.daysPracticed),  label: 'Days', color: BLUE },
          ].map(({ val, label, color }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, color: color ?? WHITE, fontWeight: 900 }}>{val}</div>
              <div style={{ fontSize: 11, color: DIM, fontWeight: 600 }}>{label}</div>
            </div>
          ))}
        </div>

        <div style={{ fontSize: 11, color: DIM, fontWeight: 500 }}>{data.date}</div>
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

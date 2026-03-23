# CLAUDE.md — MathSpark Implementation Prompt
# Drop this file in your project root. Claude Code reads it automatically.

## Project Overview

MathSpark is an IPM (Institute for Promotion of Mathematics) exam preparation app for Indian students in Grades 2-9. It's built with **Next.js + React + Tailwind CSS**. The app has a mascot called **Sparky** who guides kids through practice, flashcards, and exam prep.

The app is backed by **14 pre-built JSON knowledge assets** that power every feature. These assets were programmatically generated from a verified bank of 12,452 MCQs. Every mathematical answer in the system was computed by a deterministic Python engine — zero hallucinated content.

## Critical Rules

1. **Child safety first.** All content, language, and UI must be appropriate for ages 7-15. Tonality is encouraging, never shaming. When a student gets something wrong, Sparky says "Not quite! Here's how to think about it..." — never "Wrong!"
2. **Zero hallucination.** Never generate mathematical answers, formulas, or solutions on the fly. ALL math content comes from the pre-built JSON assets. If the data isn't in the JSON, don't invent it.
3. **Kid-friendly language.** Simple words, short sentences, encouraging tone. Grade 2 students and Grade 9 students both use this app — the language adapts based on the grade context.
4. **Professional quality.** This is a commercial product. Every component should be polished, accessible, and performant.

## Tech Stack

- **Framework:** Next.js 14+ (App Router)
- **UI:** React 18+ with Tailwind CSS
- **State:** React Context + localStorage for persistence (no backend yet)
- **Math rendering:** KaTeX for LaTeX formulas
- **Charts:** Recharts for progress/analytics visualisations
- **Animations:** Framer Motion for card flips, transitions, reveals

## Project Structure (scaffold this first)

```
mathspark/
├── CLAUDE.md                          # This file
├── data/                              # ALL 14 JSON knowledge assets
│   ├── question-bank.json             # 12,452 MCQs
│   ├── paper-bank.json                # 240 adaptive papers + simulator metadata
│   ├── skill-drills.json              # 290 skill drill sessions
│   ├── flashcards.json                # 653 concept + mental math cards
│   ├── mistake-patterns.json          # 50 named error patterns
│   ├── dependency-graph.json          # 88 concept nodes, 123 edges
│   ├── worked-examples.json           # 212 Sparky Explains examples
│   ├── ipm-predictor.json             # Exam prediction data
│   ├── parent-report.json             # Report template + narrative rules
│   ├── daily-challenges.json          # 2,630 daily challenges
│   ├── concept-map.json               # Visualisation data (88 nodes, 15 islands)
│   ├── strategy-bank.json             # 35 exam strategies
│   └── math-stories.json              # 30 real-world stories
├── src/
│   ├── app/                           # Next.js App Router pages
│   │   ├── layout.tsx                 # Root layout with Sparky context
│   │   ├── page.tsx                   # Home/Dashboard
│   │   ├── practice/
│   │   │   ├── page.tsx               # Practice hub
│   │   │   ├── daily/page.tsx         # Daily Challenge (Asset 10)
│   │   │   ├── papers/page.tsx        # Paper selection
│   │   │   ├── papers/[paperId]/page.tsx  # Exam simulator (Assets 2+13)
│   │   │   └── skill-drill/
│   │   │       ├── page.tsx           # Topic selection grid
│   │   │       └── [topicId]/[levelId]/page.tsx  # Drill session (Asset 3)
│   │   ├── learn/
│   │   │   ├── page.tsx               # Learn hub
│   │   │   ├── flashcards/page.tsx    # Flashcard decks (Asset 4)
│   │   │   ├── flashcards/[deckId]/page.tsx  # Flashcard session
│   │   │   ├── concepts/page.tsx      # Concept map (Assets 6+11)
│   │   │   ├── examples/page.tsx      # Sparky Explains (Asset 7)
│   │   │   ├── examples/[exampleId]/page.tsx  # Single worked example
│   │   │   ├── stories/page.tsx       # Math Stories (Asset 14)
│   │   │   └── strategies/page.tsx    # Strategy Bank (Asset 12)
│   │   ├── exam-prep/
│   │   │   ├── page.tsx               # Exam prep hub
│   │   │   ├── predictor/page.tsx     # IPM Predictor (Asset 8)
│   │   │   └── mock-test/page.tsx     # Mock test selector → routes to papers/[paperId]
│   │   ├── progress/
│   │   │   ├── page.tsx               # Student progress dashboard
│   │   │   └── report/page.tsx        # Parent report view (Asset 9)
│   │   ├── mistakes/page.tsx          # My Mistake Patterns (Asset 5)
│   │   └── settings/page.tsx          # Grade selection, preferences
│   ├── components/
│   │   ├── ui/                        # Generic UI (Button, Card, Modal, Badge, etc.)
│   │   ├── sparky/
│   │   │   ├── SparkyAvatar.tsx       # Sparky mascot component (various emotions)
│   │   │   ├── SparkyMessage.tsx      # Speech bubble with Sparky's messages
│   │   │   └── SparkyTip.tsx          # Tip card with Sparky icon
│   │   ├── question/
│   │   │   ├── QuestionCard.tsx       # Single MCQ display (text, options, selection)
│   │   │   ├── OptionButton.tsx       # Single option (A/B/C/D) with states
│   │   │   ├── HintRevealer.tsx       # Progressive hint reveal (hint 1, 2, 3)
│   │   │   ├── StepByStep.tsx         # Animated step-by-step solution reveal
│   │   │   └── MisconceptionPopup.tsx # Explains why the chosen wrong answer is wrong
│   │   ├── flashcard/
│   │   │   ├── FlashcardDeck.tsx      # Deck of cards with swipe/tap navigation
│   │   │   ├── FlashcardItem.tsx      # Single card with 3D flip animation
│   │   │   └── MentalMathDrill.tsx    # Speed drill with timer
│   │   ├── exam/
│   │   │   ├── ExamSimulator.tsx      # Full exam experience (timer, navigator, palette)
│   │   │   ├── QuestionNavigator.tsx  # Grid showing answered/unanswered/marked
│   │   │   ├── CountdownTimer.tsx     # Exam timer with warnings at 10/5/1 min
│   │   │   └── PostExamReport.tsx     # Score breakdown, time analysis, mistake patterns
│   │   ├── progress/
│   │   │   ├── StreakCounter.tsx       # 🔥 daily streak display
│   │   │   ├── TopicHeatmap.tsx       # Mastery heatmap across topics
│   │   │   ├── ProgressChart.tsx      # Line chart of accuracy over time
│   │   │   └── ExamReadiness.tsx      # Readiness score gauge (0-100)
│   │   ├── concept-map/
│   │   │   ├── ConceptMapView.tsx     # Interactive node graph (D3 or React Flow)
│   │   │   └── ConceptNode.tsx        # Single node (locked/in-progress/mastered states)
│   │   └── layout/
│   │       ├── Navbar.tsx             # Top nav with grade selector
│   │       ├── Sidebar.tsx            # Side menu (Practice, Learn, Exam Prep, Progress)
│   │       └── BottomNav.tsx          # Mobile bottom navigation
│   ├── lib/
│   │   ├── data-loader.ts            # Functions to load/cache JSON assets
│   │   ├── scoring.ts                # Score calculation (with negative marking)
│   │   ├── streak.ts                 # Streak logic (localStorage)
│   │   ├── spaced-repetition.ts      # Leitner box system for flashcards
│   │   ├── difficulty-classifier.ts  # Classify questions by difficulty
│   │   ├── mistake-detector.ts       # Detect mistake patterns from wrong answers
│   │   ├── report-generator.ts       # Generate parent report from activity data
│   │   ├── challenge-selector.ts     # Pick today's daily challenge
│   │   └── types.ts                  # TypeScript types for ALL JSON schemas
│   ├── contexts/
│   │   ├── StudentContext.tsx         # Student state (grade, progress, streak)
│   │   ├── ExamContext.tsx            # Active exam state (answers, time, marks)
│   │   └── FlashcardContext.tsx       # Leitner box states per card
│   └── hooks/
│       ├── useQuestionBank.ts         # Load/filter questions by grade, topic, difficulty
│       ├── usePapers.ts              # Load/filter papers by grade, duration
│       ├── useSkillDrills.ts         # Load drills by topic, level
│       ├── useFlashcards.ts          # Load cards, manage Leitner state
│       ├── useDailyChallenge.ts      # Get today's challenge, manage streaks
│       ├── useTimer.ts               # Countdown timer for exams
│       └── useMistakePatterns.ts     # Track and detect mistake patterns
└── public/
    └── sparky/                        # Sparky mascot SVGs/images
```

## Data Asset Schemas (what's inside each JSON)

### 1. question-bank.json (12,452 MCQs)
```typescript
interface QuestionBank {
  meta: { totalQuestions: number; grades: Record<string, number> };
  questions: Question[];
}
interface Question {
  id: string;               // "EXT_G6_MF_2020_001" or "VAR_EXT_G6_..."
  grade: number;            // 2-9
  subTopic: string;         // "Grade 6 — Angles"
  difficulty: string;       // "Easy" | "Medium" | "Hard"
  questionText: string;     // The question in plain text
  questionLatex: string;    // LaTeX version (may be empty)
  options: { id: string; text: string }[];  // Always 4 options: A, B, C, D
  correctAnswer: string;    // "A" | "B" | "C" | "D"
  hints: string[];          // 3 progressive hints
  stepByStep: { step: number; text: string; latex: string }[];
  misconceptions: Record<string, string>;  // Per option: why that wrong answer is wrong
  isVariant?: boolean;      // true if generated by variant engine
  variantOf?: string;       // parent question ID
  source: string;
}
```

### 2. paper-bank.json (240 papers)
```typescript
interface Paper {
  paperId: string;          // "G6_60min_v01"
  templateId: string;       // "G6_60min"
  variantNumber: number;    // 1-10
  grade: number;
  duration: number;         // 15, 30, or 60 minutes
  totalQuestions: number;    // 10, 20, or 40
  totalMarks: number;
  difficultyDistribution: { easy: number; medium: number; hard: number; easyPercent: number; mediumPercent: number; hardPercent: number };
  topicsCovered: string[];
  topicDistribution: Record<string, number>;
  instructions: { examName: string; subtitle: string; duration: string; totalQuestions: number; totalMarks: number; rules: string[] };
  markingScheme: { correct: string; wrong: string; unanswered: string; negativeMarking: boolean; maxMarks: number; passingMarks: number };
  questions: PaperQuestion[];  // Same as Question but with questionNumber, timeEstimateSeconds, topicBucket
  answerKey: Record<string, string>;  // { "1": "A", "2": "C", ... }
  uniqueHash: string;
  simulatorMetadata: {
    timeAllocationGuide: Record<string, number>;
    recommendedSequence: Record<string, { name: string; minutes: string; instruction: string }>;
    analyticsTemplate: { scoreBreakdown: any; timeAnalysis: any; topicBreakdown: any; mistakePatternsDetected: any; negativeMarkingImpact: any };
    uiFeatures: { countdownTimer: boolean; questionNavigator: boolean; markForReview: boolean; questionPalette: Record<string, string>; warningAt: number[] };
  };
}
```

### 3. skill-drills.json (290 sessions)
```typescript
interface SkillDrillBank {
  meta: { totalTopics: number; levelsPerTopic: number; totalSessions: number; scoringModel: any; levelLabels: Record<string, { label: string; emoji: string; description: string }> };
  topics: Record<string, { topicId: string; displayName: string; icon: string; description: string; levels: Record<string, { levelId: string; name: string; label: string; color: string; gradeRange: number[]; questionPoolSize: number; sessionsAvailable: number; sessionIds: string[] }> }>;
  sessions: DrillSession[];
}
interface DrillSession {
  sessionId: string;        // "DRILL_algebra_equations_L2_s03"
  topicId: string;
  levelId: string;          // "L1"-"L5"
  levelNumber: number;      // 1-5
  topicDisplayName: string;
  topicIcon: string;
  levelName: string;
  levelLabel: string;       // "Beginner", "Explorer", "Builder", "Thinker", "Master"
  levelColor: string;
  gradeRange: number[];
  totalQuestions: number;    // always 10
  questions: DrillQuestion[];
  answerKey: Record<string, string>;
  passingScore: number;     // 7
  masteryScore: number;     // 9
  unlockNextLevel: number;  // 8
}
```

### 4. flashcards.json (653 cards)
```typescript
interface FlashcardBank {
  meta: any;
  conceptCards: ConceptCard[];
  mentalMathCards: MentalMathCard[];
  topicIndex: Record<string, string[]>;
  difficultyIndex: Record<string, string[]>;
  preBuiltDecks: Record<string, { name: string; description: string; cardIds: string[] }>;
}
interface ConceptCard {
  id: string;               // "FC_0042"
  type: "concept";
  topicId: string;
  concept: string;          // "BODMAS Rule"
  front: string;            // Question side
  back: string;             // Answer side (multi-line)
  formula: string;          // LaTeX formula
  visual: string;           // Reference to SVG/component
  difficulty: number;       // 1=fundamental, 2=important, 3=advanced
  sparkyTip: string;        // Kid-friendly insight
  funFact: string;
  voiceQuestion: string;    // For TTS
  voiceKeywords: string[];  // For STT matching
  tags: string[];
  gradeRange: number[];
  example: string;
}
interface MentalMathCard {
  id: string;               // "MM_0015"
  type: "mental_math";
  category: string;         // "squares", "quick_lcm", etc.
  front: string;            // "12² = ?"
  back: string;             // "144"
  difficulty: number;
  speedTargetSeconds: number;
  voiceQuestion: string;
  voiceAnswer: string;
}
```

### 5. mistake-patterns.json (50 patterns)
```typescript
interface MistakePattern {
  id: string;               // "MP_001"
  name: string;             // "The Speed Average Trap"
  emoji: string;            // "🚗"
  category: string;         // "wrong_formula", "procedural_error", "sign_error", etc.
  description: string;
  whyItHappens: string;
  howToFix: string;
  example: { question: string; wrongAnswer: string; rightAnswer: string; wrongThinking: string; rightThinking: string } | null;
  frequency: string;        // "Very High", "High", "Medium"
  affectedTopics: string[];
  affectedGrades: number[];
  sparkyMessage: string;    // What Sparky says when detecting this mistake
  difficulty: number;
}
```

### 6. dependency-graph.json (88 nodes, 123 edges)
```typescript
interface DependencyGraph {
  nodes: { id: string; domain: string; name: string; description: string; gradeRange: number[]; difficulty: number; icon: string; color: string; questionCount: number; estimatedMinutesToMaster: number; masteryThreshold: number }[];
  edges: { source: string; target: string; type: "must_know" | "helpful"; sourceName: string; targetName: string }[];
  domains: Record<string, { name: string; nodeIds: string[]; color: string }>;
}
```

### 7. worked-examples.json (212 examples)
```typescript
interface WorkedExample {
  id: string;
  grade: number;
  topic: string;
  questionText: string;
  options: { id: string; text: string }[];
  correctAnswer: string;
  sparkyThinking: string[];     // Narration of HOW to approach the problem
  stepByStep: { stepNumber: number; instruction: string; latex: string; sparkyNarration: string; revealDelay: number }[];
  trapWarning: { exists: boolean; text: string; sparkyWarning: string };
  voiceScript: { intro: string; steps: string[]; conclusion: string };
  practiceQuestionIds: string[];
}
```

### 8. ipm-predictor.json
```typescript
interface ExamPredictor {
  predictions: Record<string, { grade: number; totalQuestionsAnalyzed: number; yearsAnalyzed: number; topicFrequency: { topic: string; count: number; percentage: number }[]; alwaysAppears: string[]; frequentlyAppears: string[]; predictedFocusAreas: string[] }>;
  insights: { topStrategicAdvice: string[] };
}
```

### 9. parent-report.json (template system)
```typescript
interface ParentReport {
  reportTemplate: { header: any; sections: { id: string; title: string; fields?: any[]; rules?: any; narrativeTemplates?: string[]; toneGuide?: string }[] };
  postExamTemplate: { sections: string[]; timeAnalysis: any; negativeMarkingAnalysis: any };
  narrativeRules: { tone: string; principles: string[]; sparkyClosing: string[] };
}
```

### 10. daily-challenges.json (2,630 challenges)
```typescript
interface DailyChallengeSystem {
  meta: { questionsPerChallenge: number; streakMechanics: { milestones: Record<string, string> }; monthlyThemes: Record<string, string> };
  challenges: Record<string, DailyChallenge[]>;  // keyed by grade: "2", "3", ..., "9"
}
interface DailyChallenge {
  challengeId: string;      // "DC_G6_D042"
  grade: number;
  day: number;              // 1-365
  questionsCount: number;   // 5
  estimatedMinutes: number; // 3
  questions: { questionNumber: number; sourceId: string; questionText: string; options: any[]; correctAnswer: string; hints: string[]; stepByStep: any[]; topicBucket: string }[];
  answerKey: Record<string, string>;
}
```

### 11. concept-map.json (visualisation)
```typescript
interface ConceptMap {
  nodes: { id: string; name: string; domain: string; domainIsland: string; icon: string; color: string; x: number; y: number; size: number; gradeRange: number[]; difficulty: number; questionCount: number; status: "locked"|"in_progress"|"mastered"; glowOnMastery: boolean }[];
  edges: { source: string; target: string; type: string; style: "solid"|"dashed" }[];
  domains: Record<string, { name: string; island: string; description: string }>;
  meta: { gradeOverlays: Record<string, string[]>; renderingHints: any };
}
```

### 12. strategy-bank.json (35 strategies)
```typescript
interface Strategy {
  id: string;
  category: string;         // "time_management", "elimination", "speed_tricks", etc.
  name: string;
  emoji: string;
  description: string;
  whenToUse: string;
  howItWorks: string;
  example: { scenario: string; action: string; result: string };
  sparkyTip: string;
  difficulty: number;
  gradeRange: number[];
  estimatedTimeSaved: string;
}
```

### 13. math-stories.json (30 stories)
```typescript
interface MathStory {
  id: string;
  title: string;
  emoji: string;
  topicId: string;
  contextCategory: string;  // "sports", "space", "nature", "food", "money", "games", etc.
  gradeRange: number[];
  storyText: string;        // The engaging narrative
  mathConnection: string;   // How it connects to math
  sparkyQuestion: string;   // Follow-up question for the student
  funFactor: number;        // 1-5
}
```

## Implementation Order

### Phase 0: Scaffold + Data Layer (do this first)
1. Create the full directory structure above
2. Place all 14 JSON files in `data/`
3. Create `types.ts` with all TypeScript interfaces above
4. Create `data-loader.ts` — lazy-loading functions for each JSON (use dynamic import, cache in memory)
5. Create shared UI components: Button, Card, Badge, Modal
6. Create SparkyAvatar and SparkyMessage components
7. Create the root layout with Navbar, Sidebar/BottomNav, grade selector
8. Create StudentContext (stores: selected grade, name, progress, streak in localStorage)

### Phase 1: Daily Challenge (Asset 10) — the daily hook
This is the #1 engagement feature. Build it first.
- Dashboard shows today's challenge with streak counter
- 5 questions, clean UI, tap to select A/B/C/D
- After answering: show correct/wrong with Sparky reaction
- End screen: score, streak update, encouragement
- Streak stored in localStorage with freeze mechanic
- Monthly theme displayed in header

### Phase 2: Exam Simulator (Assets 2 + 13) — the core product
Full IPM mock test experience.
- Paper selection: filter by grade, duration (15/30/60 min)
- Exam screen: countdown timer, question navigator palette, mark-for-review
- Each question: text, 4 options, LaTeX rendering (KaTeX)
- Post-exam: full analytics — score breakdown, time per question, topic accuracy, mistake patterns detected, negative marking impact
- Uses `simulatorMetadata` from the paper for time allocation guidance
- Uses `mistake-detector.ts` to match wrong answers to Mistake Patterns (Asset 5)

### Phase 3: Skill Drills (Asset 3) — progressive topic mastery
- Topic grid: 16 topics with icons, show level progress (L1-L5)
- Level selection: show sessions available, lock/unlock based on score
- Drill session: 10 questions, progressive difficulty
- Score screen: pass (7/10), unlock (8/10), mastery (9/10)
- Connects to dependency graph (Asset 6) for "recommended next" suggestions

### Phase 4: Flashcards (Asset 4) — concept recall
- Deck browser: 20 pre-built decks + custom topic-based decks
- Full-screen flashcard with 3D flip animation (Framer Motion)
- Self-rating: ✅ Got it / 🤔 Not sure / ❌ Forgot
- Leitner spaced repetition: track each card in 5 boxes (localStorage)
- Mental math speed drills: timer per card, speed target display
- Pre-exam warm-up mode: 10-15 rapid-fire mixed cards

### Phase 5: Learn Section (Assets 7, 12, 14) — enrichment
- **Sparky Explains** (Asset 7): Browse by topic/grade, tap-to-reveal step-by-step animation with Sparky narration, trap warnings
- **Strategy Bank** (Asset 12): Organised by category, each strategy as a card with example, Sparky tip, estimated time saved
- **Math Stories** (Asset 14): Stories with illustrations, math connection highlight, follow-up question

### Phase 6: Concept Map (Assets 6 + 11) — visual learning path
- Interactive graph rendering (suggest: @xyflow/react or custom SVG)
- Nodes are circles with icons, sized by question count
- Edges: solid for must_know, dashed for helpful
- Colours by domain
- Click node: shows description, linked drill sessions, question count, mastery status
- Grade overlay toggle: highlight which concepts belong to which grade
- Glow animation on mastered nodes

### Phase 7: Progress & Reports (Assets 5, 8, 9) — analytics
- **Student dashboard**: streak, accuracy trend (Recharts line chart), topic heatmap, exam readiness score
- **Mistake Patterns** (Asset 5): "Your top 3 mistakes" with Sparky's explanation of each, linked fix drills
- **IPM Predictor** (Asset 8): "Most likely to appear" topics, focus recommendations
- **Parent Report** (Asset 9): Generate from template, sections populate from activity data, warm encouraging tone

## Component Design Guidelines

### Question Display
- Question text: `text-lg font-medium` with KaTeX rendering for any LaTeX
- Options: 4 large tap targets, A/B/C/D badges on the left
- Selected state: blue border + fill
- Correct state: green border + ✓ icon
- Wrong state: red border + ✗ icon, then show misconception tooltip
- After answering: show step-by-step solution below (animated reveal)

### Flashcard Flip
- Use `perspective: 1000px` on container
- Front and back both `backface-visibility: hidden`
- On tap/swipe: `rotateY(180deg)` transition (0.6s ease)
- Front: large question text, topic badge
- Back: answer, formula (KaTeX), Sparky tip in speech bubble

### Exam Simulator
- Timer: fixed top-right, red when < 5 min
- Question palette: grid of numbered squares
  - Grey: not visited
  - Green: answered
  - Orange: marked for review
  - Red: not answered (visited but skipped)
- Navigation: Previous/Next buttons + "Mark for Review" toggle
- Auto-submit on timeout with warning modal at 1 minute

### Sparky Mascot
- Small avatar (40-50px) in corner or next to messages
- Expressions: happy 😊, thinking 🤔, excited 🎉, encouraging 💪, sad 😢
- Speech bubble component for messages
- Appears after every answer, after daily challenge, in flashcards

### Colour System
```
Primary: #6366F1 (indigo)
Success: #22C55E (green)
Warning: #F59E0B (amber)
Error:   #EF4444 (red)
Sparky:  #8B5CF6 (violet)

Difficulty colours:
  Easy:   #4CAF50
  Medium: #FFC107
  Hard:   #F44336

Level colours (from skill drills):
  L1: #4CAF50 (Beginner)
  L2: #8BC34A (Explorer)
  L3: #FFC107 (Builder)
  L4: #FF9800 (Thinker)
  L5: #F44336 (Master)
```

### Responsive Design
- Desktop: sidebar navigation + main content
- Tablet: collapsible sidebar
- Mobile: bottom navigation bar (Practice / Learn / Exam / Progress)
- All question/flashcard components must work in both orientations

## Key Implementation Details

### Data Loading (data-loader.ts)
```typescript
// Lazy-load and cache JSON assets
const cache: Record<string, any> = {};

export async function loadQuestionBank() {
  if (!cache.questionBank) {
    cache.questionBank = (await import('@/data/question-bank.json')).default;
  }
  return cache.questionBank;
}

// Similar for each asset. Only load what's needed per page.
```

### Scoring (scoring.ts)
```typescript
export function calculateScore(
  answers: Record<string, string>,  // { "1": "A", "2": "C" }
  answerKey: Record<string, string>,
  negativeMarking: boolean
): { correct: number; wrong: number; skipped: number; netScore: number } {
  let correct = 0, wrong = 0, skipped = 0;
  for (const [qNum, correctAns] of Object.entries(answerKey)) {
    const studentAns = answers[qNum];
    if (!studentAns) skipped++;
    else if (studentAns === correctAns) correct++;
    else wrong++;
  }
  const netScore = correct - (negativeMarking ? wrong * 0.25 : 0);
  return { correct, wrong, skipped, netScore };
}
```

### Mistake Detection (mistake-detector.ts)
```typescript
// After an exam, check which Mistake Patterns the student triggered
export function detectMistakes(
  wrongAnswers: { questionId: string; chosenOption: string; correctOption: string; misconceptionText: string }[],
  mistakePatterns: MistakePattern[]
): { patternId: string; patternName: string; occurrences: number }[] {
  // Match misconception keywords against mistake pattern keywords
  // Return sorted by occurrences descending
}
```

### Streak Management (streak.ts)
```typescript
interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastCompletedDate: string;  // ISO date
  freezesRemaining: number;
  freezesUsedThisWeek: number;
  weekStartDate: string;
}
// Store in localStorage under "mathspark_streak"
// On daily challenge completion: check if lastCompletedDate is yesterday → increment streak
// If missed a day and freezes > 0 → use freeze, maintain streak
// If missed and no freeze → reset to 0
```

### Leitner Spaced Repetition (spaced-repetition.ts)
```typescript
interface CardState {
  cardId: string;
  box: number;            // 1-5
  lastReviewed: string;   // ISO date
  nextReview: string;     // ISO date
}
// Box intervals: 1=today, 2=2days, 3=5days, 4=14days, 5=30days
// On "Got it ✅": move to next box (increase interval)
// On "Not sure 🤔": stay in same box
// On "Forgot ❌": move back to Box 1
// Daily deck = all cards where nextReview <= today
```

## What NOT to Do

- **Do NOT** generate math questions, answers, or solutions at runtime. ALL content comes from the JSON files.
- **Do NOT** use `localStorage` for question/paper data. It's too large. Use in-memory cache from dynamic imports.
- **Do NOT** build a backend or database yet. This is a frontend-first MVP. All state is localStorage + JSON files.
- **Do NOT** implement authentication yet. Single-student mode for now.
- **Do NOT** over-engineer. Use simple React state and Context before reaching for complex state management.
- **Do NOT** use dark mode by default. Light, friendly, colourful UI for kids.

## When Building Each Feature

Before building any feature, **read the relevant JSON file first** to understand the exact schema. The JSON files are the source of truth. The TypeScript types above are guides — if the JSON has extra fields, include them.

After building each feature, verify:
1. Questions display correctly with all 4 options
2. KaTeX formulas render properly (test with `\\frac{1}{2}`, `x^2`, `\\sqrt{144}`)
3. Answers are verified against the `answerKey` in the JSON
4. Sparky messages appear at appropriate moments
5. Mobile responsive layout works
6. The feature works offline (all data is local JSON)

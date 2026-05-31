# CLAUDE.md — MathSpark MVP Configuration

## Project Overview
MathSpark is a child-safe, kid-friendly math learning and IPM exam prep app for Grade 4 students in India. The app must NEVER hallucinate, use age-appropriate language, and feel warm and encouraging at all times.

## Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Database:** SQLite via Prisma ORM (file: `prisma/mathspark.db`)
- **Math Rendering:** KaTeX (`katex` npm package)
- **Styling:** Tailwind CSS
- **State:** React Context (no Redux)
- **Deployment:** Vercel (later)

## Project Structure
```
mathspark/
├── CLAUDE.md              ← this file
├── prisma/
│   ├── schema.prisma      ← database schema
│   ├── seed.ts            ← loads mathspark_complete_seed.json
│   └── mathspark.db       ← SQLite database (auto-created)
├── data/
│   └── mathspark_complete_seed.json  ← 2,345 questions (COPY HERE)
├── src/
│   ├── app/
│   │   ├── layout.tsx     ← root layout with bottom nav
│   │   ├── page.tsx       ← landing → redirects to /start or /chapters
│   │   ├── start/
│   │   │   └── page.tsx   ← onboarding + diagnostic quiz
│   │   ├── chapters/
│   │   │   └── page.tsx   ← chapter grid (21 chapters)
│   │   ├── practice/
│   │   │   └── [topicId]/
│   │   │       └── page.tsx  ← adaptive practice mode
│   │   └── dashboard/
│   │       └── page.tsx   ← student progress
│   ├── components/
│   │   ├── QuestionCard.tsx
│   │   ├── HintSystem.tsx
│   │   ├── StepByStep.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── ChapterGrid.tsx
│   │   └── BottomNav.tsx
│   ├── lib/
│   │   ├── db.ts          ← Prisma client
│   │   ├── adaptive.ts    ← adaptive problem picker
│   │   └── mastery.ts     ← mastery calculation
│   └── types/
│       └── index.ts       ← TypeScript interfaces
├── package.json
└── tailwind.config.ts
```

## Database Schema (Prisma)

```prisma
datasource db {
  provider = "sqlite"
  url      = "file:./mathspark.db"
}

generator client {
  provider = "prisma-client-js"
}

model Student {
  id        String   @id @default(cuid())
  name      String
  grade     Int      @default(4)
  createdAt DateTime @default(now())
  progress  Progress[]
  attempts  Attempt[]
}

model Topic {
  id            String   @id
  name          String
  chapterNumber String
  questions     Question[]
  progress      Progress[]
}

model Question {
  id              String   @id
  topicId         String
  topic           Topic    @relation(fields: [topicId], references: [id])
  subTopic        String
  difficulty      String   // "Easy" | "Medium" | "Hard"
  questionText    String
  questionLatex   String   @default("")
  option1         String
  option2         String
  option3         String
  option4         String
  correctAnswer   String   // "A" | "B" | "C" | "D"
  hint1           String   @default("")
  hint2           String   @default("")
  hint3           String   @default("")
  stepByStep      String   @default("[]")  // JSON string
  misconceptionA  String   @default("")
  misconceptionB  String   @default("")
  misconceptionC  String   @default("")
  misconceptionD  String   @default("")
  source          String   @default("hand_crafted")
  attempts        Attempt[]
}

model Progress {
  id        String   @id @default(cuid())
  studentId String
  student   Student  @relation(fields: [studentId], references: [id])
  topicId   String
  topic     Topic    @relation(fields: [topicId], references: [id])
  attempted Int      @default(0)
  correct   Int      @default(0)
  mastery   String   @default("NotStarted") // "NotStarted" | "Practicing" | "Mastered"
  updatedAt DateTime @updatedAt

  @@unique([studentId, topicId])
}

model Attempt {
  id         String   @id @default(cuid())
  studentId  String
  student    Student  @relation(fields: [studentId], references: [id])
  questionId String
  question   Question @relation(fields: [questionId], references: [id])
  selected   String   // "A" | "B" | "C" | "D"
  isCorrect  Boolean
  hintUsed   Int      @default(0) // 0, 1, 2, or 3
  timeTakenMs Int     @default(0)
  createdAt  DateTime @default(now())
}
```

### Local Setup (first time)
```bash
npm install
npx prisma generate
npx prisma db push        # creates tables in your Postgres DB
# After schema changes, apply to DB:
npx prisma db push
# Then visit /seed in the browser to load the 2,345 questions
# OR run: npm run db:seed (requires local DB access)
```

## Seed Script Behavior

The seed script (`prisma/seed.ts`) must:
1. Read `data/mathspark_complete_seed.json`
2. Create Topic records for each unique chapter
3. Create Question records from the JSON, mapping:
   - `options[0].text` → `option1`, `options[1].text` → `option2`, etc.
   - `hints[0]` → `hint1`, `hints[1]` → `hint2`, `hints[2]` → `hint3`
   - `stepByStep` → JSON.stringify the array
   - `misconceptions.A` → `misconceptionA`, etc.
   - Map question ID prefix to topicId (e.g., `Q_CH11_xxx` → topic `ch11`)
4. Use `upsert` so the script can be re-run safely

### Topic Mapping
```
ch01-05  → "Number System & Place Value"
ch06     → "Factors & Multiples"
ch07-08  → "Fractions"
ch09-10  → "Operations & BODMAS"
ch11     → "Decimal Fractions"
ch12     → "Decimal Units of Measurement"
ch13     → "Algebraic Expressions"
ch14     → "Equations"
ch15     → "Puzzles & Magic Squares"
ch16     → "Sequence & Series"
ch17     → "Measurement of Time & Calendar"
ch18     → "Angles"
ch19     → "Triangles"
ch20     → "Quadrilaterals"
ch21     → "Circle"
dh       → "Data Handling & Graphs"
```

## Content Bank Stats
- **Total questions:** 2,345
- **Hand-crafted:** 395 (IPM worksheet quality with full hints + solutions)
- **Auto-generated:** 1,950 (Python-computed answers, zero hallucination)
- **Difficulty:** 20% Easy, 45% Medium, 34% Hard
- **All IDs unique:** ✓ Validated

## Adaptive Engine Rules (`src/lib/adaptive.ts`)

```
function getNextQuestion(studentId, topicId):
  1. Fetch student's mastery for this topic and prerequisites
  2. Pick questions they haven't seen this session
  3. Distribution:
     - 70% from current ZPD (topics at 30-70% mastery)
     - 20% review (mastered topics, weighted by days since last attempt)
     - 10% stretch (one difficulty above current)
  4. Streak adjustments:
     - 3 wrong in a row → drop difficulty by 1 level
     - 5 right in a row → increase difficulty by 1 level
  5. Never repeat same question within a session
```

## Mastery Calculation (`src/lib/mastery.ts`)

```
Based on last 10 attempts per topic:
- >= 80% correct → "Mastered"
- >= 40% correct → "Practicing"
- < 40% correct  → "NotStarted"
```

## UI/UX Rules — CRITICAL

### Kid-Friendly Tone (NON-NEGOTIABLE)
- **NEVER say:** "Wrong!", "Incorrect!", "Failed", "Error", "You got it wrong"
- **ALWAYS say:** "Not quite — let's think about this together!", "Almost! Here's a hint.", "Good try! Let's look at it another way."
- **On correct:** Randomly pick from: "Great job! ⭐", "You got it! 🎯", "Excellent thinking! 🧠", "Well done! 🌟", "Awesome! 🎉"
- **On streak:** "You're on fire! 🔥" (3 in a row), "Unstoppable! ⚡" (5 in a row)

### Hint System (3 levels, progressive)
1. **Level 1** (auto-show on wrong answer): Strategic hint — "Think about what type of problem this is"
2. **Level 2** (button: "Need more help?"): Procedural hint — "Try this first step..."  
3. **Level 3** (button: "Show me how"): Worked example — similar solved problem, NOT the actual answer

### Step-by-Step Solution
- Only shown AFTER student answers (right or wrong)
- Each step in its own card/accordion
- Math rendered with KaTeX
- Green highlight for what changed between steps

### Mobile-First Design
- Minimum touch target: 48px height for all buttons
- Question fills the screen, options are large cards
- No horizontal scrolling
- Progress bar at top
- Bottom navigation: 📚 Chapters | 🎯 Practice | 📊 Dashboard
- Font: clean sans-serif, minimum 16px for body text
- Colors: bright but not overwhelming, high contrast

### Onboarding Flow (/start)
1. Welcome: "Hi! Let's find out what you already know! 🌟"
2. Name input (first name only, one field, large)
3. Diagnostic quiz: 15 questions
   - Start at Medium difficulty, Chapter 11
   - Correct → harder / next chapter
   - Wrong → easier / same chapter  
   - Cover at least 6 different chapters
   - Progress bar, no visible timer
4. Results: "Wow, you already know a lot! 🎉"
   - Visual grid: ✅ Strong, 🟡 Learning, ⬜ Not Yet
   - Celebrate strengths FIRST
   - "Ready to start? Let's go!" → /chapters

### Dashboard (/dashboard)
- Greeting: "Hi [name]! 🌟"
- Stats: total solved, streak days, topics mastered
- Topic grid: green/amber/gray per chapter
- "Continue learning" → weakest topic
- Weekly bar chart: questions per day

## Safety & Content Rules (NON-NEGOTIABLE)

1. **No math answer reaches a child without verification.** Every answer in the database is either human-verified (hand-crafted) or Python-computed (auto-generated). The app displays ONLY pre-verified answers.
2. **No LLM-generated answers at runtime.** The app does NOT call any AI API to generate math answers. All content is pre-loaded from the seed file.
3. **No user-generated content.** Students cannot input content that other students see.
4. **No social features in MVP.** No chat, no messaging, no profiles visible to others.
5. **No data collection beyond name and answers.** No email, no phone, no location.
6. **Session-based auth in MVP.** No account creation required. Just first name + progress stored locally.

## Build Order (Sequential Prompts)

1. Scaffold Next.js + Prisma + SQLite + Tailwind
2. Create schema + seed script + load all 2,345 questions
3. Build /chapters page (chapter grid with mastery colors)
4. Build /practice/[topicId] (question card + options + hints + solution)
5. Build adaptive engine (getNextQuestion with ZPD logic)
6. Build /start (onboarding + diagnostic quiz)
7. Build /dashboard (stats + progress + streak)
8. Polish: bottom nav, PWA manifest, loading skeletons, page transitions

# CLAUDE.md — MathSpark MVP Configuration

## Project Overview
MathSpark is a child-safe, kid-friendly math learning and IPM exam prep app for Grade 4 students in India. The app must NEVER hallucinate, use age-appropriate language, and feel warm and encouraging at all times.

## Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Database:** PostgreSQL (Neon) via Prisma ORM — connection via `DATABASE_URL` env var
- **Math Rendering:** KaTeX (`katex` npm package)
- **Styling:** Tailwind CSS
- **State:** Local component state + localStorage (no Redux, no Context)
- **Deployment:** Vercel (configured — `vercel.json` present)

## Project Structure
```
mathspark/
├── CLAUDE.md              ← this file
├── vercel.json            ← Vercel deployment config
├── prisma/
│   ├── schema.prisma      ← database schema (PostgreSQL)
│   └── seed.ts            ← CLI seed script (local dev only)
├── data/
│   └── mathspark_complete_seed.json  ← 2,345 questions
├── src/
│   ├── app/
│   │   ├── layout.tsx     ← root layout with bottom nav
│   │   ├── page.tsx       ← landing → redirects to /start or /chapters
│   │   ├── start/
│   │   │   └── page.tsx   ← onboarding + diagnostic quiz
│   │   ├── chapters/
│   │   │   └── page.tsx   ← chapter grid (16 topics)
│   │   ├── practice/
│   │   │   ├── page.tsx   ← smart redirect to weakest topic
│   │   │   └── [topicId]/
│   │   │       └── page.tsx  ← adaptive practice mode
│   │   ├── dashboard/
│   │   │   └── page.tsx   ← student progress
│   │   ├── seed/
│   │   │   └── page.tsx   ← admin UI for web-based seeding
│   │   └── api/
│   │       ├── students/
│   │       │   ├── route.ts      ← POST create student
│   │       │   └── [id]/route.ts ← GET student by id
│   │       ├── topics/route.ts   ← GET all 16 topics
│   │       ├── progress/route.ts ← GET progress by studentId
│   │       ├── attempts/route.ts ← POST record attempt
│   │       ├── diagnostic/route.ts ← GET diagnostic question
│   │       ├── dashboard/route.ts  ← GET full dashboard data
│   │       ├── questions/
│   │       │   └── next/route.ts ← GET adaptive next question
│   │       └── seed/route.ts     ← GET paginated seed (secret-protected)
│   ├── components/
│   │   ├── QuestionCard.tsx
│   │   ├── HintSystem.tsx
│   │   ├── StepByStep.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── ChapterGrid.tsx
│   │   ├── BottomNav.tsx
│   │   └── KatexRenderer.tsx
│   ├── lib/
│   │   ├── db.ts          ← Prisma client singleton
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
  provider = "postgresql"
  url      = env("DATABASE_URL")
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

## Environment Variables

| Variable       | Required | Description |
|----------------|----------|-------------|
| `DATABASE_URL` | Yes      | PostgreSQL connection string (e.g. Neon: `postgresql://user:pass@host/db`) |
| `SEED_SECRET`  | Yes      | Passphrase to authorize the `/api/seed` endpoint |

For local dev, create a `.env` file in the project root (already `.gitignore`d):
```
DATABASE_URL="postgresql://user:pass@host/db"
SEED_SECRET="any-secret-string"
```

### Local Setup (first time)
```bash
npm install
npx prisma generate
npx prisma db push        # creates tables in your Postgres DB
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

### Web-Based Seeding (Production / Vercel)
The CLI seed script requires direct DB access. For production Vercel deployments, use the paginated web seeder instead:
1. Deploy the app with `DATABASE_URL` and `SEED_SECRET` env vars set in Vercel
2. Visit `/seed` in the browser
3. Enter your `SEED_SECRET` value and click "Start Seeding"
4. The UI polls `GET /api/seed?secret=&page=N` until all 2,345 questions are loaded (75 questions/request, ~32 requests, within Vercel's 300s function limit)

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

## Adaptive Engine — Current Implementation (`src/lib/adaptive.ts`)

```
function getNextQuestion(studentId, topicId, seenIds, consecutiveWrong, consecutiveRight):
  1. Fetch student's mastery for this topic from the Progress table
  2. Base difficulty:
       NotStarted → Easy
       Practicing → Medium
       Mastered   → Hard
  3. Streak adjustments:
       consecutiveWrong >= 3 → drop difficulty one level
       consecutiveRight >= 5 → raise difficulty one level
  4. Find first unseen question at target difficulty (orderBy id asc — deterministic)
  5. Fallback: if none at target difficulty, return any unseen question in the topic
  6. Return null if all questions seen (session complete)

NOTE: Session state (seenIds, consecutiveWrong, consecutiveRight) is maintained
client-side and passed as query params on each request. The server is stateless.
```

**Planned but not yet implemented:**
- 70% ZPD / 20% review / 10% stretch difficulty distribution
- Cross-topic prerequisite graph
- Randomized question ordering (currently deterministic by question ID)

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

## Build Status

### ✅ Complete
1. Scaffold Next.js + Prisma + PostgreSQL (Neon) + Tailwind
2. Schema + CLI seed script + web seeder (`/seed` page + `/api/seed` route)
3. `/chapters` — chapter grid with mastery colours (green/amber/gray)
4. `/practice/[topicId]` — question card, 4 options, 3-tier hints, step-by-step KaTeX, misconception feedback
5. Adaptive engine — mastery-based difficulty + streak + 70/20/10 ZPD distribution + Fisher-Yates shuffle
6. `/start` — onboarding + 15-question diagnostic quiz covering all 16 topics with adaptive difficulty
7. `/dashboard` — stats (solved, mastered, streak), weekly bar chart, topic grid, "Continue learning" CTA, reset progress button
8. `/offline` — kid-friendly offline fallback page
9. Bottom nav (hidden on `/`, `/start`, `/seed`)
10. Full REST API layer — 10 routes under `/api/` (including `POST /api/progress/reset`)
11. Server-side `isCorrect` computation — attempts route verifies answer independently
12. SEED_SECRET in POST body — never in URL or logs
13. Attempt error handling — retry banner shown on failure; fire-and-forget removed
14. Session-state persistence — `seenIds`/cw/cr stored in `sessionStorage` per topic; survives hard refresh
15. Question randomization — Fisher-Yates shuffle on each pool fetch (no deterministic order)
16. DB performance indexes — on `Attempt(studentId)`, `Attempt(studentId, createdAt)`, `Attempt(questionId)`, `Question(topicId)`, `Question(topicId, difficulty)`
17. Accessibility — ARIA roles, labels, `aria-pressed`, `aria-expanded`, `aria-current` across all components
18. Kid-friendly error boundaries — `error.tsx` + `global-error.tsx` with encouraging copy
19. PWA — `manifest.json`, 192px + 512px icons, service worker with offline cache-first strategy
20. Rate limiting — in-memory sliding-window middleware (60 req/min per IP) on all `/api/*` routes
21. Structured logging — `src/lib/logger.ts` + `src/lib/withLogging.ts` for JSON-line observability
22. Test suite — 45 unit/integration tests (Vitest): adaptive engine, mastery calculation, API routes
23. CI/CD — GitHub Actions pipeline: test + typecheck + build on every push
24. Lockfile — `package-lock.json` committed for reproducible installs

### ⬜ Remaining
- **Full ZPD cross-topic prerequisites** — topic graph and prerequisite-aware sequencing
- **Page transitions / animations** — Framer Motion or CSS transitions between questions
- **Sentry / external error monitoring** — requires SENTRY_DSN; structured logging is in place as foundation
- **Rate limiting at scale** — current in-memory map resets on cold start; Upstash Redis needed for multi-instance

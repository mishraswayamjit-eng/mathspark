# CLAUDE.md — MathSpark / Socratic Configuration

## CRITICAL: No Local Node.js

**The developer does NOT have Node.js installed locally. NEVER instruct to run `npm`, `npx`, `node`, `prisma`, or any Node-based CLI command.**

All build, migration, and seeding happens on Vercel automatically:
- `vercel.json` buildCommand: `prisma generate && prisma db push --accept-data-loss && next build`
- Pushing to `main` triggers Vercel → schema migrates → app builds → deploys
- Database seeding: call `GET /api/seed?secret=SEED_SECRET&page=0` (paginated, 200 per batch)

**The development loop is: edit code → git push → Vercel deploys → test in browser.**

## Project Overview
MathSpark (Socratic) is a child-safe, kid-friendly math learning and IPM exam prep app for Indian students (Grades 2-9). The app must NEVER hallucinate, use age-appropriate language, and feel warm and encouraging at all times.

## Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Database:** PostgreSQL (Neon) via Prisma ORM
- **Math Rendering:** KaTeX (lazy-loaded in `KatexRenderer` component)
- **Styling:** Tailwind CSS with `duo-*` design tokens
- **Auth:** JWT cookies via `jose` (`src/lib/studentAuth.ts`)
- **Deployment:** Vercel (auto-deploy on push to `main`)

## Deployment & Database Workflow

### Schema Changes (Prisma)
1. Edit `prisma/schema.prisma`
2. Commit and push to `main`
3. Vercel runs `prisma db push` automatically during build
4. **NEVER tell the user to run `npx prisma db push` locally**

### Seeding Data
- API route: `GET /api/seed?secret=xxx&page=0` (upserts questions in batches of 200)
- Test data: `GET /api/seed-test?secret=xxx`
- Static JSON data (lessons, skill-drills, etc.) is bundled via `outputFileTracingIncludes` in `next.config.mjs`

### Adding New Data Files
When adding JSON files to `data/`:
1. Create the file
2. Add the API route that reads it with `fs.readFileSync` + in-memory cache
3. Add to `next.config.mjs` `outputFileTracingIncludes` so Vercel bundles it
4. Commit and push — Vercel handles the rest

## Key Architecture

| Component | Location | Purpose |
|-----------|----------|---------|
| Student auth | `src/lib/studentAuth.ts` | JWT cookie, `getAuthenticatedStudentId()` |
| Rate limiting | `src/lib/rateLimit.ts` | In-memory `checkRateLimit()` |
| Body validation | `src/lib/validateBody.ts` | `validateBody()` + `ValidationError` |
| XP / Leaderboard | `src/lib/leaderboard.ts` | `addWeeklyXP()` in `$transaction` |
| Shared utils | `src/lib/sharedUtils.ts` | `TOPIC_ORDER`, `computeStreak` |
| Topic colors | `src/data/topicColors.ts` | Extracted color map |
| Flashcard hook | `src/hooks/useFlashcardDeck.ts` | Shared deck fetch pattern |
| Design tokens | `tailwind.config.ts` | `duo-green`, `duo-blue`, `duo-orange`, `duo-red`, `duo-gold`, `duo-dark` |

## UI/UX Rules — CRITICAL

### Kid-Friendly Tone (NON-NEGOTIABLE)
- **NEVER say:** "Wrong!", "Incorrect!", "Failed", "Error"
- **ALWAYS say:** "Not quite — let's think about this together!", "Almost! Here's a hint."
- **On correct:** "Great job! ⭐", "You got it! 🎯", "Excellent thinking! 🧠"

### Mobile-First Design
- Minimum touch target: 48px height for all buttons
- `max-w-lg mx-auto px-4` centered container
- Sticky header: `bg-duo-dark px-4 py-4`
- Cards: `bg-white rounded-2xl p-4 border border-gray-100 shadow-sm`
- Transitions: `active:scale-[0.98] transition-transform`
- Loading: `animate-pulse` skeletons
- Page entry: `animate-fade-in`
- Bottom padding: `pb-24` (for BottomNav)

### Accessibility
- `aria-hidden="true"` on decorative emojis
- `aria-label` on icon-only buttons and inputs
- WCAG contrast: avoid `text-white/30`, use `/60` or `/70` minimum
- `@media (prefers-reduced-motion: reduce)` in `globals.css`

## Safety & Content Rules (NON-NEGOTIABLE)

1. No math answer reaches a child without verification — all content is pre-verified
2. No LLM-generated answers at runtime
3. No user-generated content visible to other students
4. Server-side grading only (never trust client answers)
5. All student API routes use `getAuthenticatedStudentId()` cookie auth
6. Rate limiting on all POST endpoints
7. `validateBody()` on all POST request bodies

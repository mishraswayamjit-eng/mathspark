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
2. No LLM-generated answers at runtime for **graded practice**. Grading is always 100% deterministic and server-side; the LLM is NEVER the arbiter of correctness.
3. No user-generated content visible to other students
4. Server-side grading only (never trust client answers)
5. All student API routes use `getAuthenticatedStudentId()` cookie auth
6. Rate limiting on all POST endpoints
7. `validateBody()` on all POST request bodies

### Truth vs Delivery — permitted LLM usage (amendment)

The LLM may expand the *teaching delivery* (explaining, rephrasing, coaching,
narrating), but math **truth** (correct answers, grading, valid steps, mastery)
stays deterministic. Specifically:

- **Grounded re-expression of already-verified content is permitted.** Re-wording
  a verified answer/steps/misconception for clarity does not change the truth, so
  it is allowed (Features 1–4: misconception nudge, session/report narrative,
  lesson re-explain, stuck-coach). These are always grounded in verified data and
  must never contradict it.
- **Fresh/homework solving (5a) is permitted only behind self-consistency
  verification** (N-sample majority agreement) **and an explicit "double-check
  this yourself" disclaimer.** It is never fed into graded practice. Gated by
  `AI_SOLVE_ENABLED`.
- **AI-authored questions (5b) are permitted only when tagged
  `source='ai_generated'`**, kill-switchable (`AI_QUESTIONS_SERVE`), excluded
  from mock tests entirely, and ranked last in adaptive selection. An optional
  sanity self-check (`AI_QUESTIONS_SANITY`) runs before persist.
- **Surfacing/narration (5c) decides presentation only.** The numbers come from
  the deterministic Brain Engine; the LLM only orders/explains them. Gated by
  `AI_SURFACE_ENABLED`.

All LLM usage goes through the single `src/lib/llm/` seam and degrades gracefully
(static fallback) when `ANTHROPIC_API_KEY` is unset.

---

# Codebase Cleanup Protocol — 7-Track Low-Risk Pass

## MISSION

Clean up the codebase and improve code quality through a careful, low-risk cleanup pass. Work in **7 focused tracks**, executed sequentially. This is not a rewrite — it is a surgical cleanup.

## OPERATING PRINCIPLES (apply to every track)

1. **Inspect before you touch.** Read the code thoroughly before proposing any change.
2. **Write a critical assessment first.** For each track, produce a written analysis of what was found, the risks, and the trade-offs — before editing anything.
3. **Rank every proposed change by confidence (High / Medium / Low) and risk (Low / Medium / High).**
4. **Implement ONLY High-confidence, Low-risk changes.** Everything else goes in a "Deferred" list with reasoning, for manual review.
5. **Small, atomic commits per track.** One logical change per commit, with a clear message. Never bundle tracks.
6. **Run all checks after every track**: typecheck, lint, tests, build. If anything breaks, stop and report — do not "fix forward" without approval.
7. **Preserve behavior.** This is cleanup, not refactoring-for-its-own-sake. If a change alters observable behavior, it is out of scope.
8. **No new abstractions** unless removing one. No new dependencies. No framework changes.
9. **When in doubt, leave it alone** and add it to the Deferred list.

## TRACK 1 — DEDUPLICATION
Scan the codebase for repeated logic, copy-pasted functions, and redundant abstractions. Consolidate only where DRY genuinely simplifies. Do not merge code that merely LOOKS similar but serves different purposes. Defer cases requiring new parameters/flags/branches inside the shared function.

## TRACK 2 — TYPE CONSOLIDATION
Find duplicated type/interface/schema definitions. Merge into a single source of truth using the existing repo convention. Defer types that belong to different bounded contexts.

## TRACK 3 — DEAD CODE REMOVAL
Use static analysis (`knip`, `ts-prune`, `depcheck`) to find unused exports. Manually verify before removing (dynamic imports, string-based references, framework conventions, codegen, tests, public API). Remove only what is CONFIRMED dead.

## TRACK 4 — CIRCULAR DEPENDENCIES
Use `madge` / `dpdm` to map the dependency graph. Untangle by extracting shared logic into neutral modules. Do NOT introduce new abstractions/indirection layers just to break a cycle.

## TRACK 5 — TYPE STRENGTHENING
Find every `any`, weak `unknown`, `object`, `Function`, `@ts-ignore`, `@ts-expect-error`. Replace with strong types. Run typecheck after every batch. PRESERVE legitimate `unknown` at trust boundaries and well-justified `any` escape hatches.

## TRACK 6 — ERROR HANDLING CLEANUP
Classify every `try/catch` as: real boundary (keep), silent swallow (remove/surface), or over-defensive (remove). No error hiding. No silent fallbacks. Where fallback is genuinely needed, add explicit logging.

## TRACK 7 — FINAL VERIFICATION
Typecheck, lint, tests, build, dependency audit, bundle size diff, and a grouped-by-track diff summary.

## DELIVERABLES (per track)
1. Assessment document (findings ranked by confidence + risk)
2. Change list (file paths + one-line reason)
3. Deferred list (what was intentionally NOT done, and why)
4. Verification output

## CONSTRAINTS
- Do not proceed to the next track until the current one is complete, committed, and all checks pass.
- If any check fails mid-track, stop and report before fixing.
- If a track produces zero high-confidence low-risk changes, say so explicitly — do not manufacture changes.
- Ask before touching: public APIs, database schemas, migration files, CI config, or deployment code.
- **Node.js constraint still applies:** typecheck/lint/tests/build cannot be run locally. Verification will be via git push → Vercel build logs, or by asking the user to run checks.

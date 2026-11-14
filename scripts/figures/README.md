# Question figures: build brief

Read this first if you are building any part of the question-figure feature.

## What we are building

Every question screen gets a second pane.

- **Before the child answers** it shows the figure the question needs: givens only, the unknown marked "?".
- **After they answer** (practice and review, never during a mock test) it walks through the solution one step at a time, and the figure is redrawn for each step.
- **Questions with no figure** show the same steps as text. Before answering, their pane holds hints and a pencil pad.

Nothing is generated while a child uses the app. Figures are produced offline, checked by a script, and stored in the repo.

## The contract (do not change these without telling the lead)

| File | What it is |
|---|---|
| `src/lib/figures/types.ts` | Every figure type, `QuestionVisual` (stored) and `ServedVisual` (sent to screens). Read all of it. |
| `scripts/figures/validate.py` | The checker. Mirrors `types.ts`. `--build` writes the served file. |
| `scripts/figures/examples.json` | Two worked examples that pass the checker. |
| `data/question-figures/parts/*.json` | Content. One JSON object per file: `{ "<question id>": QuestionVisual }`. |
| `src/data/questionFigures/figures.json` | Built output. Never edit by hand. |
| `src/lib/figures/lookup.ts` | Server-only: `visualFor(id, { withSolution })`, `withVisual(question, { withSolution })`. |
| `src/components/figures/FigureView.tsx` | `<FigureView spec={...} className? />`: the one component that draws a figure. Currently a placeholder. |
| `Question.visual` in `src/types/index.ts` | Optional `ServedVisual` on a question sent to the browser. |

If the contract is missing something you need, do not invent a private extension. Work within it, and say what was missing in your final report.

## Rules for figures (the checker enforces these)

1. The before-answering `figure` shows **givens only**: every number in it is in the question text. Mark the unknown "?". Never show the answer.
2. A step figure shows only numbers stated in the question, the answer choices, or the steps up to and including its own.
3. `stepFigures` has exactly one entry per step in the question's own `stepByStep`, `null` where a step needs no picture.
4. `steps` (a full solution) is only for questions with no `stepByStep`, only with `origin: "rule"`, computed in Python, and the last step must state the correct answer.
5. `usesOptions: true` when the figure needs numbers from the answer choices.
6. `essential: true` (authored only) when the question cannot be answered without the figure and its text lacks the figure's data. The figure is then rebuilt from the answer key and listed for human review.
7. Draw honestly. "Base 20 cm, height 7 cm" is a general triangle with a dashed height, not a right-angled triangle, unless the question says so.
8. A figure is not required. If a picture would not help a child see the question, leave the question out. Do not force one.
9. Labels at most 18 characters, notes at most 70. Never use "wrong", "incorrect", "failed" or "error".

Run the checker on your own part file until it passes:

    python -X utf8 scripts/figures/validate.py --part data/question-figures/parts/<yours>.json

Question data is in `data/mathspark_complete_seed.json` under `questions`: `id`, `topicId` (`grade5`), `subTopic`, `questionText`, `options` (`[{id, text}]`), `correctAnswer`, `stepByStep` (`[{step, text, latex}]`), `source`.

## This machine and this codebase

- **No Node.js.** You cannot run `npm`, `npx`, `node`, `tsc`, `eslint` or `next`. Do not try, and do not suggest it. TypeScript is only compiled later on Vercel, so write carefully and re-read your own code for type errors.
- **Python 3.13 is available.** On Windows, run it as `python -X utf8` so Unicode prints.
- Shell is Git Bash. Quote every path: the home folder contains a space.
- TypeScript is strict and the target is ES5: no regex `u` or `s` flags, no lookbehind, no `for...of` over a `Map` or `Set` (use `Array.from` or index loops), no `Array.prototype.at`.
- ESLint is `next/core-web-vitals`: escape apostrophes in JSX text (`&apos;`), no unused `eslint-disable` comments.
- Design system: read `design/DESIGN.md`, especially "Diagrams and the whiteboard". Use the role tokens (`ink`, `ink-muted`, `canvas`, `card`, `soft`, `line`, `action`, `success`, `star`, `hint`), `rounded-card` / `rounded-control` / `rounded-tile`, 2px borders. SVG colours come from `C` in `src/components/visuals/parts.tsx`. The whiteboard visuals in `src/components/visuals/` are the style reference for drawings.
- Every button is at least 48px tall. Decorative emoji get `aria-hidden="true"`. Icon-only buttons get an `aria-label`.
- Child-facing copy is warm and never says "Wrong", "Incorrect", "Failed" or "Error".
- Grading stays on the server and deterministic. Nothing in this feature changes XP, mastery or grading.
- Do not run `git add -A`: the repo has untracked files that must stay uncommitted. Add your own files by name.
- Do not push. Commit your work on your branch with a clear message and stop.
- Never write secrets into files. Do not read `.env.local`.

## Who owns which files

Only edit files in your own row. Read anything.

| Workstream | Owns |
|---|---|
| Renderer | `src/components/figures/FigureView.tsx`, new files under `src/components/figures/kinds/`, `src/app/(app)/dev/figures/page.tsx`, `src/app/api/figures/gallery/route.ts` |
| Templated content | `scripts/figures/templated.py`, `scripts/figures/audit_missing.py`, `data/question-figures/parts/templated.json`, `data/question-figures/missing-figure-audit.json` |
| Past papers A | `data/question-figures/parts/finals-2016-2020.json` (+ any helper script under `scripts/figures/authoring/a_*.py`) |
| Past papers B | `data/question-figures/parts/finals-2021-2025.json` (+ `scripts/figures/authoring/b_*.py`) |
| Extracted questions | `data/question-figures/parts/extracted.json` (+ `scripts/figures/authoring/c_*.py`) |
| Practice pane | `src/app/(app)/practice/[topicId]/page.tsx`, new files `src/components/figures/WorkPane.tsx`, `src/components/figures/StepPlayer.tsx`, `src/components/figures/ScratchPad.tsx`, `src/app/api/questions/next/route.ts`, `src/app/api/questions/similar/route.ts` |

The lead merges the branches, runs `validate.py --build`, and pushes one preview build.

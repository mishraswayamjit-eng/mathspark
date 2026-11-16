# Teach mode: build brief

Read this first if you are building any part of "Explain it to me".

## What we are building

The aim is the best maths tutor a Grade 5 child (about 10 years old, in India) could have. Today the app can read a question and its printed solution aloud. That is narration, and it is not teaching. A real teacher does something different, and the two reference lessons the product owner gave us show it:

- **A handwritten equation.** The teacher writes `4(3x − 5) − 2(x + 7) = 3x + 15`, draws two arcs from the 4 into the bracket as they say "4 times 3x, and 4 times minus 5", writes the next line, crosses out the `3x` on the right with a small "−3x" above it as they take it from both sides, draws a bar under both sides to divide by 7, and rings `x = 7`.
- **A place-value lesson.** The teacher writes 825,046 under a place-value chart and asks "Which digit is in the thousands place?", waits, underlines the 5 and labels it, then asks "What is the value of the 2?" and writes 20,000, showing where the zeros come from. "Isn't that cool?"

What they share:
1. One move at a time. Say what you are doing and why, and show it on the board at the same moment.
2. The board is marked, not just written: arcs, strike-throughs with a note, underlines, a ring round the answer.
3. The child is asked what comes next before it is shown.
4. Warm, short, spoken sentences. The teacher is talking with a child, not reading a textbook.
5. It ends with a check and the method in one line.

There are three parts to the product:

- **Explain it to me (teach mode).** After a child answers a practice question (or asks for help), a lesson plays in the right-hand pane: the teacher's voice, and a board that is written and marked in step with it. Lessons are written offline, one per question, and checked by `scripts/teach/validate.py`.
- **The tutor's voice the rest of the time.** Outside teach mode the tutor does not lecture. It reacts to what the child does: a right answer, a miss, a hint, a long pause. Short, specific, never the same line twice in a row.
- **The live board coach.** The child can work on a pencil pad with a stylus, finger or mouse. When they pause, an AI model looks at what they have written and the tutor says, in a sentence or two, what to do next.

## The contract (do not change these without telling the lead)

| File | What it is |
|---|---|
| `src/lib/teach/types.ts` | `TeachScript`, `TeachBeat`, `BoardOp`, `BeatAsk`. Read all of it. |
| `scripts/teach/validate.py` | The checker for lessons. `--part <name>`, `--show <question id>`, `--build`. |
| `scripts/teach/example.json` | One complete lesson that passes the checker. Read it before writing any. |
| `data/teach/parts/<name>.json` | Lessons: `{ "<question id>": TeachScript }`. |
| `src/data/teach/scripts.json` | Built output. Never edit by hand. |
| `src/lib/teach/lookup.ts` | Server-only: `teachFor(questionId)`. |
| `src/components/teach/WorkingBoard.tsx` | `<WorkingBoard ops={...} animateFrom={n} beatMs={ms} />`: draws the board. Placeholder today. |
| `src/lib/tutor/reactions.ts` | `tutorLine(event, ctx)`: what the tutor says in reaction to something. Placeholder today. |
| `src/hooks/useTutorVoice.ts` | `useTutorVoice()`: speaks tutor lines. Placeholder today. |

A placeholder's exported names and props are the contract other workstreams build on: replace the body, never the signature. If the contract is missing something you need, work within it and say what was missing in your report.

## How the teacher sounds

The teacher is Sparky: a kind, quick, slightly playful teacher who loves maths and likes this child.

- **Talk, do not read.** "Here is our equation." "So, what is in the way?" "Nearly there." Use "we" and "you". Contractions are fine.
- **One idea per beat, one or two sentences.** If a beat needs a third sentence, it is two beats.
- **Say why, not only what.** Not "Add 11 to both sides." but "To undo minus 11, we add 11. And to keep the balance level, we add it to both sides."
- **Ask before you tell.** At the one or two turning points of the solution, stop and ask the child to choose the next move. Make the other choices the slips children really make (the question's own misconception texts, where it has them, tell you what those are). After a miss, never say "wrong" or "no": say what to look at again, then carry on.
- **Name the trap.** If there is a classic slip in this kind of question, say it at the moment it would happen: "Careful here: the minus 2 multiplies the 7 as well, so that is minus 14."
- **Sound pleased, in moderation.** One "There is our hidden number!" is charming. Praise in every beat is noise.
- **Check, then sum up.** Put the answer back into the question to show it works, then give the method in one sentence the child can reuse.
- **Speakable words only.** What the teacher says is spoken by a text-to-speech voice. Write "4 x, minus 11, equals 5", never "4x − 11 = 5". Numbers stay as digits. Units in full. Commas where a breath goes.
- **Say only numbers the child can see.** Anything the teacher says must be in the question or already written on the board by the end of that beat. So write it, then say it (in the same beat is fine).

## How the board is used

- The first thing written is the question itself (`tone: "given"`). Working is `tone: "work"` (the default). The final answer is written with `tone: "answer"` and ringed.
- A line is maths as it would be written by hand: `4x − 11 = 5`, `3/4 + 1/8 = 7/8`, `25% of 240 = 60`, `5² = 25`. Use `−`, `×`, `÷`. Keep a line under 60 characters; split long working over two lines.
- A line of words (a formula in words, a label) needs `label: true`: `Area = length × breadth`.
- Mark the board while you talk: `arc` when a number multiplies into a bracket; `strike` with a `note` when a term is moved or cancelled; `both` when the same thing is done to both sides; `divide` for dividing both sides; `group` to gather like terms; `mark` to underline, box or ring; `note` for a small label. A lesson with no marks at all is just dictation.
- Use `figure` to put a picture from the figure library beside the working when the idea is easier to see than to write (a bar model for a ratio, fraction bars, a place-value chart, a triangle). Figure types are in `src/lib/figures/types.ts`.
- The checker verifies every maths line: an equation with the unknown must hold when the answer is put in (`check: { variable, value }`), and a sum with no unknown must be exactly true. So the board cannot show a false line.

## Writing lessons for a topic

Question data is in the bank, `data/bank/grade5/` (one file per topic; see `scripts/bank/README.md`). Read it only through `scripts/bank/bank.py` (`bank.load_pool("grade5")`), never by opening the files. Each question has: `id`, `node` (its topic), `subTopic`, `questionText`, `options`, `correctAnswer`, `hints`, `stepByStep`, `misconceptions`, `source`. The steps were recently rewritten and are sound: build the lesson on them. Your lesson must reach the keyed answer.

- **Generated families** (ids starting `VAR_`, `VAR2_`, `BOOST_`, `PH3_`) share a wording, so write the lesson once per wording as a Python rule that fills in the numbers, computes every line, and adapts the words to the case (a plus or a minus, a divide that leaves 1, a zero). Vary the phrasing across a family with a few alternatives picked by a stable hash of the question id, so a child doing five in a row does not hear the same sentences five times.
- **One-off questions** (past papers `EXT_G5_FP_...`, worksheets `EXT_G5_WS_...`) each need a lesson written for that question.
- Put your script(s) in `scripts/teach/gen/`, named after your part, writing `data/teach/parts/<your part>.json`.
- Check often: `python -X utf8 scripts/teach/validate.py --part <your part>`. Read lessons the way a child would hear them with `python -X utf8 scripts/teach/validate.py --show <question id>`.
- Passing the checker is the floor. Before you finish, read at least 30 whole lessons across every wording in your part and fix anything you would not say to a child.

## This machine and this codebase

- **No Node.js.** You cannot run `npm`, `npx`, `node`, `tsc`, `eslint` or `next`. TypeScript is compiled later on Vercel, so write carefully and re-read your own code for type errors.
- **Python 3.13**, run as `python -X utf8`.
- **Nobody is watching this run, so a command that asks for permission will hang.** Use ONLY the Read, Edit and Write tools for files, and plain single commands from the repo root (`python -X utf8 <script> <args>`). Do NOT use heredocs, `python -c`, `cd ... &&` chains, pipes or redirects. Run no git command at all.
- Several agents are working in this folder at once. Edit only the files your brief gives you. Never edit, move or delete anything else.
- Work in small steps: several small edits, never one enormous write.
- TypeScript is strict and the target is ES5: no regex `u` or `s` flags, no lookbehind, no `for...of` over a `Map` or `Set`, no `Array.prototype.at`. ESLint is `next/core-web-vitals`: escape apostrophes in JSX text (`&apos;`).
- Design system: `design/DESIGN.md`. Role tokens (`ink`, `ink-muted`, `canvas`, `card`, `soft`, `line`, `action`, `success`, `star`, `hint`), `rounded-card` / `rounded-control` / `rounded-tile`, 2px borders. SVG colours from `C` in `src/components/visuals/parts.tsx`. Every button at least 48px tall. Decorative emoji get `aria-hidden="true"`.
- Child-facing words are warm and never include "wrong", "incorrect", "failed" or "error".
- Grading stays on the server and deterministic. Nothing in this feature changes XP, mastery or grading, and an AI model is never the judge of whether an answer is right.
- Never write secrets into files. Do not read `.env.local`. Quote every path: the home folder contains a space.

## Your report

What you built; what you read or checked and how much; what you could not do; anything in the contract that was missing; and, for TypeScript, the parts least sure to compile.

# Question fixes: build brief

Read this first if you are fixing hints or steps in the Grade 5 question bank.

## What this is

Children aged about 10 practise maths questions in this app. Each question has three hints and a step-by-step solution. A close read of the bank found content that should not reach a child:

- **Generic hints** that say nothing about the question ("Read the question carefully", "Check your answer by substituting back").
- **Thinking aloud** left in from when the content was drafted ("Hmm, but let me check again... But option C is 22 not A").
- **Filler steps** ("The answer is option B", "Apply the relevant formula").
- **Hints that belong to a different question** (a simple-interest example on a fractions question).
- **Hints that state the answer**, and sums written out that are not true.

Your job is to replace that content with hints and steps a good teacher would give for that exact question.

## How a fix is recorded

You do not edit the question bank. You write a part file, `data/question-fixes/parts/<your part>.json`:

    {
      "<question id>": {
        "hints": ["hint 1", "hint 2", "hint 3"],
        "steps": [{"text": "step 1", "latex": ""}, {"text": "step 2", "latex": ""}],
        "why": "what was the matter with the old content"
      }
    }

Give only what you are replacing: `hints`, `steps`, or both. `hints` is always all three. `steps` is always the whole solution. Leave good content alone: do not rewrite a question that has nothing the matter with it.

Tools (run from the repo root):

    python -X utf8 scripts/fixes/find.py --ids --prefix <id prefix>     # questions with problems found by rule
    python -X utf8 scripts/fixes/check.py --show <question id>           # the question as it stands
    python -X utf8 scripts/fixes/check.py --part <your part>             # check your fixes

`find.py` catches generic hints, thinking aloud, filler, false sums, hints that state the answer, and missing hints. It cannot tell that a hint belongs to a different question, or that a hint is merely poor: read the questions in your set.

## What makes a good hint

The three hints get more direct, and none of them gives the answer.

1. **Hint 1, the idea.** What kind of problem is this, or what to notice. "The two angles sit on a straight line. What do angles on a straight line add up to?"
2. **Hint 2, the first move.** How to start, using the question's own numbers, stopping before the answer. "First find one share: divide 40 by the 3 + 5 = 8 parts."
3. **Hint 3, a similar example.** A worked example of the same method with DIFFERENT, simpler numbers, so the child can copy the method. "Try a smaller one: to share 12 in the ratio 1 : 2, there are 3 parts, each worth 4, so the shares are 4 and 8." Never the question's own answer.

Write for a 10-year-old: short sentences, plain words, warm. One idea per hint. No "simply", no "obviously".

## What makes a good solution

Two to five steps. Each step does one thing and says why, with the working written out. The last step states the answer in words with its unit ("So the perimeter is 60 cm."). Never refer to the option letter. The steps must reach the answer the question's key gives: you are explaining the verified answer, not solving afresh. If you believe the key itself is mistaken, do not write a fix: list the id in your report.

Steps use the same notation as the rest of the bank: `×`, `÷`, `−`, `=`, fractions as `3/4`, `Rs.` or `₹` as the question does. Put a formula or the key line of working in `latex` only if the question's other steps do; otherwise leave `latex` as `""`.

## What the checker enforces

- Exactly three different hints, none generic, none thinking aloud, none stating the answer (a number from the correct choice that is not in the question).
- Two to five steps, no filler, no thinking aloud, the last one stating the correct answer.
- Every sum written out in a hint or step is true. `20000 ÷ 300 = 66` fails; write `20000 ÷ 300 = 66 remainder 200`, or "about 66.7".
- No "wrong", "incorrect", "failed", "error". Say "does not work", "not a match", "not quite".

Passing the checker is the floor. The point is a hint that would actually help that child with that question.

## Some ids are reserved

`scripts/fixes/answers_ids.txt` lists questions that may have a mistaken answer key or question. They belong to the "answers" workstream. Everyone else must skip them.

## This machine

- Python 3.13 only, run as `python -X utf8`. No Node.js: never run `npm`, `npx` or `node`.
- Nobody is watching this run, so a command that asks for permission will hang. Use ONLY: the Read, Edit and Write tools for files, and plain single commands from the repo root in the forms shown above (plus `python -X utf8 <a script of yours>`). Do NOT use heredocs, `python -c`, `cd ... &&` chains, pipes or redirects.
- Several agents are working in this folder at once. Run no git command at all. Edit only your own files: your part file, and scripts under `scripts/fixes/gen/` whose names start with your part name. Never edit, move or delete anything else.
- Work in small steps: several small edits, never one enormous write. Keep your part file valid JSON on disk at every stage.
- Quote every path: the home folder contains a space.

## Your report

How many questions you fixed, by kind of problem; how many you looked at and left alone; ids where you believe the answer key or the question itself is mistaken (with one line of reasoning each); anything you could not fix within these rules.

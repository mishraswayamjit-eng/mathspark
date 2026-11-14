# Question narration: build brief

Read this first if you are writing narration for a topic.

## What this is

The app reads questions aloud to children aged about 10 (Grade 5, India) with a text-to-speech voice: the question, its four answer choices, its hints, and each step of its solution. Until now the spoken words were made from the printed text by a few general rules, so the voice often stumbles: it reads symbols, abbreviations and layout that only make sense on a page.

Your job is to write the words the voice should say, for every question in one topic, so that listening feels like a good teacher reading the question to the child.

The child sees the printed text while they listen. So narration is the SAME content, made speakable. It is not a rewrite, a summary, or an explanation.

## The contract

| File | What it is |
|---|---|
| `scripts/speech/common.py` | Shared helpers. Read it. Do not edit it. |
| `scripts/speech/validate.py` | The checker. `--topic <slug>` checks your part. Do not edit it. |
| `scripts/speech/show.py` | Prints source and narration side by side; lists your questions; dumps source as JSON. |
| `data/question-speech/parts/<slug>.json` | Your output: `{ "<question id>": entry }` for every question in your topic. |
| `scripts/speech/topics/<slug>.py` (and `<slug>_*.py`) | Your script that writes the part file. |

An entry, with every list the same length as the source it narrates:

    {
      "q": "the question as spoken",
      "options": ["choice A", "choice B", "choice C", "choice D"],
      "hints": ["hint 1", "hint 2", "hint 3"],
      "steps": ["step 1", "step 2", "..."]
    }

- `options`: say only the choice. The app says "Option A" itself.
- `hints` and `steps`: one string per source string, in order. Where the source string is empty, yours is `""`.
- Get the exact source for a question with `common.source_strings(q)` (steps come from the question itself, or from computed steps where it has none).

## What the checker enforces

1. **Same numbers, same order.** Each string must say exactly the numbers its source prints, in the same order. `2,345` and `2345` count as the same; `3/4`, `¾` and "three quarters" count as the same; `x²`, `x^2` and "x squared" count as the same. This is what stops narration from changing the maths, adding a value or giving an answer away. For a step with a separate maths line, you may say either the numbers of its text, or of its text followed by its maths line.
2. **Speakable words only.** None of `× ÷ = + % ₹ ° √ / \ ^ _ { } < > * |`, no arrows, boxes, stars or emoji, no dash between numbers, and no unit abbreviations (`cm`, `km`, `kg`, `ml`, `sq`, `hr`, `Rs`...).
3. **Present where the source has text**, empty where it is empty. At most 700 characters.

Passing the checker is the floor, not the goal. The base converter in `common.speak` passes for most strings and still sounds poor. Quality is what you are here for.

## How to write for the ear

Write what a warm, clear teacher would say when reading this exact text to a child.

- **Short breaths.** Use commas and full stops where a speaker would pause. Break a long line of working into two or three short sentences. Never leave a run of numbers with nothing between them.
- **Numbers.** Keep numbers as digits: `250`, `2,345`, `0.75`, `23,45,678`. Do not spell them out, and do not regroup them (the voice reads Indian place values itself). Write ordinals as printed (`1st`, `3rd`).
- **Operations.** `×` is "times" (or "multiplied by" in a formal definition), `÷` "divided by", `+` "plus", `−` "minus", `=` "equals" or "is". A line that starts with `=` becomes "That equals..." or "So we get...".
- **Fractions.** `3/8` is "3 over 8". Common ones may be words: "one half", "one quarter", "three quarters", "one third", "two thirds". A mixed number `2 3/4` is "2 and 3 over 4" or "2 and three quarters". `3/4 of 20` is "three quarters of 20".
- **Money.** `₹250` and `Rs. 250` are "250 rupees". `Rs. 12.50` is "12.50 rupees" or "12 rupees 50 paise" (same numbers, same order).
- **Units.** Always in full and in the plural where needed: "centimetres", "square centimetres", "kilometres per hour", "millilitres", "degrees".
- **Percent, ratio, time.** `25%` is "25 percent". `3 : 5` is "3 is to 5", and `a : b = c : d` is "a is to b, as c is to d". `9:33 pm` is "9 33 p m".
- **Algebra.** Letters are said as letters: `2x + 3 = 11` is "2 x plus 3 equals 11". `x²` is "x squared". Brackets matter in maths: say "open bracket" and "close bracket" where the grouping changes the meaning (BODMAS), and leave them out where they are only punctuation.
- **Geometry.** `∠ABC` is "angle A B C". `△PQR` is "triangle P Q R". `90°` is "90 degrees".
- **Abbreviations.** `HCF` is "H C F", `LCM` is "L C M". Spell out anything a voice would mangle.
- **Blanks and placeholders.** `___`, `□`, `?`, `★` in a sum become "blank" or "what number", whichever reads naturally: `1/4 = ?/12` is "one quarter equals what, over 12".
- **Arrows and layout.** `→` and `⇒` become "gives", "so" or "which means". Bullets, numbering and line breaks become sentences.
- **Lists of choices or numbers** are separated by commas, with "and" before the last where it is natural.
- **Do not add content.** No praise, no extra explanation, no "let's see". A small joining word ("so", "then", "which is") is fine when it makes a line of working sound like a sentence.
- **Do not fix the maths.** If a source step is poor (thinking aloud, "wait", a filler such as "The answer is option B"), narrate it faithfully and as briefly as the checker allows, and list the question id in your report. Do not invent better content.

Read your narration back as if you were the voice. If you would stumble, the voice will too.

## How to work

1. `python -X utf8 scripts/speech/show.py --topic <slug> --list` to see every question, then group them by kind: generated families with regular wording, and one-off questions (past papers `EXT_G5_FP_...`, worksheets `EXT_G5_WS_...`).
2. Write `scripts/speech/topics/<slug>.py`. Start from `common.speak`, then add rules for the notation of your topic, then handle what rules cannot. Regular families deserve carefully written rules. One-off questions deserve individual attention: where a rule does not produce a line you would be happy to hear, write that line by hand in an overrides table keyed by question id.
3. Run it, then `python -X utf8 scripts/speech/validate.py --topic <slug>`, then read a sample with `python -X utf8 scripts/speech/show.py --topic <slug> --n 20 --seed <k>`. Repeat with different seeds. Fix what sounds wrong, not only what fails.
4. Aim for every question in the topic. Before you finish, read at least 80 questions' narration in full across all the kinds in your topic, and every past-paper and worksheet question at least once.

Work in small steps: several small edits to your script, never one enormous write. Keep the part file valid on disk at every stage.

## This machine

- Python 3.13 only, run as `python -X utf8`. No Node.js: never run `npm`, `npx` or `node`.
- Shell is Git Bash. Quote every path: the home folder contains a space.
- Ten agents are working in this folder at once, one topic each. Run no git command that changes anything (no add, commit, stash, checkout, reset, restore, clean) and do not push. Edit only your own files (the two paths with your topic's slug in the table above). Never edit, move or delete anything else.
- Do not delete files, including `__pycache__` folders.
- Never write secrets into files. Do not read `.env.local`.

## Your report

When your part passes the checker, report: how many of your topic's questions are narrated and pass; how many lines you wrote by hand versus by rule; the notation rules you added for your topic; the ids of questions whose source text is poor (thinking aloud, filler steps, apparent mistakes); anything the checker forced you to say awkwardly; and anything about how the voice should be configured that you think matters for your topic.

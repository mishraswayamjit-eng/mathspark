"""Check (and, with --write, apply) repairs to the hints or wording of Grade 5 questions.

    python -X utf8 scripts/fixes/check_repair.py <patch file> [<patch file> ...]
    python -X utf8 scripts/fixes/check_repair.py --write <patch file> [...]

A patch file is JSON: { "<question id>": { "why": "...", "question": {...}, "speech": {...} } }

  question   the fields to replace in the bank. Only these are allowed:
               "hints"         a list of exactly as many hints as the question has now
               "questionText"  the question's wording (numbers must not change)
               "steps"         the worked steps, rewritten: a list of 2 to 8 items, each
                               { "text": "...", "latex": "..." } (latex optional, plain sums
                               only). The last step must state the right answer.
               "keepStepPictures"  true only when there are as many steps as before and
                               each still shows what its picture shows; otherwise the
                               question's step pictures are dropped (its main figure stays)
  speech     the spoken form of what changed, for the narration:
               "hints"  one string per hint (give all of them, changed or not; "" keeps the
                        existing narration of that hint, which is only allowed when that
                        hint's text did not change)
               "q"      required when questionText changes
               "steps"  one string per step, required when steps change
  why        a few words on what was not right

Checks: the id is a Grade 5 bank question; nothing but hints and wording changes; no hint
names an option letter or uses a word the app never says to a child; the question's numbers
are unchanged; and the narration that results passes the narration checker for that
question (same numbers in the same order, speakable words only). With --write the bank
and the narration part files are updated; nothing is written if any patch has a problem.
"""
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
import bank  # noqa: E402
import common  # noqa: E402
import validate as speech_validate  # noqa: E402

SPEECH_PARTS = os.path.join(ROOT, "data", "question-speech", "parts")
BANNED_WORDS = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)
LETTER_REF = re.compile(r"\b[Oo]ption\s+\(?[A-D]\)?(?![A-Za-z])|\([A-D]\)|\b[Aa]nswer(?:\s+is|\s*:)\s+\(?[A-D]\)?(?![A-Za-z])")
THINKING = re.compile(r"\b(wait|hmm+|oops|nope|let'?s pick a (?:cleaner|better|different)|doesn'?t work|does not work|not a whole number, so)\b", re.I)


FIGURE_PARTS = os.path.join(ROOT, "data", "question-figures", "parts")
# The only LaTeX commands a rewritten step may use: plain sums.
LATEX_OK = re.compile(r"\\(?:times|div|frac|text|circ|approx|rightarrow|quad|%|,| )")


def load_parts(folder):
    parts = {}
    owner = {}
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with io.open(path, encoding="utf-8") as f:
            parts[path] = json.load(f)
        for qid in parts[path]:
            owner[qid] = path
    return parts, owner


def main():
    write = "--write" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    questions = bank.load_bank()
    by_id = {q["id"]: q for q in questions if q.get("topicId") == "grade5"}
    parts, owner = load_parts(SPEECH_PARTS)
    fig_parts, fig_owner = load_parts(FIGURE_PARTS)
    pictures_dropped = 0
    fig_touched = set()

    problems = []
    applied = 0
    skipped = 0
    seen = set()
    for path in files:
        with io.open(path, encoding="utf-8") as f:
            patch = json.load(f)
        name = os.path.basename(path)
        for qid, fix in patch.items():
            where = "%s: %s" % (name, qid)
            q = by_id.get(qid)
            if q is None:
                skipped += 1  # no longer in the bank (removed since the patch was written)
                continue
            if qid in seen:
                problems.append("%s: repaired in two patch files" % where)
                continue
            seen.add(qid)
            new_q = fix.get("question") or {}
            extra = set(new_q) - {"hints", "questionText", "steps", "keepStepPictures"}
            if extra:
                problems.append("%s: may only change hints, questionText and steps, not %s" % (where, sorted(extra)))
                continue
            trial = dict(q)
            old_hints = list(q.get("hints") or [])
            if "hints" in new_q:
                hints = new_q["hints"]
                if not isinstance(hints, list) or len(hints) != len(old_hints) or not all(isinstance(h, str) and h.strip() for h in hints):
                    problems.append("%s: hints must be %d non-empty strings" % (where, len(old_hints)))
                    continue
                for i, h in enumerate(hints):
                    if BANNED_WORDS.search(h):
                        problems.append("%s: hint %d uses a word the app never says to a child" % (where, i + 1))
                    if LETTER_REF.search(h):
                        problems.append("%s: hint %d names an option by letter" % (where, i + 1))
                    if THINKING.search(h):
                        problems.append("%s: hint %d still thinks aloud" % (where, i + 1))
                trial["hints"] = hints
            if "questionText" in new_q:
                text = new_q["questionText"]
                if not isinstance(text, str) or not text.strip():
                    problems.append("%s: questionText must be text" % where)
                    continue
                if common.number_tokens(text) != common.number_tokens(q.get("questionText") or ""):
                    problems.append("%s: the numbers in the question changed" % where)
                if BANNED_WORDS.search(text):
                    problems.append("%s: the question uses a word the app never says to a child" % where)
                trial["questionText"] = text

            old_steps = list(q.get("stepByStep") or [])
            if "steps" in new_q:
                steps = new_q["steps"]
                if not isinstance(steps, list) or not 2 <= len(steps) <= 8 or not all(
                        isinstance(st, dict) and set(st) <= {"text", "latex"} and isinstance(st.get("text"), str)
                        and st["text"].strip() and isinstance(st.get("latex", ""), str) for st in steps):
                    problems.append("%s: steps must be 2 to 8 items of {text, latex}" % where)
                    continue
                for i, st in enumerate(steps):
                    if BANNED_WORDS.search(st["text"]):
                        problems.append("%s: step %d uses a word the app never says to a child" % (where, i + 1))
                    if THINKING.search(st["text"]) or "**" in st["text"]:
                        problems.append("%s: step %d thinks aloud or has markdown asterisks" % (where, i + 1))
                    if "\\" in LATEX_OK.sub("", st.get("latex") or ""):
                        problems.append("%s: step %d latex uses more than plain sums" % (where, i + 1))
                right = next(o["text"] for o in q["options"] if o["id"] == q["correctAnswer"])
                want = common.number_tokens(right)
                last = common.number_tokens(steps[-1]["text"] + " " + (steps[-1].get("latex") or ""))
                if want and not all(t in last for t in want):
                    problems.append("%s: the last step does not state the answer (%s)" % (where, right))
                trial["stepByStep"] = [
                    dict([("step", i + 1), ("text", st["text"])] + ([("latex", st["latex"])] if st.get("latex") else []))
                    for i, st in enumerate(steps)]
                if new_q.get("keepStepPictures") and len(steps) != len(old_steps):
                    problems.append("%s: keepStepPictures needs the same number of steps as before (%d)" % (where, len(old_steps)))

            entry = parts[owner[qid]][qid] if qid in owner else None
            if entry is None:
                problems.append("%s: has no narration entry to update" % where)
                continue
            new_entry = {"q": entry["q"], "options": list(entry["options"]), "hints": list(entry["hints"]), "steps": list(entry["steps"])}
            speech = fix.get("speech") or {}
            if "questionText" in new_q:
                if not speech.get("q"):
                    problems.append("%s: needs speech.q for the new wording" % where)
                    continue
                new_entry["q"] = speech["q"]
            if "hints" in new_q:
                spoken = speech.get("hints")
                if not isinstance(spoken, list) or len(spoken) != len(old_hints):
                    problems.append("%s: speech.hints must have %d strings" % (where, len(old_hints)))
                    continue
                for i, s in enumerate(spoken):
                    if s:
                        new_entry["hints"][i] = s
                    elif trial["hints"][i] != old_hints[i]:
                        problems.append("%s: hint %d changed, so its spoken form is needed" % (where, i + 1))
            if "steps" in new_q:
                spoken = speech.get("steps")
                if not isinstance(spoken, list) or len(spoken) != len(new_q["steps"]) or not all(isinstance(x, str) and x.strip() for x in spoken):
                    problems.append("%s: speech.steps must have %d strings" % (where, len(new_q["steps"])))
                    continue
                new_entry["steps"] = spoken
            found = speech_validate.check_entry(qid, new_entry, trial)
            problems += ["%s: %s" % (name, p) for p in found]
            if not found:
                applied += 1
                if write:
                    q.update({k: trial[k] for k in ("hints", "questionText", "stepByStep") if k in trial})
                    parts[owner[qid]][qid] = new_entry
                    if "steps" in new_q and not new_q.get("keepStepPictures") and qid in fig_owner:
                        fig = fig_parts[fig_owner[qid]][qid]
                        fig_touched.add(fig_owner[qid])
                        if fig.pop("stepFigures", None) is not None:
                            pictures_dropped += 1
                        if not any(k in fig for k in ("figure", "stepFigures", "steps")):
                            del fig_parts[fig_owner[qid]][qid]

    print("%d repairs pass, %d skipped (question no longer in the bank), %d problems" % (applied, skipped, len(problems)))
    for p in problems[:80]:
        print("  " + p)
    if problems:
        sys.exit(1)
    if not write:
        print("nothing written (use --write)")
        return
    bank.save_bank(questions)
    for path, part in list(parts.items()) + list(fig_parts.items()):
        if path in fig_parts and path not in fig_touched:
            continue
        with io.open(path, encoding="utf-8") as f:
            before = f.read()
        if path in fig_parts and "\n " not in before[:2000]:  # a compact file stays compact
            text = json.dumps(part, ensure_ascii=False, separators=(",", ":")) + ("\n" if before.endswith("\n") else "")
        else:
            text = json.dumps(part, ensure_ascii=False, indent=1) + "\n"
        if text != before:
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    print("bank and narration parts written; step pictures dropped for %d questions" % pictures_dropped)


if __name__ == "__main__":
    main()

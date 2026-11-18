"""Check a reviewer's Grade 4 output file. Reads only; exit 1 on any problem.

    python -X utf8 scripts/fixes/g4_check_patch.py <file> [<file> ...]

The kind of file is taken from its name:
  teach-out-*.json    { "<id>": { "hints": [3], "steps": [{text, latex?}, ...], "notes": {A,B,C,D} } }
  dupopts-out.json    { "<id>": { "replace": "C", "with": "new option text", "why": "..." } }
  new-*.json          [ { "topic": "gr4_...", "difficulty": "...", "question": "...", "options": [4 texts],
                          "answer": 0-3 (index of the right option), "hints": [3],
                          "steps": [{text, latex?}], "notes": [4 strings, one per option] } ]
Rules checked for every piece of child-facing text: none of the words the app never says to
a child; no option named by letter; no thinking aloud; no markdown asterisks or emoji; latex
limited to plain sums. Hints are three non-empty strings; steps are 2 to 7 with the last one
stating the right answer; the third hint must not contain the right answer's own numbers
unless they are also in the question; options are four different values.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
from g4_cleanup import value  # noqa: E402

BANNED = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)
LETTER = re.compile(r"\b[Oo]ption\s+\(?[A-D]\)?(?![A-Za-z])|\([A-D]\)|\b(?:[Aa]nswer|[Cc]hoice)(?:\s+is|\s*:)\s+\(?[A-D]\)?(?![A-Za-z])")
THINKING = re.compile(r"\b(wait|hmm+|oops|nope|let'?s pick a (?:cleaner|better|different)|doesn'?t work|actually,)\b", re.I)
CLUTTER = re.compile(u"\\*\\*|[\U0001F300-\U0001FAFF]")
LATEX_OK = re.compile(r"\\(?:times|div|frac|text|circ|approx|quad|%|,| )")
NUM = re.compile(r"\d+(?:\.\d+)?")
DIFFS = ("Easy", "Medium", "Hard")


def nums(text):
    return [n.rstrip("0").rstrip(".") if "." in n else n for n in NUM.findall((text or "").replace(",", ""))]


def check_text(where, text, problems):
    if not isinstance(text, str) or not text.strip():
        problems.append("%s: empty" % where)
        return
    for rx, what in ((BANNED, "uses a word the app never says to a child"), (LETTER, "names an option by letter"),
                     (THINKING, "thinks aloud"), (CLUTTER, "has markdown asterisks or emoji")):
        if rx.search(text):
            problems.append("%s: %s" % (where, what))


def check_teaching(where, question, options, right, hints, steps, notes, problems):
    if not isinstance(hints, list) or len(hints) != 3:
        problems.append("%s: needs exactly three hints" % where)
    else:
        for i, h in enumerate(hints):
            check_text("%s hint %d" % (where, i + 1), h, problems)
        mine = [n for n in nums(right) if n not in nums(question)]
        if mine and isinstance(hints[2], str) and all(n in nums(hints[2]) for n in mine) and len(mine[0]) > 1:
            problems.append("%s hint 3: contains this question's answer (%s)" % (where, right))
    if not isinstance(steps, list) or not 2 <= len(steps) <= 7:
        problems.append("%s: needs 2 to 7 steps" % where)
    else:
        for i, st in enumerate(steps):
            if not isinstance(st, dict) or set(st) - {"text", "latex"}:
                problems.append("%s step %d: must be {text, latex?}" % (where, i + 1))
                continue
            check_text("%s step %d" % (where, i + 1), st.get("text"), problems)
            if "\\" in LATEX_OK.sub("", st.get("latex") or ""):
                problems.append("%s step %d: latex uses more than plain sums" % (where, i + 1))
        last = steps[-1] if isinstance(steps[-1], dict) else {}
        want = nums(right)
        have = nums((last.get("text") or "") + " " + (last.get("latex") or ""))
        if want and not all(n in have for n in want):
            problems.append("%s: the last step does not state the answer (%s)" % (where, right))
        if not want and right and re.sub(r"[^a-z]", "", right.lower())[:12] not in re.sub(r"[^a-z]", "", (last.get("text") or "").lower()):
            problems.append("%s: the last step does not state the answer (%s)" % (where, right))
    if len(notes) != 4:
        problems.append("%s: needs a note for each of the four options" % where)
    for i, n in enumerate(notes):
        check_text("%s note %d" % (where, i + 1), n, problems)


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    by_id = {q["id"]: q for q in bank.load_bank(4)}
    nodes = {n["id"] for n in bank.tree_nodes(4)}
    problems = []
    ok = 0
    for path in files:
        name = os.path.basename(path)
        with io.open(path, encoding="utf-8") as f:
            data = json.load(f)
        if name.startswith("teach-out"):
            for qid, p in data.items():
                q = by_id.get(qid)
                if q is None:
                    problems.append("%s: %s is not a Grade 4 bank question" % (name, qid))
                    continue
                right = next(o["text"] for o in q["options"] if o["id"] == q["correctAnswer"])
                notes = p.get("notes") or {}
                before = len(problems)
                if set(notes) != {"A", "B", "C", "D"}:
                    problems.append("%s: notes must have A, B, C, D" % qid)
                check_teaching(qid, q.get("questionText"), q["options"], right, p.get("hints"), p.get("steps"),
                               [notes.get(k, "") for k in "ABCD"], problems)
                ok += 1 if len(problems) == before else 0
        elif name.startswith("dupopts-out"):
            for qid, p in data.items():
                q = by_id.get(qid)
                if q is None:
                    problems.append("%s: %s is not a Grade 4 bank question" % (name, qid))
                    continue
                if p.get("remove"):
                    ok += 1
                    continue
                if p.get("replace") not in "ABCD" or p.get("replace") == q["correctAnswer"]:
                    problems.append("%s: replace must be a letter other than the key (%s)" % (qid, q["correctAnswer"]))
                    continue
                opts = [p["with"] if o["id"] == p["replace"] else o["text"] for o in q["options"]]
                check_text("%s new option" % qid, p.get("with"), problems)
                if len({value(t) for t in opts}) < 4:
                    problems.append("%s: two options are still the same value" % qid)
                else:
                    ok += 1
        elif name.startswith("new-"):
            for i, p in enumerate(data):
                where = "%s[%d]" % (name, i)
                before = len(problems)
                if p.get("topic") not in nodes:
                    problems.append("%s: unknown topic %r" % (where, p.get("topic")))
                if p.get("difficulty") not in DIFFS:
                    problems.append("%s: difficulty must be Easy, Medium or Hard" % where)
                opts = p.get("options")
                if not isinstance(opts, list) or len(opts) != 4 or len({value(t) for t in opts}) < 4:
                    problems.append("%s: needs four options of different value" % where)
                    continue
                if p.get("answer") not in (0, 1, 2, 3):
                    problems.append("%s: answer must be 0, 1, 2 or 3" % where)
                    continue
                check_text("%s question" % where, p.get("question"), problems)
                for t in opts:
                    check_text("%s option" % where, str(t), problems)
                check_teaching(where, p.get("question"), opts, str(opts[p["answer"]]), p.get("hints"), p.get("steps"),
                               p.get("notes") or [], problems)
                ok += 1 if len(problems) == before else 0
        else:
            problems.append("%s: not a file this checker knows" % name)
    print("%d entries pass, %d problems" % (ok, len(problems)))
    for p in problems[:80]:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

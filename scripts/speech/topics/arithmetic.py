"""Narration for the arithmetic topic (BODMAS, the four operations, averages, missing digits).

    python -X utf8 scripts/speech/topics/arithmetic.py            # writes data/question-speech/parts/arithmetic.json
    python -X utf8 scripts/speech/topics/arithmetic.py --stats    # also prints how many lines came from rules and by hand

Every line starts from the rules in arithmetic_engine.py. Lines the rules cannot read well are
written by hand in the override tables (arithmetic_fp.py for past papers, arithmetic_ws_*.py for
worksheets), keyed by question id. An override entry may give any of:
    "q": "...", "options": {index: "..."}, "hints": {index: "..."}, "steps": {index: "..."}
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from arithmetic_engine import say, say_option  # noqa: E402

SLUG = "arithmetic"

OVERRIDES = {}
for _name in ("arithmetic_fp", "arithmetic_ws_a", "arithmetic_ws_b"):
    try:
        OVERRIDES.update(__import__(_name).OVERRIDES)
    except ImportError:
        pass

# Hints that many generated questions share, written once by hand.
SHARED = {
    "Don't just go left to right — check for × and ÷ first!":
        "Don't just go left to right. Check for multiplication and division first!",
    "Follow BODMAS: Brackets, Orders, Division/Multiplication, Addition/Subtraction":
        "Follow BODMAS: Brackets, Orders, Division and Multiplication, Addition and Subtraction.",
    "Similar: SI on Rs.500 at 8% for 3yr = 500×8×3/100 = Rs.120.":
        "Similar: simple interest on 500 rupees at 8 percent for 3 years, equals 500 times 8 times 3, over 100, which is 120 rupees.",
}


def _latex_words(latex):
    """The maths line of an equation step, for the 'Solve' family only (2x = 17 - 5 = 12)."""
    t = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"\1/\2", latex)
    t = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", t)
    return say(t.replace("-", "−"))


def narrate(q):
    src = source_strings(q)
    own = q.get("stepByStep") or []
    entry = {
        "q": say(src["q"]),
        "options": [say_option(t) for t in src["options"]],
        "hints": [SHARED.get(t) or say(t) for t in src["hints"]],
        "steps": [SHARED.get(t) or say(t) for t in src["steps"]],
    }
    if src["q"].startswith("Solve:") and "x" in src["q"]:
        for i, st in enumerate(own):
            if st.get("latex") and "x" in st["latex"]:
                entry["steps"][i] = "%s %s" % (entry["steps"][i], _latex_words(st["latex"]))
    hand = 0
    ov = OVERRIDES.get(q["id"], {})
    if "q" in ov:
        entry["q"] = ov["q"]
        hand += 1
    for key in ("options", "hints", "steps"):
        for i, line in (ov.get(key) or {}).items():
            entry[key][i] = line
            hand += 1
    return entry, hand


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part, hand, total = {}, 0, 0
    for q in questions:
        entry, h = narrate(q)
        part[q["id"]] = entry
        hand += h
        total += 1 + sum(1 for k in ("options", "hints", "steps") for t in entry[k] if t)
    unknown = sorted(set(OVERRIDES) - set(part))
    if unknown:
        sys.exit("override ids that are not arithmetic questions: %s" % ", ".join(unknown))
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), os.path.relpath(path)))
    if "--stats" in sys.argv:
        print("%d lines: %d by hand, %d by rule" % (total, hand, total - hand))


if __name__ == "__main__":
    main()

"""Narration for the factors topic: writes data/question-speech/parts/factors.json.

    python -X utf8 scripts/speech/topics/factors.py

Generated families are narrated by the exact-wording rules in factors_rules.py. Past-paper and
worksheet questions are narrated by hand in factors_fp.py and factors_ws1..3.py (key 'q', 'o'
for the four options, 'h0'..'h2' for hints, 's0'.. for steps); anything a hand entry leaves
out goes through the general converter.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_entry  # noqa: E402
import factors_rules as R  # noqa: E402

SLUG = "factors"
HAND = {}
for name in ("factors_fp", "factors_ws1", "factors_ws2", "factors_ws3"):
    if os.path.exists(os.path.join(HERE, name + ".py")):
        HAND.update(importlib.import_module(name).HAND)

counts = {"hand": 0, "family": 0, "general": 0}


def line(text, hand=None):
    if not (text or "").strip():
        return ""
    if hand is not None:
        counts["hand"] += 1
        return hand
    fam = R.family_line(text)
    if fam is not None:
        counts["family"] += 1
        return fam
    counts["general"] += 1
    said = R.say(text)
    if " " in said and said[-1].isalnum():
        said += "."  # a sentence printed without its full stop still ends like one
    return said


def step_line(q, i, text, hand=None):
    """A step; a generated 'Solve' step also reads the maths line printed under it."""
    own = q.get("stepByStep") or []
    if (hand is None and i < len(own) and own[i].get("latex") and not q["id"].startswith("EXT_")
            and R.family_line(text) is None):
        words = R.latex_words(own[i]["latex"])
        if words:
            counts["family"] += 1
            return "%s. %s" % (text.rstrip("."), words)
    return line(text, hand)


def narrate(q):
    src = source_strings(q)
    hand = HAND.get(q["id"], {})
    opts = hand.get("o")
    return {
        "q": line(src["q"], hand.get("q")),
        "options": [line(t, opts[i] if opts else None) if opts else _option(t) for i, t in enumerate(src["options"])],
        "hints": [line(t, hand.get("h%d" % i)) for i, t in enumerate(src["hints"])],
        "steps": [step_line(q, i, t, hand.get("s%d" % i)) for i, t in enumerate(src["steps"])],
    }


def _option(text):
    counts["general"] += 1
    return R.option(text)


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part, bad = {}, []
    for q in questions:
        entry = narrate(q)
        problems = check_entry(q["id"], entry, q)
        if problems:
            bad += problems
        part[q["id"]] = entry
    unknown = sorted(set(HAND) - {q["id"] for q in questions})
    os.makedirs(PARTS, exist_ok=True)
    with io.open(os.path.join(PARTS, SLUG + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions; lines by hand %d, by family rule %d, by general rule %d"
          % (len(part), counts["hand"], counts["family"], counts["general"]))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if bad:
        print("%d problems" % len(bad))
        for p in bad[:int(os.environ.get("MAXP", "40"))]:
            print("  " + p)


if __name__ == "__main__":
    main()

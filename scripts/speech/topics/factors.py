"""Narration for the factors topic: writes data/question-speech/parts/factors.json.

    python -X utf8 scripts/speech/topics/factors.py

Generated families are narrated by the exact-wording rules in factors_rules.py. Past-paper and
worksheet questions are narrated by hand in factors_fp.py and factors_ws1..3.py (key 'q', 'o'
for the four options, 'h0'..'h2' for hints, 's0'.. for steps); anything a hand entry leaves
out goes through the general converter.
"""
import glob
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from common import PARTS, load_grade5, number_tokens, source_strings, topic_of  # noqa: E402
from validate import check_entry, check_string  # noqa: E402
import factors_rules as R  # noqa: E402

SLUG = "factors"
HAND = {}
for name in ("factors_fp", "factors_ws1", "factors_ws2", "factors_ws3"):
    if os.path.exists(os.path.join(HERE, name + ".py")):
        HAND.update(importlib.import_module(name).HAND)

# Imported questions (AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_): hand entries live in
# factors_imported*.py, and what they leave out goes through factors_imported_rules.say.
import factors_imported_rules as IR  # noqa: E402

IMPORTED_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
IMPORTED_HAND = {}
for path in sorted(glob.glob(os.path.join(HERE, "factors_imported_hand*.py"))):
    IMPORTED_HAND.update(importlib.import_module(os.path.splitext(os.path.basename(path))[0]).HAND)


def hand_key(qid):
    """The key of a question in the imported hand files: AIGEN ids are cut to 'AIGEN_grade5_' + 8."""
    return qid[:21] if qid.startswith("AIGEN_grade5_") else qid

# The part file as it was before the imported questions were narrated. Entries in it are final:
# they are written back exactly as they were.
BEFORE_PATH = os.path.join(HERE, "_scratch_factors", "factors_before.json")
BEFORE = {}
if os.path.exists(BEFORE_PATH):
    with io.open(BEFORE_PATH, encoding="utf-8") as _f:
        BEFORE = json.load(_f)

counts = {"hand": 0, "family": 0, "general": 0}
_imported = [False]


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
    said = IR.say(text) if _imported[0] else R.say(text)
    if " " in said and said[-1].isalnum():
        said += "."  # a sentence printed without its full stop still ends like one
    return said


def imported_step(own, i, text, hand):
    """A step of an imported question: its text, then the maths line printed under it, if that reads cleanly."""
    said = line(text, hand)
    latex = own[i].get("latex", "") if i < len(own) else ""
    if hand is not None or not latex.strip() or not said:
        return said
    words = IR.latex_words(latex)
    if not words:
        return said
    in_text, in_maths = number_tokens(said), number_tokens(words)
    n = len(in_maths)
    if in_maths and in_text[-n:] == in_maths:
        return said  # the text already says its maths line
    if n >= 2 and any(in_text[k:k + n] == in_maths for k in range(len(in_text) - n + 1)):
        return said
    both = "%s %s" % (said, words)
    also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex))
    if check_string(both, text, "step", also):
        return said
    return both


def step_line(q, i, text, hand=None):
    """A step; a generated 'Solve' step also reads the maths line printed under it."""
    own = q.get("stepByStep") or []
    if _imported[0]:
        return imported_step(own, i, text, hand)
    if (hand is None and i < len(own) and own[i].get("latex") and not q["id"].startswith("EXT_")
            and R.family_line(text) is None):
        words = R.latex_words(own[i]["latex"])
        if words:
            counts["family"] += 1
            return "%s. %s" % (text.rstrip("."), words)
    return line(text, hand)


def narrate(q):
    _imported[0] = q["id"].startswith(IMPORTED_PREFIXES)
    src = source_strings(q)
    hand = IMPORTED_HAND.get(hand_key(q["id"]), {}) if _imported[0] else HAND.get(q["id"], {})
    opts = hand.get("o")
    return {
        "q": line(src["q"], hand.get("q")),
        "options": [line(t, opts[i] if opts else None) if opts else _option(t) for i, t in enumerate(src["options"])],
        "hints": [line(t, hand.get("h%d" % i)) for i, t in enumerate(src["hints"])],
        "steps": [step_line(q, i, t, hand.get("s%d" % i)) for i, t in enumerate(src["steps"])],
    }


def _option(text):
    counts["general"] += 1
    return IR.option(text) if _imported[0] else R.option(text)


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part, bad = {}, []
    drift = []
    new = {"questions": 0, "hand": 0, "rule": 0}
    for q in questions:
        before = dict(counts)
        entry = narrate(q)
        if q["id"] in BEFORE:
            if entry != BEFORE[q["id"]]:
                drift.append(q["id"])
            entry = BEFORE[q["id"]]  # an existing entry is never rewritten
        else:
            new["questions"] += 1
            new["hand"] += counts["hand"] - before["hand"]
            new["rule"] += (counts["family"] - before["family"]) + (counts["general"] - before["general"])
        problems = check_entry(q["id"], entry, q)
        if problems:
            bad += problems
        part[q["id"]] = entry
    unknown = sorted(set(HAND) - {q["id"] for q in questions})
    keys = [hand_key(q["id"]) for q in questions if q["id"].startswith(IMPORTED_PREFIXES)]
    unknown += sorted(set(IMPORTED_HAND) - set(keys))
    unknown += sorted("not unique: " + k for k in set(keys) if keys.count(k) > 1 and k in IMPORTED_HAND)
    os.makedirs(PARTS, exist_ok=True)
    with io.open(os.path.join(PARTS, SLUG + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions; lines by hand %d, by family rule %d, by general rule %d"
          % (len(part), counts["hand"], counts["family"], counts["general"]))
    if BEFORE:
        print("existing entries kept as they were: %d; new questions: %d (lines by hand %d, by rule %d)"
              % (len(BEFORE), new["questions"], new["hand"], new["rule"]))
        if drift:
            print("the script would now narrate %d existing entries differently (kept as they were): %s"
                  % (len(drift), drift[:10]))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if bad:
        print("%d problems" % len(bad))
        for p in bad[:int(os.environ.get("MAXP", "40"))]:
            print("  " + p)


if __name__ == "__main__":
    main()

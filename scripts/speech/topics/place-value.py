"""Narration for the place-value topic. Writes data/question-speech/parts/place-value.json.

    python -X utf8 scripts/speech/topics/place-value.py

Generated families (BOOST_, VAR_, PH3_) are narrated by the rules in place_value_rules.py.
Past-paper and worksheet questions (EXT_G5_FP_, EXT_G5_WS_) are narrated by hand in the
place_value_hand_*.py tables; only their answer choices go through a rule (`option`).
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
from validate import check_entry  # noqa: E402
import place_value_rules as rules  # noqa: E402

SLUG = "place-value"
HAND = {}
for name in ("place_value_hand_fp_a", "place_value_hand_fp_b", "place_value_hand_fp_c", "place_value_hand_ws",
             "place_value_hand_ws2"):
    try:
        HAND.update(__import__(name).HAND)
    except ImportError:
        pass

# Imported questions (AI-written word problems, IPM textbook, IPM 2020 paper): narrated by the
# rules in place_value_imported_rules.py; single strings are replaced by hand in the
# place_value_imported_*.py tables: {id: {"q": "...", "options": {i: "..."}, "hints": {i: "..."}, "steps": {i: "..."}}}.
import place_value_imported_rules as imported  # noqa: E402

IMPORTED_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
IMPORTED_HAND = {}
for name in ("place_value_imported_a", "place_value_imported_b", "place_value_imported_c", "place_value_imported_d"):
    try:
        IMPORTED_HAND.update(__import__(name).HAND)
    except ImportError:
        pass
HAND_STRINGS = [0]


def narrate_imported(q):
    src = source_strings(q)
    own = q.get("stepByStep") or []
    entry = {
        "q": imported.sentence(src["q"]),
        "options": [imported.option(o) for o in src["options"]],
        "hints": [imported.sentence(h) for h in src["hints"]],
        "steps": [imported.step(s, own[i].get("latex", "") if i < len(own) else "") for i, s in enumerate(src["steps"])],
    }
    hand = IMPORTED_HAND.get(q["id"], {})
    for key, value in hand.items():
        if key == "q":
            entry["q"] = value
            HAND_STRINGS[0] += 1
            continue
        for i, said in value.items():
            entry[key][i] = said
            HAND_STRINGS[0] += 1
    return entry


_PLAIN = re.compile(r"^[A-Za-z0-9 .,?'’-]+$")


def option(text):
    """An answer choice of a hand-narrated question: a number, an expression such as (x + 54), or a few words."""
    s = (text or "").strip()
    m = re.match(r"^Rs\.?\s*([\d,]+(?:\.\d+)?)$", s)
    if m:
        return m.group(1) + " rupees"
    m = re.match(r"^\(?([A-Za-z]) ([+−]) (\d+)\)?$", s)
    if m:
        return "%s %s %s" % (m.group(1), "plus" if m.group(2) == "+" else "minus", m.group(3))
    if _PLAIN.match(s) and not re.search(r"\d\s*-\s*\d", s):
        return s
    raise ValueError("no rule for option: %r" % s)


def narrate(q):
    if q["id"].startswith(IMPORTED_PREFIXES):
        return narrate_imported(q)
    src = source_strings(q)
    hand = HAND.get(q["id"])
    if hand:
        return {
            "q": hand["q"],
            "options": hand.get("options") or [option(o) for o in src["options"]],
            "hints": hand["hints"],
            "steps": hand["steps"],
        }
    if q["id"].startswith("EXT_"):
        return None  # a one-off with no hand narration yet
    return {
        "q": rules.say(src["q"]),
        "options": [rules.say(o) for o in src["options"]],
        "hints": [rules.say(h) for h in src["hints"]],
        "steps": [rules.say(s, src["q"]) for s in src["steps"]],
    }


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part, problems, missing = {}, [], []
    for q in questions:
        entry = narrate(q)
        if entry is None:
            missing.append(q["id"])
            continue
        found = check_entry(q["id"], entry, q)
        problems += found
        part[q["id"]] = entry
    os.makedirs(PARTS, exist_ok=True)
    with io.open(os.path.join(PARTS, SLUG + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d of %d questions (%d by hand)" % (len(part), len(questions), sum(1 for k in part if k in HAND)))
    new = [k for k in part if k.startswith(IMPORTED_PREFIXES)]
    print("imported: %d questions, %d strings replaced by hand in %d of them" % (
        len(new), HAND_STRINGS[0], sum(1 for k in new if k in IMPORTED_HAND)))
    if missing:
        print("not yet narrated: %d" % len(missing))
        print("  " + " ".join(missing))
    for p in problems:
        print("  PROBLEM " + p)


if __name__ == "__main__":
    main()

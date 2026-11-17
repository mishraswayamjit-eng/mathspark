"""Narration for the money-percent topic. Writes data/question-speech/parts/money-percent.json.

    python -X utf8 scripts/speech/topics/money-percent.py
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
from money_percent_rules import say  # noqa: E402
import money_percent_hand as hand  # noqa: E402
from money_percent_imported_rules import say as say_imported  # noqa: E402
import money_percent_imported as imported  # noqa: E402

SLUG = "money-percent"

# Questions imported into the bank later (one-off story problems).
IMPORTED = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")

# Lines of working from the generated families that deserve their own wording.
FAMILY = [
    (r"^Divide: (\d+) ÷ (\d+)\.$", r"Divide \1 by \2."),
    (r"^SP = CP \+ Profit = (\d+) \+ (\d+) = Rs\.(\d+)$",
     r"Selling price equals cost price plus profit. That is \1 plus \2, which equals \3 rupees."),
    (r"^SP = CP − Loss = (\d+) − (\d+) = Rs\.(\d+)$",
     r"Selling price equals cost price minus loss. That is \1 minus \2, which equals \3 rupees."),
    (r"^Profit = (\d+)/100 × (\d+)\.$", r"Profit equals \1 over 100, times \2."),
]


def narrate(text, option=False, si=False):
    t = (text or "").strip()
    for pat, rep in FAMILY:
        if re.match(pat, t):
            return re.sub(pat, rep, t)
    return say(t, option=option, si=si)


def apply_hand(entry, lines):
    for key, spoken in lines.items():
        if key == "q":
            entry["q"] = spoken
        else:
            entry[{"o": "options", "h": "hints", "s": "steps"}[key[0]]][int(key[1:])] = spoken
    return entry


def imported_entry(q):
    """The imported story problems have their own rules and their own hand-written lines."""
    src = source_strings(q)
    entry = {
        "q": say_imported(src["q"]),
        "options": [say_imported(o, option=True) for o in src["options"]],
        "hints": [say_imported(h) for h in src["hints"]],
        "steps": [say_imported(s) for s in src["steps"]],
    }
    return apply_hand(entry, imported.LINES.get(q["id"], {}))


def entry_for(q):
    if q["id"].startswith(IMPORTED):
        return imported_entry(q)
    src = source_strings(q)
    si = "interest" in q.get("subTopic", "").lower() or "simple_interest" in q["id"]
    entry = {
        "q": narrate(src["q"], si=si),
        "options": [narrate(o, option=True, si=si) for o in src["options"]],
        "hints": [narrate(h, si=si) for h in src["hints"]],
        "steps": [narrate(s, si=si) for s in src["steps"]],
    }
    for key, spoken in hand.LINES.get(q["id"], {}).items():
        if key == "q":
            entry["q"] = spoken
        else:
            entry[{"o": "options", "h": "hints", "s": "steps"}[key[0]]][int(key[1:])] = spoken
    return entry


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part = {q["id"]: entry_for(q) for q in questions}
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), path))


if __name__ == "__main__":
    main()

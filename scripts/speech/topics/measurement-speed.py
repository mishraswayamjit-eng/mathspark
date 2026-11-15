"""Narration for the measurement-speed topic. Writes data/question-speech/parts/measurement-speed.json.

    python -X utf8 scripts/speech/topics/measurement-speed.py

Past-paper and worksheet questions are written by hand (measurement_speed_hand*.py).
The generated families go through the rules in measurement_speed_rules.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_entry  # noqa: E402
import measurement_speed_hand1 as hand1  # noqa: E402
import measurement_speed_hand2 as hand2  # noqa: E402
import measurement_speed_hand3 as hand3  # noqa: E402
from measurement_speed_rules import say, say_option  # noqa: E402

SLUG = "measurement-speed"

HAND = {}
for module in (hand1, hand2, hand3):
    HAND.update(module.HAND)


def narrate(q):
    if q["id"] in HAND:
        return HAND[q["id"]]
    src = source_strings(q)
    return {
        "q": say(src["q"]),
        "options": [say_option(o) for o in src["options"]],
        "hints": [say(h) for h in src["hints"]],
        "steps": [say(s) for s in src["steps"]],
    }


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part = {}
    problems = []
    for q in questions:
        entry = narrate(q)
        found = check_entry(q["id"], entry, q)
        problems += found
        part[q["id"]] = entry
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, path)
    print("wrote %d of %d questions (%d by hand)" % (len(part), len(questions), sum(1 for q in questions if q["id"] in HAND)))
    for p in problems[:40]:
        print("  " + p)
    if problems:
        print("%d problems" % len(problems))


if __name__ == "__main__":
    main()

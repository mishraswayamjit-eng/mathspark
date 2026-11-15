"""Build data/teach/parts/squares-patterns.json from the rules and the hand-written lessons.

    python -X utf8 scripts/teach/gen/squares_patterns_build.py
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from squares_patterns_lib import GENERATED, PART, lesson, questions  # noqa: E402
from squares_patterns_rules import RULES  # noqa: E402

HAND_MODULES = [
    "squares_patterns_hand_a", "squares_patterns_hand_b", "squares_patterns_hand_c",
    "squares_patterns_hand_d", "squares_patterns_hand_e", "squares_patterns_hand_f",
]


def main():
    qs = questions()
    out = {}
    by_rule = {}
    hand = {}
    for name in HAND_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, beats in mod.LESSONS.items():
            if qid in hand:
                sys.exit("two hand-written lessons for %s" % qid)
            hand[qid] = beats
    for qid in sorted(qs):
        q = qs[qid]
        if qid in hand:
            out[qid] = lesson(qid, hand[qid], "authored")
            continue
        for rule in RULES:
            made = rule(q)
            if made:
                beats, check = made
                out[qid] = lesson(qid, beats, "rule", check)
                by_rule[rule.__name__] = by_rule.get(rule.__name__, 0) + 1
                break
    for qid in hand:
        if qid not in qs:
            sys.exit("%s is not a squares-patterns question" % qid)
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons of %d questions: %d by hand" % (len(out), len(qs), len(hand)))
    for name in sorted(by_rule):
        print("  rule %-22s %d" % (name, by_rule[name]))
    missing = [qid for qid in sorted(qs) if qid not in out]
    print("missing: %d (%d generated, %d one-off)" % (
        len(missing), sum(1 for m in missing if m.startswith(GENERATED)),
        sum(1 for m in missing if not m.startswith(GENERATED))))


if __name__ == "__main__":
    main()

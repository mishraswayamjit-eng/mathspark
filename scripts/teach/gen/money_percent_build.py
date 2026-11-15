"""Build data/teach/parts/money-percent.json: lessons for every money-percent question.

    python -X utf8 scripts/teach/gen/money_percent_build.py

Generated families get a lesson from a rule (money_percent_rules.py). One-off questions
get a lesson written by hand (money_percent_hand_*.py). Check the result with
    python -X utf8 scripts/teach/validate.py --part money-percent
"""
import collections
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402
from money_percent_rules import rule_for  # noqa: E402

OUT = os.path.join(ROOT, "data", "teach", "parts", "money-percent.json")
HAND_MODULES = ["money_percent_hand_a", "money_percent_hand_b", "money_percent_hand_c", "money_percent_hand_d"]


def main():
    hand = {}
    for name in HAND_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, script in importlib.import_module(name).LESSONS.items():
            assert qid not in hand, "two hand-written lessons for %s" % qid
            hand[qid] = script

    out = {}
    by_rule = collections.Counter()
    missing = []
    for q in load_grade5():
        if topic_of(q) != "money-percent":
            continue
        qid = q["id"]
        if qid in hand:
            out[qid] = hand[qid]
            by_rule["by hand"] += 1
            continue
        found = rule_for(q)
        if found:
            by_rule[found[0]] += 1
            out[qid] = found[1]
        else:
            missing.append(qid)
    stray = sorted(set(hand) - set(out))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d lessons" % (os.path.relpath(OUT, ROOT), len(out)))
    for name, n in sorted(by_rule.items()):
        print("  %-26s %d" % (name, n))
    if stray:
        print("hand-written lessons for ids that are not money-percent questions: %s" % ", ".join(stray))
    print("%d questions with no lesson%s" % (len(missing), (": " + ", ".join(missing)) if missing else ""))


if __name__ == "__main__":
    main()

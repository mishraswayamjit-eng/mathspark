"""Build data/teach/parts/g4-gr4_decimals.json: a lesson for every gr4_decimals question.

    python -X utf8 scripts/teach/gen/g4_gr4_decimals_build.py

The generated family gets its lesson from a rule (g4_gr4_decimals_rules.py). Every other
question has a lesson written for it (g4_gr4_decimals_hand_*.py). Check the result with
    python -X utf8 scripts/teach/validate.py --part g4-gr4_decimals
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
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402
from g4_gr4_decimals_rules import rule_for  # noqa: E402

TOPIC = "gr4_decimals"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
HAND_MODULES = ["g4_gr4_decimals_hand_%s" % c for c in "abcdefgh"]


def main():
    hand = {}
    for name in HAND_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, script in importlib.import_module(name).LESSONS.items():
            assert qid not in hand, "two hand-written lessons for %s" % qid
            hand[qid] = script

    out = {}
    counts = collections.Counter()
    missing = []
    for q in bank.load_bank(4):
        if q.get("node") != TOPIC:
            continue
        qid = q["id"]
        if qid in hand:
            out[qid] = hand[qid]
            counts["written for the question"] += 1
            continue
        found = rule_for(q)
        if found:
            counts["rule: " + found[0]] += 1
            out[qid] = found[1]
        else:
            missing.append(qid)
    stray = sorted(set(hand) - set(out))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d lessons" % (os.path.relpath(OUT, ROOT), len(out)))
    for name, n in sorted(counts.items()):
        print("  %-28s %d" % (name, n))
    if stray:
        print("hand-written lessons for ids that are not %s questions: %s" % (TOPIC, ", ".join(stray)))
    print("%d questions with no lesson%s" % (len(missing), (": " + ", ".join(missing)) if missing else ""))


if __name__ == "__main__":
    main()

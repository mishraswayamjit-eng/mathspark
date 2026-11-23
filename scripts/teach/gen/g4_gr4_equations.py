"""Build data/teach/parts/g4-gr4_equations.json: a lesson for every Grade 4 equations question.

    python -X utf8 scripts/teach/gen/g4_gr4_equations.py

Generated families get a rule lesson (g4_gr4_equations_rules.py). Every other question gets a
lesson written for that question (g4_gr4_equations_hand_*.py). Then check with:

    python -X utf8 scripts/teach/validate.py --part g4-gr4_equations
"""
import collections
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_equations_lib import OUT, ROOT, questions, spread_answers  # noqa: E402
from g4_gr4_equations_rules import rule_for  # noqa: E402

HAND_MODULES = ["g4_gr4_equations_hand_%s" % c for c in "abcdefgh"]
GENERATED = ("VAR_", "VAR2_", "BOOST_")


def is_generated(qid):
    return qid.startswith(GENERATED) or (qid.startswith("Q_CH") and "_V" in qid)


def main():
    hand = {}
    for name in HAND_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, script in importlib.import_module(name).LESSONS.items():
            if qid in hand:
                sys.exit("%s has two lessons" % qid)
            spread_answers(qid, script)
            hand[qid] = script

    qs = questions()
    stray = sorted(set(hand) - {q["id"] for q in qs})
    if stray:   # questions since removed from the bank
        print("skipped, no longer in this topic: %s" % ", ".join(stray))
        for qid in stray:
            del hand[qid]

    part = {}
    missing = []
    kinds = collections.Counter()
    for q in sorted(qs, key=lambda q: q["id"]):
        script = hand.get(q["id"])
        if script is None and is_generated(q["id"]):
            script = rule_for(q)
        if script is None:
            missing.append(q)
            continue
        part[q["id"]] = script
        kinds[script["origin"]] += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d lessons (%s), %d questions without one"
          % (os.path.relpath(OUT, ROOT), len(part), ", ".join("%d %s" % (n, k) for k, n in sorted(kinds.items())),
             len(missing)))
    for q in (missing if len(sys.argv) > 1 else []):
        print("  no lesson: %s  %s" % (q["id"], q["questionText"][:70]))


if __name__ == "__main__":
    main()

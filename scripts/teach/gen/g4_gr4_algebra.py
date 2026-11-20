"""Build data/teach/parts/g4-gr4_algebra.json: a lesson for every Grade 4 algebra question.

    python -X utf8 scripts/teach/gen/g4_gr4_algebra.py

Generated families get a rule lesson (g4_gr4_algebra_rules.py). Every other question gets a lesson
written for that question (g4_gr4_algebra_hand_*.py). Then check with:

    python -X utf8 scripts/teach/validate.py --part g4-gr4_algebra
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
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402
from g4_gr4_algebra_lib import pick  # noqa: E402
from g4_gr4_algebra_rules import rule_for  # noqa: E402

NODE = "gr4_algebra"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_algebra.json")
HAND_MODULES = ["g4_gr4_algebra_hand_a", "g4_gr4_algebra_hand_b", "g4_gr4_algebra_hand_c", "g4_gr4_algebra_hand_d",
                "g4_gr4_algebra_hand_e", "g4_gr4_algebra_hand_f", "g4_gr4_algebra_hand_g"]


def spread_answers(qid, script):
    """Hand-written asks tend to put the right choice in the same slot. Rotate each one in a stable
    way so that a child cannot learn "it is always the first one"."""
    for i, beat in enumerate(script["beats"]):
        ask = beat.get("ask")
        if not ask or ask.get("kind") != "choose":
            continue
        choices = ask["choices"]
        right = choices[ask["answer"]]
        k = pick(qid, "spread%d" % i, list(range(len(choices))))
        ask["choices"] = choices[k:] + choices[:k]
        ask["answer"] = ask["choices"].index(right)


def main():
    hand = {}
    for name in HAND_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        lessons = importlib.import_module(name).LESSONS
        for qid, script in lessons.items():
            if qid in hand:
                sys.exit("%s has two lessons" % qid)
            spread_answers(qid, script)
            hand[qid] = script

    questions = [q for q in bank.load_bank(4) if q.get("node") == NODE]
    ids = {q["id"] for q in questions}
    stray = sorted(set(hand) - ids)
    if stray:
        sys.exit("not %s questions: %s" % (NODE, ", ".join(stray)))

    part = {}
    missing = []
    kinds = collections.Counter()
    for q in sorted(questions, key=lambda q: q["id"]):
        script = hand.get(q["id"]) or rule_for(q)
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
    for q in missing if "list" in sys.argv[1:] else []:
        print("  no lesson: %s  %s" % (q["id"], q["questionText"][:70]))


if __name__ == "__main__":
    main()

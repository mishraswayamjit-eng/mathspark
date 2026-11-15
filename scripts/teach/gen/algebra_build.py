"""Build data/teach/parts/algebra.json: a lesson for every Grade 5 algebra question.

    python -X utf8 scripts/teach/gen/algebra_build.py

Generated families get a rule lesson (algebra_rules.py). One-off questions get a lesson
written for that question (algebra_authored_*.py). Then check with:

    python -X utf8 scripts/teach/validate.py --part algebra
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
from algebra_lib import pick  # noqa: E402
from algebra_rules import rule_for  # noqa: E402

OUT = os.path.join(ROOT, "data", "teach", "parts", "algebra.json")
AUTHORED_MODULES = ["algebra_authored_a", "algebra_authored_b", "algebra_authored_c", "algebra_authored_d",
                    "algebra_authored_e", "algebra_authored_f"]


def spread_answers(qid, script):
    """Hand-written asks tend to put the right choice in the same slot. Rotate each one in a stable
    way so that a child cannot learn "it is always the middle one"."""
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
    authored = {}
    for name in AUTHORED_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        lessons = importlib.import_module(name).LESSONS
        for qid, script in lessons.items():
            if qid in authored:
                sys.exit("%s has two lessons" % qid)
            spread_answers(qid, script)
            authored[qid] = script

    questions = [q for q in load_grade5() if topic_of(q) == "algebra"]
    ids = {q["id"] for q in questions}
    stray = sorted(set(authored) - ids)
    if stray:
        sys.exit("not algebra questions: %s" % ", ".join(stray))

    part = {}
    missing = []
    kinds = collections.Counter()
    for q in sorted(questions, key=lambda q: q["id"]):
        script = authored.get(q["id"]) or rule_for(q)
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
    for q in missing:
        print("  no lesson: %s  %s" % (q["id"], q["questionText"][:70]))


if __name__ == "__main__":
    main()

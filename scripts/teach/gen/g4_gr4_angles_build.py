"""Build data/teach/parts/g4-gr4_angles.json: a lesson for every Grade 4 angles question.

    python -X utf8 scripts/teach/gen/g4_gr4_angles_build.py

Rule-made lessons come from g4_gr4_angles_rules.py (one function per wording); lessons
written for one question come from g4_gr4_angles_authored_*.py. Every lesson is checked
with scripts/teach/validate.py; problems are printed. A lesson with problems is still
written so it can be read with --show, and the checker will refuse it.
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(ROOT, "scripts", "bank"))

from g4_gr4_angles_lib import teach_check  # noqa: E402
from g4_gr4_angles_rules import RULES  # noqa: E402
import bank  # noqa: E402

TOPIC = "gr4_angles"
AUTHORED = {}
for filename in sorted(os.listdir(HERE)):
    if filename.startswith("g4_gr4_angles_authored_") and filename.endswith(".py"):
        AUTHORED.update(__import__(filename[:-3]).LESSONS)

OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)


def main():
    questions = [q for q in bank.load_bank(4) if q.get("node") == TOPIC]
    ids = {q["id"] for q in questions}
    part = {}
    by_rule = collections.Counter()
    missing = []
    problems = []
    for qid in AUTHORED:
        if qid not in ids:
            problems.append("authored lesson for an id not in the topic: %s" % qid)
    for q in questions:
        qid = q["id"]
        script = None
        if qid in AUTHORED:
            script = AUTHORED[qid]
            by_rule["authored"] += 1
        else:
            for pattern, fn in RULES:
                m = pattern.match(q["questionText"].strip())
                if m:
                    script = fn(q, m)
                    by_rule[fn.__name__] += 1
                    break
        if script is None:
            missing.append(qid)
            continue
        problems += teach_check.check_script(qid, script, q)
        part[qid] = script

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote %d lessons of %d questions" % (len(part), len(questions)))
    for name, n in sorted(by_rule.items()):
        print("  %-28s %d" % (name, n))
    if missing:
        print("%d with no lesson yet:" % len(missing))
        for qid in missing[:15]:
            print("  " + qid)
    if problems:
        print("%d PROBLEMS" % len(problems))
        for p in problems[:80]:
            print("  " + p)


if __name__ == "__main__":
    main()

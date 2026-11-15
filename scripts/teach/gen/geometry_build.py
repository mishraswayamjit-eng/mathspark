"""Build data/teach/parts/geometry.json: a lesson for every Grade 5 geometry question.

    python -X utf8 scripts/teach/gen/geometry_build.py

Rule-made lessons come from geometry_rules.py (one function per wording); lessons written
for one question come from geometry_authored_*.py. Every lesson is checked with
scripts/teach/validate.py before the file is written; problems are printed.
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

from geometry_lib import teach_check  # noqa: E402
from geometry_rules import RULES  # noqa: E402

AUTHORED = {}
for filename in sorted(os.listdir(HERE)):
    if filename.startswith("geometry_authored_") and filename.endswith(".py"):
        AUTHORED.update(__import__(filename[:-3]).LESSONS)

OUT = os.path.join(ROOT, "data", "teach", "parts", "geometry.json")


def main():
    questions = [q for q in load_grade5() if topic_of(q) == "geometry"]
    part = {}
    by_rule = collections.Counter()
    missing = []
    problems = []
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
        found = teach_check.check_script(qid, script, q)
        problems += found
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

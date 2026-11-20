"""Build data/teach/parts/g4-gr4_triangles.json: a lesson for every Grade 4 triangles question.

    python -X utf8 scripts/teach/gen/g4_gr4_triangles.py

Rule-made lessons come from g4_gr4_triangles_rules.py (generated families only); lessons
written for one question come from g4_gr4_triangles_hand_*.py. Every lesson is checked with
scripts/teach/validate.py; only lessons that pass are written, and problems are printed.
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

from g4_gr4_triangles_lib import questions, teach_check  # noqa: E402
from g4_gr4_triangles_rules import RULES  # noqa: E402

AUTHORED = {}
for filename in sorted(os.listdir(HERE)):
    if filename.startswith("g4_gr4_triangles_hand_") and filename.endswith(".py"):
        AUTHORED.update(__import__(filename[:-3]).LESSONS)

OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_triangles.json")
GENERATED = re.compile(r"^(PH3_|VAR|BOOST)|_V\d+$")


def main():
    qs = questions()
    part = {}
    counts = collections.Counter()
    missing = []
    problems = []
    for q in qs:
        qid = q["id"]
        script = None
        if qid in AUTHORED:
            script = AUTHORED[qid]
            name = "authored"
        elif GENERATED.search(qid):
            for pattern, fn in RULES:
                m = pattern.match(q["questionText"].strip())
                if m:
                    script = fn(q, m)
                    name = fn.__name__
                    break
        if script is None:
            missing.append(qid)
            continue
        found = teach_check.check_script(qid, script, q)
        if found:
            problems += found
            continue
        counts[name] += 1
        part[qid] = script

    unknown = sorted(set(AUTHORED) - {q["id"] for q in qs})
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote %d lessons of %d questions" % (len(part), len(qs)))
    for name, n in sorted(counts.items()):
        print("  %-28s %d" % (name, n))
    if unknown:
        print("authored for ids not in the topic: %s" % ", ".join(unknown))
    if missing:
        print("%d with no lesson yet:" % len(missing))
        for qid in missing:
            print("  " + qid)
    if problems:
        print("%d PROBLEMS (those lessons were left out)" % len(problems))
        for p in problems[:80]:
            print("  " + p)


if __name__ == "__main__":
    main()

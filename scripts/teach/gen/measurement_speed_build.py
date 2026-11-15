"""Write data/teach/parts/measurement-speed.json: one lesson per measurement-speed question.

    python -X utf8 scripts/teach/gen/measurement_speed_build.py

Generated families get a lesson from a rule in measurement_speed_rules.py; one-off
questions get the lesson written for them in measurement_speed_authored.py.
Then check with: python -X utf8 scripts/teach/validate.py --part measurement-speed
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
from measurement_speed_rules import RULES  # noqa: E402

try:
    from measurement_speed_authored import AUTHORED  # noqa: E402
except ImportError:
    AUTHORED = {}

OUT = os.path.join(ROOT, "data", "teach", "parts", "measurement-speed.json")


def main():
    qs = [q for q in load_grade5() if topic_of(q) == "measurement-speed"]
    out = {}
    missing = []
    counts = collections.Counter()
    for q in qs:
        qid = q["id"]
        if qid in AUTHORED:
            out[qid] = AUTHORED[qid](q)
            counts["authored"] += 1
            continue
        for pattern, rule in RULES:
            m = pattern.match(q["questionText"].strip())
            if m:
                out[qid] = rule(q, m)
                counts[rule.__name__] += 1
                break
        else:
            missing.append(qid)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons of %d questions" % (len(out), len(qs)))
    for k, v in sorted(counts.items()):
        print("  %-18s %d" % (k, v))
    for qid in missing:
        print("  NO LESSON  %s" % qid)


if __name__ == "__main__":
    main()

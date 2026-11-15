"""Print squares-patterns questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/squares_patterns_dump.py oneoff 0 20   # one-off questions 0..19
    python -X utf8 scripts/teach/gen/squares_patterns_dump.py gen 0 20      # generated questions
    python -X utf8 scripts/teach/gen/squares_patterns_dump.py missing       # questions with no lesson yet
    python -X utf8 scripts/teach/gen/squares_patterns_dump.py EXT_G5_FP_2016   # ids starting with this
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "oneoff"
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    qs = [q for q in load_grade5() if topic_of(q) == "squares-patterns"]
    brief = False
    if what == "oneoff":
        qs = [q for q in qs if not q["id"].startswith(GENERATED)]
    elif what == "gen":
        qs = [q for q in qs if q["id"].startswith(GENERATED)]
    elif what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "squares-patterns.json")
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
        brief = True
    else:
        qs = [q for q in qs if q["id"].startswith(what)]
    total = len(qs)
    qs = qs[lo:hi]
    for q in qs:
        if brief:
            print(q["id"], "|", q["questionText"][:80])
            continue
        print("=" * 70)
        print(q["id"], "|", q.get("subTopic"), "|", q.get("source"))
        print("Q:", q["questionText"])
        for o in q.get("options", []):
            print("   ", o.get("id", "") if isinstance(o, dict) else "", o.get("text", "") if isinstance(o, dict) else o)
        print("KEY:", q.get("correctAnswer"))
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", ""))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            print("MIS %s: %s" % (k, v))
    print(len(qs), "of", total, "questions")


if __name__ == "__main__":
    main()

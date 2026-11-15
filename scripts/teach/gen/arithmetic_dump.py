"""Print arithmetic questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/arithmetic_dump.py oneoff 0 20     # one-off questions 0..19
    python -X utf8 scripts/teach/gen/arithmetic_dump.py VAR_EXT_G5_WS_B2_012   # ids starting with this
    python -X utf8 scripts/teach/gen/arithmetic_dump.py missing         # questions with no lesson yet
    python -X utf8 scripts/teach/gen/arithmetic_dump.py brief           # generated ones, one line each with options
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


def opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "oneoff"
    qs = [q for q in load_grade5() if topic_of(q) == "arithmetic"]
    if what == "brief":
        for q in qs:
            if q["id"].startswith(GENERATED):
                print(q["id"], "|", q["questionText"], "|", opts(q), q.get("correctAnswer"))
        return
    if what == "oneoff":
        qs = [q for q in qs if not q["id"].startswith(GENERATED)]
        if len(sys.argv) > 3:
            qs = qs[int(sys.argv[2]):int(sys.argv[3])]
    elif what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "arithmetic.json")
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
        for q in qs:
            print(q["id"], "|", q["questionText"][:90])
        print(len(qs), "missing")
        return
    else:
        qs = [q for q in qs if q["id"].startswith(what)]
    for q in qs:
        print("=" * 70)
        print(q["id"], "|", q.get("subTopic"), "|", q.get("source"))
        print("Q:", q["questionText"])
        print("OPTS:", " | ".join(opts(q)), "  KEY:", q.get("correctAnswer"))
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", ""))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            print("MIS %s: %s" % (k, v))
    print(len(qs), "questions")


if __name__ == "__main__":
    main()

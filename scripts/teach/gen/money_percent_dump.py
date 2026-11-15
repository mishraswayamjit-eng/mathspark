"""Print money-percent questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/money_percent_dump.py oneoff        # every one-off question
    python -X utf8 scripts/teach/gen/money_percent_dump.py VAR2          # ids starting with this
    python -X utf8 scripts/teach/gen/money_percent_dump.py missing       # questions with no lesson yet
    python -X utf8 scripts/teach/gen/money_percent_dump.py sample        # one of each generated wording
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def shape(text):
    return re.sub(r"[A-Z][a-z]+", "N", re.sub(r"\d+(\.\d+)?", "#", text))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "oneoff"
    qs = [q for q in load_grade5() if topic_of(q) == "money-percent"]
    if what == "oneoff":
        qs = [q for q in qs if not q["id"].startswith(GENERATED)]
    elif what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "money-percent.json")
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
    elif what == "sample":
        seen = set()
        keep = []
        for q in qs:
            if not q["id"].startswith(GENERATED):
                continue
            words = shape(q["questionText"]).split()
            key = " ".join(words[:3] + words[-4:])
            if key not in seen:
                seen.add(key)
                keep.append(q)
        qs = keep
    else:
        qs = [q for q in qs if q["id"].startswith(what)]
    for q in qs:
        print("=" * 70)
        print(q["id"], "|", q.get("subTopic"), "|", q.get("source"))
        print("Q:", q["questionText"])
        for o in q.get("options", []):
            print("   ", o.get("id", "") if isinstance(o, dict) else "", o.get("text", "") if isinstance(o, dict) else o)
        print("KEY:", q.get("correctAnswer"))
        for h in q.get("hints") or []:
            print("HINT:", h)
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", ""))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            print("MIS %s: %s" % (k, v))
    print(len(qs), "questions")


if __name__ == "__main__":
    main()

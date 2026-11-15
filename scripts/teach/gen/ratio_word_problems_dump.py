"""Print ratio-word-problems questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/ratio_word_problems_dump.py oneoff     # every one-off question
    python -X utf8 scripts/teach/gen/ratio_word_problems_dump.py gen        # generated families, briefly
    python -X utf8 scripts/teach/gen/ratio_word_problems_dump.py missing    # questions with no lesson yet
    python -X utf8 scripts/teach/gen/ratio_word_problems_dump.py <prefix>   # ids starting with this
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
PART = "ratio-word-problems"


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "oneoff"
    qs = [q for q in load_grade5() if topic_of(q) == PART]
    brief = False
    if what == "oneoff":
        qs = [q for q in qs if not q["id"].startswith(GENERATED)]
    elif what == "gen":
        qs = [q for q in qs if q["id"].startswith(GENERATED)]
        brief = True
    elif what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", PART + ".json")
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
    else:
        qs = [q for q in qs if q["id"].startswith(what)]
    for q in qs:
        print("=" * 70)
        print(q["id"], "|", q.get("subTopic"), "|", q.get("source"))
        print("Q:", q["questionText"])
        opts = [(o.get("text", "") if isinstance(o, dict) else str(o)) for o in q.get("options", [])]
        print("OPTS:", " | ".join(opts), " KEY:", q.get("correctAnswer"))
        if brief:
            continue
        for h in q.get("hints") or []:
            print("HINT:", h)
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", ""))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            print("MIS %s: %s" % (k, v))
    print(len(qs), "questions")


if __name__ == "__main__":
    main()

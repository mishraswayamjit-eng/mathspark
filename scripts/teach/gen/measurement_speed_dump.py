"""Print measurement-speed questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/measurement_speed_dump.py oneoff     # every one-off question
    python -X utf8 scripts/teach/gen/measurement_speed_dump.py VAR2       # ids starting with this
    python -X utf8 scripts/teach/gen/measurement_speed_dump.py missing    # questions with no lesson yet
    python -X utf8 scripts/teach/gen/measurement_speed_dump.py lessons A B   # lessons number A to B, as spoken
    python -X utf8 scripts/teach/gen/measurement_speed_dump.py ids X Y Z     # lessons whose id ends with X, Y or Z
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
PART = os.path.join(ROOT, "data", "teach", "parts", "measurement-speed.json")


def have():
    if os.path.exists(PART):
        with io.open(PART, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "oneoff"
    qs = [q for q in load_grade5() if topic_of(q) == "measurement-speed"]
    if what in ("lessons", "ids"):
        lessons = have()
        if what == "ids":
            wanted = sys.argv[2:]
            chosen = [q for q in qs if any(q["id"].endswith(x) for x in wanted)]
        else:
            a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            b = int(sys.argv[3]) if len(sys.argv) > 3 else a
            chosen = qs[a:b + 1]
        for q in chosen:
            print("=" * 70)
            print(q["id"])
            print("Q:", q["questionText"])
            for i, beat in enumerate(lessons.get(q["id"], {}).get("beats", [])):
                print(" %2d  %s" % (i + 1, beat["say"]))
                for op in beat.get("board", []):
                    rest = {k: v for k, v in op.items() if k != "op"}
                    print("       [%s] %s" % (op["op"], json.dumps(rest, ensure_ascii=False)))
                if beat.get("ask"):
                    ask = beat["ask"]
                    if ask["kind"] == "choose":
                        print("       ASK %s -> %d | %s" % (ask["choices"], ask["answer"], ask["ifNot"]))
                    else:
                        print("       ASK think")
        return
    if what == "oneoff":
        qs = [q for q in qs if not q["id"].startswith(GENERATED)]
    elif what == "missing":
        lessons = have()
        qs = [q for q in qs if q["id"] not in lessons]
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

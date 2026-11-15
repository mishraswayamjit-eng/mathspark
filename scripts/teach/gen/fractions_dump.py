"""Print fractions questions in full, for writing lessons.

    python -X utf8 scripts/teach/gen/fractions_dump.py 81 137        # by index range in the topic list
    python -X utf8 scripts/teach/gen/fractions_dump.py --grep "Which is greater" --max 3
    python -X utf8 scripts/teach/gen/fractions_dump.py --opts          # option/answer shapes of the generated families
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of, option_texts  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lo", nargs="?", type=int)
    ap.add_argument("hi", nargs="?", type=int)
    ap.add_argument("--grep")
    ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--opts", action="store_true")
    ap.add_argument("--brief", action="store_true")
    args = ap.parse_args()
    qs = sorted([q for q in load_grade5() if topic_of(q) == "fractions"], key=lambda q: q["id"])
    n = 0
    for i, q in enumerate(qs):
        if args.lo is not None and not (args.lo <= i <= (args.hi if args.hi is not None else args.lo)):
            continue
        if args.grep and args.grep not in q["questionText"]:
            continue
        n += 1
        if n > args.max:
            break
        opts = option_texts(q)
        key = q.get("correctAnswer")
        if args.opts or args.brief:
            print("%3d %s | %s | %s | key %s" % (i, q["id"], q["questionText"], " ; ".join(opts), key))
            continue
        print("=== %d %s  [%s]" % (i, q["id"], q.get("subTopic")))
        print("Q: %s" % q["questionText"])
        print("OPTS: %s   KEY %s" % (" | ".join(opts), key))
        for s in q.get("stepByStep") or []:
            print("  STEP: %s" % s.get("text", ""))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            if v:
                print("  MIS %s: %s" % (k, v))
    print("%d shown" % min(n, args.max))


if __name__ == "__main__":
    main()

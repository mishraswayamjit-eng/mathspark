"""Print batch 15 compactly, for reading.

    python -X utf8 scripts/teach/gen/imported_15_dump.py [start] [end]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-15.json"), encoding="utf-8") as f:
        batch = json.load(f)
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    b = int(sys.argv[2]) if len(sys.argv) > 2 else len(batch)
    for i, q in enumerate(batch[a:b], a):
        print("#%d %s [%s %s]" % (i, q["id"], q["topic"], q["difficulty"]))
        print("  Q:", q["question"])
        print("  O:", " | ".join("%s) %s" % (k, v) for k, v in q["options"].items()), " ANS:", q["answer"])
        print("  S:", " ;; ".join((s.get("latex") or s.get("text") or "")[:90] for s in q["steps"]))


if __name__ == "__main__":
    main()

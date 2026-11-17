"""Print the in-17 batch compactly (id, question, options, answer), for the writer.

    python -X utf8 scripts/teach/gen/imported_17_dump.py [start] [end]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-17.json"), encoding="utf-8") as f:
        batch = json.load(f)
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    b = int(sys.argv[2]) if len(sys.argv) > 2 else len(batch)
    for i, q in enumerate(batch[a:b], a):
        print("%d %s [%s] %s" % (i, q["id"], q["topic"], q["difficulty"]))
        print("   Q: %s" % q["question"].replace("\n", " / "))
        print("   " + " | ".join("%s) %s" % (k, v) for k, v in sorted(q["options"].items())) + "   ANS " + q["answer"])
        if len(sys.argv) > 3:
            for s in q["steps"]:
                print("      - %s  %s" % (s.get("text", "").replace("\n", " "), s.get("latex", "")))


if __name__ == "__main__":
    main()

"""Scratch helper: dump the place-value questions in full to a text file to read.

    python -X utf8 scripts/teach/gen/place_value_dump.py            # write place_value_dump.txt
    python -X utf8 scripts/teach/gen/place_value_dump.py --remove   # delete it again
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of, option_texts  # noqa: E402

OUT = os.path.join(HERE, "place_value_dump.txt")


def main():
    if "--remove" in sys.argv:
        if os.path.exists(OUT):
            os.remove(OUT)
        print("removed")
        return
    qs = [q for q in load_grade5() if topic_of(q) == "place-value"]
    brief = "--brief" in sys.argv
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for i, q in enumerate(qs):
            f.write("#%d %s [%s] {%s}\n" % (i, q["id"], q.get("subTopic", ""), q.get("source", "")))
            f.write("Q: %s\n" % q["questionText"].replace("\n", " // "))
            f.write("O: %s  KEY %s\n" % (" | ".join(option_texts(q)), q.get("correctAnswer")))
            if not brief:
                for s in q.get("stepByStep") or []:
                    f.write("S: %s\n" % s.get("text", "").replace("\n", " // "))
                for k, v in sorted((q.get("misconceptions") or {}).items()):
                    if v:
                        f.write("M%s: %s\n" % (k, v.replace("\n", " // ")))
            f.write("\n")
    print("wrote %d questions" % len(qs))


if __name__ == "__main__":
    main()

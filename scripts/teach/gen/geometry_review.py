"""Look over data/teach/parts/geometry.json for things the checker does not catch.

    python -X utf8 scripts/teach/gen/geometry_review.py            # the flags
    python -X utf8 scripts/teach/gen/geometry_review.py say <id>   # just what the teacher says, to read aloud
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "geometry.json")

MARKS = {"arc", "strike", "note", "mark", "both", "divide", "group"}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    if len(sys.argv) > 2 and sys.argv[1] == "say":
        for i, beat in enumerate(part[sys.argv[2]]["beats"]):
            print("%2d  %s" % (i + 1, beat["say"]))
            if beat.get("ask"):
                print("      ? %s" % " | ".join(beat["ask"].get("choices", ["(think)"])))
        return

    lengths = collections.Counter()
    origins = collections.Counter()
    flags = []
    for qid, script in sorted(part.items()):
        beats = script["beats"]
        lengths[len(beats)] += 1
        origins[script["origin"]] += 1
        ops = [op for beat in beats for op in beat.get("board", [])]
        if not any(op["op"] in MARKS for op in ops):
            flags.append("%s: no marks on the board" % qid)
        figures = [op for op in ops if op["op"] == "figure"]
        if not figures and "check" not in script:
            flags.append("%s: no figure" % qid)
        first = beats[0].get("board", [])
        if "check" not in script and not any(op["op"] == "figure" for op in first):
            flags.append("%s: no figure in the first beat" % qid)
        ids = [op["id"] for op in figures]
        if len(ids) != len(set(ids)):
            flags.append("%s: a figure id is used twice" % qid)
        asks = [b for b in beats if b.get("ask")]
        if len(asks) < 2:
            flags.append("%s: only %d ask" % (qid, len(asks)))
        for i, beat in enumerate(beats):
            n = len(sentences(beat["say"]))
            if n > 4:
                flags.append("%s beat %d: %d sentences (%d chars)" % (qid, i + 1, n, len(beat["say"])))
            if len(beat.get("board", [])) == 0 and not beat.get("ask") and i not in (len(beats) - 1,):
                flags.append("%s beat %d: nothing on the board and no ask" % (qid, i + 1))
    print("%d lessons; origin %s" % (len(part), dict(origins)))
    print("beats per lesson: %s" % ", ".join("%d×%d" % (n, k) for k, n in sorted(lengths.items())))
    print("%d flags" % len(flags))
    for flag in flags:
        print("  " + flag)


if __name__ == "__main__":
    main()

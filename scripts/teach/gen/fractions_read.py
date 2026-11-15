"""Read fractions lessons compactly, the way a child would hear them.

    python -X utf8 scripts/teach/gen/fractions_read.py <question id> [<question id> ...]
    python -X utf8 scripts/teach/gen/fractions_read.py --grep "Which is greater" --every 9
    python -X utf8 scripts/teach/gen/fractions_read.py --stats
"""
import argparse
import collections
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions_lib import OUT, questions  # noqa: E402


def show(q, script):
    print("=== %s  [%s]  %s" % (q["id"], script["origin"], q["questionText"]))
    for i, beat in enumerate(script["beats"]):
        print(" %2d. %s" % (i + 1, beat["say"]))
        for op in beat.get("board", []):
            kind = op["op"]
            if kind == "write":
                print("        | %s%s" % (op["text"], "   <%s>" % op["tone"] if op.get("tone") else ""))
            elif kind == "figure":
                spec = op["spec"]
                if spec["kind"] == "fractionBars":
                    print("        [bars %s]" % ", ".join("%s/%s %s" % (b["shaded"], b["parts"], b.get("label", "")) for b in spec["bars"]))
                elif spec["kind"] == "set":
                    print("        [set %s in %s groups, %s shaded]" % (spec["total"], spec.get("groups"), spec.get("shadedGroups", 0)))
                else:
                    print("        [%s]" % spec["kind"])
            else:
                rest = {k: v for k, v in op.items() if k not in ("op", "line")}
                print("        (%s %s: %s)" % (kind, op.get("line"), json.dumps(rest, ensure_ascii=False)))
        ask = beat.get("ask")
        if ask and ask["kind"] == "choose":
            print("        ? %s   -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
            print("        ifNot: %s" % ask["ifNot"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--grep")
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    qs = questions()
    if args.stats:
        beats = collections.Counter(len(part[q["id"]]["beats"]) for q in qs if q["id"] in part)
        longest = max(len(b["say"]) for s in part.values() for b in s["beats"])
        asks = collections.Counter(sum(1 for b in part[q["id"]]["beats"] if b.get("ask")) for q in qs if q["id"] in part)
        marks = sum(1 for s in part.values() if not any(op["op"] not in ("write", "figure") for b in s["beats"] for op in b.get("board", [])))
        print("beats per lesson: %s" % sorted(beats.items()))
        print("asks per lesson:  %s" % sorted(asks.items()))
        print("longest thing said: %d characters" % longest)
        print("lessons with no board marks at all: %d" % marks)
        return
    n = 0
    for q in qs:
        if q["id"] not in part:
            continue
        if args.ids and q["id"] not in args.ids:
            continue
        if args.grep and args.grep not in q["questionText"]:
            continue
        n += 1
        if (n - 1) % args.every:
            continue
        show(q, part[q["id"]])


if __name__ == "__main__":
    main()

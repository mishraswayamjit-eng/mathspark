"""Print algebra lessons compactly, to read them the way a child would hear them.

    python -X utf8 scripts/teach/gen/algebra_read.py <id or id-prefix> [...]   # those lessons
    python -X utf8 scripts/teach/gen/algebra_read.py --every 9 VAR_G5         # every 9th lesson with that prefix
    python -X utf8 scripts/teach/gen/algebra_read.py --stats                   # sizes and marks across the part
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "algebra.json")


def show(qid, script):
    print("=" * 78)
    print(qid, "(%s)" % script["origin"], script.get("check", ""))
    for i, beat in enumerate(script["beats"]):
        print("%2d  %s" % (i + 1, beat["say"]))
        for op in beat.get("board", []):
            rest = {k: v for k, v in op.items() if k != "op"}
            if op["op"] == "write":
                extra = [k for k in ("tone", "label") if k in rest]
                print("      [%s] %s%s" % (rest["id"], rest["text"], ("   <%s>" % ",".join(
                    str(rest[k]) if k == "tone" else k for k in extra)) if extra else ""))
            else:
                print("      %s %s" % (op["op"], json.dumps(rest, ensure_ascii=False)))
        ask = beat.get("ask")
        if ask and ask["kind"] == "choose":
            print("      ? %s   -> %s" % (" | ".join(ask["choices"]), ask["choices"][ask["answer"]]))
            print("      ifNot: %s" % ask["ifNot"])
        elif ask:
            print("      ? (think)")


def stats(part):
    beats = collections.Counter()
    ops = collections.Counter()
    asks = collections.Counter()
    longest = 0
    for script in part.values():
        beats[len(script["beats"])] += 1
        n = 0
        for beat in script["beats"]:
            longest = max(longest, len(beat["say"]))
            for op in beat.get("board", []):
                ops[op["op"]] += 1
            if beat.get("ask"):
                n += 1
        asks[n] += 1
    slots = collections.Counter()
    for script in part.values():
        for beat in script["beats"]:
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                slots["%d of %d" % (ask["answer"] + 1, len(ask["choices"]))] += 1
    print("right choice in slot:", dict(sorted(slots.items())))
    print("lessons:", len(part))
    print("beats per lesson:", dict(sorted(beats.items())))
    print("asks per lesson:", dict(sorted(asks.items())))
    print("board ops:", dict(ops.most_common()))
    print("longest say:", longest)
    says = collections.Counter(b["say"] for s in part.values() for b in s["beats"])
    print("most repeated lines:")
    for text, n in says.most_common(8):
        print("  %3d  %s" % (n, text))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    args = sys.argv[1:]
    if args and args[0] == "--stats":
        stats(part)
        return
    every = 1
    if args and args[0] == "--every":
        every = int(args[1])
        args = args[2:]
    for prefix in args:
        ids = sorted(k for k in part if k.startswith(prefix))
        for qid in ids[::every]:
            show(qid, part[qid])


if __name__ == "__main__":
    main()

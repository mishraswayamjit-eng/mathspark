"""Print several squares-patterns lessons compactly, to read them the way a child hears them.

    python -X utf8 scripts/teach/gen/squares_patterns_read.py <question id or prefix> [more ...]
    python -X utf8 scripts/teach/gen/squares_patterns_read.py --stats
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from squares_patterns_lib import PART, questions  # noqa: E402


def brief(op):
    kind = op["op"]
    if kind == "write":
        tag = op.get("tone", "work") + (", words" if op.get("label") else "")
        return "write [%s] %s" % (tag, op["text"])
    if kind == "figure":
        spec = op["spec"]
        if spec["kind"] == "grid":
            return "figure grid %d × %d%s" % (spec["rows"], spec["cols"], " dots" if spec.get("dots") else "")
        return "figure %s" % json.dumps(spec, ensure_ascii=False)
    rest = {k: v for k, v in op.items() if k != "op"}
    return "%s %s" % (kind, json.dumps(rest, ensure_ascii=False))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = questions()
    args = sys.argv[1:]
    if args == ["--stats"]:
        beats = collections.Counter(len(s["beats"]) for s in part.values())
        asks = collections.Counter(sum(1 for b in s["beats"] if b.get("ask")) for s in part.values())
        marks = collections.Counter()
        figs = 0
        nomark = []
        for qid, s in part.items():
            n = 0
            has_fig = False
            for b in s["beats"]:
                for op in b.get("board", []):
                    if op["op"] not in ("write", "figure", "clear"):
                        marks[op["op"]] += 1
                        n += 1
                    if op["op"] == "figure":
                        has_fig = True
            figs += has_fig
            if n == 0:
                nomark.append(qid)
        longest = max(len(b["say"]) for s in part.values() for b in s["beats"])
        print("lessons", len(part), "| beats per lesson", sorted(beats.items()))
        print("asks per lesson", sorted(asks.items()))
        print("marks", dict(marks), "| lessons with a figure", figs, "| longest say", longest)
        print("lessons with no mark at all:", nomark)
        firsts = collections.Counter(s["beats"][i]["ask"]["answer"] for s in part.values()
                                     for i in range(len(s["beats"])) if s["beats"][i].get("ask", {}).get("kind") == "choose")
        print("position of the right choice", sorted(firsts.items()))
        return
    for qid in sorted(part):
        if not any(qid == a or qid.startswith(a) for a in args):
            continue
        q = qs[qid]
        print("=" * 78)
        print("%s  [%s]" % (qid, part[qid]["origin"]))
        print("Q: %s" % q["questionText"])
        for i, b in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, b["say"]))
            for op in b.get("board", []):
                print("       · %s" % brief(op))
            ask = b.get("ask")
            if ask and ask["kind"] == "choose":
                print("       ? %s   (right: %s)" % (" | ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("       ~ %s" % ask["ifNot"])


if __name__ == "__main__":
    main()

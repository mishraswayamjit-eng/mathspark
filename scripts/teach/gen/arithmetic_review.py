"""Print arithmetic lessons compactly, the way a child would hear them, for reading before they ship.

    python -X utf8 scripts/teach/gen/arithmetic_review.py <question id> [<question id> ...]
    python -X utf8 scripts/teach/gen/arithmetic_review.py --stats
"""
import collections
import io
import json
import sys

from arithmetic_common import PART, questions


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = questions()
    if sys.argv[1:] == ["--stats"]:
        beats = collections.Counter(len(s["beats"]) for s in part.values())
        asks = collections.Counter(sum(1 for b in s["beats"] if b.get("ask")) for s in part.values())
        marks = collections.Counter()
        unmarked = []
        for qid, s in part.items():
            n = sum(1 for b in s["beats"] for op in b.get("board", []) if op["op"] not in ("write", "figure", "clear"))
            marks[min(n, 5)] += 1
            if n == 0:
                unmarked.append(qid)
        longest = max(len(b["say"]) for s in part.values() for b in s["beats"])
        print("lessons", len(part), "of", len(qs))
        print("beats per lesson", sorted(beats.items()))
        print("asks per lesson", sorted(asks.items()))
        print("marks per lesson (5 = 5 or more)", sorted(marks.items()))
        print("lessons with no marks", unmarked)
        print("longest thing said", longest)
        return
    for qid in sys.argv[1:]:
        s = part[qid]
        print("=" * 60)
        print(qid, "|", qs[qid]["questionText"].replace("\n", " / "))
        for i, b in enumerate(s["beats"]):
            print(" %2d. %s" % (i + 1, b["say"]))
            for op in b.get("board", []):
                if op["op"] == "write":
                    print("       [%s] %s" % (op.get("tone", "work"), op["text"]))
                elif op["op"] == "figure":
                    print("       (figure: %s)" % op["spec"]["kind"])
                else:
                    t = op.get("target") or op.get("targets") or op.get("from") or ""
                    extra = op.get("note") or op.get("text") or op.get("by") or op.get("label") or op.get("shape") or ""
                    print("       ~%s %s %s" % (op["op"], json.dumps(t, ensure_ascii=False), extra))
            if b.get("ask"):
                a = b["ask"]
                if a["kind"] == "choose":
                    print("       ASK %s  -> %s" % (" | ".join(a["choices"]), a["choices"][a["answer"]]))
                    print("       IF NOT: %s" % a["ifNot"])
                else:
                    print("       ASK (think)")


if __name__ == "__main__":
    main()

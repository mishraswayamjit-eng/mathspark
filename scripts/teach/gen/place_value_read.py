"""Print several place-value lessons compactly, to read them the way a child hears them.

    python -X utf8 scripts/teach/gen/place_value_read.py <question id> [<question id> ...]
    python -X utf8 scripts/teach/gen/place_value_read.py --lengths     # longest things said, beats per lesson
"""
import collections
import io
import json
import sys

from place_value_lib import PART, load_questions


def brief(op):
    k = op["op"]
    if k == "write":
        return "WRITE[%s%s] %s" % (op.get("tone", "work")[0], "L" if op.get("label") else "", op["text"])
    if k == "figure":
        s = op["spec"]
        extra = s.get("number") or s.get("rows") or ("%s..%s" % (s.get("min"), s.get("max")))
        return "FIG %s %s %s %s" % (s["kind"], extra, s.get("headers", ""), s.get("highlight", ""))
    if k in ("mark", "note", "strike"):
        t = op["target"]
        return "%s %s@%s#%d %s %s" % (k.upper(), t["text"], op["line"], t.get("nth", 1), op.get("shape", ""), op.get("text", op.get("note", "")))
    return "%s %s" % (k.upper(), json.dumps({a: b for a, b in op.items() if a != "op"}, ensure_ascii=False))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in load_questions()}
    if "--lengths" in sys.argv:
        says = []
        counts = collections.Counter()
        for qid, lesson in part.items():
            counts[len(lesson["beats"])] += 1
            for beat in lesson["beats"]:
                says.append((len(beat["say"]), qid, beat["say"]))
        print("beats per lesson:", sorted(counts.items()))
        for n, qid, say in sorted(says, reverse=True)[:12]:
            print(n, qid, say)
        return
    for qid in sys.argv[1:]:
        q = qs[qid]
        print("=" * 100)
        print("%s  [%s]  Q: %s" % (qid, part[qid]["origin"], q["questionText"]))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("        " + brief(op))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("        ASK %s  right=%s" % (ask["choices"], ask["choices"][ask["answer"]]))
                print("        IFNOT %s" % ask["ifNot"])


if __name__ == "__main__":
    main()

"""Read factors lessons the way a child would hear them, several at a time.

    python -X utf8 scripts/teach/gen/factors_read.py <id or id prefix> [...]   # those lessons
    python -X utf8 scripts/teach/gen/factors_read.py --sample 12 3             # every 12th lesson, starting at the 3rd
    python -X utf8 scripts/teach/gen/factors_read.py --stats                   # lengths, and beats that run long
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "factors.json")
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")


def brief(op):
    kind = op["op"]
    if kind == "write":
        return "[%s] %s" % (op.get("tone", "label" if op.get("label") else "work"), op["text"])
    if kind == "figure":
        spec = op["spec"]
        extra = spec.get("number") or spec.get("both") or ""
        return "(figure: %s %s)" % (spec["kind"], extra)
    if kind in ("mark", "strike", "note"):
        t = op["target"]
        more = op.get("note") or op.get("text") or op.get("shape") or ""
        return "(%s %s%s on %s: %s)" % (kind, t["text"], "#%d" % t["nth"] if "nth" in t else "", op["line"], more)
    return "(%s %s)" % (kind, json.dumps({k: v for k, v in op.items() if k != "op"}, ensure_ascii=False))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    args = sys.argv[1:]
    if args and args[0] == "--stats":
        beats = [len(s["beats"]) for s in part.values()]
        print("lessons %d, beats %d to %d, mean %.1f" % (len(part), min(beats), max(beats), sum(beats) / len(beats)))
        for qid, script in part.items():
            for i, beat in enumerate(script["beats"]):
                sentences = len(re.findall(r"[.!?](?:\s|$)", beat["say"].replace("a.m.", "am").replace("p.m.", "pm").replace("Mr.", "Mr")))
                if len(beat["say"]) > 215 or sentences > 4:
                    print("LONG %s beat %d (%d chars, %d sentences): %s" % (qid, i + 1, len(beat["say"]), sentences, beat["say"]))
        return
    if args and args[0] == "--sample":
        step, start = int(args[1]), int(args[2]) if len(args) > 2 else 0
        ids = list(part)[start::step]
    else:
        ids = [qid for qid in part if any(qid == a or qid.startswith(a) for a in args)]
    with io.open(SEED, encoding="utf-8") as f:
        questions = {q["id"]: q for q in json.load(f)["questions"]}
    for qid in ids:
        q = questions[qid]
        print("=" * 78)
        print("%s  [%s]  %s" % (qid, part[qid]["origin"], q["questionText"]))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("       %s" % brief(op))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("       ASK %s  -> %s" % (" | ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("       IF NOT: %s" % ask["ifNot"])
    print("%d lessons" % len(ids))


if __name__ == "__main__":
    main()

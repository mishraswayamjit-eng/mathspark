"""Print whole lessons from data/teach/parts/g4-gr4_triangles.json, to read as a child would hear them.

    python -X utf8 scripts/teach/gen/g4_gr4_triangles_read.py <question id> [<question id> ...]
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_read.py slice 0 10     # by sorted id
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_read.py says           # every say, compact
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
from g4_gr4_triangles_lib import questions  # noqa: E402

PART = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_triangles.json")


def brief(op):
    k = op["op"]
    if k == "write":
        return "WRITE %s[%s]%s  %s" % (op["id"], op.get("tone", "work"), " label" if op.get("label") else "", op["text"])
    if k == "figure":
        return "FIG   %s" % json.dumps(op["spec"], ensure_ascii=False)
    return "%-5s %s" % (k.upper(), json.dumps({a: b for a, b in op.items() if a != "op"}, ensure_ascii=False))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in questions()}
    args = sys.argv[1:]
    if args and args[0] == "slice":
        ids = sorted(part)[int(args[1]):int(args[2])]
    elif args and args[0] == "says":
        for qid in sorted(part):
            print("== %s" % qid)
            for beat in part[qid]["beats"]:
                print("   " + beat["say"])
                if beat.get("ask", {}).get("ifNot"):
                    print("      [%s] -> %s" % (" | ".join(beat["ask"]["choices"]), beat["ask"]["ifNot"]))
        return
    else:
        ids = args
    for qid in ids:
        q = qs[qid]
        print("=" * 72)
        print("%s  (%s, %s)" % (qid, q.get("difficulty"), part[qid]["origin"]))
        print("Q: %s" % q["questionText"])
        print("   %s   key %s" % (" | ".join(o["text"] for o in q["options"]), q["correctAnswer"]))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("       " + brief(op))
            a = beat.get("ask")
            if a:
                if a["kind"] == "think":
                    print("       ASK think")
                else:
                    print("       ASK %s  (right: %s)" % (" | ".join(a["choices"]), a["choices"][a["answer"]]))
                    print("           if not: %s" % a["ifNot"])


if __name__ == "__main__":
    main()

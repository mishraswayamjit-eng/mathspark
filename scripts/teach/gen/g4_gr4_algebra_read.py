"""Print whole lessons from the built part, the way a child would meet them, for reading.

    python -X utf8 scripts/teach/gen/g4_gr4_algebra_read.py rule 0 12      # rule lessons 0..11 of the sorted list
    python -X utf8 scripts/teach/gen/g4_gr4_algebra_read.py authored 0 12  # hand-written lessons 0..11
    python -X utf8 scripts/teach/gen/g4_gr4_algebra_read.py id <question id> [<question id> ...]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_algebra.json")


def brief(op):
    k = op["op"]
    if k == "write":
        return "WRITE[%s]%s %s" % (op["id"], " (%s)" % op["tone"] if op.get("tone") else "", op["text"])
    if k == "figure":
        return "FIGURE %s" % op["spec"].get("kind")
    rest = {a: b for a, b in op.items() if a != "op"}
    return "%s %s" % (k.upper(), json.dumps(rest, ensure_ascii=False))


def main():
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in bank.load_bank(4) if q.get("node") == "gr4_algebra"}
    what = sys.argv[1]
    if what == "id":
        ids = sys.argv[2:]
    else:
        ids = sorted(i for i in part if part[i]["origin"] == what)[int(sys.argv[2]):int(sys.argv[3])]
    for qid in ids:
        q = qs[qid]
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("=" * 78)
        print("%s  [%s]  %s" % (qid, q.get("difficulty"), q["questionText"]))
        print("   %s   key %s" % (" | ".join(opts), q["correctAnswer"]))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("       " + brief(op))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("       ASK %s  -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("       IF NOT: %s" % ask["ifNot"])


if __name__ == "__main__":
    main()

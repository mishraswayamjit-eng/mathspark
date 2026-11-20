"""Print whole lessons compactly, several at a time, for reading.

    python -X utf8 scripts/teach/gen/g4_gr4_factors_read.py <question id> [<question id> ...]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_factors.json")


def op_text(op):
    k = op["op"]
    if k == "write":
        tone = op.get("tone", "")
        return "[%s%s] %s" % (op["id"], "/" + tone if tone else "", op["text"])
    if k == "figure":
        s = op["spec"]
        return "FIGURE %s %s" % (s.get("kind"), json.dumps({a: b for a, b in s.items() if a != "kind"}, ensure_ascii=False)[:150])
    if k in ("mark", "strike", "note"):
        t = op["target"]
        extra = op.get("shape") or op.get("note") or op.get("text") or ""
        return "%s %s:'%s'%s %s" % (k, op["line"], t["text"], "#%d" % t["nth"] if t.get("nth") else "", extra)
    return json.dumps(op, ensure_ascii=False)


def main():
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in bank.load_bank(4) if q.get("node") == "gr4_factors"}
    for qid in sys.argv[1:]:
        q = qs[qid]
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("=" * 60)
        print(qid, "|", q["questionText"], "|", " ; ".join(opts), "|", q["correctAnswer"], "|", part[qid]["origin"])
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("       " + op_text(op))
            ask = beat.get("ask")
            if ask:
                if ask["kind"] == "choose":
                    print("       ASK %s -> %s | IF NOT: %s" % (ask["choices"], ask["choices"][ask["answer"]], ask["ifNot"]))
                else:
                    print("       ASK think")


if __name__ == "__main__":
    main()

"""Print built lessons compactly, for reading many in one go (the same content as validate.py --show).

    python -X utf8 scripts/teach/gen/g4_gr4_equations_read.py rule [start] [count]
    python -X utf8 scripts/teach/gen/g4_gr4_equations_read.py authored [start] [count]
    python -X utf8 scripts/teach/gen/g4_gr4_equations_read.py <id> <id> ...
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_equations_lib import OUT, questions  # noqa: E402


def brief(op):
    k = op["op"]
    if k == "write":
        return "[%s%s] %s" % (op["id"], {"given": " given", "answer": " ANSWER"}.get(op.get("tone"), ""), op["text"])
    if k == "figure":
        return "figure " + json.dumps(op["spec"], ensure_ascii=False)
    rest = {a: b for a, b in op.items() if a != "op"}
    return "%s %s" % (k, json.dumps(rest, ensure_ascii=False))


def main():
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in questions()}
    args = sys.argv[1:]
    if args and args[0] in ("rule", "authored"):
        ids = sorted(i for i in part if part[i]["origin"] == args[0])
        start = int(args[1]) if len(args) > 1 else 0
        count = int(args[2]) if len(args) > 2 else 10
        ids = ids[start:start + count]
    else:
        ids = args
    for qid in ids:
        q = qs[qid]
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]
        print("=" * 78)
        print("%s  [%s, %s]" % (qid, q.get("difficulty"), part[qid]["origin"]))
        print("Q: %s" % q["questionText"])
        print("   %s   (key %s)" % (" | ".join(opts), q.get("correctAnswer")))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("        " + brief(op))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("      ? %s   -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("      ifNot: %s" % ask["ifNot"])
    print(len(ids), "lessons shown")


if __name__ == "__main__":
    main()

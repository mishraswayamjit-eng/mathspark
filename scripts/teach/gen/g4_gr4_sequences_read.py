"""Print whole lessons of a part compactly, for reading many in a row.

    python -X utf8 scripts/teach/gen/g4_gr4_sequences_read.py gr4_sequences rule 0 12
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_read.py gr4_puzzles authored 0 20
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_read.py gr4_puzzles <id prefix>
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_sequences_lib import part_path, questions  # noqa: E402


def brief(op):
    k = op["op"]
    if k == "write":
        return "[%s%s] %s" % (op["id"], {"given": " given", "answer": " ANSWER"}.get(op.get("tone"), ""), op["text"])
    if k == "figure":
        s = op["spec"]
        return "FIGURE %s %s" % (s.get("kind"), json.dumps({x: y for x, y in s.items() if x in ("rows", "headers", "note")}, ensure_ascii=False)[:200])
    if k in ("note", "strike"):
        t = op["target"]
        return "%s %s@%s#%d: %s" % (k, op["line"], t["text"], t.get("nth", 1), op.get("text") or op.get("note") or "")
    if k == "mark":
        return "%s %s@%s" % (op["shape"], op["line"], op["target"]["text"])
    if k == "group":
        return "group %s %s: %s" % (op["line"], [t["text"] for t in op["targets"]], op.get("label", ""))
    return json.dumps(op, ensure_ascii=False)


def main():
    topic, what = sys.argv[1], sys.argv[2]
    lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    qs = questions(topic)
    with io.open(part_path(topic), encoding="utf-8") as f:
        part = json.load(f)
    ids = sorted(part)
    if what in ("rule", "authored"):
        ids = [i for i in ids if part[i]["origin"] == what][lo:hi]
    else:
        ids = [i for i in ids if i.startswith(what)]
    for qid in ids:
        q = qs[qid]
        key = "ABCD".find(q["correctAnswer"])
        opts = [o.get("text", "") for o in q["options"]]
        print("=" * 78)
        print("%s  [%s]  %s" % (qid, q.get("difficulty"), q["questionText"].replace("\n", " / ")))
        print("   options: %s   KEY: %s" % (" | ".join(opts), opts[key]))
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("        " + brief(op))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("        ASK %s  -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("        IF NOT: " + ask["ifNot"])
            elif ask:
                print("        ASK (think)")
    print(len(ids), "lessons")


if __name__ == "__main__":
    main()

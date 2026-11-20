"""Print whole lessons compactly, for reading.

    python -X utf8 scripts/teach/gen/g4_gr4_operations_read.py <id or id prefix> [more ids...]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_operations_common import PART, questions, opts  # noqa: E402


def main():
    qs = questions()
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    n = 0
    for want in sys.argv[1:]:
        for qid, script in part.items():
            if not (qid == want or (want.endswith("*") and qid.startswith(want[:-1]))):
                continue
            q = qs[qid]
            n += 1
            print("=" * 78)
            print(qid, "|", q["questionText"].replace("\n", " / "), "|", opts(q), q.get("correctAnswer"))
            for i, beat in enumerate(script["beats"]):
                print(" %2d. %s" % (i + 1, beat["say"]))
                for op in beat.get("board", []):
                    k = op["op"]
                    if k == "write":
                        print("       [%s%s] %s" % (op["id"], {"given": " given", "answer": " ANSWER"}.get(op.get("tone"), ""), op["text"]))
                    elif k == "figure":
                        print("       FIGURE %s" % json.dumps(op["spec"], ensure_ascii=False)[:150])
                    else:
                        print("       %s %s" % (k, json.dumps({a: b for a, b in op.items() if a != "op"}, ensure_ascii=False)))
                ask = beat.get("ask")
                if ask:
                    if ask["kind"] == "think":
                        print("       ASK think")
                    else:
                        print("       ASK %s -> %s | ifNot: %s" % (ask["choices"], ask["choices"][ask["answer"]], ask["ifNot"]))
    print(n, "lessons")


if __name__ == "__main__":
    main()

"""Print whole lessons compactly, several at a time, to read them as a child would hear them.

    python -X utf8 scripts/teach/gen/g4_gr4_fractions_read.py <question id> [<question id> ...]
    python -X utf8 scripts/teach/gen/g4_gr4_fractions_read.py --range 0 9      # by index in the topic list
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_fractions_lib import OUT, option_texts, questions  # noqa: E402


def main():
    qs = questions()
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    args = sys.argv[1:]
    if args and args[0] == "--range":
        ids = [q["id"] for q in qs[int(args[1]):int(args[2]) + 1]]
    else:
        ids = args
    by_id = {q["id"]: q for q in qs}
    for qid in ids:
        q = by_id[qid]
        print("=" * 8, qid, "[%s]" % q.get("difficulty"))
        print("Q:", q["questionText"], "|", " ; ".join(option_texts(q)), "| key", q["correctAnswer"])
        for i, beat in enumerate(part[qid]["beats"]):
            print(" %2d. %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                k = op["op"]
                if k == "write":
                    print("       [%s%s] %s" % (op["id"], "/" + op["tone"] if op.get("tone") else "", op["text"]))
                elif k == "figure":
                    s = op["spec"]
                    if s["kind"] == "fractionBars":
                        d = "; ".join("%d/%d %s" % (b["shaded"], b["parts"], b.get("label", "")) for b in s["bars"])
                    elif s["kind"] == "barModel":
                        d = " | ".join("%s%s" % (g.get("label", ""), "*" if g.get("tone") == "a" else "") for g in s["bars"][0]["segments"]) + \
                            "  {%s}" % s["bars"][0].get("brace", "")
                    elif s["kind"] == "set":
                        d = "%d in %d groups, %d shaded" % (s["total"], s.get("groups", 1), s.get("shadedGroups", 0))
                    else:
                        d = json.dumps({k2: v for k2, v in s.items() if k2 != "kind"}, ensure_ascii=False)
                    print("       <%s> %s" % (s["kind"], d))
                else:
                    rest = {k2: v for k2, v in op.items() if k2 != "op"}
                    print("       (%s) %s" % (k, json.dumps(rest, ensure_ascii=False)))
            ask = beat.get("ask")
            if ask and ask["kind"] == "choose":
                print("       ASK %s  -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("       IFNOT %s" % ask["ifNot"])
            elif ask:
                print("       ASK (think)")


if __name__ == "__main__":
    main()

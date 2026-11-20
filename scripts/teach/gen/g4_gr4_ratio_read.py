"""Print whole lessons of a Grade 4 part compactly, for reading them through.

    python -X utf8 scripts/teach/gen/g4_gr4_ratio_read.py <topic> rule            # every lesson made by rule
    python -X utf8 scripts/teach/gen/g4_gr4_ratio_read.py <topic> authored <from> <to>   # authored lessons from..to
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
from g4_gr4_ratio_lib import questions  # noqa: E402


def show_op(op):
    k = op["op"]
    if k == "write":
        tone = op.get("tone", "work")
        return "%s[%s] %s" % ({"given": "Q", "work": "W", "answer": "ANS"}[tone], op["id"], op["text"])
    if k == "figure":
        s = op["spec"]
        if s["kind"] == "barModel":
            return "FIG bars: " + " / ".join(
                "%s(%s)%s" % (b.get("label", ""), ",".join("%s%s" % (g.get("label", ""), "x%d" % g["units"] if g["units"] != 1 else "") or "." for g in b["segments"]),
                              " brace=" + b["brace"] if b.get("brace") else "") for b in s["bars"])
        return "FIG " + json.dumps(s, ensure_ascii=False)
    if k == "arc":
        return "arc %s: %s -> %s" % (op["line"], op["from"]["text"], [t["text"] for t in op["to"]])
    tgt = op.get("target") or {}
    extra = op.get("text") or op.get("note") or op.get("shape") or ""
    return "%s %s:'%s'%s %s" % (k, op.get("line"), tgt.get("text", ""), ("#%d" % tgt["nth"]) if tgt.get("nth") else "", extra)


def main():
    topic, what = sys.argv[1], sys.argv[2]
    with io.open(os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic), encoding="utf-8") as f:
        part = json.load(f)
    qs = [q for q in questions(topic) if q["id"] in part and part[q["id"]]["origin"] == what]
    if what == "authored" and len(sys.argv) > 4:
        qs = qs[int(sys.argv[3]):int(sys.argv[4])]
    for q in qs:
        opts = [(o.get("text", "") if isinstance(o, dict) else str(o)) for o in q.get("options", [])]
        print("=" * 60)
        print(q["id"], "|", q.get("difficulty"))
        print("Q:", q["questionText"], "  [", " | ".join(opts), "] key", q["correctAnswer"])
        for i, b in enumerate(part[q["id"]]["beats"]):
            print("%2d. %s" % (i + 1, b["say"]))
            for op in b.get("board", []):
                print("      " + show_op(op))
            a = b.get("ask")
            if a and a["kind"] == "choose":
                print("      ASK " + " | ".join(("*" if j == a["answer"] else "") + c for j, c in enumerate(a["choices"])))
                print("      IFNOT " + a["ifNot"])
    print(len(qs), "lessons")


if __name__ == "__main__":
    main()

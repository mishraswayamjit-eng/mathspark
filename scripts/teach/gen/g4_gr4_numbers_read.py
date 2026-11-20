"""Scratch reader: print built lessons compactly to a text file, to read them as a child would hear them.

    python -X utf8 scripts/teach/gen/g4_gr4_numbers_read.py gr4_numbers rule        # the rule lessons
    python -X utf8 scripts/teach/gen/g4_gr4_numbers_read.py gr4_numbers authored 0 30   # authored lessons 0..29
    python -X utf8 scripts/teach/gen/g4_gr4_numbers_read.py gr4_squares labels      # label lines that hold an '='
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def main():
    topic, what = sys.argv[1], sys.argv[2]
    with io.open(os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic), encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in bank.load_bank(4) if q.get("node") == topic}
    out = os.path.join(HERE, "g4_%s_read.txt" % topic)
    lines = []
    if what == "labels":
        for qid, s in part.items():
            for beat in s["beats"]:
                for op in beat.get("board", []):
                    if op["op"] == "write" and op.get("label") and "=" in op["text"]:
                        lines.append("%-28s %s" % (qid, op["text"]))
    else:
        ids = [k for k, s in part.items() if s["origin"] == what]
        if len(sys.argv) > 4:
            ids = ids[int(sys.argv[3]):int(sys.argv[4])]
        for qid in ids:
            q = qs[qid]
            options = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
            lines.append("## %s [%s]  Q: %s" % (qid, q.get("difficulty", ""), q["questionText"]))
            lines.append("   OPTIONS %s   KEY %s" % (" | ".join(options), q["correctAnswer"]))
            for i, beat in enumerate(part[qid]["beats"]):
                lines.append("%2d. %s" % (i + 1, beat["say"]))
                for op in beat.get("board", []):
                    k = op["op"]
                    if k == "write":
                        lines.append("      [%s%s%s] %s" % (op["id"], " " + op["tone"] if op.get("tone") else "",
                                                           " L" if op.get("label") else "", op["text"]))
                    elif k == "figure":
                        sp = op["spec"]
                        lines.append("      [fig] %s %s %s" % (sp["kind"], sp.get("number", ""), sp.get("note", "")))
                    else:
                        rest = {x: y for x, y in op.items() if x != "op"}
                        lines.append("      [%s] %s" % (k, json.dumps(rest, ensure_ascii=False)))
                ask = beat.get("ask")
                if ask and ask["kind"] == "choose":
                    cs = ["%s%s" % (c, "*" if j == ask["answer"] else "") for j, c in enumerate(ask["choices"])]
                    lines.append("      ASK %s" % "  /  ".join(cs))
                    lines.append("      IFNOT %s" % ask["ifNot"])
                elif ask:
                    lines.append("      ASK (think)")
            lines.append("")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote %d lines to %s" % (len(lines), os.path.basename(out)))


if __name__ == "__main__":
    main()

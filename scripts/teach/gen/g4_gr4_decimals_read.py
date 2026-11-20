"""Print gr4_decimals lessons the way a child would meet them, several at a time.

    python -X utf8 scripts/teach/gen/g4_gr4_decimals_read.py 0 14        # lessons 0..13 of the part, in file order
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_read.py PYQ          # ids starting with this
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_read.py lint         # soft checks the validator does not make
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

PART = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_decimals.json")


def short(op):
    k = op["op"]
    if k == "write":
        return "WRITE%s%s  %s" % ("/" + op["tone"] if op.get("tone") else "", "/label" if op.get("label") else "", op["text"])
    if k == "figure":
        s = op["spec"]
        bits = [s["kind"]]
        for key in ("number", "note", "highlight"):
            if s.get(key):
                bits.append("%s=%s" % (key, s[key]))
        if s["kind"] == "table":
            bits.append(json.dumps(s["rows"], ensure_ascii=False))
        if s["kind"] == "numberLine":
            bits.append(json.dumps(s.get("points"), ensure_ascii=False))
        return "FIGURE  " + "  ".join(str(b) for b in bits)
    rest = {a: b for a, b in op.items() if a != "op"}
    return "%-6s  %s" % (k.upper(), json.dumps(rest, ensure_ascii=False))


def show(qid, script, q):
    print("=" * 78)
    print("%s  [%s, %s, %s]" % (qid, q.get("difficulty"), script.get("origin"), len(script["beats"])))
    print("Q: " + q["questionText"])
    opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]
    print("   %s   (key %s)" % (" | ".join(opts), q.get("correctAnswer")))
    for i, beat in enumerate(script["beats"]):
        print(" %2d  %s" % (i + 1, beat["say"]))
        for op in beat.get("board", []):
            print("       · " + short(op))
        ask = beat.get("ask")
        if ask:
            if ask["kind"] == "think":
                print("       ? (think)")
            else:
                print("       ? %s   -> %s" % (" | ".join(ask["choices"]), ask["choices"][ask["answer"]]))
                print("         if not: " + ask["ifNot"])


def lint(part, questions):
    n = 0
    for qid, script in part.items():
        beats = script["beats"]
        asks = sum(1 for b in beats if b.get("ask"))
        marks = sum(1 for b in beats for op in b.get("board", []) if op["op"] not in ("write", "figure"))
        long_says = [b["say"] for b in beats if len(b["say"]) > 215]
        sentences = [b["say"] for b in beats if len(re.findall(r"[.!?](?:\s|$)", b["say"])) > 4]
        notes = []
        if asks < 2:
            notes.append("only %d ask" % asks)
        if marks == 0:
            notes.append("no marks")
        if long_says:
            notes.append("%d long says" % len(long_says))
        if sentences:
            notes.append("%d says with 5+ sentences" % len(sentences))
        if notes:
            n += 1
            print("%-32s %s" % (qid, "; ".join(notes)))
    print(n, "lessons with notes, of", len(part))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    questions = {q["id"]: q for q in bank.load_bank(4)}
    args = sys.argv[1:]
    if args and args[0] == "lint":
        lint(part, questions)
        return
    ids = list(part)
    if len(args) == 2 and args[0].isdigit():
        ids = ids[int(args[0]):int(args[1])]
    elif args:
        ids = [i for i in ids if i.startswith(args[0])]
    for qid in ids:
        show(qid, part[qid], questions[qid])
    print(len(ids), "lessons")


if __name__ == "__main__":
    main()

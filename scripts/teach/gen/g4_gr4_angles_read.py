"""Print whole lessons from the built part, compactly, for reading.

    python -X utf8 scripts/teach/gen/g4_gr4_angles_read.py <id> <id> ...
    python -X utf8 scripts/teach/gen/g4_gr4_angles_read.py prefix <prefix> [start] [end]
    python -X utf8 scripts/teach/gen/g4_gr4_angles_read.py stats
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

PART = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_angles.json")


def op_text(op):
    k = op["op"]
    if k == "write":
        return "W[%s]%s %s" % (op["id"], {"given": "(given)", "answer": "(ANSWER)"}.get(op.get("tone"), ""), op["text"])
    if k == "figure":
        s = op["spec"]
        bits = [s["kind"]]
        for key in ("layout", "facing", "hour", "minute", "shape"):
            if key in s:
                bits.append(str(s[key]))
        if "parts" in s:
            bits.append("/".join(p["label"] for p in s["parts"]))
        if "turns" in s:
            bits.append(" ".join("%d%s" % (t["degrees"], t["direction"][0]) for t in s["turns"]))
        return "FIG " + " ".join(bits)
    rest = {kk: v for kk, v in op.items() if kk != "op"}
    return "%s %s" % (k, json.dumps(rest, ensure_ascii=False))


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in bank.load_bank(4) if q.get("node") == "gr4_angles"}
    args = sys.argv[1:]
    if args and args[0] == "stats":
        longest = max((len(b["say"]), qid) for qid, s in part.items() for b in s["beats"])
        print("lessons", len(part), "longest say", longest)
        counts = sorted(len(s["beats"]) for s in part.values())
        print("beats min/max", counts[0], counts[-1])
        return
    if args and args[0] == "prefix":
        ids = sorted(i for i in part if i.startswith(args[1]))
        if len(args) > 3:
            ids = ids[int(args[2]):int(args[3])]
    else:
        ids = args
    for qid in ids:
        q = qs[qid]
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("=" * 60)
        print(qid, "|", q["questionText"])
        print("   ", " | ".join(opts), " key", q["correctAnswer"])
        for i, beat in enumerate(part[qid]["beats"]):
            print("%2d  %s" % (i + 1, beat["say"]))
            for op in beat.get("board", []):
                print("      · " + op_text(op))
            a = beat.get("ask")
            if a and a["kind"] == "choose":
                print("      ? %s  -> %s" % (" / ".join(a["choices"]), a["choices"][a["answer"]]))
                print("      ! " + a["ifNot"])


if __name__ == "__main__":
    main()

"""Print the source strings of gr4_decimals questions (for the narration writer to read).

    python -X utf8 scripts/speech/g4/gr4_decimals_dump.py            # compact list of every question
    python -X utf8 scripts/speech/g4/gr4_decimals_dump.py 0 40       # full source for questions 0..39
    python -X utf8 scripts/speech/g4/gr4_decimals_dump.py out 0 40   # source and narration side by side
    python -X utf8 scripts/speech/g4/gr4_decimals_dump.py diff 0 40  # only the lines whose narration differs from print
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NODE = "gr4_decimals"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")


def questions():
    return sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])


def main():
    qs = questions()
    args = sys.argv[1:]
    mode = "src"
    if args and args[0] in ("out", "diff"):
        mode = args[0]
        args = args[1:]
    if not args:
        for i, q in enumerate(qs):
            print("%3d %-28s %s" % (i, q["id"], q.get("questionText", "").replace("\n", " // ")[:110]))
        return
    part = {}
    if mode != "src" and os.path.exists(OUT):
        with io.open(OUT, encoding="utf-8") as f:
            part = json.load(f)
    lo, hi = int(args[0]), int(args[1])

    def line(tag, a, b, extra=""):
        if not a.strip():
            return
        if mode == "src":
            print("%s: %s%s" % (tag, json.dumps(a, ensure_ascii=False), extra))
        elif mode == "diff":
            if a.strip() != b:
                print("%s: %s%s\n  > %s" % (tag, json.dumps(a, ensure_ascii=False), extra, b))
        else:
            print("%s: %s%s\n  > %s" % (tag, json.dumps(a, ensure_ascii=False), extra, b))

    for i, q in enumerate(qs[lo:hi], lo):
        src = common.source_strings(q)
        own = q.get("stepByStep") or []
        e = part.get(q["id"]) or {"q": "", "options": [""] * 4, "hints": [""] * 3, "steps": [""] * len(src["steps"])}
        print("=== %d %s" % (i, q["id"]))
        line("Q ", src["q"], e["q"])
        for j, o in enumerate(src["options"]):
            line("O%d" % j, o, e["options"][j])
        for j, h in enumerate(src["hints"]):
            line("H%d" % j, h, e["hints"][j])
        for j, s in enumerate(src["steps"]):
            lx = own[j].get("latex") if j < len(own) else None
            line("S%d" % j, s, e["steps"][j], ("   [latex: %s]" % lx) if lx else "")


if __name__ == "__main__":
    main()

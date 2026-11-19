"""Print the source strings of gr4_factors questions (for the narration writer to read).

    python -X utf8 scripts/speech/g4/gr4_factors_dump.py            # compact list of every question
    python -X utf8 scripts/speech/g4/gr4_factors_dump.py 0 40       # full source for questions 0..39
    python -X utf8 scripts/speech/g4/gr4_factors_dump.py out 0 40   # source and narration side by side (differences only)
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NODE = "gr4_factors"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")


def questions():
    return sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])


def main():
    qs = questions()
    args = sys.argv[1:]
    side = False
    brief = False
    if args and args[0] == "new":            # new: only the questions whose help was rewritten, side by side
        with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
            listed = set(json.load(f)[NODE])
        qs = [q for q in qs if q["id"] in listed]
        args = ["out", "0", str(len(qs))]
    if args and args[0] in ("out", "say"):   # say: only the narrated lines that differ from print
        side = True
        brief = args[0] == "say"
        args = args[1:]
    if not args:
        for i, q in enumerate(qs):
            print("%3d %-28s %s" % (i, q["id"], q.get("questionText", "").replace("\n", " // ")[:110]))
        return
    part = {}
    if side and os.path.exists(OUT):
        with io.open(OUT, encoding="utf-8") as f:
            part = json.load(f)
    lo, hi = int(args[0]), int(args[1])
    for i, q in enumerate(qs[lo:hi], lo):
        src = common.source_strings(q)
        own = q.get("stepByStep") or []
        e = part.get(q["id"])
        print("=== %d %s" % (i, q["id"]))

        def line(tag, s, spoken, extra=""):
            if not s.strip():
                return
            if brief:
                if s.strip() != spoken and not s.strip().isdigit():
                    print("%s> %s" % (tag, spoken))
            elif e is None:
                print("%s: %s%s" % (tag, json.dumps(s, ensure_ascii=False), extra))
            elif s.strip() == spoken:
                print("%s= %s" % (tag, spoken))
            else:
                print("%s: %s%s\n   > %s" % (tag, json.dumps(s, ensure_ascii=False), extra, spoken))

        line("Q ", src["q"], e and e["q"])
        for j, o in enumerate(src["options"]):
            line("O%d" % j, o, e and e["options"][j])
        for j, h in enumerate(src["hints"]):
            line("H%d" % j, h, e and e["hints"][j])
        for j, s in enumerate(src["steps"]):
            lx = own[j].get("latex") if j < len(own) else None
            line("S%d" % j, s, e and e["steps"][j], ("   [latex: %s]" % lx) if lx else "")


if __name__ == "__main__":
    main()

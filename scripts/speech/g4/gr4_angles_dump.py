"""Print the source strings of gr4_angles questions (for the narration writer to read).

    python -X utf8 scripts/speech/g4/gr4_angles_dump.py            # compact list of every question
    python -X utf8 scripts/speech/g4/gr4_angles_dump.py 0 40       # full source for questions 0..39
    python -X utf8 scripts/speech/g4/gr4_angles_dump.py out 0 40   # source and narration side by side
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NODE = "gr4_angles"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")


def questions():
    return sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])


def main():
    qs = questions()
    args = sys.argv[1:]
    side = False
    if args and args[0] == "out":
        side = True
        args = args[1:]
    if not args:
        for i, q in enumerate(qs):
            print("%3d %-28s %s" % (i, q["id"], q.get("questionText", "").replace("\n", " // ")[:110]))
        return
    if args and args[0] == "re":
        # The questions whose help was rewritten: new source of hints and steps, with narration under each.
        with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
            listed = set(json.load(f).get(NODE, []))
        part = {}
        if os.path.exists(OUT):
            with io.open(OUT, encoding="utf-8") as f:
                part = json.load(f)
        chosen = [q for q in qs if q["id"] in listed]
        lo, hi = (int(args[1]), int(args[2])) if len(args) > 2 else (0, len(chosen))
        print("%d listed, %d found" % (len(listed), len(chosen)))
        for q in chosen[lo:hi]:
            src = common.source_strings(q)
            own = q.get("stepByStep") or []
            e = part.get(q["id"])
            print("=== %s" % q["id"])
            print("Q : %s" % src["q"])
            print("O : %s" % " | ".join(src["options"]))
            for key, tag in (("hints", "H"), ("steps", "S")):
                for j, t in enumerate(src[key]):
                    lx = own[j].get("latex") if key == "steps" and j < len(own) else None
                    print("%s%d: %s%s" % (tag, j, json.dumps(t, ensure_ascii=False), ("   [latex: %s]" % lx) if lx else ""))
                    if e and j < len(e[key]):
                        print("  > " + e[key][j])
        return
    if args and args[0] == "nar":
        # Narration only, for reading back as the voice would say it.
        with io.open(OUT, encoding="utf-8") as f:
            part = json.load(f)
        for i, q in enumerate(qs[int(args[1]):int(args[2])], int(args[1])):
            e = part[q["id"]]
            print("=== %d %s" % (i, q["id"]))
            print("Q : " + e["q"])
            print("O : " + " | ".join(e["options"]))
            for j, h in enumerate(e["hints"]):
                print("H%d: %s" % (j, h))
            for j, s in enumerate(e["steps"]):
                print("S%d: %s" % (j, s))
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
        print("Q : " + json.dumps(src["q"], ensure_ascii=False))
        if e:
            print("  > " + e["q"])
        for j, o in enumerate(src["options"]):
            print("O%d: %s" % (j, json.dumps(o, ensure_ascii=False)))
            if e:
                print("  > " + e["options"][j])
        for j, h in enumerate(src["hints"]):
            print("H%d: %s" % (j, json.dumps(h, ensure_ascii=False)))
            if e:
                print("  > " + e["hints"][j])
        for j, s in enumerate(src["steps"]):
            lx = own[j].get("latex") if j < len(own) else None
            print("S%d: %s%s" % (j, json.dumps(s, ensure_ascii=False), ("   [latex: %s]" % lx) if lx else ""))
            if e:
                print("  > " + e["steps"][j])


if __name__ == "__main__":
    main()

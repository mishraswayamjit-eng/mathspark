"""List Grade 4 questions of a topic, for the figure writer.

    python -X utf8 scripts/figures/authoring/g4_gr4_time_list.py gr4_time summary
    python -X utf8 scripts/figures/authoring/g4_gr4_time_list.py gr4_time full 0 60 [regex on id or text]
    python -X utf8 scripts/figures/authoring/g4_gr4_time_list.py gr4_time brief 0 400 [regex]
    python -X utf8 scripts/figures/authoring/g4_gr4_time_list.py gr4_time show 0 40 [regex]   (with figures from the part file)
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def prefix(qid):
    return re.sub(r"\d+", "#", qid)


def brief(f):
    """One line for a figure."""
    if f is None:
        return "-"
    k = f["kind"]
    if k == "table":
        s = "TABLE " + (" | ".join(f.get("headers", [])) + " :: " if f.get("headers") else "") + " / ".join(" | ".join(r) for r in f["rows"])
    elif k == "barChart":
        s = "CHART " + ", ".join("%s=%g" % (b["label"], b["value"]) for b in f["bars"]) + (" each=%g" % f["each"] if "each" in f else "") + (" unit=" + f["unit"] if "unit" in f else "")
    elif k == "barModel":
        s = "BARS " + " ;; ".join("%s[%s]%s" % (b.get("label", ""), " | ".join("%s~%g%s" % (x.get("label", "_"), x["units"], "?" if x.get("tone") == "unknown" else "") for x in b["segments"]), "{%s}" % b["brace"] if "brace" in b else "") for b in f["bars"])
    elif k == "numberLine":
        s = "LINE %g..%g/%g %s pts[%s] hops[%s]" % (f["min"], f["max"], f["step"], f.get("tickLabels", ""), ", ".join("%g:%s" % (p["at"], p.get("label", "")) for p in f.get("points", [])), ", ".join("%g>%g:%s" % (h["from"], h["to"], h.get("label", "")) for h in f.get("hops", [])))
    elif k == "clock":
        s = "CLOCK %d:%02d%s" % (f["hour"], f["minute"], " angle" if f.get("showAngle") else "")
    elif k == "journey":
        s = "ROAD " + " ... ".join(f["places"]) + " legs " + " ; ".join("%s/%s" % (g.get("top", ""), g.get("bottom", "")) for g in f["legs"])
    else:
        s = json.dumps({x: y for x, y in f.items() if x not in ("note", "highlight")}, ensure_ascii=False)
    return s + ("  NOTE: " + f["note"] if "note" in f else "") + ("  HL " + ",".join(f["highlight"]) if "highlight" in f else "")


def main():
    topic = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "summary"
    qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
    if mode == "summary":
        print(len(qs), "questions")
        c = collections.Counter((prefix(q["id"]), q.get("source"), q.get("subTopic")) for q in qs)
        for k, v in sorted(c.items()):
            print("%4d  %s" % (v, k))
        print("keys:", sorted(qs[0].keys()))
        return
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    pat = sys.argv[5] if len(sys.argv) > 5 else None
    if pat:
        qs = [q for q in qs if re.search(pat, q["id"] + " || " + q.get("questionText", ""), re.I)]
    part = {}
    if mode == "figs":
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        qs = [q for q in qs if q["id"] in part]
        for q in qs[start:start + count]:
            e = part[q["id"]]
            print("=== %s  %s%s" % (q["id"], e["origin"], " usesOptions" if e.get("usesOptions") else ""))
            print("Q: %s  [%s]" % (q.get("questionText", "").replace("\n", " / "), " | ".join(o["text"] for o in q["options"])))
            print("  B: " + brief(e.get("figure")))
            for i, f in enumerate(e.get("stepFigures") or []):
                print("  %d: %s" % (i, brief(f)))
        return
    if mode == "show":
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        if len(sys.argv) > 6 and sys.argv[6] == "only":
            qs = [q for q in qs if q["id"] in part]
        if len(sys.argv) > 6 and sys.argv[6] == "none":
            qs = [q for q in qs if q["id"] not in part]
    print(len(qs), "match")
    for q in qs[start:start + count]:
        opts = " | ".join("%s) %s" % (o["id"], o["text"]) for o in q.get("options", []))
        if mode == "brief":
            print("%s :: %s :: %s :: ans %s :: %d steps" % (q["id"], q.get("questionText", "").replace("\n", " / "), opts, q.get("correctAnswer"), len(q.get("stepByStep") or [])))
            continue
        print("=" * 8, q["id"], "[%s]" % q.get("subTopic"), q.get("source"))
        print("Q:", q.get("questionText", "").replace("\n", " / "))
        print("O:", opts, " ANS", q.get("correctAnswer"))
        for i, s in enumerate(q.get("stepByStep") or []):
            print("  s%d: %s  {%s}" % (i, s.get("text", ""), s.get("latex") or ""))
        if mode == "show":
            e = part.get(q["id"])
            if e:
                print("  FIG:", json.dumps(e.get("figure"), ensure_ascii=False), "essential" if e.get("essential") else "", e.get("origin"))
                for i, f in enumerate(e.get("stepFigures") or []):
                    print("   f%d: %s" % (i, json.dumps(f, ensure_ascii=False)))
            else:
                print("  (no figure)")


main()

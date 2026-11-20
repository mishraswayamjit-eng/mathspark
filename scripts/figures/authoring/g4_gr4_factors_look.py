"""Print questions of a Grade 4 topic for reading (a working aid for the figure writer).

    python -X utf8 scripts/figures/authoring/g4_gr4_factors_look.py gr4_factors summary
    python -X utf8 scripts/figures/authoring/g4_gr4_factors_look.py gr4_factors brief 0 200
    python -X utf8 scripts/figures/authoring/g4_gr4_factors_look.py gr4_factors full 0 40 [id-prefix]
    python -X utf8 scripts/figures/authoring/g4_gr4_factors_look.py gr4_factors figs 0 40 [kind]
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def family(qid):
    return re.sub(r"\d+", "#", qid)


def main():
    topic, mode = sys.argv[1], sys.argv[2]
    qs = sorted([q for q in bank.load_bank(4) if q.get("node") == topic], key=lambda q: q["id"])
    if mode == "summary":
        print(len(qs), "questions")
        for k, v in collections.Counter(family(q["id"]) for q in qs).most_common():
            print("  %4d  %s" % (v, k))
        for k, v in collections.Counter(q.get("subTopic") for q in qs).most_common():
            print("  sub %4d  %s" % (v, k))
        for k, v in collections.Counter(q.get("source") for q in qs).most_common():
            print("  src %4d  %s" % (v, k))
        print("  no steps:", sum(1 for q in qs if not q.get("stepByStep")))
        print("  keys:", sorted(qs[0].keys()))
        return
    lo, hi = int(sys.argv[3]), int(sys.argv[4])
    extra = sys.argv[5] if len(sys.argv) > 5 else None
    part = {}
    path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
    if mode == "figs":
        qs = [q for q in qs if q["id"] in part and (not extra or part[q["id"]].get("figure", {}).get("kind") == extra
                                                     or any(f and f["kind"] == extra for f in part[q["id"]].get("stepFigures", [])))]
    elif mode == "nofig":
        qs = [q for q in qs if q["id"] not in part and (not extra or re.search(extra, q["questionText"], re.I))]
    elif extra:
        qs = [q for q in qs if re.search(extra, q["id"]) or re.search(extra, q["questionText"], re.I)]
    print(len(qs), "match")
    for q in qs[lo:hi]:
        opts = " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"])
        text = q["questionText"].replace("\n", " ⏎ ")
        if mode == "brief":
            print("%s [%s] %s  {%s} =%s  (%d steps)%s" % (q["id"], q.get("subTopic"), text, opts, q["correctAnswer"],
                                                         len(q.get("stepByStep") or []), " FIG" if q["id"] in part else ""))
            continue
        print("=" * 100)
        print(q["id"], "[%s]" % q.get("subTopic"), q.get("source"))
        print("Q:", text)
        print("O:", opts, " KEY", q["correctAnswer"])
        v = part.get(q["id"])
        if v and "figure" in v:
            print("  FIGURE:", json.dumps(v["figure"], ensure_ascii=False), "| origin", v["origin"],
                  "| essential" if v.get("essential") else "", "| usesOptions" if v.get("usesOptions") else "")
        for i, s in enumerate(q.get("stepByStep") or []):
            print("  S%d: %s%s" % (i, s.get("text", "").replace("\n", " ⏎ "), ("   [latex: %s]" % s["latex"]) if s.get("latex") else ""))
            if v and v.get("stepFigures") and v["stepFigures"][i]:
                print("      FIG:", json.dumps(v["stepFigures"][i], ensure_ascii=False))


main()

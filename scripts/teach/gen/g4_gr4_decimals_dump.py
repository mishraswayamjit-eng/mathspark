"""Print gr4_decimals questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_decimals_dump.py stats          # counts by id family and wording
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_dump.py all            # write every question to g4_gr4_decimals_all.txt
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_dump.py missing        # questions with no lesson yet (printed)
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_dump.py ids            # ids, one per line with difficulty
    python -X utf8 scripts/teach/gen/g4_gr4_decimals_dump.py <prefix>       # ids starting with this (printed)
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

TOPIC = "gr4_decimals"
PART = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
FIGS = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


def shape(text):
    return re.sub(r"[A-Z][a-z]+", "N", re.sub(r"\d+(\.\d+)?", "#", text))


def family(qid):
    m = re.match(r"(.*?)(_V\d+|_\d+)?$", qid)
    return re.sub(r"\d+", "#", qid)


def text_of(q, figs):
    out = []
    out.append("=" * 70)
    out.append("%s | %s | %s | %s%s" % (q["id"], q.get("subTopic"), q.get("difficulty"), q.get("source"),
                                       " | FIG" if q["id"] in figs else ""))
    out.append("Q: " + q["questionText"])
    for o in q.get("options", []):
        out.append("    %s %s" % ((o.get("id", ""), o.get("text", "")) if isinstance(o, dict) else ("", o)))
    out.append("KEY: %s" % q.get("correctAnswer"))
    for h in q.get("hints") or []:
        out.append("HINT: %s" % h)
    for s in q.get("stepByStep") or []:
        out.append("STEP: %s" % (s.get("text", "") if isinstance(s, dict) else s))
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        out.append("MIS %s: %s" % (k, v))
    return "\n".join(out)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "stats"
    qs = questions()
    figs = {}
    if os.path.exists(FIGS):
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
    if what == "stats":
        fam = collections.Counter(family(q["id"]) for q in qs)
        for k, n in sorted(fam.items()):
            print("%4d  %s" % (n, k))
        print(len(qs), "questions;", len(figs), "figure entries")
        print(collections.Counter(q.get("difficulty") for q in qs))
        print(collections.Counter(q.get("source") for q in qs))
        print(collections.Counter(q.get("subTopic") for q in qs))
        return
    if what == "ids":
        for q in qs:
            print(q["id"], "|", q.get("difficulty"), "|", q.get("source"), "|", q["questionText"][:90].replace("\n", " "))
        return
    if what == "all":
        path = os.path.join(HERE, "g4_gr4_decimals_all.txt")
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            for q in qs:
                f.write(text_of(q, figs) + "\n")
        print("wrote", path, len(qs))
        return
    if what == "figs":
        path = os.path.join(HERE, "g4_gr4_decimals_figs.txt")
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            for qid, entry in figs.items():
                f.write("== %s\n" % qid)
                f.write("  F: %s\n" % json.dumps(entry.get("figure"), ensure_ascii=False))
                for i, s in enumerate(entry.get("stepFigures") or []):
                    f.write("  S%d: %s\n" % (i, json.dumps(s, ensure_ascii=False)))
        print("wrote", path, len(figs))
        return
    if what == "missing":
        have = {}
        if os.path.exists(PART):
            with io.open(PART, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
    else:
        qs = [q for q in qs if q["id"].startswith(what)]
    for q in qs:
        print(text_of(q, figs))
    print(len(qs), "questions")


if __name__ == "__main__":
    main()

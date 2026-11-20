"""Working aid: writes my three topics' questions as plain text for reading (not part of the build)."""
import io
import os
import sys
import collections
import re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "bank")))
import bank  # noqa: E402

TOPICS = ("gr4_equations", "gr4_ages", "gr4_algebra")
qs = bank.load_bank(4)
for t in TOPICS:
    mine = [q for q in qs if q.get("node") == t]
    fam = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in mine)
    src = collections.Counter(q.get("source") for q in mine)
    print(t, len(mine), dict(src))
    for k, v in fam.most_common():
        print("   ", v, k)
    out = os.path.join(HERE, "g4_%s_dump.txt" % t)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        for q in sorted(mine, key=lambda q: q["id"]):
            f.write("### %s | %s | %s | key %s\n" % (q["id"], q.get("subTopic"), q.get("source"), q.get("correctAnswer")))
            f.write("Q: %s\n" % q.get("questionText", "").replace("\n", " / "))
            if q.get("questionLatex"):
                f.write("QL: %s\n" % q["questionLatex"])
            f.write("O: %s\n" % " | ".join("%s) %s" % (o.get("id"), o.get("text")) for o in q.get("options", [])))
            for i, s in enumerate(q.get("stepByStep") or []):
                f.write("  %d. %s%s\n" % (i, s.get("text", "").replace("\n", " / "), (" [L: %s]" % s["latex"]) if s.get("latex") else ""))
            f.write("\n")
print("keys:", sorted(mine[0].keys()))

"""Exploration helper: dump my three topics to text files for reading, and print stats."""
import collections
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

TOPICS = ["gr4_numbers", "gr4_squares", "gr4_decimals"]


def family(qid):
    return re.sub(r"\d+", "#", qid)


def main():
    allq = bank.load_bank(4)
    for t in TOPICS:
        qs = [q for q in allq if q.get("node") == t]
        print("==", t, len(qs))
        fam = collections.Counter(family(q["id"]) for q in qs)
        for k, n in fam.most_common():
            print("   %4d %s" % (n, k))
        sub = collections.Counter(q.get("subTopic", "") for q in qs)
        for k, n in sub.most_common():
            print("   sub %4d %s" % (n, k))
        nosteps = sum(1 for q in qs if not q.get("stepByStep"))
        print("   no steps:", nosteps)
        out = os.path.join(HERE, "g4_%s_dump.txt" % t)
        with io.open(out, "w", encoding="utf-8", newline="\n") as f:
            for q in sorted(qs, key=lambda q: q["id"]):
                f.write("### %s | %s | %s | ans %s\n" % (q["id"], q.get("subTopic", ""), q.get("source", ""), q.get("correctAnswer")))
                f.write("Q: %s\n" % q.get("questionText", "").replace("\n", " / "))
                f.write("O: %s\n" % " | ".join("%s) %s" % (o.get("id"), o.get("text")) for o in q.get("options", [])))
                for i, s in enumerate(q.get("stepByStep") or []):
                    f.write("  S%d: %s\n" % (i, (s.get("text") or "").replace("\n", " / ")))
                f.write("\n")


if __name__ == "__main__":
    main()

"""Decide what to do with each Grade 4 original whose key the first reviewer did not confirm,
by comparing that reviewer with the blind second solver.

    python -X utf8 scripts/fixes/g4_key_decisions.py

Reads originals-out-*.json and blind-out-*.json; writes data/bank-import/g4/key-decisions.json
({ id: { "action": ..., "to": letter?, "why": ... } }). Changes nothing in the bank.

  correct   both reviewers, independently, reached the same option and it is not the key
  keep      the blind solver reached the keyed option (the first reviewer's doubt is not upheld,
            or it was only about a second option)... see "repair"
  repair    the key is right but another option is the same value or also right
  remove    both say it cannot be answered as written, or no option is right
  dispute   the two reviewers differ; needs a third look
"""
import collections
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

G4 = os.path.join(ROOT, "data", "bank-import", "g4")


def load_all(pattern):
    out = {}
    for path in sorted(glob.glob(os.path.join(G4, pattern))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                out[row["id"]] = row
    return out


def main():
    by_id = {q["id"]: q for q in bank.load_bank(4)}
    first = load_all("originals-out-*.json")
    blind = load_all("blind-out-*.json")
    decisions = {}
    tally = collections.Counter()
    by_group = collections.defaultdict(collections.Counter)
    disputes = []
    for qid, b in blind.items():
        q, f = by_id[qid], first[qid]
        key = q["correctAnswer"]
        f_ans = "cannot" if f["answerOk"] == "unsure" else (f.get("rightAnswer") or "none")
        b_ans = b["answer"]
        if f_ans == key:
            f_ans = "multiple"  # first reviewer: key right, another option right too
        if b_ans in "ABCD" and f_ans == b_ans and b_ans != key:
            d = {"action": "correct", "to": b_ans, "why": "%s | %s" % (f.get("issue") or "", b.get("working") or "")}
        elif b_ans == "multiple" and f_ans == "multiple":
            d = {"action": "repair", "why": "another option is also right: %s" % (b.get("also") or f.get("issue"))}
        elif b_ans in ("none", "cannot") and f_ans in ("none", "cannot"):
            d = {"action": "remove", "why": "%s | %s" % (f.get("issue") or "", b.get("working") or "")}
        elif b_ans == key and f_ans == "multiple":
            d = {"action": "repair", "why": "first reviewer: %s" % (f.get("issue") or "")}
        else:
            d = {"action": "dispute", "why": "key %s; first %s (%s); blind %s %s (%s)" % (
                key, f_ans, f.get("issue") or "", b_ans, b.get("confidence"), b.get("working") or "")}
            disputes.append((qid, d["why"]))
        decisions[qid] = d
        tally[d["action"]] += 1
        s = q.get("source") or ""
        by_group["past paper (EXT)" if s.startswith("g4_mse") else "past paper (PYQ)" if s.startswith("previous") else s][d["action"]] += 1

    print("%d doubted originals: %s" % (len(decisions), dict(tally)))
    for g, c in sorted(by_group.items()):
        print("  %-22s %s" % (g, dict(c)))
    print("\nDisputes (%d):" % len(disputes))
    for qid, why in disputes:
        print("  %s: %s" % (qid, why[:230]))
    with io.open(os.path.join(G4, "key-decisions.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(decisions, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()

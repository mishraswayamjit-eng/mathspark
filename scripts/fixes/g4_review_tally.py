"""Tally the reviewers' verdicts on the Grade 4 originals, and cross-check the two
transcriptions of the 2016-2019 papers against each other.

    python -X utf8 scripts/fixes/g4_review_tally.py

Reads data/bank-import/g4/originals-out-NN.json and the bank. Changes nothing.
"""
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

G4 = os.path.join(ROOT, "data", "bank-import", "g4")


def norm(text):
    return re.sub(r"[^a-z0-9.]+", "", (text or "").lower())


def opt(q, letter):
    return next((o["text"] for o in q["options"] if o["id"] == letter), None)


def main():
    by_id = {q["id"]: q for q in bank.load_bank(4)}
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    verdict = {}
    for path in sorted(glob.glob(os.path.join(G4, "originals-out-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                verdict[row["id"]] = row
    print("%d verdicts for %d originals" % (len(verdict), sum(1 for q in by_id.values() if q["id"] in verdict)))

    def group(q):
        s = q.get("source") or ""
        return "past paper (EXT)" if s.startswith("g4_mse") else "past paper (PYQ)" if s.startswith("previous") else s

    table = collections.defaultdict(collections.Counter)
    for qid, v in verdict.items():
        q = by_id[qid]
        kind = v["answerOk"]
        if kind == "no" and v.get("rightAnswer") == q.get("correctAnswer"):
            kind = "second option also right"
        elif kind == "no":
            kind = "key wrong"
        table[group(q)][kind] += 1
    print("\n%-22s %6s %10s %12s %8s" % ("", "yes", "key wrong", "2nd right", "unsure"))
    for g, c in sorted(table.items()):
        print("%-22s %6d %10d %12d %8d" % (g, c["yes"], c["key wrong"], c["second option also right"], c["unsure"]))
    years = collections.defaultdict(collections.Counter)
    for qid, v in verdict.items():
        m = re.match(r"EXT_G4_FP_(\d{4})_", qid)
        if m:
            wrong = v["answerOk"] == "no" and v.get("rightAnswer") != by_id[qid].get("correctAnswer")
            years[m.group(1)]["wrong" if wrong else "other"] += 1
    print("\nEXT past papers, wrong keys by year: " + ", ".join("%s %d/%d" % (y, c["wrong"], c["wrong"] + c["other"]) for y, c in sorted(years.items())))

    # Where does the keyed letter sit when wrong? (a constant letter would mean a default was stored)
    letters = collections.Counter()
    for qid, v in verdict.items():
        if qid.startswith("EXT_G4_FP") and v["answerOk"] == "no" and v.get("rightAnswer") != by_id[qid].get("correctAnswer"):
            letters[by_id[qid].get("correctAnswer")] += 1
    print("keyed letter on the wrong EXT keys: %s;  all EXT keys: %s" % (
        dict(letters), dict(collections.Counter(q.get("correctAnswer") for q in by_id.values() if q["id"].startswith("EXT_G4_FP")))))

    # Cross-check the two transcriptions.
    print("\nTwo transcriptions of 2016-2019 (EXT_G4_FP_yyyy_nnn against PYQ_yyyy_Qnn)")
    pairs = same_q = same_key = 0
    agree = collections.Counter()
    samples = []
    for qid, q in by_id.items():
        m = re.match(r"PYQ_(\d{4})_Q(\d+)$", qid)
        if not m:
            continue
        other = by_id.get("EXT_G4_FP_%s_%03d" % (m.group(1), int(m.group(2))))
        if not other:
            continue
        pairs += 1
        if norm(q.get("questionText"))[:40] == norm(other.get("questionText"))[:40]:
            same_q += 1
        pk, ek = norm(opt(q, q["correctAnswer"])), norm(opt(other, other["correctAnswer"]))
        if pk == ek:
            same_key += 1
        vp, ve = verdict.get(qid), verdict.get(other["id"])
        if not vp or not ve:
            continue

        def final(v, qq):
            if v["answerOk"] == "unsure":
                return "?"
            letter = v.get("rightAnswer") if v["answerOk"] == "no" else qq["correctAnswer"]
            return norm(opt(qq, letter)) if letter in ("A", "B", "C", "D") else "none"

        fp, fe = final(vp, q), final(ve, other)
        if "?" in (fp, fe):
            agree["one or both unsure"] += 1
        elif fp == fe:
            agree["reviewers agree on the answer"] += 1
            if ek != fe:
                agree["  ...and the EXT key differs from it"] += 1
            if pk != fp:
                agree["  ...and the PYQ key differs from it"] += 1
        else:
            agree["reviewers disagree"] += 1
            if len(samples) < 12:
                samples.append("%s / %s: PYQ reviewer %r, EXT reviewer %r | %s" % (qid, other["id"], fp, fe, (q.get("questionText") or "")[:70].replace("\n", " ")))
    print("  %d pairs; same question wording in %d; same keyed answer text in %d" % (pairs, same_q, same_key))
    for k, n in agree.items():
        print("  %-42s %d" % (k, n))
    for s in samples:
        print("     " + s)

    print("\nTopic the reviewers gave the originals (current filing in brackets where it differs most)")
    topics = collections.Counter()
    moved = 0
    for qid, v in verdict.items():
        t = v["topic"] if v["topic"] != "other" else "other: " + (v.get("otherTopic") or "?")
        topics[t] += 1
        if by_id[qid].get("node") and by_id[qid].get("node") != v["topic"]:
            moved += 1
    for t, n in topics.most_common():
        print("  %-36s %4d" % (names.get(t, t), n))
    print("  originals that have a chapter today and were given a different topic: %d" % moved)
    diff = collections.Counter(v["difficulty"] for v in verdict.values())
    print("\nDifficulty given: %s" % dict(diff))
    print("Issues flagged: %d of %d" % (sum(1 for v in verdict.values() if v.get("issue")), len(verdict)))


if __name__ == "__main__":
    main()

"""Project the Grade 4 bank by topic if the reviewers' verdicts are applied.

    python -X utf8 scripts/fixes/g4_projection.py

Originals keep their reviewed topic; generated templates and variant forms keep the number
the reviewer set. Reads the bank and data/bank-import/g4/*-out.json; changes nothing.
"""
import collections
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

G4 = g4.OUT


def load(name):
    with io.open(os.path.join(G4, name), encoding="utf-8") as f:
        return json.load(f)


def topic_of(v):
    return v["topic"] if v["topic"] != "other" else "other: " + (v.get("otherTopic") or "?")


def main():
    rows = bank.load_bank(4)
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    verdict = {}
    for path in sorted(glob.glob(os.path.join(G4, "originals-out-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                verdict[row["id"]] = row
    now = collections.Counter(q.get("node") for q in rows)
    real = collections.Counter()
    crafted = collections.Counter()
    diff = collections.defaultdict(collections.Counter)
    for q in rows:
        v = verdict.get(q["id"])
        if not v:
            continue
        t = topic_of(v)
        s = q.get("source") or ""
        (real if s.startswith(("g4_mse", "previous")) else crafted)[t] += 1
        diff[t][v["difficulty"]] += 1
    gen = collections.Counter()
    gen_now = collections.Counter()
    for name in ("templates-out.json", "forms-out.json"):
        counts = {(e.get("template") or e.get("form")): e["count"] for e in load(name.replace("-out", "-in"))}
        for e in load(name):
            t = topic_of(e)
            gen[t] += e["keep"]
            gen_now[t] += counts.get(e.get("template") or e.get("form"), 0)
            diff[t][e["difficulty"]] += e["keep"]
    topics = [n["id"] for n in bank.tree_nodes(4) if n["id"] != "gr4_ipm"]
    topics += sorted(t for t in set(real) | set(crafted) | set(gen) if t.startswith("other"))
    print("%-30s %6s | %5s %5s %5s %6s | %4s %4s %4s" % ("topic", "now", "real", "hand", "gen", "total", "E", "M", "H"))
    tot = collections.Counter()
    for t in topics:
        total = real[t] + crafted[t] + gen[t]
        print("%-30s %6s | %5d %5d %5d %6d | %4d %4d %4d" % (
            names.get(t, t)[:30], now.get(t, 0) if t in names else "-", real[t], crafted[t], gen[t], total,
            diff[t]["Easy"], diff[t]["Medium"], diff[t]["Hard"]))
        tot.update({"real": real[t], "hand": crafted[t], "gen": gen[t]})
    print("%-30s %6d | %5d %5d %5d %6d" % ("TOTAL", len(rows), tot["real"], tot["hand"], tot["gen"], sum(tot.values())))
    print("generated questions today: %d; kept: %d" % (sum(gen_now.values()), tot["gen"]))


if __name__ == "__main__":
    main()

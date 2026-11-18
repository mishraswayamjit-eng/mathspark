"""Settle Grade 4 difficulty from two independent ratings (and a third where they differ).

    python -X utf8 scripts/fixes/difficulty_settle.py report     # agreement, benchmark, what would change
    python -X utf8 scripts/fixes/difficulty_settle.py tiebreak   # write the questions the raters split on
    python -X utf8 scripts/fixes/difficulty_settle.py apply      # write the settled labels to the bank

Ratings are data/bank-import/difficulty/g4-out-N-{A,B}.json (and g4-tie-out-*.json for the
third rating). A label is settled when two raters agree; where A and B differ, the third
rating decides (it always matches one of them or sits between). Until a third rating
exists, a split is settled as the level between them, or Medium for Easy/Hard... see final().
The Grade 5 sample (g5cal-out-{A,B}.json) is reported as the benchmark; Grade 5 is not changed.
The settled labels are saved in scripts/fixes/g4_difficulty.json.
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

D = os.path.join(ROOT, "data", "bank-import", "difficulty")
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_difficulty.json")
LEVELS = ("Easy", "Medium", "Hard")
RANK = {"Easy": 0, "Medium": 1, "Hard": 2}
REAL = re.compile(r"^(g\d_final_|g\d_mse_final_|previous_year_)\d{4}$")


def load_ratings(pattern):
    out = {}
    for path in sorted(glob.glob(os.path.join(D, pattern))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                out[row["id"]] = row
    return out


def pct(c, n):
    return " ".join("%3d%%" % round(100.0 * c[l] / max(1, n)) for l in LEVELS)


def agreement(a, b):
    ids = [i for i in a if i in b]
    exact = sum(1 for i in ids if a[i]["level"] == b[i]["level"])
    far = sum(1 for i in ids if abs(RANK[a[i]["level"]] - RANK[b[i]["level"]]) == 2)
    table = collections.Counter((a[i]["level"], b[i]["level"]) for i in ids)
    n = float(len(ids))
    pa = collections.Counter(a[i]["level"] for i in ids)
    pb = collections.Counter(b[i]["level"] for i in ids)
    # weighted kappa (linear weights)
    obs = sum(table[(x, y)] * (1 - abs(RANK[x] - RANK[y]) / 2.0) for x in LEVELS for y in LEVELS) / n
    exp = sum(pa[x] * pb[y] * (1 - abs(RANK[x] - RANK[y]) / 2.0) for x in LEVELS for y in LEVELS) / (n * n)
    kappa = (obs - exp) / (1 - exp) if exp < 1 else 1.0
    return ids, exact, far, table, kappa


def final(a, b, t):
    if a["level"] == b["level"]:
        return a["level"]
    if t:
        return t["level"]
    return "Medium" if abs(RANK[a["level"]] - RANK[b["level"]]) == 2 else None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    a, b = load_ratings("g4-out-*-A.json"), load_ratings("g4-out-*-B.json")
    tie = load_ratings("g4-tie-out-*.json")
    rows = bank.load_bank(4)
    by_id = {q["id"]: q for q in rows}
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    ids, exact, far, table, kappa = agreement(a, b)

    if mode == "tiebreak":
        split = sorted(i for i in ids if a[i]["level"] != b[i]["level"])
        src = {}
        for path in sorted(glob.glob(os.path.join(D, "g4-in-*.json"))):
            with io.open(path, encoding="utf-8") as f:
                for row in json.load(f):
                    src[row["id"]] = row
        parts = 2
        size = (len(split) + parts - 1) // parts
        for i in range(parts):
            chunk = split[i * size:(i + 1) * size]
            with io.open(os.path.join(D, "g4-tie-in-%d.json" % (i + 1)), "w", encoding="utf-8", newline="\n") as f:
                json.dump([dict(src[q], between=sorted([a[q]["level"], b[q]["level"]], key=RANK.get)) for q in chunk], f, ensure_ascii=False, indent=1)
            print("g4-tie-in-%d.json  %d questions" % (i + 1, len(chunk)))
        return

    print("GRADE 4: %d questions rated twice" % len(ids))
    print("  same level from both raters: %d (%d%%); one level apart: %d; Easy against Hard: %d; weighted kappa %.2f" % (
        exact, round(100.0 * exact / len(ids)), len(ids) - exact - far, far, kappa))
    print("  rater A across / rater B down:      Easy Medium  Hard")
    for y in LEVELS:
        print("    %-30s %5d %6d %5d" % (y, table[("Easy", y)], table[("Medium", y)], table[("Hard", y)]))

    g5a, g5b = load_ratings("g5cal-out-A.json"), load_ratings("g5cal-out-B.json")
    if g5a and g5b:
        gid, gex, gfar, _, gk = agreement(g5a, g5b)
        g5 = {q["id"]: q for q in bank.load_bank(5)}
        print("\nGRADE 5 benchmark: %d real-paper questions rated twice; same level %d%%, weighted kappa %.2f" % (len(gid), round(100.0 * gex / len(gid)), gk))
        print("  %-34s Easy  Med Hard" % "")
        for label, rs in (("rater A", g5a), ("rater B", g5b)):
            print("  %-34s %s" % (label, pct(collections.Counter(r["level"] for r in rs.values()), len(rs))))
        print("  %-34s %s" % ("stored label (by position)", pct(collections.Counter(g5[i]["difficulty"] for i in gid), len(gid))))
        for stored in LEVELS:
            sub = [i for i in gid if g5[i]["difficulty"] == stored]
            c = collections.Counter()
            for i in sub:
                c[g5a[i]["level"]] += 0.5
                c[g5b[i]["level"]] += 0.5
            print("    stored %-6s (n=%3d) judged as:  %s" % (stored, len(sub), pct(c, len(sub))))

    settled = {}
    unsettled = 0
    for i in ids:
        f = final(a[i], b[i], tie.get(i))
        if f is None:
            unsettled += 1
            f = sorted([a[i]["level"], b[i]["level"]], key=RANK.get)[0] if False else None
        settled[i] = f
    done = {i: f for i, f in settled.items() if f}
    print("\nSettled: %d; still split and waiting for a third rating: %d" % (len(done), unsettled))
    if unsettled:
        print("  (run 'tiebreak' and have the split questions rated a third time)")

    def kind(q):
        s = q.get("source") or ""
        return "real past papers" if REAL.match(s) else {"hand_crafted": "hand-written", "g4_authored": "newly written"}.get(s, "worksheets" if "worksheet" in s else "generated")

    print("\nGrade 4, stored label against settled label (settled questions only)")
    print("  %-22s %-16s %-16s %s" % ("", "stored E/M/H", "settled E/M/H", "labels that change"))
    groups = collections.defaultdict(list)
    for i in done:
        groups[kind(by_id[i])].append(i)
    groups["ALL"] = list(done)
    for k, g in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        st = collections.Counter(by_id[i]["difficulty"] for i in g)
        se = collections.Counter(done[i] for i in g)
        ch = sum(1 for i in g if by_id[i]["difficulty"] != done[i])
        print("  %-22s %-16s %-16s %d of %d" % (k, pct(st, len(g)), pct(se, len(g)), ch, len(g)))
    print("\n  by topic (settled E/M/H, count; then real-paper questions)")
    for node, name in names.items():
        g = [i for i in done if by_id[i].get("node") == node]
        r = [i for i in g if kind(by_id[i]) == "real past papers"]
        nr = [i for i in g if kind(by_id[i]) != "real past papers"]
        c = collections.Counter(done[i] for i in nr)
        print("    %-30s %s %4d   real %s %3d   not-real counts E/M/H %d/%d/%d" % (
            name[:30], pct(collections.Counter(done[i] for i in g), len(g)), len(g),
            pct(collections.Counter(done[i] for i in r), len(r)) if r else "   -    -    -", len(r), c["Easy"], c["Medium"], c["Hard"]))

    if mode != "apply":
        return
    if unsettled:
        raise SystemExit("not applied: %d questions are still split" % unsettled)
    questions = bank.load_bank()
    changed = 0
    for q in questions:
        if q["id"] in done and q.get("difficulty") != done[q["id"]]:
            q["difficulty"] = done[q["id"]]
            changed += 1
    bank.save_bank(questions)
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(done.items())), f, ensure_ascii=False, indent=0)
        f.write("\n")
    print("\n%d difficulty labels changed; record in %s" % (changed, os.path.relpath(RECORD, ROOT)))


if __name__ == "__main__":
    main()

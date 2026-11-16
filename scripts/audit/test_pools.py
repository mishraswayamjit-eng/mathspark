"""Do the tests draw the questions their labels promise? Reads data files only; changes nothing.

    python -X utf8 scripts/audit/test_pools.py [grade]

For one grade (default 5) it reports:
  1. the real past papers held for that grade, year by year;
  2. the share of each topic in those real papers, beside the share the mock-test
     blueprint gives it (examWeight in src/data/topicTree.ts);
  3. for the 15-question quick test and the 40-question mock, how many questions each
     topic gets and whether the bank can fill each one at the difficulty asked for
     (a short pool makes the generator fall back to any question of the grade).
The blueprint arithmetic mirrors buildGradeBlueprint in src/lib/mockTest.ts.
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GRADE = int(sys.argv[1]) if len(sys.argv) > 1 else 5
CONFIG = {"quick": (15, 4, 6, 5), "ipm": (40, 9, 19, 12)}
PAST = re.compile(r"^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)(\d{4})$")


def load_seed():
    with io.open(os.path.join(ROOT, "data", "mathspark_complete_seed.json"), encoding="utf-8") as f:
        return json.load(f)["questions"]


def tree_nodes(grade):
    with io.open(os.path.join(ROOT, "src", "data", "topicTree.ts"), encoding="utf-8") as f:
        text = f.read()
    nodes = []
    for m in re.finditer(r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)'.*?grade:\s*(\d+),\s*examWeight:\s*([\d.]+),\s*dbTopicId:\s*'([^']+)'(?:,\s*subTopicKey:\s*'([^']+)')?", text):
        if int(m.group(3)) == grade and not m.group(1).endswith("_ipm"):
            nodes.append({"id": m.group(1), "name": m.group(2), "w": float(m.group(4)), "db": m.group(5), "key": m.group(6)})
    return nodes


def matches(sub, key):
    """Same rule as matchesSubTopicKey: the key must start a word."""
    if not key:
        return True
    hay, needle = (sub or "").lower(), key.lower()
    start = 0
    while True:
        i = hay.find(needle, start)
        if i == -1:
            return False
        if i == 0 or not re.match(r"[a-z0-9]", hay[i - 1]):
            return True
        start = i + 1


def js_round(x):
    return int(x + 0.5)


def blueprint(nodes, total, easy, medium, hard):
    floor = 1 if total >= len(nodes) else 0
    raw = [{"n": n, "c": max(floor, js_round(n["w"] * total))} for n in nodes]
    s = sum(r["c"] for r in raw)
    while s > total:
        big = sorted([r for r in raw if r["c"] > floor], key=lambda r: -r["c"])
        if not big:
            break
        big[0]["c"] -= 1
        s -= 1
    while s < total:
        raw.sort(key=lambda r: -r["n"]["w"])
        raw[0]["c"] += 1
        s += 1
    left = {"Easy": easy, "Medium": medium, "Hard": hard}
    slots = []
    for r in raw:
        if r["c"] <= 0:
            continue
        want = collections.Counter()
        for _ in range(r["c"]):
            pick = "Medium"
            for d in ("Easy", "Medium", "Hard"):
                if left[d] > left[pick]:
                    pick = d
            if left[pick] > 0:
                left[pick] -= 1
                want[pick] += 1
            else:
                want["Medium"] += 1
        slots.append((r["n"], r["c"], want))
    return slots


def main():
    seed = load_seed()
    nodes = tree_nodes(GRADE)
    db_ids = sorted(set(n["db"] for n in nodes))
    pool = [q for q in seed if q.get("topicId") in db_ids]
    print("GRADE %d: %d topics in the tree, %d questions in the bank (%s)" % (GRADE, len(nodes), len(pool), ", ".join(db_ids)))

    papers = collections.defaultdict(list)
    for q in seed:
        m = PAST.match(str(q.get("source")))
        if m and q.get("topicId") in db_ids + ["grade%d" % GRADE]:
            papers[q["source"]].append(q)
    print("\n1. REAL PAST PAPERS HELD")
    real = []
    for src in sorted(papers, key=lambda s: s[-4:]):
        rows = papers[src]
        d = collections.Counter(r["difficulty"] for r in rows)
        print("   %-22s %2d questions   easy/medium/hard %d/%d/%d" % (src, len(rows), d["Easy"], d["Medium"], d["Hard"]))
        real.extend(rows)
    if not papers:
        print("   none")

    print("\n2. TOPIC SHARE: REAL PAPERS vs MOCK BLUEPRINT (a real question may match no topic or several)")
    unmatched = 0
    share = collections.Counter()
    for q in real:
        hit = [n for n in nodes if n["db"] == q.get("topicId") and matches(q.get("subTopic"), n["key"])]
        if not hit:
            unmatched += 1
        for n in hit:
            share[n["id"]] += 1.0 / len(hit)
    total_real = max(1.0, sum(share.values()))
    print("   %-34s %-16s %8s %10s %8s" % ("topic", "key", "real %", "blueprint %", "gap"))
    for n in sorted(nodes, key=lambda n: -share[n["id"]]):
        r = 100.0 * share[n["id"]] / total_real
        b = 100.0 * n["w"]
        flag = "  <-- off by %.0f points" % abs(r - b) if abs(r - b) >= 3 and real else ""
        print("   %-34s %-16s %7.1f %10.1f %+8.1f%s" % (n["name"][:34], n["key"] or "-", r, b, r - b, flag))
    print("   real questions matching no topic: %d of %d; blueprint weights sum to %.2f" % (unmatched, len(real), sum(n["w"] for n in nodes)))

    for kind, (total, e, m_, h) in CONFIG.items():
        print("\n3. %s: %d questions, easy/medium/hard %d/%d/%d" % (kind.upper(), total, e, m_, h))
        slots = blueprint(nodes, total, e, m_, h)
        short = 0
        left_out = [n["name"] for n in nodes if n["id"] not in [s[0]["id"] for s in slots]]
        for n, count, want in sorted(slots, key=lambda s: -s[1]):
            have = collections.Counter(q["difficulty"] for q in pool if q.get("topicId") == n["db"] and matches(q.get("subTopic"), n["key"]))
            notes = []
            for d in ("Easy", "Medium", "Hard"):
                if want[d] > have[d]:
                    short += want[d] - have[d]
                    notes.append("SHORT %s: wants %d, bank has %d" % (d.lower(), want[d], have[d]))
                elif want[d] and have[d] < 3 * want[d]:
                    notes.append("thin %s: wants %d, bank has %d" % (d.lower(), want[d], have[d]))
            print("   %-34s %2d  (E%d M%d H%d)   bank E%-3d M%-3d H%-3d %s" % (
                n["name"][:34], count, want["Easy"], want["Medium"], want["Hard"], have["Easy"], have["Medium"], have["Hard"], "; ".join(notes)))
        print("   topics left out of this paper: %s" % (", ".join(left_out) or "none"))
        print("   questions that would fall back to a random topic: %d" % short)


if __name__ == "__main__":
    main()

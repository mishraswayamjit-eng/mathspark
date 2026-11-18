"""File every Grade 4 question under the topic it tests, and thin the generated sets.

    python -X utf8 scripts/fixes/g4_refile.py            # report only
    python -X utf8 scripts/fixes/g4_refile.py --write

Applies the reviewers' verdicts (data/bank-import/g4/*-out.json):
  originals   past-paper, worksheet and hand-written questions take the topic and difficulty
              a reviewer gave them by reading and working each one;
  generated   template questions and "variants" take the verdict of their template or form,
              and only the number the reviewer set is kept (spread across number sizes,
              no exact repeats, no negative answers); terse templates are reworded into a
              full sentence where the reviewer gave one;
  papers      the first transcription of the 2016-2019 papers (EXT_G4_FP_2016..2019) is
              removed: the second (PYQ_*) is the one the past-paper tests use and its keys
              are far more reliable.
A question filed under a chapter moves into that chapter's pool; one filed under an added
topic (squares, ratio, ages, counting) stays in the 'grade4' pool with that topic's label.
Only Grade 4 is touched. The decisions are saved in scripts/fixes/g4_filing.json.
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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

G4 = g4.OUT
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_filing.json")

# Reviewers' names for topics outside the chapters -> the node they are filed under.
OTHER = {
    "Squares & Square Roots": "gr4_squares", "Ratio & Proportion": "gr4_ratio",
    "Age Problems": "gr4_ages", "Counting & Arrangements": "gr4_counting",
    "Money": "gr4_decimals", "Average": "gr4_data", "Probability": "gr4_data",
    "Lines & Symmetry": "gr4_angles", "Speed, Distance & Time": "gr4_operations",
    "Profit & Loss": "gr4_operations", "Percentage": "gr4_decimals", "Simple Interest": "gr4_operations",
}
FIRST_TRANSCRIPTION = re.compile(r"^EXT_G4_FP_(2016|2017|2018|2019)_\d+$")
NUM = re.compile(r"\d+(?:\.\d+)?")


def load(name):
    with io.open(os.path.join(G4, name), encoding="utf-8") as f:
        return json.load(f)


def node_of(v):
    if v["topic"] != "other":
        return v["topic"]
    return OTHER.get(v.get("otherTopic") or "", "gr4_operations")


def words_in_forms(forms):
    out = set()
    for f in forms:
        out.update(w for w in re.findall(r"[a-z]+", f["form"]))
    return out


def form_of(text, common):
    text = re.sub(r"\d+(?:[.,]\d+)*", "N", text or "")
    return re.sub(r"[A-Za-z]+", lambda m: m.group(0).lower() if m.group(0).lower() in common else "_", text).strip()


def right_text(q):
    return next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), "")


def size(q):
    return sum(float(x) for x in NUM.findall(q.get("questionText") or "")[:6])


def pick(qs, k):
    """k of the questions: no exact repeats, no negative answers, spread across number size."""
    seen = set()
    pool = []
    for q in sorted(qs, key=lambda q: (size(q), q["id"])):
        text = re.sub(r"\s+", " ", (q.get("questionText") or "").strip().lower())
        if text in seen or re.match(r"^\s*[-−]\s*\d", right_text(q)):
            continue
        seen.add(text)
        pool.append(q)
    if k >= len(pool):
        return pool
    if k <= 0:
        return []
    step = (len(pool) - 1) / float(max(1, k - 1)) if k > 1 else 0
    idx = sorted({int(round(i * step)) for i in range(k)}) if k > 1 else [len(pool) // 2]
    return [pool[i] for i in idx]


def reword(q, pattern):
    """The reviewer's full-sentence wording with this question's numbers put in, or None."""
    if not pattern:
        return None
    nums = NUM.findall(q.get("questionText") or "")
    slots = re.findall(r"\bN\b", pattern)
    if not slots or len(slots) != len(nums):
        return None
    it = iter(nums)
    return re.sub(r"\bN\b", lambda m: next(it), pattern)


def main():
    write = "--write" in sys.argv
    nodes = {n["id"]: n for n in bank.tree_nodes(4)}
    questions = bank.load_bank()
    verdict = {}
    for path in sorted(glob.glob(os.path.join(G4, "originals-out-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                verdict[row["id"]] = row
    templates = {t["template"]: t for t in load("templates-out.json")}
    forms = {f["form"]: f for f in load("forms-out.json")}
    common = words_in_forms(load("forms-in.json"))

    ids4 = {q["id"] for q in bank.load_bank(4)}
    grade4 = [q for q in questions if q["id"] in ids4]
    groups = collections.defaultdict(list)
    unknown = collections.Counter()
    decided = {}   # id -> (node, difficulty, rewording or None)
    removed = {}   # id -> why
    for q in grade4:
        kind, key = g4.family(q)
        if kind == "original":
            if FIRST_TRANSCRIPTION.match(q["id"]):
                removed[q["id"]] = "first transcription of a 2016-2019 paper; the PYQ copy is kept"
            else:
                v = verdict[q["id"]]
                decided[q["id"]] = (node_of(v), v["difficulty"], None)
        elif kind == "template":
            if key in templates:
                groups[("t", key)].append(q)
            else:
                unknown["template"] += 1
        else:
            f = form_of(q.get("questionText"), common)
            if f in forms:
                groups[("f", f)].append(q)
            else:
                unknown["form"] += 1

    reworded = 0
    for (kind, key), qs in groups.items():
        v = templates[key] if kind == "t" else forms[key]
        chosen = {q["id"] for q in pick(qs, v["keep"])}
        for q in qs:
            if q["id"] in chosen:
                new_text = reword(q, v.get("rewording")) if kind == "t" else None
                reworded += 1 if new_text else 0
                decided[q["id"]] = (node_of(v), v["difficulty"], new_text)
            else:
                removed[q["id"]] = "generated: more of this form than the bank needs" if v["keep"] else "generated: form not kept (%s)" % (v.get("note") or v.get("quality"))[:120]

    moved = collections.Counter()
    out = []
    for q in questions:
        if q["id"] not in ids4:
            out.append(q)
            continue
        if q["id"] in removed:
            continue
        if q["id"] not in decided:
            out.append(q)
            continue
        node_id, difficulty, new_text = decided[q["id"]]
        node = nodes[node_id]
        if q.get("node") != node_id:
            moved[(q.get("node"), node_id)] += 1
        q["node"] = node_id
        q["topicId"] = node["db"]
        q["subTopic"] = ("Grade 4 — %s" % node["name"]) if node.get("key") else node["name"]
        q["difficulty"] = difficulty
        if new_text:
            q["questionText"] = new_text
        if node.get("key") and bank.assign_node(q, bank.tree_nodes()) != node_id:
            raise SystemExit("label of %s does not reach %s" % (q["id"], node_id))
        out.append(q)

    after = collections.Counter(q.get("node") for q in out if q["id"] in ids4)
    print("Grade 4: %d questions reviewed; %d kept, %d removed; %d not recognised %s" % (
        len(grade4), len(decided), len(removed), sum(unknown.values()), dict(unknown)))
    print("  removed: %s" % dict(collections.Counter(w.split(":")[0].split(";")[0] for w in removed.values())))
    print("  moved to a different topic: %d; terse questions reworded: %d" % (sum(moved.values()), reworded))
    print("\n%-30s %6s   %s" % ("topic", "total", "Easy/Medium/Hard, real"))
    for n in bank.tree_nodes(4):
        qs = [q for q in out if q["id"] in ids4 and q.get("node") == n["id"]]
        d = collections.Counter(q.get("difficulty") for q in qs)
        real = sum(1 for q in qs if (q.get("source") or "").startswith(("g4_mse", "previous")))
        print("%-30s %6d   %d/%d/%d, %d real" % (n["name"][:30], len(qs), d["Easy"], d["Medium"], d["Hard"], real))
    print("%-30s %6d" % ("(no topic)", after.get(None, 0)))
    if not write:
        print("\nnothing written (use --write)")
        return
    record = {"filed": {qid: {"node": d[0], "difficulty": d[1]} for qid, d in sorted(decided.items())},
              "removed": dict(sorted(removed.items()))}
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, ensure_ascii=False, indent=0)
        f.write("\n")
    bank.save_bank(out)
    print("\nbank and %s written" % os.path.relpath(RECORD, ROOT))


if __name__ == "__main__":
    main()

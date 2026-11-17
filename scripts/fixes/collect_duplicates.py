"""Check the reviewers' lists of repeated question templates and write the removal list.

    python -X utf8 scripts/fixes/collect_duplicates.py            # report only
    python -X utf8 scripts/fixes/collect_duplicates.py --write

Reads data/bank-import/repairs/dedupe-out-N.json (templates with `keep` and `remove` ids)
against dedupe-in-N.json. Refuses an id that is not in the reviewer's input, is listed
twice, or is not an AI-written Grade 5 question. With --write, saves
scripts/fixes/removed_duplicates.json ({ id: "topic: template" }), which
remove_flawed.py reads. Changes nothing in the bank.
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

REPAIRS = os.path.join(ROOT, "data", "bank-import", "repairs")
OUT = os.path.join(ROOT, "scripts", "fixes", "removed_duplicates.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    by_id = {q["id"]: q for q in bank.load_bank(5)}
    names = {n["id"]: n["name"] for n in bank.tree_nodes(5)}
    problems = []
    remove = {}
    kept = set()
    for path in sorted(glob.glob(os.path.join(REPAIRS, "dedupe-out-*.json"))):
        name = os.path.basename(path)
        given = {q["id"] for q in load(path.replace("dedupe-out-", "dedupe-in-"))}
        seen = set()
        for t in load(path)["templates"]:
            for qid in t.get("keep", []) + t.get("remove", []):
                if qid not in given:
                    problems.append("%s: %s is not in the input" % (name, qid))
                elif qid in seen:
                    problems.append("%s: %s is listed twice" % (name, qid))
                elif by_id.get(qid, {}).get("source") != "ai_generated":
                    problems.append("%s: %s is not an AI-written bank question" % (name, qid))
                seen.add(qid)
            kept.update(t.get("keep", []))
            for qid in t.get("remove", []):
                remove[qid] = "%s: %s" % (t.get("topic"), t.get("template"))
            if not t.get("keep"):
                problems.append("%s: template %r keeps nothing" % (name, t.get("template")))

    before = collections.Counter(q.get("node") for q in by_id.values())
    gone = collections.Counter(by_id[i].get("node") for i in remove if i in by_id)
    print("%d questions to remove, %d problems" % (len(remove), len(problems)))
    for p in problems[:40]:
        print("  " + p)
    print("\nGrade 5 questions per topic (all sources): before -> after")
    for node, n in sorted(before.items(), key=lambda kv: names.get(kv[0], "")):
        if gone.get(node):
            print("  %-34s %4d -> %4d" % (names.get(node, node), n, n - gone[node]))
    if problems:
        sys.exit(1)
    if "--write" not in sys.argv:
        print("\nnothing written (use --write)")
        return
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(remove.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("\nwrote %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()

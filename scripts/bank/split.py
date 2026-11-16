"""One-time migration: split the old single seed file into the bank.

    python -X utf8 scripts/bank/split.py            # refuses if the bank already exists
    python -X utf8 scripts/bank/split.py --force    # rebuild the bank from the old file

Reads data/mathspark_complete_seed.json ({ metadata, questions }), gives every question
its `node` (bank.assign_node) and writes data/bank/** through bank.save_bank. Then it
reads the bank back and proves nothing was lost: same count, same ids, and every old
question identical, key for key and byte for byte, once `node` is set aside.

After the migration the bank is the source of truth: do not run this again, or edits
made in the bank would be overwritten by the old file.
"""
import collections
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402

OLD = os.path.join(bank.ROOT, "data", "mathspark_complete_seed.json")


def canon(row):
    """The exact bytes the old file used for a row (ASCII-only compact JSON, keys in order)."""
    return json.dumps(row, ensure_ascii=True, separators=(",", ":"))


def main():
    force = "--force" in sys.argv[1:]
    if bank.bank_files() and not force:
        raise SystemExit("The bank already exists (%s). It is the source of truth now; use --force to rebuild it from the old file."
                         % os.path.relpath(bank.BANK, bank.ROOT))
    with io.open(OLD, encoding="utf-8") as f:
        data = json.load(f)
    old = data["questions"]
    nodes = bank.tree_nodes()

    questions = []
    for q in old:
        row = dict(q)
        row["node"] = bank.assign_node(q, nodes)
        questions.append(row)
    changed = bank.save_bank(questions, meta=data["metadata"])
    print("%d questions read from %s; %d files written or removed" % (len(old), os.path.relpath(OLD, bank.ROOT), len(changed)))

    # ── Read it back and compare ─────────────────────────────────────────────
    back = bank.load_bank()
    back_by_id = bank.by_id(back)
    problems = []
    if len(back) != len(old):
        problems.append("count: old %d, bank %d" % (len(old), len(back)))
    if len(back_by_id) != len(back):
        problems.append("the bank holds %d rows but %d distinct ids" % (len(back), len(back_by_id)))
    old_ids = set(q["id"] for q in old)
    if old_ids != set(back_by_id):
        problems.append("ids differ: %d only in the old file, %d only in the bank" % (
            len(old_ids - set(back_by_id)), len(set(back_by_id) - old_ids)))
    differ = 0
    for q in old:
        new = back_by_id.get(q["id"])
        if new is None:
            continue
        if list(new.keys())[:2] != ["id", "node"]:
            problems.append("%s: bank row does not start with id, node" % q["id"])
        stripped = dict((k, v) for k, v in new.items() if k != "node")
        if stripped != q or canon(stripped) != canon(q):
            differ += 1
            if differ <= 10:
                problems.append("%s: differs from the old row" % q["id"])
        if new["node"] != bank.assign_node(q, nodes):
            problems.append("%s: node changed on the way back" % q["id"])
    if differ > 10:
        problems.append("... %d rows differ in all" % differ)
    if bank.load_meta().get("totalQuestions") != len(back):
        problems.append("_meta.json totalQuestions is not %d" % len(back))
    stale = dict((k, v) for k, v in bank.load_meta().items() if k != "totalQuestions") != dict(
        (k, v) for k, v in data["metadata"].items() if k != "totalQuestions")
    if stale:
        problems.append("_meta.json does not carry the old metadata")
    if bank.load_seed_ids() != sorted(old_ids):
        problems.append("src/data/bank/seedIds.json is not the bank's ids")

    # ── What was built ───────────────────────────────────────────────────────
    per_grade = collections.Counter(bank.grade_of(q["topicId"]) for q in back)
    unsorted = collections.Counter(bank.grade_of(q["topicId"]) for q in back if q["node"] is None)
    print("%-8s %6s %10s %9s %6s" % ("grade", "files", "questions", "unsorted", "empty"))
    for g in bank.GRADES:
        files = bank.bank_files(g)
        empty = sum(1 for p in files if bank.read_file(p) == "[\n]\n")
        print("%-8s %6d %10d %9d %6d" % ("grade%d" % g, len(files), per_grade[g], unsorted[g], empty))
    print("%-8s %6d %10d %9d" % ("all", len(bank.bank_files()), len(back), sum(unsorted.values())))

    if problems:
        print("%d PROBLEMS: the migration is NOT loss-free" % len(problems))
        for p in problems[:40]:
            print("  " + p)
        sys.exit(1)
    print("LOSS-FREE: %d of %d old questions read back from the bank identical (same ids, every field byte-identical), plus node"
          % (len(old) - differ, len(old)))


if __name__ == "__main__":
    main()

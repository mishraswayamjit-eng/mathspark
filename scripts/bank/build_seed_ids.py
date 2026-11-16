"""Write the list of question ids held in the seed file, for the bank audit.

    python -X utf8 scripts/bank/build_seed_ids.py

The audit on the seed screen (/api/admin/topic-audit) compares the database with this
list to say which questions exist only in the database. Run it after any change that
adds or removes questions in data/mathspark_complete_seed.json.
"""
import io
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
OUT = os.path.join(ROOT, "src", "data", "bank", "seedIds.json")


def main():
    with io.open(SEED, encoding="utf-8") as f:
        ids = sorted(q["id"] for q in json.load(f)["questions"])
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ids, f, ensure_ascii=True, separators=(",", ":"))
        f.write("\n")
    print("%d ids written to %s" % (len(ids), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()

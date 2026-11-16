"""Write the list of question ids held in the bank (data/bank/), for the bank audit.

    python -X utf8 scripts/bank/build_seed_ids.py

The audit on the seed screen (/api/admin/topic-audit) compares the database with this
list to say which questions exist only in the database. bank.save_bank keeps the list
in step by itself; run this after adding or removing questions in the bank by hand.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402

OUT = bank.SEED_IDS


def main():
    questions = bank.load_bank()
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(bank.seed_ids_text(questions))
    print("%d ids written to %s" % (len(questions), os.path.relpath(OUT, bank.ROOT)))


if __name__ == "__main__":
    main()

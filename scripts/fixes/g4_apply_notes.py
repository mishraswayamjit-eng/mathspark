"""Apply rewritten option notes to the Grade 4 bank. Only the notes change.

    python -X utf8 scripts/fixes/g4_apply_notes.py            # report only
    python -X utf8 scripts/fixes/g4_apply_notes.py --write

Reads data/bank-import/g4/notes-out-*.json (checked by g4_check_patch.py):
    { "<id>": { "notes": {A, B, C, D}, "claims": {...} } }
and sets each question's option notes. Each note is recorded with the option text it was
written for; if an option has changed since, the question is refused, because the note may
no longer fit. Everything applied is saved in scripts/fixes/g4_notes.json, from which this
script can re-apply it when the notes-out files are gone.

ORDER when rebuilding from the records: g4_apply_teaching.py first, then this script
(g4_apply_teaching.py resets the notes of the questions it rewrites).
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

G4 = os.path.join(ROOT, "data", "bank-import", "g4")
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_notes.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def build_record(by_id):
    record = load(RECORD) if os.path.exists(RECORD) else {}
    for path in sorted(glob.glob(os.path.join(G4, "notes-out-*.json"))):
        for qid, p in load(path).items():
            q = by_id.get(qid)
            if q is None:
                sys.exit("%s: %s is not a Grade 4 question" % (os.path.basename(path), qid))
            record[qid] = {"notes": {k: p["notes"][k] for k in "ABCD"},
                           "options": {o["id"]: o["text"] for o in q["options"]}}
    return record


def main():
    write = "--write" in sys.argv
    questions = bank.load_bank()
    ids4 = {q["id"] for q in bank.load_bank(4)}
    record = build_record({q["id"]: q for q in questions if q["id"] in ids4})
    changed = same = 0
    problems = []
    for q in questions:
        r = record.get(q["id"])
        if not r or q["id"] not in ids4:
            continue
        if {o["id"]: o["text"] for o in q["options"]} != r["options"]:
            problems.append("%s: an option has changed since its notes were written" % q["id"])
            continue
        if q.get("misconceptions") == r["notes"]:
            same += 1
        else:
            q["misconceptions"] = dict(r["notes"])
            changed += 1
    gone = sorted(set(record) - ids4)
    print("Grade 4: option notes set on %d questions (%d already as recorded); %d recorded ids no longer in the bank" % (changed, same, len(gone)))
    for p in problems:
        print("  PROBLEM " + p)
    if problems:
        sys.exit(1)
    if not write:
        print("nothing written (use --write)")
        return
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: record[k] for k in sorted(record)}, f, ensure_ascii=False, indent=0)
        f.write("\n")
    bank.save_bank(questions)
    print("bank and %s written" % os.path.relpath(RECORD, ROOT))


if __name__ == "__main__":
    main()

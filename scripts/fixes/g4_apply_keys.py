"""Apply the agreed answer-key corrections and removals to the Grade 4 bank.

    python -X utf8 scripts/fixes/g4_apply_keys.py            # report only
    python -X utf8 scripts/fixes/g4_apply_keys.py --write

From data/bank-import/g4/key-decisions.json (two independent reviewers compared) and the
variant checkers' variants-out-*.json:
  correct  the key becomes the option both reviewers reached. The old worked steps and
           per-option notes were written for the old answer, so the steps are cleared and
           the notes reset; real steps are written with the teaching layer later.
  remove   originals that cannot be answered as written or on which the reviewers differ
           (all of those are damaged), and variants with no right option or that are not
           sound questions.
The decisions are saved, with reasons, in scripts/fixes/g4_key_corrections.json so the
change can be audited and re-applied. Only Grade 4 is touched.
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
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_key_corrections.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def build_record():
    """{ id: {action, to?, why} } from the review files, or the saved record if they are gone."""
    decisions_path = os.path.join(G4, "key-decisions.json")
    if not os.path.exists(decisions_path):
        return load(RECORD)
    record = {}
    for qid, d in load(decisions_path).items():
        if d["action"] == "correct":
            record[qid] = {"action": "correct", "to": d["to"], "why": d["why"][:300]}
        elif d["action"] in ("remove", "dispute"):
            record[qid] = {"action": "remove", "why": ("reviewers differ; " if d["action"] == "dispute" else "") + d["why"][:300]}
    for path in sorted(glob.glob(os.path.join(G4, "variants-out-*.json"))):
        for v in load(path):
            if v.get("sound") == "no" or (v.get("answerOk") == "no" and v.get("rightAnswer") == "none") or v.get("answerOk") == "unsure":
                record[v["id"]] = {"action": "remove", "why": "variant: " + (v.get("issue") or "not a sound question")[:300]}
    return dict(sorted(record.items()))


def main():
    write = "--write" in sys.argv
    record = build_record()
    questions = bank.load_bank()
    corrected = removed = 0
    keep = []
    for q in questions:
        d = record.get(q["id"])
        if not d or q.get("topicId") not in ("grade4",) and not q["id"].startswith(("Q_", "EXT_G4", "PYQ_")):
            keep.append(q)
            continue
        if d["action"] == "remove":
            removed += 1
            continue
        if d["action"] == "correct":
            if q["correctAnswer"] != d["to"]:
                corrected += 1
                q["correctAnswer"] = d["to"]
                q["stepByStep"] = []
                q["misconceptions"] = {o["id"]: ("Correct!" if o["id"] == d["to"] else "Not quite!") for o in q["options"]}
        keep.append(q)
    wanted = {"correct": sum(1 for d in record.values() if d["action"] == "correct"),
              "remove": sum(1 for d in record.values() if d["action"] == "remove")}
    print("record: %d corrections, %d removals" % (wanted["correct"], wanted["remove"]))
    print("bank:   %d keys to change now, %d questions to remove now, %d questions stay" % (corrected, removed, len(keep)))
    if not write:
        print("nothing written (use --write)")
        return
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, ensure_ascii=False, indent=1)
        f.write("\n")
    bank.save_bank(keep)
    print("bank and %s written" % os.path.relpath(RECORD, ROOT))


if __name__ == "__main__":
    main()

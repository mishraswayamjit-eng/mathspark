"""Apply the reviewers' teaching help and option repairs to the Grade 4 bank.

    python -X utf8 scripts/fixes/g4_apply_teaching.py            # report only
    python -X utf8 scripts/fixes/g4_apply_teaching.py --write

From data/bank-import/g4/:
  teach-out-*.json   three hints, worked steps and a note per option, for questions that had
                     filler ("Read the question carefully.", "Answer: B") or nothing;
  dupopts-out.json   a new wrong option where two options had the same value.
Plus the decisions below: questions the writers found cannot be answered as written are
removed, and one garbled past-paper question is reworded. Everything applied is saved in
scripts/fixes/g4_teaching.json, from which this script can re-apply it. Only Grade 4 changes.
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
from g4_cleanup import value  # noqa: E402

G4 = os.path.join(ROOT, "data", "bank-import", "g4")
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_teaching.json")

REMOVE = {
    "EXT_G4_FP_2020_022": "as typed, two 3-digit numbers whose product is larger than every option",
    "EXT_G4_FP_2025_005": "magic-square layout garbled",
    "Q_CH15_016": "three other options are also valid corners of the magic square",
    "EXT_G4_WS2_CH11_008": "0.545 has two 5s and both matching options are offered",
    "EXT_G4_FP_2020_038": "text garbled; states the answer inside the question",
    "Q_CH09_020_V03": "working goes below zero part-way (16 - 3 x 8 + 11)",
}
# Repairs that need more than one option changed, or that the checker's first version refused.
EXTRA_OPTIONS = {
    "Q_CH13_017": {"C": "8 + x"},
    "EXT_G4_WS2_CH11_001": {"B": "2/8", "C": "7/50"},
    "Q_CH07_012": {"B": "9/8", "C": "6/12"},
}
REWORD = {
    "EXT_G4_FP_2025_027": "15th August 2024 was a Thursday. Which of these days came 5 times in that month?",
}
STALE_NOTE = "Not quite. Work through the steps once more and compare your answer with this one."


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def build_record():
    if not glob.glob(os.path.join(G4, "teach-out-*.json")):
        return load(RECORD)
    record = {"remove": dict(REMOVE), "options": {k: dict(v) for k, v in EXTRA_OPTIONS.items()}, "reword": dict(REWORD), "teach": {}}
    for qid, p in load(os.path.join(G4, "dupopts-out.json")).items():
        if p.get("remove"):
            record["remove"][qid] = "options cannot be repaired: " + (p.get("why") or "")[:160]
        else:
            record["options"].setdefault(qid, {})[p["replace"]] = p["with"]
    for path in sorted(glob.glob(os.path.join(G4, "teach-out-*.json"))):
        record["teach"].update(load(path))
    # Help written AFTER the options were repaired already describes the new options.
    fresh = os.path.join(G4, "teach-out-07.json")
    record["freshNotes"] = sorted(load(fresh)) if os.path.exists(fresh) else []
    # Later repairs of questions raters flagged: rewordings, option replacements, removals.
    repairs = os.path.join(G4, "repairs-out.json")
    if os.path.exists(repairs):
        for qid, p in load(repairs).items():
            if p.get("remove"):
                record["remove"][qid] = "repair: " + (p.get("why") or "")[:160]
                continue
            if p.get("question"):
                record["reword"][qid] = p["question"]
            for letter, text in (p.get("options") or {}).items():
                record["options"].setdefault(qid, {})[letter] = text
    return record


def main():
    write = "--write" in sys.argv
    record = build_record()
    questions = bank.load_bank()
    ids4 = {q["id"] for q in bank.load_bank(4)}
    out = []
    done = {"removed": 0, "options": 0, "reworded": 0, "taught": 0}
    problems = []
    for q in questions:
        qid = q["id"]
        if qid not in ids4:
            out.append(q)
            continue
        if qid in record["remove"]:
            done["removed"] += 1
            continue
        changed_letters = set()
        replaced_letters = set(record["options"].get(qid, {}))
        if qid in record["options"]:
            for letter, text in record["options"][qid].items():
                if letter == q["correctAnswer"]:
                    problems.append("%s: would replace the keyed option" % qid)
                    continue
                for o in q["options"]:
                    if o["id"] == letter and o["text"] != text:
                        o["text"] = text
                        changed_letters.add(letter)
            if len({value(o["text"]) for o in q["options"]}) < 4:
                problems.append("%s: two options are still the same value" % qid)
            done["options"] += 1 if changed_letters else 0
        if qid in record["reword"] and q["questionText"] != record["reword"][qid]:
            q["questionText"] = record["reword"][qid]
            done["reworded"] += 1
        t = record["teach"].get(qid)
        if t:
            q["hints"] = list(t["hints"])
            q["stepByStep"] = [dict([("step", i + 1), ("text", s["text"])] + ([("latex", s["latex"])] if s.get("latex") else []))
                               for i, s in enumerate(t["steps"])]
            q["misconceptions"] = {k: t["notes"][k] for k in "ABCD"}
            done["taught"] += 1
        # A note written for an option whose text has since been replaced no longer fits it.
        stale = set() if qid in record.get("freshNotes", []) else (replaced_letters if t else changed_letters)
        for letter in stale:
            if isinstance(q.get("misconceptions"), dict) and letter in q["misconceptions"]:
                q["misconceptions"][letter] = STALE_NOTE
        out.append(q)
    print("Grade 4: %(removed)d removed, %(options)d with an option replaced, %(reworded)d reworded, %(taught)d given hints, steps and notes" % done)
    for p in problems:
        print("  PROBLEM " + p)
    if problems:
        sys.exit(1)
    if not write:
        print("nothing written (use --write)")
        return
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, ensure_ascii=False, indent=0)
        f.write("\n")
    bank.save_bank(out)
    print("bank and %s written" % os.path.relpath(RECORD, ROOT))


if __name__ == "__main__":
    main()

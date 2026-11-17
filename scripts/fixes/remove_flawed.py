"""Take flawed imported questions out of the bank, with their narration, lesson and figure.

    python -X utf8 scripts/fixes/remove_flawed.py            # report only
    python -X utf8 scripts/fixes/remove_flawed.py --write

These Grade 5 questions passed the answer check (the asked-for sum is right) but were
found, while their figures and lessons were being made, to be unfit for a child:
  - geometry stories whose measurements cannot all be true (a triangle with sides 5, 5, 7
    said to have 55 degree base angles, and so on);
  - two BODMAS stories where the story and the expression it asks about disagree, so a
    child who follows the story lands on one of the other options.
The question is removed from data/bank/, and its entry from the narration, lesson and
figure part files. Run this again after re-running any generator that might put one back.
The database keeps the row; it is hidden once BANK_RETIRE_MISSING is on.
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

# id prefix -> why
FLAWED = {
    "AIGEN_grade5_352cbeaf": "angles and sides of the triangle cannot both be true",
    "AIGEN_grade5_28e0cae9": "sides 5, 5, 7 do not give the stated 84 degrees",
    "AIGEN_grade5_5293d35a": "sides 8, 10, 15 do not give the stated 108 and 27 degrees",
    "AIGEN_grade5_73792540": "says all sides differ, then gives 5, 7, 5; angles do not fit",
    "AIGEN_grade5_7f275cb5": "sides 5, 5, 8 do not give the stated 110 degrees",
    "AIGEN_grade5_c29423a2": "sides 32, 32, 20 do not give the stated 40 degrees",
    "AIGEN_grade5_d316dfa5": "sides 8, 8, 15 do not give the stated 28 degree base angles",
    "AIGEN_grade5_d38bd58a": "angles make a right angle but sides 7, 9, 13 do not",
    "AIGEN_grade5_e9d46e9a": "the base is given shorter than the equal sides, against the angles",
    "AIGEN_grade5_6603373f": "story gives 40 (an option), the expression gives the keyed 58",
    "AIGEN_grade5_e9fcd7d2": "story gives 16 (an option), the expression gives the keyed 91",
    # found while the hints were being reviewed
    "AIGEN_grade5_c5ecf669": "the question itself says its expression does not fit the story",
    "AIGEN_grade5_d69fa5f3": "asks for diyas per rangoli, keys diyas per rangoli plus sparklers",
    "AIGEN_grade5_4db3b22f": "the story contradicts itself about the mother's 47 coins",
    "AIGEN_grade5_920aaa2e": "answer is a never-ending decimal of rupees (4,615.38...)",
    "AIGEN_grade5_3a906d76": "answer is 40/7 percent, found only with algebra beyond Grade 5",
    "AIGEN_grade5_b22920c0": "two rectangular tiles cannot meet at 65 degrees",
    "AIGEN_grade5_54aca949": "two of the options are the same value, one with its working shown",
    "AIGEN_grade5_e4f3ec79": "fourth copy of 'place value of 7 against face value of 8' (8,750)",
}

# Repeated templates thinned by reviewers: { id: "topic: template" }, written by
# collect_duplicates.py.
DUPLICATES = os.path.join(ROOT, "scripts", "fixes", "removed_duplicates.json")
if os.path.exists(DUPLICATES):
    with io.open(DUPLICATES, encoding="utf-8") as _f:
        for _qid, _template in json.load(_f).items():
            FLAWED.setdefault(_qid, "repeats a template: " + _template)

PART_DIRS = [
    os.path.join(ROOT, "data", "question-speech", "parts"),
    os.path.join(ROOT, "data", "teach", "parts"),
    os.path.join(ROOT, "data", "question-figures", "parts"),
]


def dump_like(path, data):
    """Write a part file back in the form it was in (indented or compact)."""
    with io.open(path, encoding="utf-8") as f:
        raw = f.read()
    indented = "\n " in raw[:2000]
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        if indented:
            json.dump(data, f, ensure_ascii=False, indent=1)
        else:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        if raw.endswith("\n"):
            f.write("\n")


def main():
    write = "--write" in sys.argv
    questions = bank.load_bank()
    ids = {}
    for q in questions:
        for prefix, why in FLAWED.items():
            if q["id"].startswith(prefix):
                ids[q["id"]] = why
    missing = [p for p in FLAWED if not any(i.startswith(p) for i in ids)]
    print("%d questions to remove from the bank (%d prefixes already gone)" % (len(ids), len(missing)))
    for qid, why in sorted(ids.items()):
        print("   %s  %s" % (qid, why))

    gone = set(ids)
    all_prefixes = tuple(FLAWED)
    for folder in PART_DIRS:
        for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
            with io.open(path, encoding="utf-8") as f:
                part = json.load(f)
            hit = [k for k in part if k in gone or k.startswith(all_prefixes)]
            if not hit:
                continue
            print("   %-52s %d entr%s" % (os.path.relpath(path, ROOT), len(hit), "y" if len(hit) == 1 else "ies"))
            if write:
                for k in hit:
                    del part[k]
                dump_like(path, part)

    if not write:
        print("nothing written (use --write)")
        return
    bank.save_bank([q for q in questions if q["id"] not in gone])
    print("bank written")


if __name__ == "__main__":
    main()

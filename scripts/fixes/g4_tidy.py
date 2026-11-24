"""Small tidy-ups to the Grade 4 bank. Safe to run again: it only changes what still needs it.

    python -X utf8 scripts/fixes/g4_tidy.py            # report only
    python -X utf8 scripts/fixes/g4_tidy.py --write

  - Angle and triangle questions that ask in degrees but offer bare numbers: each option
    gets its degree sign ("89" becomes "89°").
  - Profit and loss questions that ask in rupees but offer bare numbers: each option gets
    "Rs." in the question's own style ("66" becomes "Rs.66").
  - "Think of a number 12." becomes "Think of the number 12."
  - Questions listed in UNFIT are removed, each with its reason.
  - Worksheet questions that repeat a hand-written question of the same topic are removed
    (the hand-written one is kept).

Values and keys do not change. The option texts recorded with the notes
(scripts/fixes/g4_notes.json) are brought into line.

ORDER when rebuilding from the records: g4_apply_teaching.py, then g4_apply_notes.py, then
this script last.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

NOTES = os.path.join(ROOT, "scripts", "fixes", "g4_notes.json")

# worksheet copy -> the hand-written question it repeats
REPEATS = {
    "EXT_G4_WS2_CH12_001": "Q_CH12_001", "EXT_G4_WS2_CH14_005": "Q_CH14_009", "EXT_G4_WS2_CH14_001": "Q_CH14_001",
    "EXT_G4_WS2_CH21_003": "Q_CH21_004", "EXT_G4_WS2_CH15_002": "Q_CH15_006", "EXT_G4_WS2_CH16_001": "Q_CH16_001",
    "EXT_G4_WS2_CH16_002": "Q_CH16_002", "EXT_G4_WS2_CH16_004": "Q_CH16_004", "EXT_G4_WS2_CH16_005": "Q_CH16_005",
    "EXT_G4_WS2_CH16_006": "Q_CH16_006", "EXT_G4_WS2_CH16_009": "Q_CH16_009",
}
# removed outright, with the reason
UNFIT = {
    "VAR_EXT_G4_FP_2023_019_04_b2": "asks 'how many times' with the answer 0.1: decimal reasoning beyond Grade 4 place value",
}
RUPEES = ("BOOST_EXT_G4_FP_2017_021_07", "BOOST_EXT_G4_FP_2024_040_07", "VAR2_EXT_G4_FP_2018_001_02")
BARE = re.compile(r"^\d+$")
THINK = re.compile(r"\bThink of a number (\d)")


def main():
    write = "--write" in sys.argv
    questions = bank.load_bank()
    ids4 = {q["id"] for q in bank.load_bank(4)}
    done = {"degrees": 0, "rupees": 0, "wording": 0, "removed": 0, "unfit": 0}
    out = []
    changed = {}
    for q in questions:
        qid = q["id"]
        if qid not in ids4:
            out.append(q)
            continue
        if qid in UNFIT:
            done["unfit"] += 1
            continue
        if qid in REPEATS:
            if REPEATS[qid] not in ids4:
                sys.exit("%s: the question it repeats (%s) is not in the bank" % (qid, REPEATS[qid]))
            done["removed"] += 1
            continue
        texts = [o["text"].strip() for o in q["options"]]
        if q.get("node") in ("gr4_angles", "gr4_triangles") and "°" in q["questionText"] and all(BARE.match(t) for t in texts):
            for o in q["options"]:
                o["text"] = o["text"].strip() + "°"
            done["degrees"] += 1
            changed[qid] = q
        if qid in RUPEES and all(BARE.match(t) for t in texts):
            for o in q["options"]:
                o["text"] = "Rs." + o["text"].strip()
            done["rupees"] += 1
            changed[qid] = q
        if THINK.search(q["questionText"]):
            q["questionText"] = THINK.sub(r"Think of the number \1", q["questionText"])
            done["wording"] += 1
        out.append(q)
    print("Grade 4: %(degrees)d questions given degree signs, %(rupees)d given Rs., %(wording)d reworded, %(removed)d repeats removed, %(unfit)d unfit removed" % done)
    if not write:
        print("nothing written (use --write)")
        return
    if os.path.exists(NOTES):
        with io.open(NOTES, encoding="utf-8") as f:
            record = json.load(f)
        for qid, q in changed.items():
            if qid in record:
                record[qid]["options"] = {o["id"]: o["text"] for o in q["options"]}
        for qid in list(REPEATS) + list(UNFIT):
            record.pop(qid, None)
        with io.open(NOTES, "w", encoding="utf-8", newline="\n") as f:
            json.dump({k: record[k] for k in sorted(record)}, f, ensure_ascii=False, indent=0)
            f.write("\n")
    bank.save_bank(out)
    print("bank written")


if __name__ == "__main__":
    main()

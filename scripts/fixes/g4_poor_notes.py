"""Find Grade 4 questions whose option notes are not fit for a child, and write them out
for rewriting.

    python -X utf8 scripts/fixes/g4_poor_notes.py            # counts
    python -X utf8 scripts/fixes/g4_poor_notes.py --write    # also write the writers' inputs

An option note is what a child sees after picking that option. A question is picked when:
  - a note is missing or blank;
  - two wrong options carry the same note;
  - a note is generic filler ("Check your unit conversion and formula.");
  - a note uses a word the app never says to a child, names an option by letter, or thinks aloud;
  - the note on the right option only says it is right ("Correct! The answer is 75.").

With --write, the picked questions go to data/bank-import/g4/ (not part of the bank), split by
the work they need:
  notes-in-R1..R3.json   generated families: notes only, written by a rule per wording
  notes-in-H1..H2.json   other questions whose hints and steps are sound: notes only, by hand
  teach3-in-01..02.json  other questions whose hints or steps are also unfit
                         (g4_poor_teaching.py): hints, steps and notes rewritten together
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402
import g4_poor_teaching as teaching  # noqa: E402
from g4_check_patch import BANNED, LETTER, THINKING  # noqa: E402

GENERIC = re.compile(
    r"^(Check your unit conversion and formula|Read the question again|Recheck: did you use the right operation|"
    r"Substitute carefully|Remember: (Average|place value)|Check the angle sum property|Count carefully|"
    r"Check your prime factori[sz]ation|Not quite\. Work through the steps once more|Look at the pattern carefully|"
    r"When denominators match, add numerators only|Check your fraction calculation|"
    r"You may have forgotten to divide by the coefficient|Check if you moved the constant term|Recheck your steps)", re.I)
BARE_RIGHT = re.compile(r"^(Correct|Yes|Right|Great job|Well done)[!.]?\s*((The|That|This) (answer )?is\s*[^.!?=×÷+−-]{0,30})?[.!]?$", re.I)
ALOUD = re.compile(r"\.\.\.|…|not an option|that'?s not\b", re.I)
GENERATED = re.compile(r"^(VAR2?_|BOOST_|PH3_)|_V\d+$")

# Topics for each rule writer, and for each hand writer.
RULE_GROUPS = {
    "R1": ("gr4_quads", "gr4_circle", "gr4_angles", "gr4_triangles", "gr4_units"),
    "R2": ("gr4_equations", "gr4_algebra", "gr4_sequences", "gr4_numbers", "gr4_squares", "gr4_factors", "gr4_counting", "gr4_puzzles"),
    "R3": ("gr4_fractions", "gr4_ages", "gr4_ratio", "gr4_data", "gr4_decimals", "gr4_operations", "gr4_time"),
}
HAND_FIRST = ("gr4_time", "gr4_units", "gr4_algebra", "gr4_decimals", "gr4_equations", "gr4_operations", "gr4_data", "gr4_ratio", "gr4_ages")


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def reasons(q):
    notes = q.get("misconceptions") if isinstance(q.get("misconceptions"), dict) else {}
    key = q.get("correctAnswer")
    out = []
    if any(not (notes.get(k) or "").strip() for k in "ABCD"):
        out.append("blank note")
    wrong = [norm(notes.get(k)) for k in "ABCD" if k != key and (notes.get(k) or "").strip()]
    if len(set(wrong)) < len(wrong):
        out.append("same note on several options")
    if any(GENERIC.search((notes.get(k) or "").strip()) for k in "ABCD" if k != key):
        out.append("generic note")
    if any(BANNED.search(notes.get(k) or "") for k in "ABCD"):
        out.append("word the app never says")
    if any(LETTER.search(notes.get(k) or "") for k in "ABCD"):
        out.append("names an option")
    if any(THINKING.search(notes.get(k) or "") or ALOUD.search(notes.get(k) or "") for k in "ABCD"):
        out.append("thinks aloud")
    right = (notes.get(key) or "").strip()
    if right and BARE_RIGHT.match(right):
        out.append("right note gives no reason")
    return out


def entry(q, why, names):
    hints, steps = teaching.texts(q)
    return {
        "id": q["id"], "topic": names.get(q.get("node")), "node": q.get("node"), "difficulty": q.get("difficulty"),
        "source": q.get("source"), "flagged": why, "question": q.get("questionText"),
        "options": {o["id"]: o["text"] for o in q["options"]}, "answer": q.get("correctAnswer"),
        "hints": hints, "steps": steps, "notes": {k: (q.get("misconceptions") or {}).get(k, "") for k in "ABCD"},
    }


def main():
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    rows = bank.load_bank(4)
    by_reason = collections.Counter()
    groups = collections.defaultdict(list)
    picked = 0
    for q in rows:
        why = reasons(q)
        unfit = teaching.reasons(q)
        generated = bool(GENERATED.search(q["id"]))
        if not why and (generated or not unfit):
            continue
        picked += 1
        for w in why:
            by_reason[w] += 1
        node = q.get("node")
        if generated:
            name = next(("notes-in-%s.json" % g for g, nodes in RULE_GROUPS.items() if node in nodes), "notes-in-R3.json")
            groups[name].append(entry(q, why, names))
        elif unfit:
            name = "teach3-in-01.json" if node in HAND_FIRST else "teach3-in-02.json"
            groups[name].append(entry(q, why + unfit, names))
        else:
            name = "notes-in-H1.json" if node in HAND_FIRST else "notes-in-H2.json"
            groups[name].append(entry(q, why, names))
    print("%d of %d Grade 4 questions have option notes (or, if hand-written, hints and steps) to rewrite" % (picked, len(rows)))
    for w, n in by_reason.most_common():
        print("   %-32s %4d" % (w, n))
    for name in sorted(groups):
        chunk = sorted(groups[name], key=lambda e: (e["node"] or "", e["id"]))
        print("   %-20s %4d questions  (%s)" % (name, len(chunk), ", ".join(
            "%s %d" % (k[4:], v) for k, v in sorted(collections.Counter(e["node"] for e in chunk).items()))))
        if "--write" in sys.argv:
            g4.dump(name, chunk)
    if "--write" not in sys.argv:
        print("nothing written (use --write)")


if __name__ == "__main__":
    main()

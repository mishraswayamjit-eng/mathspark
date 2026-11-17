"""Narration for the arithmetic topic (BODMAS, the four operations, averages, missing digits).

    python -X utf8 scripts/speech/topics/arithmetic.py            # writes data/question-speech/parts/arithmetic.json
    python -X utf8 scripts/speech/topics/arithmetic.py --stats    # also prints how many lines came from rules and by hand

Every line starts from the rules in arithmetic_engine.py. Lines the rules cannot read well are
written by hand in the override tables (arithmetic_fp.py for past papers, arithmetic_ws_*.py for
worksheets), keyed by question id. An override entry may give any of:
    "q": "...", "options": {index: "..."}, "hints": {index: "..."}, "steps": {index: "..."}

Imported questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_) go through arithmetic_imported_rules.py
first, and their hand lines live in arithmetic_imported*.py. Entries that existed before the import are
kept exactly as they were (see BEFORE below); --no-maths lists imported steps whose maths line was not read.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from common import PARTS, load_grade5, number_tokens, source_strings, topic_of  # noqa: E402
from arithmetic_engine import say, say_option  # noqa: E402

SLUG = "arithmetic"
STALE = []
SUSPECT = []
LIMIT = 90 if "--strict" in sys.argv else 60  # percent of the source's longer words a hand line must keep

OVERRIDES = {}
for _name in ("arithmetic_fp", "arithmetic_ws_a", "arithmetic_ws_b"):
    try:
        OVERRIDES.update(__import__(_name).OVERRIDES)
    except ImportError:
        pass

# The imported questions (added to the bank later) have rules and hand tables of their own:
# arithmetic_imported_rules.py, and every other arithmetic_imported*.py beside this file.
NEW_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
from arithmetic_imported_rules import say_new, say_option_new, say_step_new  # noqa: E402
NO_MATHS = []
for _file in sorted(os.listdir(HERE)):
    if _file.startswith("arithmetic_imported") and _file.endswith(".py") and _file != "arithmetic_imported_rules.py":
        _ov = getattr(__import__(_file[:-3]), "OVERRIDES", {})
        _bad = [k for k in _ov if not k.startswith(NEW_PREFIXES)]
        if _bad:
            sys.exit("%s may only hold imported questions, not %s" % (_file, ", ".join(_bad)))
        OVERRIDES.update(_ov)

# The part file as it was before the imported questions were narrated. Older entries must not change.
BEFORE = os.path.join(HERE, "_scratch_arithmetic", "arithmetic_before.json")

# Hints that many generated questions share, written once by hand.
SHARED = {
    "Don't just go left to right — check for × and ÷ first!":
        "Don't just go left to right. Check for multiplication and division first!",
    "Follow BODMAS: Brackets, Orders, Division/Multiplication, Addition/Subtraction":
        "Follow BODMAS: Brackets, Orders, Division and Multiplication, Addition and Subtraction.",
    "Similar: SI on Rs.500 at 8% for 3yr = 500×8×3/100 = Rs.120.":
        "Similar: simple interest on 500 rupees at 8 percent for 3 years, equals 500 times 8 times 3, over 100, which is 120 rupees.",
}


def _latex_words(latex):
    """The maths line of an equation step, for the 'Solve' family only (2x = 17 - 5 = 12)."""
    t = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"\1/\2", latex)
    t = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", t)
    return say(t.replace("-", "−"))


def narrate(q):
    src = source_strings(q)
    own = q.get("stepByStep") or []
    new = q["id"].startswith(NEW_PREFIXES)
    if new:
        entry = {
            "q": say_new(src["q"]),
            "options": [say_option_new(t) for t in src["options"]],
            "hints": [say_new(t) for t in src["hints"]],
            "steps": [say_new(t) for t in src["steps"]],
        }
        for i, st in enumerate(own):
            # A step that leads into its maths line reads the maths too, if it says exactly those numbers.
            if st.get("latex") and i < len(src["steps"]):
                line = say_step_new(src["steps"][i], st["latex"])
                also = "%s %s" % (src["steps"][i], re.sub(r"\\[a-zA-Z]+", " ", st["latex"]))
                if line != entry["steps"][i] and number_tokens(line) == number_tokens(also) and len(line) <= 700:
                    entry["steps"][i] = line
                elif line != entry["steps"][i]:
                    NO_MATHS.append("%s.steps[%d]" % (q["id"], i))
    else:
        entry = {
            "q": say(src["q"]),
            "options": [say_option(t) for t in src["options"]],
            "hints": [SHARED.get(t) or say(t) for t in src["hints"]],
            "steps": [SHARED.get(t) or say(t) for t in src["steps"]],
        }
    if not new and src["q"].startswith("Solve:") and "x" in src["q"]:
        for i, st in enumerate(own):
            # Only when the step's own text does not already say the sum.
            if st.get("latex") and "x" in st["latex"] and "=" not in src["steps"][i]:
                entry["steps"][i] = "%s %s" % (entry["steps"][i], _latex_words(st["latex"]))
    hand = 0
    ov = OVERRIDES.get(q["id"], {})
    # A hand line is used only while it still says the numbers of its source. When the question
    # bank is edited, a stale hand line drops back to the rule and is listed by --stale.
    if "q" in ov:
        if number_tokens(ov["q"]) == number_tokens(src["q"]):
            entry["q"] = ov["q"]
            hand += 1
        else:
            STALE.append("%s.q" % q["id"])
    for key in ("options", "hints", "steps"):
        for i, line in (ov.get(key) or {}).items():
            ok = i < len(src[key]) and number_tokens(line) == number_tokens(src[key][i])
            if not ok and key == "steps" and i < len(own) and own[i].get("latex"):
                also = "%s %s" % (src[key][i], re.sub(r"\\[a-zA-Z]+", " ", own[i]["latex"]))
                ok = number_tokens(line) == number_tokens(also)
            if ok:
                # Same numbers but different words: the source may have been reworded. Shown by --suspect.
                words = set(re.findall(r"[a-z]{4,}", src[key][i].lower()))
                kept = sum(1 for w in words if w in line.lower())
                if len(words) >= 2 and kept * 100 < len(words) * LIMIT:
                    SUSPECT.append((q["id"], key, i, src[key][i], line))
                entry[key][i] = line
                hand += 1
            else:
                STALE.append("%s.%s[%d]" % (q["id"], key, i))
    return entry, hand


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part, hand, total = {}, 0, 0
    new_q = new_hand = new_total = 0
    for q in questions:
        entry, h = narrate(q)
        part[q["id"]] = entry
        hand += h
        n = 1 + sum(1 for k in ("options", "hints", "steps") for t in entry[k] if t)
        total += n
        if q["id"].startswith(NEW_PREFIXES):
            new_q, new_hand, new_total = new_q + 1, new_hand + h, new_total + n
    unknown = sorted(set(OVERRIDES) - set(part))
    if [k for k in unknown if k.startswith(NEW_PREFIXES)]:
        sys.exit("override ids that are not arithmetic questions: %s" % ", ".join(unknown))
    if unknown:
        # Older questions that have since been filed under another topic; their hand lines are unused.
        print("note: hand lines for questions no longer in this topic: %s" % ", ".join(unknown))
    if os.path.exists(BEFORE):
        with io.open(BEFORE, encoding="utf-8") as f:
            before = json.load(f)
        gone = sorted(k for k in before if k not in part)
        if gone:
            sys.exit("older entries would be lost, nothing written: %s" % ", ".join(gone[:20]))
        changed = sorted(k for k in before if part[k] != before[k])
        for k in changed:
            part[k] = before[k]  # the older entry is kept exactly as it was
        print("%d older entries kept as they were%s" % (len(before), (" (the rules now differ for: %s)" % ", ".join(changed)) if changed else ""))
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), os.path.relpath(path)))
    if "--no-maths" in sys.argv:
        print("%d imported steps whose maths line could not be read by rule" % len(NO_MATHS))
        for s in NO_MATHS:
            print("  " + s)
    if "--stale" in sys.argv:
        print("%d stale hand lines" % len(STALE))
        for s in STALE:
            print("  " + s)
    if "--suspect" in sys.argv:
        for qid, key, i, source, line in SUSPECT:
            print("%s.%s[%d]\n   PRINT  %s\n   HAND   %s" % (qid, key, i, source, line))
    if "--stats" in sys.argv:
        print("%d lines: %d by hand, %d by rule" % (total, hand, total - hand))
        print("imported: %d questions, %d lines: %d by hand, %d by rule" % (new_q, new_total, new_hand, new_total - new_hand))


if __name__ == "__main__":
    main()

"""Write data/question-speech/parts/fractions.json.

    python -X utf8 scripts/speech/topics/fractions.py            # write the part file
    python -X utf8 scripts/speech/topics/fractions.py --general  # also list lines narrated by the general rules

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (fractions_hand*.py, keyed by question id), for past papers and worksheets;
  2. a sentence pattern for a generated family (fractions_families.py);
  3. the general fraction rules (fractions_rules.say);
  4. the shared base converter (common.speak), as a last resort.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from common import PARTS, load_grade5, source_strings, speak, topic_of  # noqa: E402
from validate import check_string  # noqa: E402
import fractions_families as fam  # noqa: E402
import fractions_rules as rules  # noqa: E402

SLUG = "fractions"

HAND = {}
LINES = {}  # hand-written lines for source lines that repeat across worksheet questions, keyed by the printed line
for name in ("fractions_hand1", "fractions_hand2", "fractions_hand3", "fractions_hand4", "fractions_hand5", "fractions_hand6", "fractions_hand7", "fractions_imported"):
    try:
        module = __import__(name)
    except ImportError:
        continue
    HAND.update(module.HAND)
    LINES.update(getattr(module, "LINES", {}))

stats = {"hand": 0, "family": 0, "general": 0, "base": 0, "failed": 0}
general_lines = []
failures = []


def narrate_string(source, where, hand=None, latex="", also=None):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("family", fam.equation_step(source, latex)))
    tries.append(("family", fam.family(source)))
    tries.append(("general", rules.say(source)))
    tries.append(("base", speak(source)))
    for kind, spoken in tries:
        if not spoken:
            continue
        problems = check_string(spoken, source, where, also)
        if not problems:
            stats[kind] += 1
            if kind in ("general", "base"):
                general_lines.append((where, source, spoken))
            return spoken
        if kind == "hand":
            failures.extend(problems)
    stats["failed"] += 1
    failures.append("%s: no rule gives a passing line for: %s" % (where, source))
    return rules.say(source)


def pick(hand, key, i):
    items = hand.get(key) or []
    return items[i] if i < len(items) else None


def narrate(q):
    src = source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []
    qid = q["id"]
    steps = []
    for i, text in enumerate(src["steps"]):
        latex = own[i].get("latex", "") if i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        steps.append(narrate_string(text, "%s.steps[%d]" % (qid, i), pick(hand, "steps", i), latex, also))
    return {
        "q": narrate_string(src["q"], qid + ".q", hand.get("q")),
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), pick(hand, "options", i)) for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), pick(hand, "hints", i)) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), path))
    print("lines:", stats)
    unknown = sorted(set(HAND) - set(part))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if "--general" in sys.argv:
        ext = "--ext" in sys.argv
        seen = set()
        for where, source, spoken in general_lines:
            shape = re.sub(r"\d+", "#", source)
            if where.startswith("EXT_") == ext and spoken != source.strip() and ".options[" not in where and shape not in seen:
                seen.add(shape)
                print("%s\n   PRINT  %s\n   SPOKEN %s" % (where, source, spoken))
    for p in failures[:80]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()

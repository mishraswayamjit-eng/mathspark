"""Write data/question-speech/parts-g4/gr4_counting.json.

    python -X utf8 scripts/speech/g4/gr4_counting.py         # write the part file, print what failed

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_counting_hand.py, keyed by question id);
  2. a family rule, or the step's text followed by its maths line (gr4_counting_rules);
  3. the notation rules (gr4_counting_rules.say);
  4. the shared base converter (common.speak), as a last resort.

Read the result with gr4_counting_dump.py out <from> <to>.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import common  # noqa: E402
from validate import check_string  # noqa: E402
import gr4_counting_rules as rules  # noqa: E402

NODE = "gr4_counting"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")

# HAND[question id] = {"q": str, "o": {index: str}, "h": {index: str}, "s": {index: str}}
HAND = {}
try:
    HAND.update(__import__("gr4_counting_hand").HAND)
except ImportError:
    pass

stats = {"hand": 0, "rule": 0, "base": 0, "failed": 0}
failures = []


def contains(big, small):
    n = len(small)
    return any(big[i:i + n] == small for i in range(len(big) - n + 1))


def with_maths(source, latex):
    """A step's text followed by its maths line, when the maths line adds working the text does not say."""
    if not latex or re.fullmatch(r"\s*\\boxed\{.*\}\s*", latex):
        return None
    maths = rules.from_latex(latex)
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt or contains(st, mt):
        return None
    text = rules.family(source) or rules.say(source)
    if not text or not maths:
        return None
    if text[-1] not in ".?!:":
        text += "."
    if not re.search(r"\d (?:equals|times|plus|minus|divided by) \d", maths):
        maths = "That is " + maths       # "10 times" -> "That is 10 times."
    return text + " " + maths + "."


def narrate_string(source, where, hand=None, also=None, latex=""):
    if not source.strip():
        return ""
    tries = []
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex)))
    tries.append(("rule", rules.family(source)))
    tries.append(("rule", rules.say(source)))
    tries.append(("base", common.speak(source)))
    for kind, spoken in tries:
        if not spoken:
            continue
        problems = check_string(spoken, source, where, also)
        if not problems:
            stats[kind] += 1
            return spoken
        if kind == "hand":
            failures.extend(problems)
    stats["failed"] += 1
    failures.append("%s: no rule gives a passing line for: %s" % (where, source))
    return rules.say(source)


def pick(hand, key, i):
    items = hand.get(key)
    if isinstance(items, dict):
        return items.get(i)
    if isinstance(items, (list, tuple)):
        return items[i] if i < len(items) else None
    return None


def narrate(q):
    src = common.source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []
    qid = q["id"]
    steps = []
    for i, text in enumerate(src["steps"]):
        latex = own[i].get("latex", "") if i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        steps.append(narrate_string(text, "%s.steps[%d]" % (qid, i), pick(hand, "s", i), also, latex))
    return {
        "q": narrate_string(src["q"], qid + ".q", hand.get("q")),
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), pick(hand, "o", i)) for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), pick(hand, "h", i)) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def main():
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), OUT))
    print("lines:", stats)
    unknown = sorted(set(HAND) - set(part))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    for p in failures[:80]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()

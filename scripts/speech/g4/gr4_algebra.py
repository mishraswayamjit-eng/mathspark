"""Narration for the Grade 4 topic gr4_algebra. Writes data/question-speech/parts-g4/gr4_algebra.json.

    python -X utf8 scripts/speech/g4/gr4_algebra.py
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
from common import number_tokens, source_strings  # noqa: E402
from gr4_algebra_rules import say, maths_line  # noqa: E402

try:
    from gr4_algebra_hand import HAND, TEXT  # noqa: E402
except ImportError:
    HAND, TEXT = {}, {}

NODE = "gr4_algebra"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")


def latex_numbers(latex):
    return number_tokens(re.sub(r"\\[a-zA-Z]+", " ", latex))


def is_sublist(small, big):
    n = len(small)
    return any(big[i:i + n] == small for i in range(len(big) - n + 1))


def working(text, latex):
    """The maths line under a step, when it adds working the step's own text does not already say."""
    if not latex or "=" not in latex or "\\text" in latex or "\\boxed" in latex:
        return ""
    nums = latex_numbers(latex)
    if not nums or is_sublist(nums, number_tokens(text)):
        return ""
    return maths_line(latex)


# The generated family "If a=6,b=7: 3a-b=?"
_FAMILY_Q = re.compile(r"^If a=(\d+),b=(\d+): (.+)=\?$")


def by_rule(key, text, latex, sentence):
    if key == "q":
        m = _FAMILY_Q.match(text)
        if m:
            expr = say(m.group(3).replace("-", "−"), sentence=False)
            return "If A equals %s and b equals %s, what is %s?" % (m.group(1), m.group(2), expr)
    spoken = say(text, sentence)
    if key == "steps":
        extra = working(text, latex)
        if extra:
            spoken = "%s %s" % (spoken, say(extra))
    return spoken


def acceptable(spoken, text, latex):
    said = number_tokens(spoken)
    if said == number_tokens(text):
        return True
    return bool(latex) and said == number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)))


def narrate(q, counts):
    src = source_strings(q)
    over = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []

    def line(key, i, text, sentence=True):
        if not text.strip():
            return ""
        latex = own[i].get("latex", "") if key == "steps" and i < len(own) else ""
        hand = over.get(key) if key == "q" else (over.get(key) or {}).get(i)
        if hand is None:
            hand = TEXT.get(text)
        if hand is not None:
            # A hand line is used only while it still matches its source; the question bank changes.
            if acceptable(hand, text, latex):
                counts["hand"] += 1
                return hand
            counts["stale"].append("%s %s[%d]" % (q["id"], key, i))
        counts["rule"] += 1
        spoken = by_rule(key, text, latex, sentence)
        if not acceptable(spoken, text, latex):
            counts["weak"].append("%s %s[%d]" % (q["id"], key, i))
            spoken = say(text, sentence)
        return spoken

    return {
        "q": line("q", 0, src["q"]),
        "options": [line("options", i, t, sentence=False) for i, t in enumerate(src["options"])],
        "hints": [line("hints", i, t) for i, t in enumerate(src["hints"])],
        "steps": [line("steps", i, t) for i, t in enumerate(src["steps"])],
    }


def main():
    counts = {"hand": 0, "rule": 0, "stale": [], "weak": []}
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])
    unknown = sorted(set(HAND) - {q["id"] for q in questions})
    if unknown:
        sys.exit("hand lines for ids not in this topic: %s" % ", ".join(unknown))
    part = {q["id"]: narrate(q, counts) for q in questions}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions (%d lines by hand, %d by rule)" % (len(part), counts["hand"], counts["rule"]))
    for where in counts["stale"]:
        print("  stale hand line ignored: " + where)
    for where in counts["weak"]:
        print("  rule changed the numbers, fell back: " + where)


if __name__ == "__main__":
    main()

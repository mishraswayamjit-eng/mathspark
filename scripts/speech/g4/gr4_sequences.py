"""Narration for the Grade 4 topic gr4_sequences. Writes data/question-speech/parts-g4/gr4_sequences.json.

    python -X utf8 scripts/speech/g4/gr4_sequences.py
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
import validate  # noqa: E402  (only its check_string, so a rule line that would fail is never written)
from common import number_tokens, source_strings  # noqa: E402
from gr4_algebra import is_sublist, latex_numbers  # noqa: E402
from gr4_sequences_rules import say, maths_line  # noqa: E402

try:
    from gr4_sequences_hand import HAND, TEXT  # noqa: E402
except ImportError:
    HAND, TEXT = {}, {}

NODE = "gr4_sequences"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")
BR = "open bracket, %s, close bracket"


def working(text, latex):
    """The maths line under a step, when it adds working the step's own text does not already say."""
    if not latex or "=" not in latex or "\\text" in latex or "\\boxed" in latex or "_" in latex or "?" in latex:
        return ""
    nums = latex_numbers(latex)
    if not nums or is_sublist(nums, number_tokens(text)):
        return ""
    return maths_line(latex)


# Generated families, whose steps are printed as notes. Each is said as a teacher would read it.
FAMILIES = [
    (r"^First term \(a\) = (\d+), Common diff \(d\) = (\d+)$",
     "The first term, A, equals {0}. The common difference, d, equals {1}."),
    (r"^nth term = a \+ \(n−1\)d = (\d+) \+ \((\d+)−1\)×(\d+) = (\d+) \+ (\d+) = (\d+)$",
     "The nth term equals A plus, open bracket, n minus 1, close bracket, times d. "
     "That is {0} plus, open bracket, {1} minus 1, close bracket, times {2}, which is {3} plus {4}, which is {5}."),
    (r"^Calculate: (\d+) \+ \((\d+)−1\) × (\d+)\.$",
     "Calculate: {0} plus, open bracket, {1} minus 1, close bracket, times {2}."),
    (r"^Number of terms \(n\) = (\d+), first = (\d+), last = (\d+)$",
     "The number of terms, n, equals {0}. First equals {1}, last equals {2}."),
    (r"^Sum = n/2 × \(first \+ last\) = (\d+)/2 × \((\d+)\+(\d+)\) = (\d+) × (\d+)$",
     "Sum equals n over 2, times, open bracket, first plus last, close bracket. "
     "That is {0} over 2, times, open bracket, {1} plus {2}, close bracket, which is {3} times {4}."),
    (r"^Sum = (\d+)/2 × \((\d+) \+ (\d+)\)\.$",
     "Sum equals {0} over 2, times, open bracket, {1} plus {2}, close bracket."),
    (r"^Each term is multiplied by (\d+): ×(\d+) pattern$",
     "Each term is multiplied by {0}: a times {1} pattern."),
]


def by_rule(key, text, latex, sentence):
    for pattern, template in FAMILIES:
        m = re.match(pattern, text)
        if m and template:
            return template.format(*m.groups())
    spoken = say(text, sentence)
    if key == "q" and re.match(r"(?:What|Which)\b", spoken) and "?" not in spoken:
        spoken = spoken.rstrip(".") + "?"          # "What comes next: 3, 6, 12, blank?"
    if key == "steps":
        extra = working(text, latex)
        if extra:
            spoken = "%s %s" % (spoken, say(extra))
    return spoken


def acceptable(spoken, text, latex):
    also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
    return not validate.check_string(spoken, text, "", also)


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
            counts["stale"].append("%s %s[%d]: %s" % (q["id"], key, i, "; ".join(validate.check_string(
                hand, text, "", "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None))))
        counts["rule"] += 1
        spoken = by_rule(key, text, latex, sentence)
        if not acceptable(spoken, text, latex):
            spoken = say(text, sentence)
            if not acceptable(spoken, text, latex):
                counts["weak"].append("%s %s[%d]" % (q["id"], key, i))
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
        print("  no speakable line by rule, needs a hand line: " + where)


if __name__ == "__main__":
    main()

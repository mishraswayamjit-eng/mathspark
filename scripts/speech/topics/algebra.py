"""Narration for the algebra topic. Writes data/question-speech/parts/algebra.json.

    python -X utf8 scripts/speech/topics/algebra.py
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
from algebra_rules import say  # noqa: E402
from algebra_overrides import OVERRIDES  # noqa: E402
from algebra_imported_rules import say_imported, step_line  # noqa: E402
from algebra_imported_hand1 import HAND as HAND1  # noqa: E402
from algebra_imported_hand2 import HAND as HAND2  # noqa: E402

SLUG = "algebra"
IMPORTED = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
IMPORTED_HAND = dict(HAND1)
IMPORTED_HAND.update(HAND2)


def maths_line(latex):
    """A step's maths line as plain print, ready for the rules: \\frac{77}{7} -> 77/7, \\boxed{11} -> 11."""
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", latex)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\,", " ")
    return re.sub(r"(?<=[\w ])-(?=[\w ])", "−", s)


def working(q, i, text):
    """The maths line under a step, when the step text is only an instruction ("Add 3 to both sides")."""
    own = q.get("stepByStep") or []
    latex = own[i].get("latex", "") if i < len(own) else ""
    if not latex or "=" in text or "=" not in latex or "\\text" in latex:
        return ""
    return maths_line(latex)


def narrate(q, counts):
    src = source_strings(q)
    over = OVERRIDES.get(q["id"], {})

    def line(key, i, text, sentence=True):
        if not text.strip():
            return ""
        hand = over.get(key) if key == "q" else (over.get(key) or {}).get(i)
        if hand is not None:
            # A hand line is only used while it still matches its source; the question bank changes.
            wanted = [number_tokens(text)]
            if key == "steps":
                own = q.get("stepByStep") or []
                if i < len(own) and own[i].get("latex"):
                    wanted.append(number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", own[i]["latex"]))))
            if number_tokens(hand) in wanted:
                counts["hand"] += 1
                return hand
            counts["stale"].append("%s %s[%d]" % (q["id"], key, i))
        counts["rule"] += 1
        spoken = say(text, sentence)
        if key == "steps":
            extra = working(q, i, text)
            if extra:
                spoken = "%s %s" % (spoken, say(extra))
        return spoken

    return {
        "q": line("q", 0, src["q"]),
        "options": [line("options", i, t, sentence=False) for i, t in enumerate(src["options"])],
        "hints": [line("hints", i, t) for i, t in enumerate(src["hints"])],
        "steps": [line("steps", i, t) for i, t in enumerate(src["steps"])],
    }


def is_imported(q):
    return q["id"].startswith(IMPORTED)


def narrate_imported(q, counts):
    """The questions imported into the bank later: story problems and textbook items."""
    src = source_strings(q)
    over = IMPORTED_HAND.get(q["id"], {})
    own = q.get("stepByStep") or []

    def line(key, i, text, sentence=True):
        if not text.strip():
            return ""
        latex = own[i].get("latex", "") if key == "steps" and i < len(own) else ""
        hand = over.get(key) if key == "q" else (over.get(key) or {}).get(i)
        if hand is not None:
            wanted = [number_tokens(text)]
            if latex:
                wanted.append(number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex))))
            if number_tokens(hand) in wanted:
                counts["hand"] += 1
                return hand
            counts["stale"].append("%s %s[%d]" % (q["id"], key, i))
        counts["rule"] += 1
        if key == "steps":
            spoken = step_line(text, latex)
            # The maths line is only said when the checker will accept the numbers it adds.
            if number_tokens(spoken) not in (number_tokens(text), number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)))):
                spoken = say_imported(text)
            return spoken
        return say_imported(text, sentence)

    return {
        "q": line("q", 0, src["q"]),
        "options": [line("options", i, t, sentence=False) for i, t in enumerate(src["options"])],
        "hints": [line("hints", i, t) for i, t in enumerate(src["hints"])],
        "steps": [line("steps", i, t) for i, t in enumerate(src["steps"])],
    }


def main():
    counts = {"hand": 0, "rule": 0, "stale": []}
    new = {"hand": 0, "rule": 0, "stale": []}
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    ids = {q["id"] for q in questions}
    unknown = sorted((set(OVERRIDES) | set(IMPORTED_HAND)) - ids)
    if unknown:
        sys.exit("overrides for ids not in this topic: %s" % ", ".join(unknown))
    path = os.path.join(PARTS, SLUG + ".json")
    # Entries already in the part file for the older questions are kept exactly as they are:
    # the part file is the record of what was reviewed. Only what is missing is written.
    existing = {}
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            existing = json.load(f)
    part = {}
    kept = 0
    for q in questions:
        if is_imported(q):
            part[q["id"]] = narrate_imported(q, new)
        elif q["id"] in existing:
            part[q["id"]] = existing[q["id"]]
            kept += 1
        else:
            part[q["id"]] = narrate(q, counts)
    os.makedirs(PARTS, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions: %d kept as they were, %d older ones narrated afresh (%d lines by hand, %d by rule)"
          % (len(part), kept, len(part) - kept - sum(1 for q in questions if is_imported(q)), counts["hand"], counts["rule"]))
    print("imported: %d questions, %d lines by hand, %d by rule" % (sum(1 for q in questions if is_imported(q)), new["hand"], new["rule"]))
    for where in counts["stale"] + new["stale"]:
        print("  stale hand line ignored: " + where)


if __name__ == "__main__":
    main()
